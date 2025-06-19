from sqlalchemy.ext.declarative import declarative_base  # Для создания базового класса моделей

# Создаем базовый класс для всех моделей SQLAlchemy.
# Все наши модели будут наследоваться от этого класса.
# Это необходимо для работы системы ORM SQLAlchemy.
Base = declarative_base()
