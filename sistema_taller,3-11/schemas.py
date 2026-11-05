from pydantic import BaseModel, Field

class OrdenCreate(BaseModel):
    placa: str = Field(..., max_length=6)
    modelo: str
    falla_reportada: str

class OrdenUpdate(BaseModel):
    nuevo_estado: str
    costo_reparacion: float
