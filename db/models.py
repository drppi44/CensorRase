"""Database models."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transcription:
    """Transcription record."""
    id: int | None = None
    user_id: int = 0
    timestamp: datetime = None
    text: str = ""
    word_count: int = 0
