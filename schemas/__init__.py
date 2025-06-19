# Делаем все схемы доступными через from schemas import ...
from .base import BaseSchema
from .user import UserBase, UserCreate, UserUpdate, UserInDB, UserLogin
from .category import CategoryBase, CategoryCreate, CategoryUpdate, CategoryInDB
from .product import ProductBase, ProductCreate, ProductUpdate, ProductInDB, ProductWithReviews
from .order import OrderBase, OrderCreate, OrderUpdate, OrderInDB, OrderWithItems, OrderItemBase, OrderItemCreate, OrderItemInDB
from .review import ReviewBase, ReviewCreate, ReviewUpdate, ReviewInDB, ReviewWithUser
from .relations import *

# Для избежания циклических импортов
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import UserInDB
    from .category import CategoryInDB
    from .product import ProductInDB
    from .review import ReviewInDB

__all__ = [
    'BaseSchema',
    'UserBase', 'UserCreate', 'UserUpdate', 'UserInDB', 'UserLogin',
    'CategoryBase', 'CategoryCreate', 'CategoryUpdate', 'CategoryInDB', 'CategoryWithProducts',
    'ProductBase', 'ProductCreate', 'ProductUpdate', 'ProductInDB', 'ProductWithCategory', 'ProductWithReviews',
    'OrderBase', 'OrderCreate', 'OrderUpdate', 'OrderInDB', 'OrderWithItems', 'OrderItemBase', 'OrderItemCreate', 'OrderItemInDB',
    'ReviewBase', 'ReviewCreate', 'ReviewUpdate', 'ReviewInDB', 'ReviewWithUser'
]