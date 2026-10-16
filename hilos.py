import asyncio
import time

def procesar_reporte_medico():
    print("iniciando el proceso, bloqueo")
    time.sleep(3)
    print("reporte generado")
    return "reporte.pdf"

async def atender_cliente(cedula):
    print(f"atendiendo a {cedula}")
    await asyncio.sleep (1)
    print(f"paciente {cedula} se ha dado de alta")

async def main():
    tarea_pesada = asyncio.to_thread()
    tarea_clientes= [atender_cliente(i) for i in range(1, 4)]
    await asyncio.gather(tarea_pesada, *tarea_clientes) 

asyncio.run (main())