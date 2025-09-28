from app.agents.base import BaseAgent
from app.agents.prompt.schemas import PromptArticlePreviewResponse, PromptArticlePreviewAgentResponse
from app.agents.schemas import ArticleRequest


class PromptAgent(BaseAgent):

    def generate_article_preview(self, data: ArticleRequest) -> PromptArticlePreviewResponse:
        system_msg = (
            'Ты — главный редактор познавательного издания и медиа-этик. '
            'По заголовку и черновику определи, можно ли использовать ИИ-изображение, '
            'и создай ЕДИНЫЙ русский промпт для модели-писателя превью статьи.'
        )
        user_msg = (
            f'Заголовок: {data.title}\n\n'
            f'Черновик статьи:\n{data.content}\n\n'
            'РЕШЕНИЕ ПО ИЗОБРАЖЕНИЮ:\n'
            '- НЕ генерируй промпт для создания ИИ-изображение (should_generate=false),'
            'когда требуется точная передача реальных объектов/данных/снимков (микроскопия, телескопия, '
            'рентген/МРТ, судебные фото, уникальные экспериментальные установки, документы, инфографика с данными, '
            'диаграммы, карты, редкие артефакты, произведения, находки и т.п.). '
            '- Если ничего из вышеуказанного не применяется — можно генерировать (should_generate=true), '
            'но ИЗОБРАЖЕНИЕ НЕ ДОЛЖНО СОДЕРЖАТЬ НИКАКИХ НАЛОЖЕННЫХ ТЕКСТОВ (ни заголовков, ни надписей). Только естественные текстовые элементы, '
            'если они органично присутствуют на сцене (например, табличка в кадре).\n\n'
            'ПРОМПТ ДЛЯ ГЕНЕРАЦИИ ПРЕВЬЮ:\n'
            '- Сформируй один самодостаточный РУССКИЙ промпт для модели-художника, которая создаст превью\n'
            'ОТВЕТЬ СТРОГО В ВИДЕ ОДНОГО JSON-ОБЪЕКТА БЕЗ ЛИШНЕГО ТЕКСТА ВНЕ JSON:\n'
            f'{PromptArticlePreviewAgentResponse.model_str_schema()}'
        )

        messages=[
            {'role': 'system', 'content': system_msg},
            {'role': 'user', 'content': user_msg},
        ]
        response, data = self.run_model(messages, model=PromptArticlePreviewAgentResponse)
        return PromptArticlePreviewResponse(
            usage=response.usage,
            model=self.model,
            should_generate=data.should_generate,
            rationale=data.rationale,
            prompt=data.prompt,
        )
