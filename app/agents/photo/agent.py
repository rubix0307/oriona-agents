from typing import Optional, Literal, Dict, Any
from app.agents.base import BaseAgent


class PhotoAgent(BaseAgent):
    def __init__(self, model: str = 'gpt-image-1'):
        super().__init__(model=model)

    def generate(
        self,
        prompt: str,
        size: Literal['1024x1024', '1024x1536', '1536x1024', 'auto'] = 'auto',
        quality: Literal['high', 'medium', 'low', 'auto'] = 'auto',
        background: Optional[Literal['transparent']] = None,
    ) -> Dict[str, Any]:
        resp = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=size,
            quality=quality,
            background=background,
        )

        data = resp.data[0]
        b64 = getattr(data, 'b64_json', None)

        usage = getattr(resp, 'usage', None)
        if usage is not None and hasattr(usage, 'model_dump'):
            usage = usage.model_dump()

        return {
            'prompt': prompt,
            'model': self.model,
            'image_b64': b64,
            'usage': usage,
        }