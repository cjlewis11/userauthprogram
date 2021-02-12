'''
Chad Lewis 2/12/2021

The assumptions with being that we must store everything locally is that
we are not allowd to use a database. In doing so, we are utilizing a dictionary
structure that is non-persistent accross sessions. This means that our users
and passwords are reset every time. Had I been able to use a database, this
problem wouldn't exist.
'''
import csv
import secrets

class UserManager:
    def __init__(self):
        self.__filename = "storage.csv"
        self.__userStorage = {}
        self.__activeToken = {}

    def generate_active_token(self, username):
        token = secrets.token_bytes(16)
        self.__activeToken[token] = username
        return token

    def is_active_token(self):
        if self.__activeToken:
            return True
        else:
            return False

    def get_user_from_token(self, token):
        return self.__activeToken[token]

    def is_existing_user(self, username):
        return username in self.__userStorage

    def get_user_salt(self, username) -> str:
        return self.__userStorage[username]["salt"]

    def get_user_hash(self, username) -> str:
        return self.__userStorage[username]["hash"]


    def store_new_user(self, username, salt, passHash):
        self.__userStorage[username] = {
                                        "salt":salt.decode(),
                                        "hash": passHash
                                      }

    def logout_user(self, active_token) -> str:
        del self.__activeToken[active_token]
        print("Logged out successfully.")
        return ""
