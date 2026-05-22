from enum import Enum
from typing import Optional
from pydantic import BaseModel
from ..domain import CardIdentity

class ImageProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"

class DBUpdateType(str, Enum):
    CARD_IMAGE_PROCESSED = "card_image_processed"

class ImageTask(BaseModel):
    card: CardIdentity
    s3_key: str
    
class CardImageProcessedPayload(BaseModel):
    id: int
    status: ImageProcessingStatus
    error_message: Optional[str] = None
    master_image_path: Optional[str] = None

class DBUpdateMessage(BaseModel):
    event_type: DBUpdateType
    payload: CardImageProcessedPayload