#!/usr/bin/python3
"""
This is module file_storage

This module defines one class FileStorage.
This class hadles saving the information in json in a file
"""
import json
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
# from models import storage
import os


class FileStorage:
    """
    Stores objects in a file in a json format

    **Class Attributes**
        __file_path: private, the path/to/file
        __objects: private, a dictionary of all the objects

    **Instance Attributes**
        __models_available: private, classes currently handled
    """
    __file_path = "file.json"
    if os.getenv("FS_TEST", "no") == "yes":
        __file_path = "test_file.json"
    __objects = {}

    def __init__(self):
        """Instantiate the class"""
        self.__models_available = {"User": User, "BaseModel": BaseModel,
                                   "Amenity": Amenity, "City": City,
                                   "Place": Place, "Review": Review,
                                   "State": State}
        self.reload()

    def all(self, cls=None):
        """
        Returns the required objects

        **Arguments**
            cls: not required, a valid Class Name
        """
        if cls is None:
            return FileStorage.__objects
        else:
            result = {}
            for k, v in FileStorage.__objects.items():
                if v.__class__.__name__ == cls:
                    result[k] = v
            return result

    def new(self, obj):
        """
        Adds a new object to __objects

        **Arguments**
            obj: an object
        """
        if obj is not None:
            FileStorage.__objects[obj.id] = obj

    def save(self):
        """puts all the object to file after serializing them"""
        store = {}
        for k in FileStorage.__objects.keys():
            store[k] = FileStorage.__objects[k].to_json()
        with open(FileStorage.__file_path, mode="w+", encoding="utf-8") as fd:
            fd.write(json.dumps(store))

    def reload(self):
        """
        Restart from what is saved on file
        All errors will be silently skipped
        """
        FileStorage.__objects = {}
        try:
            with open(FileStorage.__file_path,
                      mode="r+", encoding="utf-8") as fd:
                temp = json.load(fd)
        except Exception as e:
            return
        for k in temp.keys():
            cls = temp[k].pop("__class__", None)
            if cls not in self.__models_available.keys():
                continue
            # call a good init function
            FileStorage.__objects[k] = self.__models_available[cls](**temp[k])

    def delete(self, obj=None):
        """Remove an object from the dictionary"""
        if obj:
            FileStorage.__objects.pop(obj.id, None)
            self.save()

    def close(self):
        """Close a session"""
        self.reload()

    def get(self, cls, uid):
        '''This is the 'get' method.

        get retrieves one object.
        Returns the object based on class name and ID; or None.
        '''
        if cls in self.__models_available.keys():
            objs = self.all(cls)
            for key in objs.keys():
                if key == uid:
                    return objs[key]
        return None

    def count(self, cls=None):
        '''This is the 'count' method.

        count counts the number of objects in storage.
        Returns number of objects in storage matching a given class name;
        counts all objects if no name is passed.
        '''
        if cls is None:
            return len(self.__objects)
        if cls in self.__models_available:
            return len(self.all(cls))
        return -1
