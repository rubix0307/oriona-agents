from app.agents.analyze.schemas import ArticleAnalyzeResponse, ArticleAnalyzeAgentResponse
from app.agents.base import BaseAgent

from app.agents.schemas import ArticleRequest


class AnalyzeAgent(BaseAgent):
    def analyze_article(self, data: ArticleRequest) -> ArticleAnalyzeResponse:
        user_msg = (
            f"Заголовок: {data.title}\n\n"
            f"Черновик статьи:\n{data.content}\n\n"
            f'Твоя задача отпределить эти параметры для статьи:\n'
            f'Нормально ли будет сгенерировать ИИ изображение'
            f' (только если генеративные модели изображений от openAI могут достойно изобразить тему,'
            f' а так же если это не новости, графики и другие схожие изоюражения где крайне важна точность изображения)\n'
            f'Нужен ли ресерч/фактчекинг информации в интернете (только в случае если тема не раскрыта, имеет возможные неточности или разногласия)\n'
            f'Предложи профессиональное СЕО название статьи\n'
            f'\n'
            f'ОТВЕТЬ СТРОГО В ВИДЕ ОДНОГО JSON-ОБЪЕКТА БЕЗ ЛИШНЕГО ТЕКСТА ВНЕ JSON:\n'
            f'{ArticleAnalyzeAgentResponse.model_str_schema()}\n'
        )

        messages = [
            {"role": "user", "content": user_msg},
        ]
        response, data = self.run_model(messages=messages, model=ArticleAnalyzeAgentResponse)

        return ArticleAnalyzeResponse(
            model=self.model,
            usage=response.usage,

            need_ai_image=data.need_ai_image,
            need_research=data.need_research,
            seo_title=data.seo_title,
        )