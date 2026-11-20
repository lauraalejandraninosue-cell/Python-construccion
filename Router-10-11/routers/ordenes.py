from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from core.database import obtener_bd
from models.orden import Orden
from models.mecanico import Mecanico
from models.repuesto import Repuesto
from models.orden_repuesto import OrdenRepuesto
from models.factura import Factura
from schemas.schemas import (OrdenCreate,OrdenPatch,OrdenResponse,OrdenRepuestoCreate
)
router = APIRouter(prefix="/ordenes",tags=["Ordenes"]
)
#metod
@router.post("/", response_model=OrdenResponse, status_code=201)
async def crear_orden(
    datos: OrdenCreate,
    db: AsyncSession = Depends(obtener_bd)
):

    mecanico = await db.get(Mecanico, datos.mecanico_id)

    if not mecanico or not mecanico.activo:
        raise HTTPException(
            status_code=404,
            detail="Mecanico no encontrado o inactivo"
        )

    nueva_orden = Orden(
        placa=datos.placa.upper(),modelo=datos.modelo,falla_reportada=datos.falla_reportada,mecanico_id=datos.mecanico_id,estado="En diagnóstico",costo_reparacion=0.0
    )
    db.add(nueva_orden)
    await db.commit()
    await db.refresh(nueva_orden)
    return nueva_orden
# ======metodoss importantes
@router.get("/", response_model=list[OrdenResponse])
async def listar_ordenes(db: AsyncSession = Depends(obtener_bd)):
    resultado = await db.execute(select(Orden))
    return resultado.scalars().all()

@router.patch("/{orden_id}", response_model=OrdenResponse)
async def actualizar_orden(
    orden_id: int,datos: OrdenPatch,db: AsyncSession = Depends(obtener_bd)
):
    if not datos.model_fields_set:
        raise HTTPException(status_code=400,detail="Debes enviar al menos un campo"
        )
    try:
        async with db.begin():
            orden = await db.get(Orden, orden_id)
            if not orden:
                raise HTTPException(status_code=404, detail="Orden no encontrada"
                )
            # Verificar si la orden ya fue facturada
            factura_previa = await db.execute(
                select(Factura).where(
                    Factura.orden_id == orden_id
                )
            )
            if factura_previa.scalar_one_or_none():
                if datos.estado in (None, "Reparada"):
                    return orden
                raise HTTPException(
                    status_code=400,
                    detail="No se puede modificar una orden ya facturada"
                )

           #subtotall
            consulta = select(
                func.coalesce(
                    func.sum(
                        OrdenRepuesto.cantidad *OrdenRepuesto.precio_unitario_historico
                    ),
                    0.0
                )
            ).where(
                OrdenRepuesto.orden_id == orden_id
            )
            resultado = await db.execute(consulta)
            subtotal = float(resultado.scalar_one())
            if datos.mano_obra is not None:
                orden.costo_reparacion = (
                    subtotal + datos.mano_obra
                )
            # Actualizar estado si esque fue enviado
            if datos.estado is not None:
                orden.estado = datos.estado

            if orden.estado == "Reparada":
                #si ya existe una factura
                consulta_factura = select(Factura).where(
                    Factura.orden_id == orden_id
                )
                resultado_factura = await db.execute(
                    consulta_factura
                )
                factura_existente = resultado_factura.scalar_one_or_none()

                # candado de id algo (el primero)
                if not factura_existente:
                    # se calcula a partir del costo acumulado, segun google.
                    if datos.mano_obra is None:
                        if orden.costo_reparacion == 0 and subtotal > 0:
                            mano_obra = 0.0
                        else:
                            mano_obra = (
                                orden.costo_reparacion - subtotal
                            )
                    else:
                        mano_obra = datos.mano_obra
                    # para validar que no nos robemos a nosotros mismos
                    if orden.costo_reparacion <= 0:
                        raise HTTPException(
                            status_code=400,
                            detail="No se puede reparar ni facturar una orden con costo igual a cero"
                        )
                    if mano_obra < 0:
                        raise HTTPException(
                            status_code=400,
                            detail="La mano de obra no puede ser negativa"
                        )
                    #maso valores tributarios
                    total_neto = subtotal + mano_obra
                    if total_neto <= 0:
                        raise HTTPException(
                            status_code=400,
                            detail="El total de la orden debe ser mayor a cero"
                        )
                    iva = round(total_neto * 0.19, 2)
                    total_pagar = round(total_neto + iva, 2)
                    # mas el iva de abelardo
                    orden.costo_reparacion = total_neto
                    nueva_factura = Factura(orden_id=orden_id,subtotal_repuestos=subtotal,costo_mano_obra=mano_obra,iva=iva,total_pagar=total_pagar
                    )
                    db.add(nueva_factura)
            await db.flush()

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="La orden ya tiene una factura asociada"
        )
    await db.refresh(orden)

    return orden
@router.post("/{orden_id}/repuestos", status_code=201)
async def agregar_repuesto_orden(
    orden_id: int,
    datos: OrdenRepuestoCreate,
    db: AsyncSession = Depends(obtener_bd)
):
    async with db.begin():
        orden = await db.get(Orden, orden_id)
        if not orden:
            raise HTTPException(
                status_code=404,
                detail="Orden no encontrada"
            )

        # CANDADO 3: INMUTABILIDAD
        factura = await db.execute(
            select(Factura).where(
                Factura.orden_id == orden_id
            )
        )

        if orden.estado == "Reparada" or factura.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="No se pueden modificar repuestos de una orden ya cerrada/facturada"
            )
        repuesto = await db.get(Repuesto, datos.repuesto_id)
        if not repuesto:
            raise HTTPException(
                status_code=404,
                detail="Repuesto no encontrado"
            )
        if repuesto.stock_actual < datos.cantidad:
            raise HTTPException(
                status_code=400,
                detail="No hay suficiente stock disponible"
            )
        nuevo_registro = OrdenRepuesto(
            orden_id=orden_id,
            repuesto_id=datos.repuesto_id,
            cantidad=datos.cantidad,
            precio_unitario_historico=repuesto.precio_venta
        )
        repuesto.stock_actual -= datos.cantidad
        db.add(nuevo_registro)
        await db.flush()

    return {
        "mensaje": "Repuesto agregado correctamente",
        "orden_id": orden_id,
        "repuesto_id": datos.repuesto_id,
        "cantidad": datos.cantidad,
        "precio_unitario_historico": repuesto.precio_venta
    }
