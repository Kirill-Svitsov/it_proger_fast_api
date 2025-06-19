from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database.database import get_db
from database.models.user import User
from schemas.user import UserCreate, UserInDB, UserUpdate
from logger import logger

router = APIRouter()


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового пользователя"""
    try:
        # Проверяем, существует ли пользователь с таким username или email
        existing_user = await db.execute(
            select(User).where(
                (User.username == user.username) |
                (User.email == user.email)
            ))
        if existing_user.scalar():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем или email уже существует"
            )

        # Хешируем пароль (в реальном проекте используйте passlib или аналоги)
        hashed_password = f"hashed_{user.password}"  # Замените на реальное хеширование

        # Создаём объект пользователя для БД
        db_user = User(
            username=user.username,
            email=user.email,
            firstname=user.firstname,
            last_name=user.last_name,
            birthday=user.birthday,
            hashed_password=hashed_password
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        logger.info(f"Создан новый пользователь: {user.username}")
        return db_user

    except Exception as e:
        logger.error(f"Ошибка при создании пользователя: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при создании пользователя"
        )


@router.get("/", response_model=List[UserInDB])
async def get_users(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    """Получение списка пользователей"""
    try:
        result = await db.execute(
            select(User)
            .offset(skip)
            .limit(min(limit, 100))
        )
        users = result.scalars().all()
        return users
    except Exception as e:
        logger.error(f"Ошибка при получении пользователей: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении пользователей"
        )


@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получение информации о конкретном пользователе"""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return user
    except Exception as e:
        logger.error(f"Ошибка при получении пользователя {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении пользователя"
        )


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Обновление информации о пользователе"""
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )

        # Обновляем только переданные поля
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)
        logger.info(f"Обновлён пользователь {user_id}")
        return user
    except Exception as e:
        logger.error(f"Ошибка при обновлении пользователя {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении пользователя"
        )
