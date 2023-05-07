"""Module that expose some useful function for onetwotext"""

from cryptography.fernet import Fernet
from os.path import *


def credential_check(user: tuple, password: str) -> bool:
    """check password credential for onetwotext user

    Input:
    ------
    - user: tuples
     represent a variable holding user data from db.
    - password: str
     represent password entered by the user.
    """

    check_flag = False
    if user:
        fernet_file = open(
            join(dirname(realpath(__file__)), "config_data", "ott_fernet.key")
        )
        key = fernet_file.read()
        fernet = Fernet(key.encode())
        db_password = fernet.decrypt(user[1].encode()).decode()
        if db_password == password:
            check_flag = True
    return check_flag
