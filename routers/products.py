from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.database import get_db
from database.models.product import Product
from schemas.product import *
from logger import logger

router = APIRouter(prefix="/products", tags=["Товары"])


@router.get("/products", response_model=list[ProductWithCategory])
async def get_products(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    """
        Получить список товаров для главной страницы.

        Параметры:
        - skip: количество товаров для пропуска (пагинация)
        - limit: максимальное количество товаров для возврата (макс. 100)

        Возвращает:
        - Список товаров с информацией о категориях
        """
    try:
        # Получаем товары из БД с пагинацией
        result = await db.execute(
            select(Product)
            .offset(skip)
            .limit(min(limit, 100))  # Ограничиваем максимум 100 товаров
        )
        products = result.scalars().all()

        if not products:
            raise HTTPException(
                status_code=404,
                detail="Товары не найдены"
            )

        return products

    except Exception as e:
        logger.error(f"Ошибка при получении товаров: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )
