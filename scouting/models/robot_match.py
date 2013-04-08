# scouting/models/robot_match.py

from.base import Base

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Text,
    Boolean,
    Enum,
    )

class RobotMatch(Base):
    __tablename__ = 'robotmatches'
    id = Column(Integer, primary_key=True)
    robot_number = Column(Integer, ForeignKey('robots.number'))
    match_number = Column(Integer, ForeignKey('matches.number'))
    is_scouted = Column(Boolean)
    scout = Column(Text)
    position = Column(Enum('r_1', 'r_2', 'r_3', 'b_1', 'b_2', 'b_3'))

# All robots
    speed = Column(Integer)
    stability = Column(Enum('low', 'medium', 'high'))
    occurrences = Column(Text)

# Shooter/Dumper
    auto_1 = Column(Integer)
    auto_2 = Column(Integer)
    auto_3 = Column(Integer)
    auto_miss = Column(Integer)

    teleop_1 = Column(Integer)
    teleop_2 = Column(Integer)
    teleop_3 = Column(Integer)
    teleop_5 = Column(Integer)
    teleop_miss = Column(Integer)

# Climber
    attempted_climb = Column(Boolean)
    level_reached = Column(Enum('0', '10', '20', '30'))
    time_at_start = Column(Integer)
    time_at_end = Column(Integer)
    frisbees_dumped = Column(Integer)

# Human Loader
    human_loaded = Column(Integer)
    human_missed = Column(Integer)

# Ground Loader
    auto_loaded = Column(Integer)
    teleop_loaded = Column(Integer)

    def __lt__(self, other): return self.match_number < other.match_number
    def __le__(self, other): return self.match_number <= other.match_number
    def __eq__(self, other): return self.match_number == other.match_number
    def __ne__(self, other): return self.match_number != other.match_number
    def __gt__(self, other): return self.match_number > other.match_number
    def __ge__(self, other): return self.match_number >= other.match_number
