from pydantic import Field

from app.agents.schemas import OpenAIUsage, AgentResponse


class ArticleAnalyzeAgentResponse(AgentResponse):
    need_ai_image: bool = Field(..., description="Генерировать ли ИИ-изображение")
    need_research: bool = Field(..., description="Нужен ли ресерч/фактчекинг")
    seo_title: str = Field(..., description="СЕО заголовок")

class ArticleAnalyzeResponse(OpenAIUsage, ArticleAnalyzeAgentResponse):
    ...