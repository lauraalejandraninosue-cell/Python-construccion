
import json
import os


# Ubicación del archivo JSON
ARCHIVO = os.path.join(os.path.dirname(__file__), "taller.json")


# Leer las órdenes guardadas
async def leer_base_datos():

    # Si el archivo no existe, lo creamos
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump([], archivo)

    # Abrir y leer el archivo
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return datos


# Guardar las órdenes actualizadas
async def guardar_base_datos(datos):

    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
