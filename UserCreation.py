from getpass import getpass

from UserManager import UserManager
from Authenticator import Authenticator

class UserCreation:
    '''
    This class handles all functions related to creating a new user.
    This class will call on Static Methods found in the following classes:
        Authenticator
    '''
    def __init__(self, userbase: UserManager):
        self.__username = ""
        self.__password = ""
        self.__salt = ""
        self.__userbase = userbase

    def create(self):
        if self.__gather_user_creation_details():
            self.__password = Authenticator.generate_hash(self.__password.encode(),self.__salt)
            self.__userbase.store_new_user(self.__username, self.__password, self.__salt)

    def __gather_user_creation_details(self) -> bool:
        '''
        This function will run through the process of generating
        user credentials. It will also do some basic checking of valid entries.

        '''

        # Username input and validation checking
        desired_username = input("Desired Username:")
        if self.__userbase.is_existing_user(desired_username):
            print("Username already exists, please try again.")
            return False
        self.__username = desired_username
        
        # Password input and validation checking.
        desired_pass = getpass("Desired Password:")
        pass_secondattempt = getpass("Please re-enter your desired password:")
        if desired_pass != pass_secondattempt:
            print("Passwords do not match, try again.")
            return False
        self.__password = desired_pass

        # Wait until after validation to create salt.
        self.__salt = Authenticator.generate_salt()
        return True