from pydantic import BaseModel
from .languages import SupportedLanguage

class CardIdentity(BaseModel):
    expansion: str
    lang: SupportedLanguage
    id: str
