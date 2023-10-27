from datetime import datetime
from typing import List, Set

from app.models.base import CharityDonationModel


def investment_process(
    target: CharityDonationModel,
    sources: List[CharityDonationModel]
) -> Set:
    if target.fully_invested:
        return target

    for source in sources:
        if source.fully_invested:
            continue

        target_invested = (
            target.invested_amount
            if target.invested_amount
            is not None else 0
        )
        source_invested = (
            source.invested_amount
            if source.invested_amount
            is not None else 0
        )

        needed_money = source.full_amount - source_invested
        amount_to_invest = min(target.full_amount - target_invested, needed_money)
        target.invested_amount = target_invested + amount_to_invest
        source.invested_amount = source_invested + amount_to_invest

        for obj in (target, source):
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()

        if target.fully_invested:
            break

    return target
