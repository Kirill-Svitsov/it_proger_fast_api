from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional, List
from pydantic import Field, field_validator
from .base import BaseSchema


class OrderItemBase(BaseSchema):
    """Базовая схема для позиции в заказе."""
    product_id: Annotated[
        int,
        Field(
            ...,
            gt=0,
            description="ID товара",
            examples=[1, 2]
        )
    ]
    quantity: Annotated[
        int,
        Field(
            1,
            gt=0,
            le=100,
            description="Количество товара (1-100)",
            examples=[1, 3]
        )
    ]


class OrderItemCreate(OrderItemBase):
    """Схема для создания позиции в заказе."""
    pass


class OrderItemInDB(OrderItemBase):
    """Схема позиции заказа для возврата из БД."""
    id: int = Field(..., description="Уникальный идентификатор позиции")
    price: Annotated[
        Decimal,
        Field(
            ...,
            gt=0,
            decimal_places=2,
            description="Цена на момент заказа"
        )
    ]
    order_id: int = Field(..., description="ID заказа")


class OrderBase(BaseSchema):
    """Базовая схема заказа."""
    address: Annotated[
        str,
        Field(
            ...,
            min_length=10,
            max_length=500,
            description="Адрес доставки (10-500 символов)",
            examples=["ул. Ленина, д. 10, кв. 25"]
        )
    ]
    phone: Annotated[
        str,
        Field(
            ...,
            min_length=5,
            max_length=20,
            description="Контактный телефон (5-20 символов)",
            examples=["+79161234567"]
        )
    ]


class OrderCreate(OrderBase):
    """Схема для создания заказа."""
    items: Annotated[
        List[OrderItemCreate],
        Field(
            ...,
            min_length=1,
            max_length=100,
            description="Список товаров в заказе (1-100 позиций)"
        )
    ]


class OrderUpdate(BaseSchema):
    """Схема для обновления заказа (в основном статуса)."""
    status: Annotated[
        Optional[str],
        Field(
            None,
            description="Новый статус заказа",
            examples=["paid", "shipped", "delivered", "cancelled"]
        )
    ] = None
    address: Annotated[
        Optional[str],
        Field(
            None,
            min_length=10,
            max_length=500,
            description="Новый адрес доставки"
        )
    ] = None
    phone: Annotated[
        Optional[str],
        Field(
            None,
            min_length=5,
            max_length=20,
            description="Новый контактный телефон"
        )
    ] = None


class OrderInDB(OrderBase):
    """Схема заказа для возврата из БД."""
    id: int = Field(..., description="Уникальный идентификатор заказа")
    status: str = Field("created", description="Текущий статус заказа")
    total_amount: Decimal = Field(..., description="Итоговая сумма заказа")
    created_at: datetime = Field(..., description="Дата создания заказа")
    user_id: int = Field(..., description="ID пользователя")


class OrderWithItems(OrderInDB):
    """Схема заказа с вложенными позициями."""
    items: List[OrderItemInDB] = Field(
        ...,
        description="Список позиций в заказе"
    )
