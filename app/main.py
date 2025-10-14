from dotenv import load_dotenv
load_dotenv('.env')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.agents import agents_router as agent_router


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

app.include_router(agent_router)

@app.get('/health')
def health():
    return {'status': 'ok'}