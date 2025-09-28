from app.routers.routers import convert_router as router
from app.services.meta.schemas import ConvertResponse, ConvertRequest
from app.services.meta.service import change_metadata


@router.post("/image/edit", response_model=ConvertResponse)
def change(req: ConvertRequest):
    return change_metadata(image_b64=req.image_b64, quality=req.quality, method=req.method, metadata=req.metadata)
