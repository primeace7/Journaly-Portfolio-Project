from sqlalchemy.orm import DeclarativeBase
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime

"""Definition of BaseModel for all other models"""

class Base(DeclarativeBase):
    pass

class BaseModel():
    """implementation of Base class for all other models"""

    created_at = mapped_column(DateTime, default=datetime.now(tz=timezone.utc).isoformat())
    updated_at = mapped_column(DateTime, default=datetime.now(tz=timezone.utc).isoformat())
    
    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                if key != '__class__':
                    setattr(self, key, val)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.fromisoformat(kwargs["created_at"])
            else:
                self.created_at = datetime.now(tz=timezone.utc)
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.fromisoformat(kwargs["updated_at"])
            else:
                self.updated_at = datetime.now(tz=timezone.utc)
        else:
            self.created_at = datetime.now(tz=timezone.utc)
            self.updated_at = self.created_at

    def to_dict(self):
        """returns a dictionary representation of the class"""
        classes = ['user', 'insights', 'entries']
        dict_copy = {}
        dict_copy.update(self.__dict__)
        if not '__class__' in dict_copy:
            dict_copy['__class__'] = self.__class__.__name__
        if 'created_at' in dict_copy:
            dict_copy['created_at'] = dict_copy['created_at'].isoformat()

        if 'updated_at' in dict_copy:
            dict_copy['updated_at'] = dict_copy['updated_at'].isoformat()

        if '_sa_instance_state'in dict_copy:
            del dict_copy['_sa_instance_state']

        for key in classes:
            if key in dict_copy:
                if type(dict_copy[key]) == list:
                    dict_copy[key] = [obj.to_dict() for obj in dict_copy[key]]
                elif dict_copy[key].__class__.__name__ in ['User', 'Entries',
                                                           'Insights']:
                    dict_copy[key] = dict_copy[key].to_dict()

        return dict_copy
