from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from download import download_mp3
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import threading
app = FastAPI()
host_url = os.getenv('RENDER_EXTERNAL_URL', 'http://localhost:8000')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],

)

app.mount("/static", StaticFiles(directory="static"), name="static")


def eliminar(filename):
    threading.Timer(5.0, os.remove, args=[f'./static/{filename}']).start()
    print("Se elimino el archivo")
    

@app.post("/download")
async def download(req: Request):
    try:
        body = await req.json()
        url = body["url"]
        filename =  ( f"{ download_mp3( url ) }.mp3" ).replace(" ", "%20")
        print({ "url_download": f"{ host_url }/download/{ filename }" } )
        return { "url_download": f"{ host_url }/download/{ filename }" } 
        
    except Exception as e:
        print(e)
        return { "error": 'Error al descargar la musica.' }

@app.get("/download/{filename}")
async def download(req: Request):
    filename = req.path_params.get("filename")
    respuesta = FileResponse(f'./static/{filename}', filename = f'{filename}', media_type="audio/mp3")
    eliminar(filename)
    return respuesta

