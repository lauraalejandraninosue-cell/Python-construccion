
from fastapi import FastAPI, HTTPException
from database import leer_base_datos, guardar_base_datos
from schemas import OrdenCreate, OrdenUpdate


# ==========================================
# INICIALIZAR LA API
# ==========================================

apiRest = FastAPI(
    title="API de Órdenes de Servicio SENA",
    description="Sistema de recepción y seguimiento de motocicletas",
    version="1.0.0"
)


# ==========================================
# POST: REGISTRAR UNA ORDEN
# ==========================================

@apiRest.post("/ordenes", status_code=201)
async def registrar_orden(orden: OrdenCreate):

    datos = await leer_base_datos()

    # 1. Validar que la moto no siga en el taller
    for dato in datos:
        if (
            dato["placa"].upper() == orden.placa.upper()
            and dato["estado"] != "Entregada"
        ):
            raise HTTPException(
                status_code=400,
                detail="La moto ya se encuentra en el taller"
            )

    # 2. Convertir los datos recibidos en un diccionario
    nueva_orden = orden.model_dump()

    # 3. Agregar los valores iniciales
    nueva_orden["placa"] = orden.placa.upper()
    nueva_orden["estado"] = "En diagnóstico"
    nueva_orden["costo_reparacion"] = 0

    # 4. Guardar la nueva orden
    datos.append(nueva_orden)
    await guardar_base_datos(datos)

    return {
        "mensaje": "Orden registrada correctamente",
        "orden": nueva_orden
    }


# ==========================================
# GET: CONSULTAR TODAS LAS ORDENES
# ==========================================

@apiRest.get("/ordenes")
async def listar_ordenes():

    datos = await leer_base_datos()

    return {
        "cantidad": len(datos),
        "ordenes": datos
    }


# ==========================================
# PUT: ACTUALIZAR ESTADO Y COSTO
# ==========================================

@apiRest.put("/ordenes/{placa}")
async def actualizar_orden(placa: str, datos_actualizados: OrdenUpdate):

    datos = await leer_base_datos()

    # 1. Buscar la orden por placa
    orden_encontrada = None

    for dato in datos:
        if dato["placa"].upper() == placa.upper():
            orden_encontrada = dato

    # 2. Validar que la placa exista
    if orden_encontrada is None:
        raise HTTPException(
            status_code=404,
            detail="Orden no encontrada"
        )

    # 3. Validar el costo si la moto está reparada
    if (
        datos_actualizados.nuevo_estado == "Reparada"
        and datos_actualizados.costo_reparacion <= 0
    ):
        raise HTTPException(
            status_code=400,
            detail="No se puede marcar como reparada sin asignar un costo de reparación"
        )

    # 4. Actualizar los datos
    orden_encontrada["estado"] = datos_actualizados.nuevo_estado
    orden_encontrada["costo_reparacion"] = datos_actualizados.costo_reparacion

    # 5. Guardar los cambios
    await guardar_base_datos(datos)

    return {
        "mensaje": "Orden actualizada correctamente",
        "orden": orden_encontrada
    }
