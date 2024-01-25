#!/usr/bin/env python3
"""Define Storage model to manage all DB storage tasks"""

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, select
import os
from .user import User
from .entries import Entries
from .insights import Insights
from .basemodel import Base



class Storage():
    """The model representing a storage object that allows for interaction
    with the db"""

    classes = {'User': User, 'Entries': Entries, 'Insights': Insights}

    def __init__(self):
        self.__db_uri = "mysql+mysqldb://{username}:{password}@{host}/{database}".format(
            username = os.getenv('USERNAME', default='journaly'),
            password = os.getenv('PASSWORD', default='journaly'),
            host = os.getenv('HOST', default='localhost'),
            database = os.getenv('DATABASE', default='journaly')
        )

        self.__engine = create_engine(self.__db_uri)

    def save(self):
        """Commit the current session to the database"""
        self.__session.commit()

    def add(self, cls):
        """Add a model class of type cls to the current session"""
        if isinstance(cls, tuple(self.classes.values())):
            self.__session.add(cls)

    def delete(self, cls):
        """Delete a model of type cls from the current session"""
        valid_class = self.validate_class(cls)
        if isinstance(cls, tuple(self.classes.values())):
            self.__session.delete(cls)

    def all_user_insights(self, user_id):
        """Return a list of dictionaries of all insights for a
        particular user_id"""
        user_dict = self.get('User', user_id)
        user = list(user_dict)[0]
        return [{insight: insight.to_dict()} for insight in user.insights]

    def all_user_entries(self, user_id):
        """Return a list of dictionaries of all entries for a
        particular user_id"""
        user_dict = self.get('User', user_id)
        user = list(user_dict)[0]
        return [{entry: entry.to_dict()} for entry in user.entries]

    def get(self, cls, item_id):
        """Fetch an item of type cls and id item_id from the database
        and return it as a dictionary"""
        valid_class = self.validate_class(cls)
        if valid_class:
            result = self.__session.execute(select(valid_class).filter_by(
                id=item_id)).first()
            if result is None:
                return {}
            return {result[0]: result[0].to_dict()}

    def all(self, cls):
        """Return all instances of type cls from storage as a list of
        dictionaries"""
        valid_class = self.validate_class(cls)
        if valid_class:
            result = self.__session.execute(select(valid_class))
            return [{row[0]: row[0].to_dict()} for row in result]
        else:
            print('invalid instance')

    def reload(self):
        """reloads data from the database or creates tables from the metadata
           collection if they don't already exist"""
        Base.metadata.create_all(self.__engine)
        self.__Session = sessionmaker(self.__engine, expire_on_commit=False)
        self.__session = self.__Session()

    def close(self):
        """close current session"""
        self.__session.close()

    def validate_class(self, cls):
        try:
            if type(cls) is str and cls in self.classes:
                return self.classes[cls]
            elif isinstance(cls, tuple(self.classes.values())):
                return type(cls)
            elif issubclass(cls, tuple(self.classes.values())):
                return cls
            else:
                return False
        except Exception:
            return False
