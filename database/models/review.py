from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import Base


class Review(Base):
    """
    Отзыв покупателя о товаре.
    """
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    rating = Column(Integer, nullable=False, comment="Оценка (1-5 звезд)")
    text = Column(Text, comment="Текст отзыва")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Дата создания")

    # Внешние ключи
    user_id = Column(Integer, ForeignKey('users.id'), comment="ID автора отзыва")
    product_id = Column(Integer, ForeignKey('products.id'), comment="ID товара")

    # Связи
    product = relationship("Product", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating})>"
