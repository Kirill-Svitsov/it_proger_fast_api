from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .base_model import Base


class Category(Base):
    """
    Категория товаров (например: "Электроника", "Одежда").
    Не поддерживает вложенность (плоская структура).
    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False, unique=True, comment="Название категории")
    slug = Column(String(100), unique=True, nullable=False, comment="URL-идентификатор (например, 'electronics')")
    description = Column(Text, comment="Описание категории для SEO")

    # Связи
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
