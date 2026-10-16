import asyncio
import time
async def verificar_inventario(item):
    print(f"Buscando {item} en la bodega...")
    await asyncio.sleep(1)
    print(f"{item} encontrado.")
    return 50009

async def procesar_pago(monto):
    print(f"Procesando pago de ${monto} con Bre-B...")
    await asyncio.sleep(2)
    print("Pago aprobado")
    return "ABC-124"

async def generar_factura(item, transaccion, cliente):
    print(f"Generando factura para {cliente}: {item} (REF: {transaccion})")
    await asyncio.sleep(1)
    print(f"Factura electrónica de {cliente} enviada.")

async def atender_cliente(cliente, item):
    print(f"-INICIO {cliente}-")

    precio = await verificar_inventario(item)
    transaccion = await procesar_pago(precio)
    await generar_factura(item, transaccion, cliente)
    print(f"FIN: {cliente}")

async def principal():
    inicio= time.time()
    await asyncio.gather(
        atender_cliente("Cliente 1", "Aceite sintético"),
        atender_cliente("Cliente 2", "Filtro"),
        atender_cliente("Cliente 3", "Aislante")
    )
    fin=time.time()
    print("Tiempo total:", round(fin - inicio, 2), "segundos")
asyncio.run(principal())