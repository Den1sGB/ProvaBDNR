from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import requests
from typing import Optional

app = FastAPI()

# Configuração para servir arquivos estáticos
app.mount("/styles", StaticFiles(directory="styles"), name="styles")

# Configuração do OAuth2 para autenticação com o Django
class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None) -> Optional[str]:
        if request:
            return await super().__call__(request)
        elif websocket:
            token = self.get_token_from_url(websocket.url.path)
            if token is None:
                raise HTTPException(status_code=403, detail="Token não fornecido")
            return token
        else:
            raise HTTPException(status_code=400, detail="Requisição não suportada")

    def get_token_from_url(self, path: str) -> Optional[str]:
        token_index = path.rfind("/") + 1
        token = path[token_index:]
        return token

oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="http://localhost:8000/api/token/")

class User(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    username: str
    content: str

@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    response = requests.post("http://localhost:8000/api/token/", data={
        "grant_type": "password",
        "username": form_data.username,
        "password": form_data.password,
    })
    if response.status_code == 200:
        response_data = response.json()
        if "access_token" in response_data:
            return {"token": response_data["access_token"]}
        else:
            raise HTTPException(status_code=400, detail="Token não encontrado na resposta")
    else:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

@app.get("/login/", response_class=HTMLResponse)
async def get_login_page():
    with open("templates/login.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/chat/", response_class=HTMLResponse)
async def get_chat_page():
    with open("templates/chat.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws/chat/{username}/")
async def websocket_endpoint(websocket: WebSocket, username: str, token: str = Depends(oauth2_scheme)):
    if not username:
        raise HTTPException(status_code=400, detail="Nome de usuário não fornecido na rota websocket")
    
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(username=username, content=data)
            # Aqui você pode processar a mensagem como necessário, por exemplo, armazená-la no Redis
            await websocket.send_text(f"{username} disse: {data}")
    except WebSocketDisconnect:
        await websocket.close()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
