# scouting/models/robot.py

from.base import Base

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    )

class Robot(Base):
    __tablename__ = 'robots'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    wheels = Column(Text)
    gearbox = Column(Text)
    drive_motors = Column(Text)
    description = Column(Text)
    scout = Column(Text)

    shooter = Column(Boolean)
    climb = Column(Boolean)
    human_loading = Column(Boolean)
    ground_loading = Column(Boolean)

    is_scouted = Column(Boolean)

    def __lt__(self, other): return self.number < other.number
    def __le__(self, other): return self.number <= other.number
    def __eq__(self, other): return self.number == other.number
    def __ne__(self, other): return self.number != other.number
    def __gt__(self, other): return self.number > other.number
    def __ge__(self, other): return self.number >= other.number
