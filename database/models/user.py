# Импортируем необходимые типы и модули
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID  # Для работы с UUID в PostgreSQL
import uuid  # Генератор уникальных идентификаторов
from .base_model import Base


class User(Base):
    """
    Модель пользователя для работы с базой данных.
    Каждый атрибут класса представляет собой колонку в таблице.
    """

    # Указываем имя таблицы в базе данных
    __tablename__ = "users"

    # Уникальный идентификатор пользователя (первичный ключ)
    # autoincrement=True - автоматическое увеличение значения
    # index=True - создание индекса для ускорения поиска
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Имя пользователя для входа в систему (должно быть уникальным)
    username = Column(String(50), unique=True, nullable=False)

    # Реальное имя пользователя
    firstname = Column(String(50), nullable=False)

    # Фамилия пользователя
    last_name = Column(String(50), nullable=False)

    # Дата рождения (тип Date для хранения только даты)
    birthday = Column(Date, nullable=False)

    # Электронная почта (максимальная длина 255 символов - стандарт для email)
    # unique=True - гарантирует уникальность email в системе
    email = Column(String(255), unique=True, nullable=False)

    # Хеш пароля (никогда не храним пароли в открытом виде!)
    # 255 символов достаточно для большинства алгоритмов хеширования
    hashed_password = Column(String(255), nullable=False)

    # Флаг активности пользователя (можно деактивировать без удаления)
    is_active = Column(Boolean, default=True)

    # Дата создания записи (автоматически устанавливается в текущую дату)
    created_at = Column(Date, default=date.today)

    # Дополнительный уникальный идентификатор для безопасности
    # UUID - это 128-битный уникальный идентификатор
    # as_uuid=True - хранить как тип UUID в PostgreSQL
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)

    # Дополнительные ограничения для таблицы
    __table_args__ = (
        # Гарантируем уникальность имени пользователя
        UniqueConstraint('username', name='uq_username'),

        # Гарантируем уникальность email
        UniqueConstraint('email', name='uq_email'),

        # Проверяем формат email с помощью регулярного выражения
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='email_format'
        ),

        # Проверяем что дата рождения не в будущем
        CheckConstraint("birthday <= CURRENT_DATE", name='valid_birthday')
    )

    def calculate_age(self) -> int:
        """
        Вычисляет возраст пользователя на текущую дату.
        Возвращает количество полных лет.
        """
        today = date.today()
        age = today.year - self.birthday.year

        # Учитываем, был ли уже день рождения в текущем году
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1

        return age

    def __repr__(self) -> str:
        """Строковое представление объекта для отладки."""
        return f"<User(id={self.id}, username='{self.username}')>"
