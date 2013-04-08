# scouting/models/match.py

from .base import (
    Base,
    DBSession,
    )

from .robot_match import RobotMatch

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Text,
    Boolean,
    )

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)

    number = Column(Integer) # This does not support eliminations or replayed matches yet
    are_scores_entered = Column(Boolean)
    scout = Column(Text)

    r_1 = Column(Integer, ForeignKey('robots.number'))
    r_2 = Column(Integer, ForeignKey('robots.number'))
    r_3 = Column(Integer, ForeignKey('robots.number'))

    b_1 = Column(Integer, ForeignKey('robots.number'))
    b_2 = Column(Integer, ForeignKey('robots.number'))
    b_3 = Column(Integer, ForeignKey('robots.number'))

    r_disc = Column(Integer)
    r_climb = Column(Integer)
    r_foul = Column(Integer)
    r_total = Column(Integer)

    b_disc = Column(Integer)
    b_climb = Column(Integer)
    b_foul = Column(Integer)
    b_total = Column(Integer)

    def __init__(self, number, r_1, r_2, r_3, b_1, b_2, b_3):
        self.number = number
        self.r_1 = r_1
        self.r_2 = r_2
        self.r_3 = r_3
        self.b_1 = b_1
        self.b_2 = b_2
        self.b_3 = b_3

        are_scores_entered = False

        robot_matches = [RobotMatch(match_number=number, position=position,
                         robot_number=robot_number, is_scouted=False)
                         for robot_number, position in
                         [(r_1, 'r_1'), (r_2, 'r_2'), (r_3, 'r_3'),
                          (b_1, 'b_1'), (b_2, 'b_2'), (b_3, 'b_3')]]
        DBSession.add(self)
        for robot_match in robot_matches:
            DBSession.add(robot_match)

    def set(self, number, r_1, r_2, r_3, b_1, b_2, b_3):
        robot_matches = DBSession.query(RobotMatch).filter_by(
                                                            match_number=number)
        for robot_number, position in [(r_1, 'r_1'), (r_2, 'r_2'), (r_3, 'r_3'),
                                      (b_1, 'b_1'), (b_2, 'b_2'), (b_3, 'b_3')]:
            robot_match = robot_matches.filter_by(position=position).first()
            robot_match.robot_number = robot_number
            robot_match.match_number = number

        self.number = number
        self.r_1 = r_1
        self.r_2 = r_2
        self.r_3 = r_3
        self.b_1 = b_1
        self.b_2 = b_2
        self.b_3 = b_3




    def __lt__(self, other): return self.number < other.number
    def __le__(self, other): return self.number <= other.number
    def __eq__(self, other): return self.number == other.number
    def __ne__(self, other): return self.number != other.number
    def __gt__(self, other): return self.number > other.number
    def __ge__(self, other): return self.number >= other.number
