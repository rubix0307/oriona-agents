import base64
import io
from typing import Optional

from PIL import Image
from app.services.meta.schemas import ConvertResponse, MetaInput
from app.services.meta.utils import build_xmp, strip_data_url


def change_metadata(image_b64: str, quality: int, method: int, metadata: Optional[MetaInput] = None) -> ConvertResponse:

    raw = base64.b64decode(strip_data_url(image_b64))
    img = Image.open(io.BytesIO(raw))

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    xmp_bytes = build_xmp(metadata) if metadata else b""
    fields_applied = []
    if metadata:
        for name, val in metadata.model_dump().items():
            if val:
                fields_applied.append(name)

    buf = io.BytesIO()
    save_kwargs = dict(format="WEBP", quality=quality, method=method)
    if xmp_bytes:
        save_kwargs["xmp"] = xmp_bytes
    img.save(buf, **save_kwargs)
    webp_bytes = buf.getvalue()
    image_webp_b64 = base64.b64encode(webp_bytes).decode("utf-8")

    return ConvertResponse(
        image_webp_b64=image_webp_b64,
        metadata_applied=bool(xmp_bytes),
        fields_applied=fields_applied,
        width=img.width,
        height=img.height,
        webp_size_bytes=len(webp_bytes),
    )