from typing import Optional

from fastapi import APIRouter, Query
from app.agents.analyzer import AnalyzerAgent
from app.agents.researcher.agent import ResearcherAgent
from app.agents.schema import Lang
from app.agents.writer import WriterAgent

agents_router = APIRouter(prefix='/agents', tags=['agents'])

@agents_router.post('/analyzer', response_model=AnalyzerAgent.OUTPUT_SCHEMA)
def analyzer(query: str = Query(..., min_length=1), output_language: Lang = 'ru'):
    answer = AnalyzerAgent().run(query=query, output_language=output_language)
    return answer.parsed

@agents_router.post('/researcher', response_model=ResearcherAgent.OUTPUT_SCHEMA)
def researcher(query: str = Query(..., min_length=1), output_language: Lang = 'ru'):
    answer = ResearcherAgent().run(query=query, output_language=output_language)
    return answer.parsed

@agents_router.post('/writer', response_model=WriterAgent.OUTPUT_SCHEMA)
def writer(query: str = Query(..., min_length=1), extra_info: Optional[dict] = None, output_language: Lang = 'ru'):
    answer = WriterAgent().run(query=query, output_language=output_language, extra_info=extra_info)
    return answer.parsed


