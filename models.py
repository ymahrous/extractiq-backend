# models.py
from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from sqlalchemy import Column, JSON
from datetime import datetime, timezone
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

class Document(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    filename: str
    s3_url: str
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner_id: str = Field(foreign_key="user.id", index=True)

class Extraction(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    document_id: str = Field(foreign_key="document.id")
    extracted_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON)) # <--- CHANGE THIS LINE
    confidence_score: float = 0.0