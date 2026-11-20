from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import obtener_bd
from models.factura import Factura
from models.orden import Orden
from models.mecanico import Mecanico
from models.orden_repuesto import OrdenRepuesto
from models.repuesto import Repuesto
from schemas.schemas import FacturaDetalladaResponse
router = APIRouter(prefix="/facturas",tags=["Facturacion"]
)
@router.get("/{orden_id}", response_model=FacturaDetalladaResponse
)
async def consultar_factura(
    orden_id: int,
    db: AsyncSession = Depends(obtener_bd)
):
# Buscar factura
    resultado = await db.execute( select(Factura).where( Factura.orden_id == orden_id
        )
    )
    factura = resultado.scalar_one_or_none()
    if not factura: raise HTTPException(status_code=404, detail="Factura no encontrada para esta orden")
    # Buscar orden
    orden = await db.get(Orden, orden_id)
    if not orden:
        raise HTTPException(status_code=404,detail="Orden no encontrada")
# Buscar mecanico
    mecanico = await db.get(Mecanico,orden.mecanico_id)
    # Consultar repuestos utilizados
    resultado_repuestos = await db.execute(
        select(OrdenRepuesto).where(
            OrdenRepuesto.orden_id == orden_id
        ))
    registros = resultado_repuestos.scalars().all()
    detalle_repuestos = []
    for registro in registros:
        repuesto = await db.get(Repuesto,registro.repuesto_id)
        if repuesto:
            subtotal_linea = (registro.cantidad * registro.precio_unitario_historico)
            detalle_repuestos.append({"nombre_repuesto": repuesto.nombre,"cantidad": registro.cantidad,"precio_unitario_historico": registro.precio_unitario_historico,"subtotal_linea": round(subtotal_linea, 2)})
    # Construir respuesta detallada
    return {"id": factura.id,"fecha_emision": factura.fecha_emision,"subtotal_repuestos": factura.subtotal_repuestos,"costo_mano_obra": factura.costo_mano_obra,"iva": factura.iva,"total_pagar": factura.total_pagar,"placa": orden.placa,"modelo": orden.modelo,
        "mecanico": (mecanico.nombre_completo
            if mecanico else "No asignado"
        ),
        "repuestos": detalle_repuestos
    }
