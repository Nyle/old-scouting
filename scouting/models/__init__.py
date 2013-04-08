#scouting/models/__init__.py

from .base import (
    DBSession,
    Base,
    )

from .robot import Robot
from .match import Match
from .robot_match import RobotMatch
from .user import User

from pyramid.security import (
    Allow,
    Everyone,
    )

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'unapproved', 'user'),
                (Allow, 'scout', 'user'),
                (Allow, 'scout', 'add'),
                (Allow, 'lead_scout', 'user'),
                (Allow, 'lead_scout', 'add'),
                (Allow, 'lead_scout', 'edit'),
                (Allow, 'lead_scout', 'manage'),]
    def __init__(self, request):
        pass
