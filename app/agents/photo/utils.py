import base64
from PIL import Image
import io



def convert_b64_to_webp_b64(b64_string: str, quality: int = 90, method: int = 6, resize: bool = True, clear_xmp: bool = False) -> str:
    img = Image.open(io.BytesIO(base64.b64decode(b64_string)))
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    if resize:
        resize_map = {
            (1024, 1024): (1020, 1020),
            (1024, 1536): (1020, 1530),
            (1536, 1024): (1530, 1020),
        }
        if img.size in resize_map:
            new_size = resize_map[img.size]
            img = img.resize(new_size, resample=Image.Resampling.LANCZOS)

    xmp_data = {}
    if clear_xmp:
        xmp_data['xmp'] = b''

    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=quality, method=method, **xmp_data)
    webp_bytes = buf.getvalue()
    return base64.b64encode(webp_bytes).decode("utf-8")