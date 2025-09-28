from typing import Optional

from openai.types import CompletionUsage
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):

    @classmethod
    def model_str_schema(cls):
        properties_clean = {}
        for name, property in cls.model_json_schema().get('properties', {}).items():
            try:
                description = property.get('description')
                properties_clean.update({name: property.get(
                                               'type',
                                               '|'.join([i['type'] for i in property.get('anyOf', [])])
                                               ) + (f' ({description})' if description else '')})
            except Exception as e:
                raise e

        return str(properties_clean)

class OpenAIUsage(BaseModel):
    model: str = Field(..., description='Name of the model')
    usage: Optional[CompletionUsage] = Field(
        None, description='Статистика по токенам, если доступна от API'
    )

class ArticleRequest(BaseModel):
    title: str = Field(..., description='Title of the article')
    content: str = Field(..., description='Content of the article')
