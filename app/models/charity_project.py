from sqlalchemy import Column, String, Text

from app.models.base import CharityDonationModel


class CharityProject(CharityDonationModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr} name={self.name}, description={self.description}'
