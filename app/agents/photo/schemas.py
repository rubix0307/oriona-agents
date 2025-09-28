from typing import Optional, Literal

from openai.types.images_response import Usage
from pydantic import BaseModel, Field
from app.agents.schemas import OpenAIUsage


class PhotoRequest(BaseModel):
    prompt: str = Field(..., description='Текстовый запрос для генерации изображения')
    size: Literal['1020x1020', '1020x1530', '1530x1020', 'auto'] = '1020x1020'
    quality: Literal['high', 'medium', 'low', 'auto'] = 'low'
    background: Literal['transparent'] | None = None


class PhotoResponse(OpenAIUsage):
    prompt: str
    image_webp_b64: Optional[str] = Field(None, description='WebP b64')
    usage: Usage
