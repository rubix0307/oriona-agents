from typing import Optional, cast

import requests
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai.types.shared_params import ChatModel

from app.agents.base import BaseAgentABC
from .schema import ResearchResultSchema, TypedStructuredResult


class ResearcherAgent(BaseAgentABC[ResearchResultSchema]):
    MODEL: ChatModel = 'gpt-5'
    OUTPUT_SCHEMA = ResearchResultSchema
    PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
        ('system', (
            'You are an experienced content analyst and SEO researcher.'
            'Your task is to independently search for and analyze up-to-date information on the Internet '
            'about the given article topic.'
            'You:'
            '1. Search for data only from authoritative and reliable sources '
            '   (official websites, well-known media outlets, industry blogs, research studies, statistical databases).'
            '2. Provide quotes in their original form with mandatory source attribution.'
            '3. Prepare a structured SEO summary that includes:'
            ' • key facts and data;'
            ' • relevant keywords and search intents;'
            ' • current trends or insights on the topic.'
            '4. Do not ask for permission to search for information — '
            'perform the search independently using the Internet.'

            'The result of your work should be an overview and summary of information suitable '
            'for writing an optimized SEO article.'
        )),
        ('human', 'Output language: {language}'),
        ('human', 'Article: {query}'),
    ])

    def __init__(self, model: Optional[ChatModel] = None):
        model = model or self.MODEL

        llm = cast(BaseChatModel,
            ChatOpenAI(
                model=model,
                temperature=0,
                service_tier='default',
                timeout=900,
            ).bind_tools(
                [{'type': 'web_search'},]
            )
        )

        super().__init__(
            llm=llm,
            model=model,
            output_schema=self.OUTPUT_SCHEMA,
            prompt_template=self.PROMPT_TEMPLATE,
        )

    def clear(self, result: TypedStructuredResult) -> TypedStructuredResult:

        clean_sources = []
        for item in result.parsed.sources:
            try:
                r = requests.get(url=item.source.url)
                r.raise_for_status()
                clean_sources.append(item)
            except requests.HTTPError:
                continue

        result.parsed.sources = clean_sources
        return result