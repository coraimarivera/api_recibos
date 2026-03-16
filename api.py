from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import os

app = FastAPI()

df = pd.read_excel("recibos.xlsx")


@app.get("/consulta")
def consulta(suministro: str):

    resultado = df[df["suministro"].astype(str) == suministro]

    if resultado.empty:
        raise HTTPException(
            status_code=404,
            detail="El número de suministro ingresado no se encuentra registrado en nuestro sistema. Por favor, verifica que hayas escrito correctamente los 6 dígitos."
        )

    data = resultado.iloc[0]

    monto = float(data["monto"])
    monto = f"{monto:.2f}"

    vencimiento = pd.to_datetime(data["vencimiento"])

    dias = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
    meses = ["enero","febrero","marzo","abril","mayo","junio","julio",
             "agosto","septiembre","octubre","noviembre","diciembre"]

    dia_semana = dias[vencimiento.weekday()]
    mes = meses[vencimiento.month - 1]

    fecha_formateada = f"{dia_semana} {vencimiento.day} de {mes} del {vencimiento.year}"

    archivo = data["archivo"]

    mensaje = f"""
Tienes un recibo por pagar de S/{monto}.
Tu último día de pago es {fecha_formateada}.

Págalo al toque a través de:
• Yape
• Plin
• Interbank
• Banca móvil BCP
• Caja de agentes
"""

    return {
        "mensaje": mensaje,
        "imagen_url": f"http://127.0.0.1:8000/recibo/{archivo}"
    }


@app.get("/recibo/{archivo}")
def obtener_recibo(archivo: str):

    ruta = f"./{archivo}"

    if not os.path.exists(ruta):
        raise HTTPException(
            status_code=404,
            detail="El archivo del recibo no se encuentra disponible."
        )

    return FileResponse(ruta)