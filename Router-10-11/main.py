from fastapi import FastAPI
from models.orden import Orden
from models.mecanico import Mecanico
from models.repuesto import Repuesto
from models.orden_repuesto import OrdenRepuesto
from models.factura import Factura
from routers import mecanicos, repuestos, ordenes, facturas
from core.database import Base, engine
app = FastAPI(
    title="API Taller SENA", description="Sistema de gestion de ordenes, repuestos y facturacion",version="2.0.0"
)
@app.on_event("startup")
async def crear_tablas():
    async with engine.begin() as conexion:
        await conexion.run_sync(Base.metadata.create_all)
app.include_router(mecanicos.router)
app.include_router(repuestos.router)
app.include_router(ordenes.router)
app.include_router(facturas.router)
@app.get("/")
async def inicio():
    return {
        "mensaje": "API Taller SENA funcionando",
        "version": "2.0.0"
    }
