'''
Chad J Lewis, 2/12/2021

This module contains the class Authenticator which is used in logging new users,
generating salt and hashes, and verifying credentials.
'''

import bcrypt
from getpass import getpass

from UserManager import UserManager

class Authenticator:
    '''
    The Authenticator class serves one major purpose, to verify login attempts
    by the user. In doing so, some static methods are also created that are used
    during the Creation of a new User. All non-static methods are used to login
    and verify attempts using PBKDF2 hashing.
    '''
    def __init__(self, userbase: UserManager):
        self.__username = ""
        self.__password = ""
        self.__salt = ""
        self.__userbase = userbase

    def login(self) -> str:
        '''
        Driver function for login operations. This function first calls
        __collect_user_credentials to gather user information, then verifys if
        that login information is correct based on PBKDF2 hash.
        '''

        if self.__collect_user_credentials():
            return self.__verify_login()


    def __collect_user_credentials(self):
        '''
        This function will run through the process of gathering user credentials
        for logging in.
        '''

        # Username input
        username = input("Username:")
        self.__username = username

        # Password input
        password = getpass("Desired Password:")
        self.__password = password

        if(self.__userbase.is_existing_user(username)):
            #After verifying that the username exists, gather the salt
            self.__salt = self.__userbase.get_user_salt(username)
        else:
            print("Username or password is incorrect. Try again")
            return False

        return True

    def __verify_login(self):
        '''
        This function is the core of the authentication system. This will use
        plaintext salt and hash with user input password, if they match
        we return a generated active_token otherwise, we return an empty token
        '''

        self.__password = Authenticator.generate_hash(self.__password,self.__salt.encode())
        if self.__userbase.get_user_hash(self.__username) == self.__password:
            return self.__userbase.generate_active_token(self.__username)
        else:
            print("Username or password is incorrect. Try again")
            return ""


    @staticmethod
    def generate_salt():
        '''
        This function is used in generating the salt for the user password
        hash. We are using bcrypt to generate the hash.
        '''
        return bcrypt.gensalt()

    @staticmethod
    def generate_hash(password,salt,desired_key_bytes=32,rounds=100):
        password = password.encode()

        '''
        We are utlizing bcrypt pbkdf function to hash our passwords. In this
        function we are doing so, and then returning the hash.
        '''
        hash = bcrypt.kdf(
            password = password,
            salt = salt,
            desired_key_bytes=desired_key_bytes,
            rounds=rounds
        )
        return hash
