from typing import List, Optional

from pydantic import BaseModel, Json

# from packaging.version import Version

__all__ = ['QuoteBase', 'QuoteCreate', 'QuoteUpdate', 'QuoteInDBBase', 'Quote']


class QuoteBase(BaseModel):
    """Quote dataclass used to create a control Quotes objects"""
    id: int
    content: str
    author: str
    tags: List[str]
    length: str


class QuoteCreate(QuoteBase):
    ...


# Properties to receive via API on update
class QuoteUpdate(QuoteBase):
    id: Optional[int]
    content: Optional[str]
    author: Optional[str]
    tags: Optional[List[str]]


class QuoteInDBBase(QuoteBase):
    id: Optional[int]
    content: Optional[str]
    author: Optional[str]
    tags: Optional[List[str]]
    created_at = Optional[List[str]]
    updated_at = Optional[List[str]]

    class Quote:
        orm_mode = True


# Additional properties to return via API
class Quote(QuoteInDBBase):
    ...