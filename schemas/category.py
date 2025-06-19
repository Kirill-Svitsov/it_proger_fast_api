from typing import Annotated

from pydantic import Field

from .base import BaseSchema, NameStr, SlugStr


class CategoryBase(BaseSchema):
    """Базовая схема категории."""
    name: NameStr = Field(
        ...,
        max_length=100,
        description="Название категории (2-100 символов)",
        examples=["Электроника", "Одежда"]
    )
    slug: SlugStr = Field(
        ...,
        max_length=100,
        description="URL-идентификатор категории (латинница, цифры, дефисы)",
        examples=["electronics", "clothing"]
    )


class CategoryCreate(CategoryBase):
    """Схема для создания категории."""
    description: Annotated[
        str,
        Field(
            None,
            max_length=2000,
            description="Описание категории для SEO (максимум 2000 символов)"
        )
    ] = None


class CategoryUpdate(BaseSchema):
    """Схема для обновления категории."""
    name: Annotated[
        NameStr,
        Field(
            None,
            max_length=100,
            description="Новое название категории"
        )
    ] = None
    description: Annotated[
        str,
        Field(
            None,
            max_length=2000,
            description="Новое описание категории"
        )
    ] = None


class CategoryInDB(CategoryBase):
    """Схема категории для возврата из БД."""
    id: int = Field(..., description="Уникальный идентификатор категории")
    description: str | None = Field(None, description="Описание категории")
