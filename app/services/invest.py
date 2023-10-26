from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def mark_as_invested_and_update(object):
    object.fully_invested = True
    object.close_date = datetime.now()


async def investment_process(
    object_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    db_object = CharityProject if isinstance(object_in, Donation) else Donation

    db_objects = await session.execute(
        select(db_object)
        .where(db_object.fully_invested.is_(False))
        .order_by(db_object.create_date.desc(), db_object.id.desc())
    )
    db_objects = db_objects.scalars().all()

    while db_objects and object_in.full_amount > object_in.invested_amount:
        db_object = db_objects.pop()

        needed_money = db_object.full_amount - db_object.invested_amount

        object_in.invested_amount += min(object_in.full_amount, needed_money)
        if object_in.invested_amount == object_in.full_amount:
            mark_as_invested_and_update(object_in)
            db_object.invested_amount += object_in.full_amount
            if db_object.invested_amount == db_object.full_amount:
                mark_as_invested_and_update(db_object)

        session.merge(db_object)
    
    session.merge(object_in)
    await session.commit()
    await session.refresh(object_in)
    return object_in
