from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=15, max_length=80)
    # le => <=
    year: int = Field(default=2022, le=2022)
    # le => <= | ge => >=
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    # Default Schema values
    class Config:
        schema_extra = {
            'example': {
                "id": 1,
                "title": "My Movie (Default)",
                "overview": "Movie Description (Default)",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
            }
        }
