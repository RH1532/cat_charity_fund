from datetime import datetime
from typing import List

from app.models.base import CharityDonationModel


def investment_process(
    target: CharityDonationModel,
    sources: List[CharityDonationModel]
) -> List[CharityDonationModel]:
    updated_sources = []
    for source in sources:
        target_invested = target.invested_amount
        source_invested = source.invested_amount
        amount_to_invest = min(target.full_amount - target_invested,
                               source.full_amount - source_invested)
        for changed_object in (target, source):
            changed_object.invested_amount += amount_to_invest
        for obj in (target, source):
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        if target.fully_invested:
            break
        updated_sources.append(source)
    return updated_sources
