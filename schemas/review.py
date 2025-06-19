from typing import Annotated, Optional

from pydantic import Field

from .base import BaseSchema
from .user import UserInDB


class ReviewBase(BaseSchema):
    """Базовая схема отзыва."""
    rating: Annotated[
        int,
        Field(
            ...,
            ge=1,
            le=5,
            description="Оценка (1-5 звезд)",
            examples=[4, 5]
        )
    ]
    text: Annotated[
        str,
        Field(
            None,
            min_length=10,
            max_length=2000,
            description="Текст отзыва (10-2000 символов)",
            examples=["Отличный товар, всем рекомендую!"]
        )
    ] = None


class ReviewCreate(ReviewBase):
    """Схема для создания отзыва."""
    product_id: Annotated[
        int,
        Field(
            ...,
            gt=0,
            description="ID товара",
            examples=[1, 2]
        )
    ]


class ReviewUpdate(BaseSchema):
    """Схема для обновления отзыва."""
    rating: Annotated[
        Optional[int],
        Field(
            None,
            ge=1,
            le=5,
            description="Новая оценка"
        )
    ] = None
    text: Annotated[
        Optional[str],
        Field(
            None,
            min_length=10,
            max_length=2000,
            description="Новый текст отзыва"
        )
    ] = None


class ReviewInDB(ReviewBase):
    """Схема отзыва для возврата из БД."""
    id: int = Field(..., description="Уникальный идентификатор отзыва")
    created_at: str = Field(..., description="Дата создания отзыва")
    user_id: int = Field(..., description="ID автора отзыва")
    product_id: int = Field(..., description="ID товара")


class ReviewWithUser(ReviewInDB):
    """Схема отзыва с информацией об авторе."""
    user: "UserInDB" = Field(..., description="Автор отзыва")
