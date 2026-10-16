import json
import aiofiles
import asyncio

ARCHIVO_BD="inventario.json"

async def leer_base_datos():
    try:
        async with aiofiles.open(ARCHIVO_BD, mode="r", encoding='utf-8') as f:
            contenido= await f.read()
            return json.loads(contenido)
        