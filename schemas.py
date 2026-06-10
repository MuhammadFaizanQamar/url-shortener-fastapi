from pydantic import BaseModel
from datetime import datetime


class URLCreate(BaseModel):
    original_url: str


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
