import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from app.routes.agents import agents_router as agent_router


sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FastApiIntegration()],
    _experiments={
        'enable_logs': True
    },
    send_default_pii=True,
    profile_session_sample_rate=1.0,
    profile_lifecycle='trace'
)
app = FastAPI(
    title='Agent API',
    version='1.0.1',
)
app.add_middleware(SentryAsgiMiddleware)
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

@app.get('/alert')
def alert():
    raise RuntimeError('Prod alert')