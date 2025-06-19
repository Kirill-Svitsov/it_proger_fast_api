from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base_model import Base


class Order(Base):
    """
    Заказ покупателя.
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    status = Column(String(50), default='created', comment="Статус: created/paid/shipped/delivered/cancelled")
    total_amount = Column(Numeric(12, 2), comment="Итоговая сумма заказа")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Дата создания заказа")
    address = Column(Text, comment="Адрес доставки")
    phone = Column(String(20), comment="Контактный телефон")

    # Внешние ключи
    user_id = Column(Integer, ForeignKey('users.id'), comment="ID покупателя")

    # Связи
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, status='{self.status}')>"


class OrderItem(Base):
    """
    Отдельная позиция в заказе.
    """
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    quantity = Column(Integer, default=1, comment="Количество товара")
    price = Column(Numeric(10, 2), comment="Цена на момент заказа (фиксируется)")

    # Внешние ключи
    order_id = Column(Integer, ForeignKey('orders.id'), comment="ID заказа")
    product_id = Column(Integer, ForeignKey('products.id'), comment="ID товара")

    # Связи
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id})>"
