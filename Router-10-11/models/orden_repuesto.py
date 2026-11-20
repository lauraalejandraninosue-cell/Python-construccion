from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
class OrdenRepuesto(Base):
    __tablename__ = "orden_repuestos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    orden_id = Column(
        Integer,
        ForeignKey("ordenes.id"),
        nullable=False
    )
    repuesto_id = Column(
        Integer,
        ForeignKey("repuestos.id"),
        nullable=False
    )
    cantidad = Column(Integer, nullable=False)
    precio_unitario_historico = Column(
        Float,
        nullable=False
    )
    orden = relationship(
        "Orden",
        back_populates="repuestos"
    )
    repuesto = relationship(
        "Repuesto",
        back_populates="ordenes"
    )
