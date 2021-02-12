'''
Chad J Lewis, 2/12/2021

This module contains the class UserCreation which is used in creating new
users.
'''

from getpass import getpass

from UserManager import UserManager
from Authenticator import Authenticator

class UserCreation:
    '''
    This class handles all functions related to creating a new user.
    This class will call on Static Methods found in the following classes:
        Authenticator
    '''
    def __init__(self, userbase: UserManager, username="",password="",salt=""):
        self.__username = username
        self.__password = password
        self.__salt = salt
        self.__userbase = userbase

    @classmethod
    def createTestUser(self, username,password,salt,userbase: UserManager):
        '''
        This constructor is used for testing purposes.
        '''
        self.__username = username
        self.__password = password
        self.__salt = salt
        self.__userbase = userbase

    def create(self):
        '''
        This function handles the creation of a new user, it drives the process
        by gathering wanted user credentials, then using existing methods in
        UserManager class to store a new user.
        '''

        if self.gather_user_creation_details():
            self.__password = Authenticator.generate_hash(self.__password,self.__salt)
            if(self.__userbase.store_new_user(self.__username, self.__salt, self.__password)):
                return True
            else:
                return False

    def gather_user_creation_details(self) -> bool:
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
