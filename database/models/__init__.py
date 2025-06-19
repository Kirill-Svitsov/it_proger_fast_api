# Делаем все модели доступными через from models import ...
from .base_model import Base
from .user import User
from .category import Category
from .product import Product
from .order import Order, OrderItem
from .review import Review

# Для Alembic (миграции) нужно явно указать все модели
__all__ = ['Base', 'User', 'Category', 'Product', 'Order', 'OrderItem', 'Review']