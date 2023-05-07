""" The Base config file that expose a Class to load and manage onetwotext file config. """

import os
from typing import Any, MutableMapping
import toml


class TomlConfig(object):
    """
    A class to holding methods of load and managing
    toml config file of onetwotext

    Parameters
    ----------
    toml_data: MutableMapping[str, Any]
        a private variable exposing onetwotext config data

    """

    toml_data: MutableMapping[str, Any] = {}

    def __init__(self, toml_path, toml_name):
        try:
            self.toml_dict = toml.load(os.path.join(toml_path, f"{toml_name}.toml"))
        except:
            raise FileNotFoundError(
                f"No config file for onetwotext in to user folder ({toml_path}). please check software installation and try again."
            )

    def get_toml_data(self) -> MutableMapping[str, Any]:
        return self.toml_dict


class AppConfig(TomlConfig):
    """A class to handle the TOML config file
    with the basic parameters of this application

    Parameters
    ----------

    __TOML_PATH: os.path.PathLike
        a private variable exposed as user folder path, where onetwotext config file is stored once installed.

    __TOML: str
        private variable exposing onetwotext config file name
    """

    __TOML_PATH = os.path.dirname(os.path.realpath(__file__))
    __TOML = "ott_data"

    def __init__(self):
        super().__init__(self.__TOML_PATH, self.__TOML)
