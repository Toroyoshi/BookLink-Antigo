from pydantic import BaseModel, Field

class WorkCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    isbn: str | None = None
    description: str | None = None
    year: int | None = None
    language: str | None = None
    subjects: str | None = None

class WorkOut(BaseModel):
    id: int
    title: str
    isbn: str | None
    year: int | None
    language: str | None
    subjects: str | None

class CopyCreate(BaseModel):
    barcode: str = Field(min_length=1, max_length=100)
    location: str | None = None

class CopyOut(BaseModel):
    id: int
    work_id: int
    barcode: str
    status: str
    location: str | None
