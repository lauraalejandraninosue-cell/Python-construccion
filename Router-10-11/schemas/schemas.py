from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class MecanicoCreate(BaseModel):
    documento: str
    nombre_completo: str
    especialidad: str

class MecanicoResponse(BaseModel):
    id: int
    documento: str
    nombre_completo: str
    especialidad: Optional[str] = None
    activo: bool

    model_config = ConfigDict(from_attributes=True)

class RepuestoCreate(BaseModel):
    codigo_sku: str
    nombre: str
    precio_compra: float = Field(ge=0)
    precio_venta: float = Field(ge=0)
    stock_actual: int = Field(default=0, ge=0)

class RepuestoResponse(BaseModel):
    id: int
    codigo_sku: str
    nombre: str
    precio_compra: float
    precio_venta: float
    stock_actual: int
    model_config = ConfigDict(from_attributes=True)

class OrdenCreate(BaseModel):
    placa: str = Field(min_length=1, max_length=6)
    modelo: str
    falla_reportada: str
    mecanico_id: int

class OrdenPatch(BaseModel):
    estado: Optional[str] = None
    mano_obra: Optional[float] = Field(default=None, ge=0)

class OrdenResponse(BaseModel):
    id: int
    placa: str
    modelo: str
    falla_reportada: str
    estado: str
    costo_reparacion: float
    mecanico_id: int
    model_config = ConfigDict(from_attributes=True)

class OrdenRepuestoCreate(BaseModel):
    repuesto_id: int
    cantidad: int = Field(gt=0)

class FacturaResponse(BaseModel):
    id: int
    orden_id: int
    fecha_emision: datetime
    subtotal_repuestos: float
    costo_mano_obra: float
    iva: float
    total_pagar: float
    model_config = ConfigDict(from_attributes=True)

class RepuestoFacturaResponse(BaseModel):
    nombre_repuesto: str
    cantidad: int
    precio_unitario_historico: float
    subtotal_linea: float
class FacturaDetalladaResponse(BaseModel):
    id: int
    fecha_emision: datetime
    subtotal_repuestos: float
    costo_mano_obra: float
    iva: float
    total_pagar: float
    placa: str
    modelo: str
    mecanico: str
    repuestos: list[RepuestoFacturaResponse]
