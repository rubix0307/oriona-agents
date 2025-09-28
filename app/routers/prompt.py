from fastapi import HTTPException
from app.agents.prompt.agent import PromptAgent
from app.agents.prompt.schemas import PromptArticlePreviewResponse
from app.agents.schemas import ArticleRequest
from app.routers.routers import generate_router as router


@router.post('/prompt/article-image-preview', response_model=PromptArticlePreviewResponse)
def generate_article_preview(payload: ArticleRequest):
    try:
        agent = PromptAgent(model='gpt-5')
        return agent.generate_article_preview(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

