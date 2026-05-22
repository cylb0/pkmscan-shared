from enum import Enum
from pydantic import BaseModel
from ..domain import CardIdentity

class ImageTask(BaseModel):
    card: CardIdentity
    s3_key: str

class DBUpdateType(str, Enum):
    CARD_IMAGE_PROCESSED = "card_image_processed"

class CardImageProcessedPayload(BaseModel):
    id: int
    master_image_path: str

class DBUpdateMessage(BaseModel):
    event_type: DBUpdateType
    payload: CardImageProcessedPayload