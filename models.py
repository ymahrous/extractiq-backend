from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import Column, JSON
import uuid

class Document(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    filename: str
    s3_url: str  # The Cloudflare R2 URL
    status: str = "PENDING" # PENDING, PROCESSING, COMPLETED, FAILED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Extraction(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    document_id: str = Field(foreign_key="document.id")
    extracted_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON)) # hold our JSON {"vendor": "Acme", "total": 100}
    confidence_score: float = 0.0

# Add this to the bottom of models.py
class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str