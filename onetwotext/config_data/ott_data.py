"""TO DO"""

from typing import List
from cryptography.fernet import Fernet
from os.path import *

from onetwotext.config_data.config import AppConfig
from dataclasses import dataclass, is_dataclass

__all__ = ["get_ott_data"]


def nested_deco(*args, **kwargs):
    """decorator to wrap original __init__"""

    def wrapper(check_class):

        # passing class to investigate
        check_class = dataclass(check_class, **kwargs)
        o_init = check_class.__init__

        def __init__(self, *args, **kwargs):

            for name, value in kwargs.items():

                # getting field type
                ft = check_class.__annotations__.get(name, None)

                if is_dataclass(ft) and isinstance(value, dict):
                    obj = ft(**value)
                    kwargs[name] = obj
                o_init(self, *args, **kwargs)

        check_class.__init__ = __init__

        return check_class

    return wrapper(args[0]) if args else wrapper


@dataclass
class DefaultUser:
    """
    A dataclass holding default user credential parameters of onetwotext library.

    Attributes
    ----------

    username: str
        name of onetwotext user.
    
    password: str
        password of onetwotext user.
    """

    username: str
    password: str


@dataclass
class Links:
    """
    A dataclass holding sites of onetwotext library.

    Attributes
    ----------

    authority: str
        a string parameter holding authority uri of LLM owner.    
    
    origin: str
        a string parameter holding origin link in header request for LLM owner.
        
    api:str
        url for LLM neural network API.
    """
    
    authority: str
    origin: str
    api: str


@dataclass
class Paths:
    """
    A dataclass holding paths of interest for onetwotext library

    Attributes
    ----------

    db_rel_path: str
        a string parameter holding path for onetwotext db.
    """

    db_rel_path: str


@nested_deco
class Data:
    """
    A dataclass holding class parameters of onetwotext library.

    Attributes
    ----------

    name
    """
    
    default_user: DefaultUser
    links: Links
    paths: Paths


def get_ott_data() -> Data:
    """a function to get all onetwotext data and return as Data class"""

    _APP = AppConfig()
    
    data_dict = _APP.get_toml_data().get("ott_data")
    data = Data(**data_dict)
    return data
