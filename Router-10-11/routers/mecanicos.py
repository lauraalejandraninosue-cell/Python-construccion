
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import obtener_bd
from models.mecanico import Mecanico
from schemas.schemas import MecanicoCreate, MecanicoResponse


# Crear router
router = APIRouter(
    prefix="/mecanicos",
    tags=["Mecanicos"]
)


# =========================
# POST: Registrar mecanico
# =========================

@router.post("/", response_model=MecanicoResponse, status_code=201)
async def crear_mecanico(
    mecanico: MecanicoCreate,
    db: AsyncSession = Depends(obtener_bd)
):

    # Crear el objeto
    nuevo_mecanico = Mecanico(
        documento=mecanico.documento,
        nombre_completo=mecanico.nombre_completo,
        especialidad=mecanico.especialidad
    )

    # Guardar en la base de datos
    db.add(nuevo_mecanico)
    await db.commit()
    await db.refresh(nuevo_mecanico)

    return nuevo_mecanico


# =========================
# GET: Listar mecanicos
# =========================

@router.get("/", response_model=list[MecanicoResponse])
async def listar_mecanicos(
    db: AsyncSession = Depends(obtener_bd)
):

    # Consultar todos los mecanicos
    consulta = select(Mecanico)

    resultado = await db.execute(consulta)

    mecanicos = resultado.scalars().all()

    return mecanicos
