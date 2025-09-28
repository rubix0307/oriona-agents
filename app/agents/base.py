import json
import re
from typing import Iterable

from openai import OpenAI, Omit, omit, Stream
from openai.types import ChatModel
from openai.types.chat import ChatCompletionMessageParam, completion_create_params, ChatCompletion, ChatCompletionChunk
from pydantic import BaseModel

class BaseAgent:

    def __init__(self, model: ChatModel = 'gpt-5-nano'):
        self.client = OpenAI()
        self.model = model

    @staticmethod
    def _extract_json(text: str) -> dict:
        fence = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S | re.I)
        if fence:
            text = fence.group(1)
        try:
            return json.loads(text)
        except Exception:
            match = re.search(r"\{(?:[^{}]|(?R))*\}", text, re.S)
            if match:
                return json.loads(match.group(0))
            raise ValueError("LLM did not return valid JSON")

    def run(self,
            messages: Iterable[ChatCompletionMessageParam],
            response_format: completion_create_params.ResponseFormat | Omit = omit,
        ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format=response_format,
        )

    def run_json(self, messages: Iterable[ChatCompletionMessageParam]) -> tuple[ChatCompletion | Stream[ChatCompletionChunk], dict]:
        resp = self.run(messages=messages, response_format={"type": "json_object"})
        content = resp.choices[0].message.content.strip()
        data = self._extract_json(content)
        return resp, data


    def run_model[T: BaseModel](
        self,
        messages: Iterable[ChatCompletionMessageParam],
        model: type[T],
    ) -> tuple[ChatCompletion | Stream[ChatCompletionChunk], T]:
        resp, data = self.run_json(messages=messages)
        return resp, model.model_validate(data)