#!/usr/bin/python3
"""
This is the db_storage module.
This module deals with storing and retrieving data from a mysql database.
This module contains one class DBStorage.
"""
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import (create_engine, func)
from sqlalchemy.orm import (sessionmaker, scoped_session)


class DBStorage:
    '''This is the 'DBStorage' class.

    Utilizes sqlAlchemy ORM to manage data from MySQL database.
    '''
    __engine = None
    __session = None

    def __init__(self):
        """
        initializes engine
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')))
        self.__models_available = {"User": User,
                                   "Amenity": Amenity, "City": City,
                                   "Place": Place, "Review": Review,
                                   "State": State}
        if getenv('HBNB_MYSQL_ENV', 'not') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        returns a dictionary of all the class objects
        """
        orm_objects = {}
        if cls:
            if cls in self.__models_available:
                for k in self.__session.query(
                        self.__models_available.get(cls)):
                    orm_objects[k.__dict__['id']] = k
        else:
            for i in self.__models_available.values():
                j = self.__session.query(i).all()
                if j:
                    for k in j:
                        orm_objects[k.__dict__['id']] = k
        return orm_objects

    def new(self, obj):
        """
        adds a new obj to the session
        """
        self.__session.add(obj)

    def save(self):
        """
        saves the objects fom the current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes an object from the current session
        """
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """
        WARNING!!!! I'm not sure if Base.metadata.create_all needs to
        be in the init method
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """
        close a session
        """
        self.__session.remove()

    def get(self, cls, uid):
        '''This is the 'get' method.

        get retrieves one object.
        Returns the object based on class name and ID; or None.
        '''
        if (cls not in self.__models_available) or (uid is None):
            return None
        return self.__session.query(
                self.__models_available[cls]).get(uid)

    def count(self, cls=None):
        '''This is the 'count' method.

        count counts the number of objects in storage.
        Returns number of objects in storage matching a given class name;
        counts all objects if no name is passed; -1 if class is invalid.
        '''
        if cls is None:
            count = 0
            for v in self.__models_available.values():
                count += self.__session.query(v).count()
            return count
        if cls in self.__models_available.keys():
            return self.__session.query(self.__models_available[cls]).count()
        return -1
