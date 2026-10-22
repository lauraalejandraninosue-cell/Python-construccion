import asyncio
import json
# espacio para las alertas
tareas_alerta = []

async def leer_base_datos():
    with open("inventario.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return datos
async def guardar_base_datos(datos):

    # Abrir el archivo para guardar los cambios
    with open("inventario.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


# ALERTA
async def alerta_stock_bajo(codigo, nombre, stock_actual):
    await asyncio.sleep(2)

    print(f"ALERTA CRÍTICA: El producto {nombre} "
        f"({codigo}) ha bajado a {stock_actual} unidades. "
        "Solicitar restock."
    )

#hacer una venta
async def vender_producto(codigo, cantidad_vendida):
    datos = await leer_base_datos()
    producto_encontrado = None
    for dato in datos:
        if dato["codigo"] == codigo:
            producto_encontrado = dato
            break

    if producto_encontrado is None:
        raise KeyError("Producto no encontrado")
    if cantidad_vendida <= 0:
        raise ValueError("La cantidad debe ser mayor que cero")
    if cantidad_vendida > producto_encontrado["stock"]:
        raise ValueError("Stock insuficiente")
    producto_encontrado["stock"] -= cantidad_vendida
    await guardar_base_datos(datos)
    stock_actual = producto_encontrado["stock"]
    nombre = producto_encontrado["nombre"]
    # La alerta de menos de 3
    if stock_actual < 3:
        tarea = asyncio.create_task(
            alerta_stock_bajo(codigo, nombre, stock_actual)
        )

        tareas_alerta.append(tarea)
    return (
        f"Venta exitosa: {nombre}. "
        f"Vendidas: {cantidad_vendida}. "
        f"Stock restante: {stock_actual}"
    )
