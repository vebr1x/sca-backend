from pydantic import BaseModel
from typing import List, Optional


class CatBase(BaseModel):
    name: str
    years_experience: int
    breed: str
    salary: float


class CatCreate(CatBase):
    pass


class CatUpdate(BaseModel):
    salary: float


class CatOut(CatBase):
    id: int
    class Config:
        orm_mode = True


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    is_complete: bool = False


class TargetCreate(TargetBase):
    pass


class TargetOut(TargetBase):
    id: int
    class Config:
        orm_mode = True


class MissionBase(BaseModel):
    is_complete: bool = False


class MissionCreate(MissionBase):
    targets: List[TargetCreate]


class MissionOut(MissionBase):
    id: int
    cat_id: Optional[int]
    targets: List[TargetOut] = []
    class Config:
        orm_mode = True
