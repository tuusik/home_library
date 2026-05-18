from pydantic import BaseModel, Field, ConfigDict

class SBookBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    author: str
    year: int
    pages: int = Field(..., gt=10)
    is_read: bool = False

class SBookAdd(SBookBase):
    pass

class SBook(SBookBase):
    id: int

