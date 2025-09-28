from typing import Optional

from pydantic import Field

from app.agents.schemas import OpenAIUsage, AgentResponse


class PromptArticlePreviewAgentResponse(AgentResponse):
    should_generate: bool = Field(..., description="Генерировать ли ИИ-изображение")
    rationale: Optional[str] = Field(
        None,
        description="Почему не генерируем (только если should_generate=false)"
    )
    prompt: str = Field(..., description="РУССКИЙ промпт для генерации превью статьи (120–200 слов)")


class PromptArticlePreviewResponse(OpenAIUsage, PromptArticlePreviewAgentResponse):
    ...