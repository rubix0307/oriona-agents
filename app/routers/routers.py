from fastapi import APIRouter

generate_router = APIRouter(prefix='/v1/agent/generate', tags=['Generate'])
analyze_router = APIRouter(prefix='/v1/agent/analyze', tags=['Analyze'])
convert_router = APIRouter(prefix='/v1/metadata', tags=['Metadata'])