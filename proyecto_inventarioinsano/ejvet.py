import asyncio
import time

async def calcular_hidratacion(mascota, peso, constant, tiempo_horas):
    print(f"Evaluando a {mascota}...")
    await asyncio.sleep(1)

    try:
        tasa = (peso * constant) / tiempo_horas
        if tasa > 500:
            raise ValueError("La tasa supera los 500 ml")
        print(f"{mascota}: Hidratación = {tasa} ml")
    except ZeroDivisionError:
        print(f"{mascota}: ¡SHOCK! Activar protocolo de bolo de emergencia.")

    except ValueError as e:
        print(f"{mascota}: {e}")
        tasa = 500
        print(f"{mascota}: Tasa ajustada a {tasa} ml.")




        

async def principal():
    inicio = time.time()

    await asyncio.gather(
        calcular_hidratacion("Firu", 10, 50, 5),
        calcular_hidratacion("Gurumino", 4, 50, 0),
        calcular_hidratacion("juan", 20, 50, 1)
    )

    fin = time.time()
    print("Tiempo total:", round(fin - inicio, 2), "S")
asyncio.run(principal())