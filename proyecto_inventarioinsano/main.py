
import asyncio
from database import vender_producto, tareas_alerta
# Procesar una vent
async def procesar_venta(codigo, cantidad):
    try:
        resultado = await vender_producto(codigo, cantidad)
        print(resultado)
    except KeyError as error:
        print(f"Error: {error}")
    except ValueError as error:
        print(f"Error: {error}")

#
async def iniciar_sistema():
    print("=== SISTEMA PARA LAS VENTAS =")

    # Ejecutar tas
    await asyncio.gather(
        procesar_venta("P01", 2),
        procesar_venta("P02", 3),
        procesar_venta("P03", 100),
        procesar_venta("P04", 4)
    )

    #await a que se termine alertas
    if tareas_alerta:
        await asyncio.gather(*tareas_alerta)

    print("== PRUEBAS FINALIZADAS=")
asyncio.run(iniciar_sistema())
