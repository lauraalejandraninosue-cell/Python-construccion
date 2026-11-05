from fastapi import FastAPI, HTTPException
from database import leer_base_datos, guardar_base_datos
from schemas import OrdenCreate, OrdenUpdate

apiRest = FastAPI(
    title="API de Órdenes de Servicio SENA",
    description="Sistema de recepción y seguimiento de motocicletas",
    version="1.0.0"
)