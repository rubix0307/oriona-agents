from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from app.agents.base import BaseAgentABC
from .schema import AnalysisResultSchema


class AnalyzerAgent(BaseAgentABC[AnalysisResultSchema]):
    MODEL = 'gpt-5-nano'
    OUTPUT_SCHEMA = AnalysisResultSchema
    PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
        ('system',(
         'You are a precise analytical agent. '
         'Your task is to analyze the provided article and produce three outputs:\n\n'
         '1. **image_prompt** — Provide a detailed and creative '
         'AI image generation prompt **only if** the topic allows safe and appropriate image synthesis. '
         'If realistic accuracy or authenticity is critical '
         '(e.g., news, politics, law, real people, evidence photos, brand visuals, medical/scientific imagery), '
         'set it to null.\n\n'
         '2. **research** — Provide a research/search prompt **only if** the article seems incomplete, outdated, or unreliable. '
         'This prompt should help a researcher verify facts, expand missing information, or confirm data accuracy. '
         'If everything is complete and credible, set it to null.\n\n'

         'Rules for **image_prompt**:\n'
         '– Allowed for conceptual, artistic, or illustrative topics where realism is not critical '
         '(e.g., animals, nature, abstract ideas, metaphors, general lifestyle, technology concepts '
         'without real brands or products).\n'
         '– Must never depict real people, brands, news events, identifiable locations, or evidence-based content.\n'
         '– When allowed, describe the subject, style, atmosphere, composition, lighting, and emotional tone vividly.\n\n'

         'Rules for **research**:\n'
         '– Use only if the article lacks depth, contains questionable claims, or feels unfinished.\n'
         '– The prompt should include: goal of research, key questions to verify, recommended source types '
         '(official sites, major media, industry blogs, databases, studies), '
         'and search operator hints (quotes, site:, filetype:, intitle:, years, etc.).\n\n'
        )),
        ('human', 'Output language: {language}'),
        ('human', 'Article: {query}')
    ])

    def __init__(self, model: Optional[str] = None):
        super().__init__(
            model=model or self.MODEL,
            output_schema=self.OUTPUT_SCHEMA,
            prompt_template=self.PROMPT_TEMPLATE,
        )