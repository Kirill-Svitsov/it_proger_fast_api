from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from pydantic import Field, field_validator

from .base import BaseSchema, SlugStr
from .review import ReviewInDB


class ProductBase(BaseSchema):
    """Базовая схема продукта."""
    name: Annotated[
        str,
        Field(
            ...,
            min_length=2,
            max_length=200,
            description="Название товара (2-200 символов)",
            examples=["iPhone 15 Pro", "Футболка хлопковая"]
        )
    ]
    slug: SlugStr = Field(
        ...,
        max_length=200,
        description="ЧПУ для URL (латинница, цифры, дефисы)",
        examples=["iphone-15-pro", "cotton-t-shirt"]
    )
    price: Annotated[
        Decimal,
        Field(
            ...,
            gt=0,
            le=99999999.99,
            decimal_places=2,
            description="Цена (от 0.01 до 99,999,999.99)",
            examples=[999.99, 1499.00]
        )
    ]


class ProductCreate(ProductBase):
    """Схема для создания продукта."""
    description: Annotated[
        str,
        Field(
            None,
            max_length=10000,
            description="Полное описание с HTML-разметкой (максимум 10000 символов)"
        )
    ] = None
    discount_price: Annotated[
        Optional[Decimal],
        Field(
            None,
            gt=0,
            le=99999999.99,
            decimal_places=2,
            description="Цена со скидкой (если есть)",
            examples=[899.99, 1299.00]
        )
    ] = None
    stock: Annotated[
        int,
        Field(
            0,
            ge=0,
            description="Количество товара на складе",
            examples=[10, 100]
        )
    ] = 0
    category_id: Annotated[
        int,
        Field(
            ...,
            gt=0,
            description="ID категории товара",
            examples=[1, 2]
        )
    ]

    @field_validator('discount_price')
    def validate_discount_price(cls, v, values):
        """Проверяем, что цена со скидкой меньше обычной цены."""
        if v is not None and 'price' in values.data and v >= values.data['price']:
            raise ValueError("Discount price must be less than regular price")
        return v


class ProductUpdate(BaseSchema):
    """Схема для обновления продукта."""
    name: Annotated[
        Optional[str],
        Field(
            None,
            min_length=2,
            max_length=200,
            description="Новое название товара"
        )
    ] = None
    description: Annotated[
        Optional[str],
        Field(
            None,
            max_length=10000,
            description="Новое описание товара"
        )
    ] = None
    price: Annotated[
        Optional[Decimal],
        Field(
            None,
            gt=0,
            le=99999999.99,
            decimal_places=2,
            description="Новая цена"
        )
    ] = None
    discount_price: Annotated[
        Optional[Decimal],
        Field(
            None,
            gt=0,
            le=99999999.99,
            decimal_places=2,
            description="Новая цена со скидкой"
        )
    ] = None
    stock: Annotated[
        Optional[int],
        Field(
            None,
            ge=0,
            description="Новое количество товара"
        )
    ] = None
    is_active: Annotated[
        Optional[bool],
        Field(
            None,
            description="Активен ли товар для продажи"
        )
    ] = None


class ProductInDB(ProductBase):
    """Схема продукта для возврата из БД."""
    id: int = Field(..., description="Уникальный идентификатор продукта")
    description: str | None = Field(None, description="Описание продукта")
    discount_price: Decimal | None = Field(None, description="Цена со скидкой")
    stock: int = Field(0, description="Остаток на складе")
    is_active: bool = Field(True, description="Активен ли товар")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата последнего обновления")
    category_id: int = Field(..., description="ID категории")


class ProductWithReviews(ProductInDB):
    """Схема продукта с отзывами."""
    reviews: list["ReviewInDB"] = Field(
        default_factory=list,
        description="Список отзывов о товаре"
    )
