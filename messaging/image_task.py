from pydantic import BaseModel
from ..domain import CardIdentity

class ImageTask(BaseModel):
    card: CardIdentity
    s3_key: str
