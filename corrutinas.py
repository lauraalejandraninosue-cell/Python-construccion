import asyncio
def verificar_respuestas_moto_sync (repuesto):
    return f"Respuesto {repuesto} verificado (Sync)"
async def verificar_respuestas_moto_sync (repuesto):
    return f"Respuesto {repuesto} verificado (Async)"
