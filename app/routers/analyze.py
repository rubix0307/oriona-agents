from fastapi import HTTPException
from app.agents.analyze.agent import AnalyzeAgent
from app.agents.analyze.schemas import ArticleAnalyzeResponse
from app.agents.schemas import ArticleRequest
from app.routers.routers import analyze_router as router


@router.post('/article', response_model=ArticleAnalyzeResponse)
def analyze_article(payload: ArticleRequest):
    try:
        agent = AnalyzeAgent(model='gpt-5-nano')
        return agent.analyze_article(data=payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

