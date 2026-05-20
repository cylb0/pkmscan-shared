from pydantic import BaseModel
from domain.card import CardIdentity

class ImageTask(BaseModel):
    card: CardIdentity
    s3_key: str
