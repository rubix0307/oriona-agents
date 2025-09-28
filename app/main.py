from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from app.agents.photo.utils import convert_b64_to_webp_b64

load_dotenv('.env')

from app.routers import photo
from app.routers import prompt
from app.routers import analyze
from app.routers import meta


app = FastAPI(
    title='Agent API',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(photo.router)
app.include_router(prompt.router)
app.include_router(analyze.router)
app.include_router(meta.router)



class B64Request(BaseModel):
    b64_string: str
    autoresize: Literal[True] = True

@app.post("/convert_b64_to_webp")
def convert_b64_to_webp_router(req: B64Request):
    b64_webp = convert_b64_to_webp_b64(req.b64_string, resize=req.autoresize)
    return Response(content=b64_webp, media_type="image/webp")

@app.get('/health')
def health():
    return {'status': 'ok'}