from sqlalchemy import Column, Integer, Text, ForeignKey

from app.core.db import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
