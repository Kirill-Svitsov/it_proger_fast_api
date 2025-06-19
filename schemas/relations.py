from pydantic import Field
from decimal import Decimal
from datetime import datetime

from .category import CategoryInDB, CategoryBase
from .product import ProductInDB, ProductBase


class ProductWithCategory(ProductInDB):
    category: CategoryInDB = Field(..., description="Категория продукта")


class CategoryWithProducts(CategoryInDB):
    products: list[ProductInDB] = Field(
        default_factory=list,
        description="Список продуктов в этой категории"
    )


class CategoryInDB(CategoryBase):
    """Схема категории для возврата из БД."""
    id: int = Field(..., description="Уникальный идентификатор категории")
    description: str | None = Field(None, description="Описание категории")


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
