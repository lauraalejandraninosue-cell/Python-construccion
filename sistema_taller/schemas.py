from pydantic import BaseModel, Field

# Esquema para registrar una orden
class OrdenCreate(BaseModel):
    placa: str = Field(..., max_length=6, description="Placa de la motocicleta, máximo 6 caracteres"
    )
    modelo: str = Field(..., description="Modelo de la motocicleta")
    falla_reportada: str = Field(..., description="Falla que reporta el cliente")
#actualizar una orden
class OrdenUpdate(BaseModel):
    nuevo_estado: str = Field(..., description="Nuevo estado de la reparación")
    costo_reparacion: float = Field(..., description="Costo de la reparación")
