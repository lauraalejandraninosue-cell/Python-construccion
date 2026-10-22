import asyncio
import json
tareas_alerta = []

# Leer los productos deJSON
async def leer_base_datos():
    with open("inventario.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos
# Guardar lenJSON
async def guardar_base_datos(datos):
    with open("inventario.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
#tock bajo
async def alerta_stock_bajo(codigo, nombre, stock_actual):
    await asyncio.sleep(2)
    print(
        f"\nALERTA: {nombre} ({codigo}) "
        f"tiene solo {stock_actual} unidades. "
        "Solicitar restock."
    )
#vent
async def vender_producto(codigo, cantidad_vendida):
    datos = await leer_base_datos()
    producto_encontrado = None
    # Buscarpor su código
    for dato in datos:
        if dato["codigo"] == codigo:
            producto_encontrado = dato
            break
    # Vericar que exista
    if producto_encontrado is None:
        raise KeyError("Producto no encontrado")

    #cantidad a vender
    if cantidad_vendida <= 0:
        raise ValueError("La cantidad debe ser mayor que cero")
    #suficiente stock
    if cantidad_vendida > producto_encontrado["stock"]:
        raise ValueError("Stock insuficiente")

    # Descontar los productos vendidos
    producto_encontrado["stock"] -= cantidad_vendida

    # Guardar los cambios
    await guardar_base_datos(datos)

    stock_actual = producto_encontrado["stock"]
    nombre = producto_encontrado["nombre"]

    # Crear una alerta si quedan menos de 3 unidades
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
