from fastapi import HTTPException

from app.agents.photo.agent import PhotoAgent
from app.agents.photo.schemas import PhotoResponse, PhotoRequest
from app.agents.photo.utils import convert_b64_to_webp_b64
from app.routers.routers import generate_router as router


@router.post('/image', response_model=PhotoResponse)
def generate_image(payload: PhotoRequest):
    try:
        agent = PhotoAgent(model='gpt-image-1')

        resize_map = {
            '1020x1020': '1024x1024',
            '1020x1530': '1024x1536',
            '1530x1020': '1536x1024',
            'auto': 'auto',
        }
        result = agent.generate(
            prompt=payload.prompt,
            size=resize_map[payload.size],
            quality=payload.quality,
            background=payload.background,
        )
        return PhotoResponse(
            model=result.get('model'),
            image_webp_b64=convert_b64_to_webp_b64(result.get('image_b64'), resize=True, clear_xmp=True),
            prompt=result.get('prompt'),
            usage=result.get('usage'),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
