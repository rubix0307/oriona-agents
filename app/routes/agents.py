from typing import Optional

from fastapi import APIRouter, Query
from app.agents.analyzer import AnalyzerAgent
from app.agents.researcher.agent import ResearcherAgent
from app.agents.schema import Lang
from app.agents.writer import WriterAgent

article_router = APIRouter(prefix='/agents', tags=['agents'])

@article_router.post('/analyzer')
def analyzer(query: str = Query(..., min_length=1), output_language: Lang = 'ru'):
    answer = AnalyzerAgent().run(query=query, output_language=output_language)
    return answer.parsed

@article_router.post('/researcher')
def researcher(query: str = Query(..., min_length=1), output_language: Lang = 'ru'):
    answer = ResearcherAgent().run(query=query, output_language=output_language)
    return answer.parsed

@article_router.post('/writer')
def writer(query: str = Query(..., min_length=1), extra_info: Optional[dict] = None, output_language: Lang = 'ru'):
    answer = WriterAgent().run(query=query, output_language=output_language, extra_info=extra_info)
    return answer.parsed


