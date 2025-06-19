from datetime import date
from typing import Optional

from pydantic import Field, EmailStr

from .base import BaseSchema, UsernameStr, NameStr, PasswordStr


class UserBase(BaseSchema):
    """Базовая схема пользователя с общими полями."""
    username: UsernameStr = Field(
        ...,
        description="Уникальное имя пользователя для входа (3-50 символов, a-z, 0-9, _)",
        examples=["john_doe", "alice123"]
    )
    email: EmailStr = Field(
        ...,
        description="Электронная почта пользователя",
        examples=["user@example.com"]
    )


class UserCreate(UserBase):
    """Схема для создания пользователя (регистрации)."""
    password: PasswordStr = Field(
        ...,
        description="Пароль (минимум 8 символов, 1 заглавная, 1 строчная, 1 цифра)",
        examples=["SecurePass123"],
        exclude=True  # Исключаем пароль из ответов API
    )
    firstname: NameStr = Field(
        ...,
        description="Имя пользователя (2-50 символов, только буквы и дефисы)",
        examples=["John", "Анна"]
    )
    last_name: NameStr = Field(
        ...,
        description="Фамилия пользователя (2-50 символов, только буквы и дефисы)",
        examples=["Doe", "Иванова"]
    )
    birthday: date = Field(
        ...,
        description="Дата рождения (не может быть в будущем)",
        examples=["1990-01-15"]
    )


class UserUpdate(BaseSchema):
    """Схема для обновления данных пользователя."""
    email: Optional[EmailStr] = Field(
        None,
        description="Новая электронная почта",
        examples=["new.email@example.com"]
    )
    firstname: Optional[NameStr] = Field(
        None,
        description="Имя пользователя",
        examples=["John"]
    )
    last_name: Optional[NameStr] = Field(
        None,
        description="Фамилия пользователя",
        examples=["Doe"]
    )
    birthday: Optional[date] = Field(
        None,
        description="Дата рождения",
        examples=["1990-01-15"]
    )


class UserInDB(UserBase):
    """Схема пользователя для возврата из БД (без пароля)."""
    id: int = Field(..., description="Уникальный идентификатор пользователя")
    firstname: NameStr = Field(..., description="Имя пользователя")
    last_name: NameStr = Field(..., description="Фамилия пользователя")
    birthday: date = Field(..., description="Дата рождения")
    is_active: bool = Field(True, description="Активен ли пользователь")
    created_at: date = Field(..., description="Дата регистрации")


class UserLogin(BaseSchema):
    """Схема для входа пользователя."""
    username: UsernameStr = Field(..., description="Имя пользователя или email")
    password: str = Field(..., description="Пароль", min_length=1)
