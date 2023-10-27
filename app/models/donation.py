from sqlalchemy import Column, Integer, Text, ForeignKey

from app.models.base import CharityDonationModel


class Donation(CharityDonationModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr} user_id={self.user_id}, comment={self.comment}'
