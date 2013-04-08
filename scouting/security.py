# scouting/security.py

from pyramid.security import unauthenticated_userid

from .models import (
    DBSession,
    User,
    )

from hashlib import sha512

def get_user(request):
    userid = unauthenticated_userid(request)
    if userid is not None:
        return DBSession.query(User).filter_by(name=userid).first()

def groupfinder(userid, request):
    user = DBSession.query(User).filter_by(name=userid).first()
    if user is not None: return [user.permission]

def authenticate(userid, password):
    user = DBSession.query(User).filter_by(name=userid).first()
    if user is None: return False
    else: return user.test(password)

