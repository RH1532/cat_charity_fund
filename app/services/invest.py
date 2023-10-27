from datetime import datetime
from typing import List

from app.models.base import CharityDonationModel


def investment_process(
    target: CharityDonationModel,
    sources: List[CharityDonationModel]
) -> List[CharityDonationModel]:
    updated = []
    for source in sources:
        amount_to_invest = min(target.full_amount - target.invested_amount,
                               source.full_amount - source.invested_amount)
        for obj in (target, source):
            obj.invested_amount += amount_to_invest
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        if target.fully_invested:
            break
        updated.append(source)
    return updated
