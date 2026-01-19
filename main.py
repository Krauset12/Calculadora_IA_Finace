from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# 1. Definimos qué datos esperamos recibir (La Comanda)
class DatosEntrada(BaseModel):
    saldo_inicial: float
    aporte_mensual: float
    tipo_moneda: str  # "CRC" o "USD"
    plazo_anos: int
    tasa_interes: float  # % Anual
    comision: float      # % Comisión

# 2. Tu función de bonificación (Idéntica a tu lógica original)
def obtener_tasa_bonificacion(meses, saldo, es_dolares):
    # (Aquí va tu lógica de if/else escalonada que ya tienes)
    # Por resumen, pongo un return simple, pero tú pega TU lógica completa aquí
    if meses < 24: return 0.0
    return 1.0 # Simplificado para el ejemplo

@app.get("/")
def home():
    return {"mensaje": "API de Pensiones BN Vital Activa"}

# 3. El Endpoint (La ventanilla donde n8n entrega los datos)
@app.post("/calcular")
def calcular(datos: DatosEntrada):
    es_dolares = True if datos.tipo_moneda == "USD" else False
    meses_totales = datos.plazo_anos * 12
    tasa_mensual = (1 + datos.tasa_interes/100)**(1/12) - 1
    
    saldo = datos.saldo_inicial
    total_invertido = datos.saldo_inicial
    
    # Ciclo de cálculo rápido
    for i in range(1, meses_totales + 1):
        rendimiento = saldo * tasa_mensual
        comision_monto = rendimiento * (datos.comision / 100)
        # Bonificación (Tu lógica)
        bonif = comision_monto * (obtener_tasa_bonificacion(i, saldo, es_dolares) / 100)
        
        saldo += (rendimiento - (comision_monto - bonif)) + datos.aporte_mensual
        total_invertido += datos.aporte_mensual

    # Devolvemos JSON limpio
    return {
        "moneda": datos.tipo_moneda,
        "saldo_proyectado": round(saldo, 2),
        "total_aportado": round(total_invertido, 2),
        "ganancia": round(saldo - total_invertido, 2)
    }