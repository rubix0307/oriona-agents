from langchain_core.messages import AIMessage
from pydantic import BaseModel
from app.agents.schema import StructuredResult


TypedStructuredResult = StructuredResult['ResearchResultSchema', AIMessage]

class ResearchResultItemSourseSchema(BaseModel):
    name: str
    url: str

class ResearchResultItemSchema(BaseModel):
    quote: str
    source: ResearchResultItemSourseSchema

class ResearchResultSchema(BaseModel):
    sources: list[ResearchResultItemSchema]
    summary: str
