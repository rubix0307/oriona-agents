from typing import Optional
from pydantic import BaseModel, Field, HttpUrl



class MetaInput(BaseModel):
    creator: Optional[str] = Field(None, description="Автор (dc:creator)")
    credit: Optional[str] = Field(None, description="Источник/кредит (photoshop:Credit)")
    rights: Optional[str] = Field(None, description="Правообладатель (dc:rights)")
    web_statement: Optional[HttpUrl] = Field(None, description="URL с условиями/правами (xmpRights:WebStatement)")
    licensor_url: Optional[HttpUrl] = Field(None, description="URL правообладателя/лицензора (plus:LicensorURL)")
    title: Optional[str] = Field(None, description="Заголовок (dc:title)")
    description: Optional[str] = Field(None, description="Описание (dc:description)")

class ConvertRequest(BaseModel):
    image_b64: str = Field(..., description="Base64 изображения (можно data:image/...;base64,...)")
    quality: int = Field(85, ge=0, le=100)
    method: int = Field(6, ge=0, le=6)
    metadata: Optional[MetaInput] = None

class ConvertResponse(BaseModel):
    image_webp_b64: str
    metadata_applied: bool
    fields_applied: list[str]
    width: int
    height: int
    webp_size_bytes: int
