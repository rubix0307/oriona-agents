from abc import ABC
from functools import cached_property
from typing import Optional, Literal, Protocol
from pydantic import BaseModel
from openai.types.shared import ChatModel
from langchain_core.messages import AIMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from .schema import StructuredResult, Lang


class BaseAgentABC[M: BaseModel](ABC):

    def __init__(
        self, *,
        model: ChatModel = 'gpt-5-nano',
        output_schema: type[M],
        prompt_template: ChatPromptTemplate,
        llm: Optional[BaseChatModel] = None,
        llm_service_tier: Literal['default'] = 'default',
    ) -> None:
        self.model: ChatModel = model
        self.output_schema: type[M] = output_schema
        self.prompt_template: ChatPromptTemplate = prompt_template
        self.llm: BaseChatModel = llm or ChatOpenAI(model=self.model, temperature=0, service_tier=llm_service_tier)

    @cached_property
    def chain(self) -> RunnableSequence:
        return self.prompt_template | self.llm.with_structured_output(self.output_schema, include_raw=True) # type: ignore

    def clear(self, result: StructuredResult) -> StructuredResult:
        return result

    def run(self, *, query: str, output_language: Lang, extra_info: Optional[dict] = None) -> StructuredResult[M, AIMessage]:
        if not query:
            raise ValueError('Query must not be empty')
        if not extra_info:
            extra_info = {}

        result = self.chain.invoke({'query': query, 'language': output_language, 'extra_info': extra_info})
        return self.clear(StructuredResult(parsed=result['parsed'], raw=result['raw']))

class AgentProtocol[M: BaseModel](Protocol):
    OUTPUT_SCHEMA: type[M]
