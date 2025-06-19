from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import Base


class Product(Base):
    """
    Товар в магазине.
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(200), nullable=False, comment="Название товара")
    slug = Column(String(200), unique=True, nullable=False, comment="ЧПУ (например, 'iphone-15-pro')")
    description = Column(Text, comment="Полное описание с HTML-разметкой")
    price = Column(Numeric(10, 2), nullable=False, comment="Цена (макс. 99999999.99)")
    discount_price = Column(Numeric(10, 2), comment="Цена со скидкой, если есть")
    stock = Column(Integer, default=0, comment="Остаток на складе")
    is_active = Column(Boolean, default=True, comment="Активен ли товар для продажи")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Дата создания записи")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                        comment="Дата последнего обновления")

    # Внешние ключи
    category_id = Column(Integer, ForeignKey('categories.id'), comment="ID категории")

    # Связи
    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
