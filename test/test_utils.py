from os.path import *
from cryptography.fernet import Fernet
from onetwotext.utils import credential_check

def test_credential_check():
    key_path = join(dirname(dirname(abspath(__file__))),"onetwotext", "config_data", "ott_fernet.key")
    fernet_file = open(key_path)
    key = fernet_file.read()
    fernet = Fernet(key.encode())
    hashed_password = fernet.encrypt(b"think bigger").decode()
    user = ("voxy", hashed_password)
    assert credential_check(user, "think bigger") == True
    assert credential_check(user, "wrongpassword") == False
    assert credential_check(None, "think bigger") == False
