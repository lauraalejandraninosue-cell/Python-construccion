import asyncio

async def consultar_inventario_fragil(repuesto):
    print(f"Buscando {repuesto}...")
    await asyncio.sleep(1)

    if repuesto == "Filtro de aire":
        raise Exception("Error 500: Se cayó la conexión con la bodega")

    return {"repuesto": repuesto, "stock": 15}


async def procesar_orden_segura(repuesto):
    try:
        resultado = await consultar_inventario_fragil(repuesto)
        print(f"Éxito: {resultado}")
    except Exception as e:
        print(f"Manejo de crisis: No se pudo consultar el {repuesto}. Motivo: {e}")