# scouting/models/user.py

from.base import Base

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Text,
    Boolean,
    Enum,
    )

from string import (
    ascii_letters,
    digits,
    )

from hashlib import sha512

from random import choice

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    password = Column(Text)
    permission = Column(Enum('unapproved', 'scout', 'lead_scout'))
    salt = Column(Text)

    def __init__(self, name, password, permission):
        self.name = name
        self.salt = ''.join(choice(ascii_letters + digits)
                            for i in range(64)).encode('utf-8')
        self.password = self.hash(password)
        self.permission = permission

    def test(self, password):
        return self.hash(password) == self.password

    def hash(self, password):
        return sha512(password.encode('utf-8') + self.salt).hexdigest()

    def set_password(self, password):
        self.password = self.hash(password)
