from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints, Field

# Общие аннотации для повторяющихся типов
NameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Zа-яА-ЯёЁ\- ]+$"  # Разрешаем буквы, дефисы и пробелы
    )
]

UsernameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=3,
        max_length=50,
        pattern=r"^[a-z0-9_]+$"  # Только латинница, цифры и подчеркивания
    )
]

# PasswordStr = Annotated[
#     str,
#     StringConstraints(
#         min_length=8,
#         max_length=128,
#         pattern=r"^[A-Za-z\d@$!%*?&]*[A-Z][A-Za-z\d@$!%*?&]*[a-z][A-Za-z\d@$!%*?&]*\d[A-Za-z\d@$!%*?&]*[@$!%*?&][A-Za-z\d@$!%*?&]*$",
#     ),
#     Field(
#         ...,
#         description="Пароль должен содержать: "
#                     "8-128 символов, "
#                     "1 заглавную букву, "
#                     "1 строчную букву, "
#                     "1 цифру, "
#                     "1 специальный символ (@$!%*?&)",
#         examples=["SecurePass123!"]
#     )
# ]

PasswordStr = Annotated[
    str,
    StringConstraints(
        min_length=4,
        max_length=128
    ),
    Field(
        ...,
        description="Пароль должен содержать от 4 до 128 символов",
        examples=["1234", "password"]
    )
]

SlugStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=2,
        max_length=200,
        pattern=r"^[a-z0-9\-]+$"  # ЧПУ: латинница, цифры, дефисы
    )
]


class BaseSchema(BaseModel):
    """Базовая схема с общими настройками для всех моделей."""
    model_config = ConfigDict(
        from_attributes=True,  # Разрешает работу с ORM (ранее known_as_orm_mode)
        populate_by_name=True,  # Разрешает alias в полях
        str_strip_whitespace=True,  # Автоматически обрезает пробелы в строках
        str_min_length=1,  # Минимальная длина строк по умолчанию
    )
