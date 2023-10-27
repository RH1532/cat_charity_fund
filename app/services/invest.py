from datetime import datetime
from typing import List

from app.models.base import BaseModel


def investment_process(
    target: BaseModel,
    sources: List[BaseModel]
):
    for source in sources:
        while (target.invested_amount or 0) < (target.full_amount or 0) and not source.fully_invested:
            source_invested = source.invested_amount if source.invested_amount is not None else 0
            needed_money = (source.full_amount or 0) - source_invested
            amount_to_invest = min((target.full_amount or 0) - (target.invested_amount or 0), needed_money)
            target.invested_amount = (target.invested_amount or 0) + amount_to_invest
            source.invested_amount = source_invested + amount_to_invest
            if (target.invested_amount or 0) == (target.full_amount or 0):
                target.fully_invested = True
                target.close_date = datetime.now()
            if (source.invested_amount or 0) == (source.full_amount or 0):
                source.fully_invested = True
                source.close_date = datetime.now()
            if source.fully_invested:
                sources.remove(source)
    return target


async def update_db(
    session,
    db_object,
    object_in
):
    session.merge(db_object)
    session.merge(object_in)
    await session.commit()
    await session.refresh(object_in)
