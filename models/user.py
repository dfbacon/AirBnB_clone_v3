#!/usr/bin/python3
"""
user module
    contains
        The User Class inherts from BaseModel, Base
"""
from models.base_model import BaseModel, Base, Table, Column, String
from sqlalchemy.orm import relationship, backref
from os import getenv


class User(BaseModel, Base):
    """
    User class
    """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
        initializes from BaseModel
        """
        value = kwargs.get("password", "")
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self.__dict__.get('_password', "")

    @password.setter
    def password(self, value):
        """
        hash the password

        Argument:
           value: password new value
        """
        pwd = bytes(value.encode("utf-8"))
        self.__dict__['_password'] = hashlib.md5(pwd).hexdigest()
