from dataclasses import dataclass
from typing import Literal


Lang = Literal['en', 'ru']

@dataclass(frozen=True)
class StructuredResult[P, R]:
    parsed: P
    raw: R