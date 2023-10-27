from datetime import datetime

from sqlalchemy import Boolean, Column, CheckConstraint, DateTime, Integer

from app.core.db import Base


class CharityDonationModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_positive_full_amount'),
        CheckConstraint('invested_amount >= 0', name='check_non_negative_invested_amount'),
        CheckConstraint('invested_amount <= full_amount', name='check_invested_not_exceed_full_amount'),
    )

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}('
            f'id={self.id}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}'
            f')>'
        )
