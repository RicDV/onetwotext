"""Module to make query on onetwotext db"""

from os.path import *
from typing import Union
from sqlite3 import connect, Connection, Cursor
from pathlib import Path
from cryptography.fernet import Fernet

from onetwotext.config_data.ott_data import get_ott_data

__OTT_DATA = get_ott_data()


def db_conn() -> Union[Cursor, Connection]:
    """function to connect to sqlite db"""

    db_path = Path(expanduser("~")) / __OTT_DATA.paths.db_rel_path
    if not Path(dirname(db_path)).exists():
        Path(dirname(db_path)).mkdir(parents=True)
    conn = connect(db_path)
    c = conn.cursor()
    return c, conn


def _create_table(c: Cursor, conn: Connection) -> None:
    """create onetwotext db"""

    c.execute("""CREATE TABLE IF NOT EXISTS ott_users (username TEXT, password TEXT)""")
    conn.commit()
    print("onetwotext db created successfully")


def get_user_data(username: str) -> tuple:
    """get user data from db"""

    c, conn = db_conn()
    c.execute(
        "SELECT * FROM ott_users WHERE username = ?",
        (username,),
    )
    user = c.fetchone()
    conn.close()
    return user


def create_db_and_default_user() -> None:
    """Create onetwotext db and insert a default user from config data"""

    c, conn = db_conn()
    _create_table(c, conn)

    username = __OTT_DATA.default_user.username
    password = __OTT_DATA.default_user.password

    c.execute(
        "INSERT INTO ott_users (username, password) VALUES (?, ?)", (username, password)
    )

    conn.commit()
    conn.close()
    print("Default onetwotext user inserted successfully")
