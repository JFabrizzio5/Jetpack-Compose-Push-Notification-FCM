# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from firebase_admin import credentials, initialize_app, messaging
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Inicializar Firebase
cred = credentials.Certificate("FCM.json")
initialize_app(cred)

app = FastAPI()

# Configurar el directorio de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

class Notification(BaseModel):
    token: str
    title: str
    body: str

@app.post("/send_notification/")
async def send_notification(notification: Notification):
    message = messaging.Message(
        token=notification.token,
        notification=messaging.Notification(
            title=notification.title,
            body=notification.body
        )
    )
    try:
        response = messaging.send(message)
        return {"success": True, "message_id": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())
