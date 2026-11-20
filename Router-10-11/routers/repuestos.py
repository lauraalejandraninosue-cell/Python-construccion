
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import obtener_bd
from models.repuesto import Repuesto
from schemas.schemas import RepuestoCreate, RepuestoResponse


# Crear router
router = APIRouter(
    prefix="/repuestos",
    tags=["Repuestos"]
)


# =========================
# POST: Registrar repuesto
# =========================

@router.post("/", response_model=RepuestoResponse, status_code=201)
async def crear_repuesto(
    repuesto: RepuestoCreate,
    db: AsyncSession = Depends(obtener_bd)
):

    # Crear el objeto
    nuevo_repuesto = Repuesto(
        codigo_sku=repuesto.codigo_sku,
        nombre=repuesto.nombre,
        precio_compra=repuesto.precio_compra,
        precio_venta=repuesto.precio_venta,
        stock_actual=repuesto.stock_actual
    )

    # Guardar en la base de datos
    db.add(nuevo_repuesto)
    await db.commit()
    await db.refresh(nuevo_repuesto)

    return nuevo_repuesto

@router.get("/", response_model=list[RepuestoResponse])
async def listar_repuestos(
    db: AsyncSession = Depends(obtener_bd)
):

    # Consultar todos los repuestos
    consulta = select(Repuesto)

    resultado = await db.execute(consulta)

    repuestos = resultado.scalars().all()

    return repuestos
