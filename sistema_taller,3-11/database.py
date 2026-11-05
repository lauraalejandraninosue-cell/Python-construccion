import json
import os

ARCHIVO = os.path.join(os.path.dirname(__file__), "taller.json")

async def leer_base_datos():

    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump([], archivo)

    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return datos

async def guardar_base_datos(datos):

    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
