from typing import Generic, List, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            object_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        db_object = await session.execute(
            select(self.model).where(
                self.model.id == object_id
            )
        )
        return db_object.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(
            self,
            object_in,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: bool = True
    ) -> ModelType:
        object_in_data = object_in.dict()
        if user is not None:
            object_in_data['user_id'] = user.id
        if 'invested_amount' not in object_in_data:
            object_in_data['invested_amount'] = 0
        db_object = self.model(**object_in_data)
        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object)
        return db_object

    async def update(
            self,
            db_object,
            object_in,
            session: AsyncSession
    ) -> ModelType:
        object_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(
            self,
            db_object: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        await session.delete(db_object)
        await session.commit()
        return db_object

    async def get_close_date(
        self,
        object_id: int,
        session: AsyncSession,
    ):
        db_object = await session.execute(
            select(self.model.close_date).where(
                self.model.id == object_id
            )
        )
        return db_object.scalars().first()

    async def get_invested_amount(
        self,
        object_id: int,
        session: AsyncSession,
    ):
        db_object = await session.execute(
            select(self.model.invested_amount).where(
                self.model.id == object_id
            )
        )
        return db_object.scalars().first()

    async def get_uninvested_objects(
        self,
        session: AsyncSession
    ):
        db_objects = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.id)
        )
        return db_objects.scalars().all()
