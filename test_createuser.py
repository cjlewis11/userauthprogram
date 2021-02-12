'''
This module will handle all testing related to generating new users.
'''
import UserCreation
from UserCreation import UserCreation
from UserManager import UserManager
from Authenticator import Authenticator

import pytest
from unittest import mock
from unittest.mock import MagicMock
from io import StringIO

class TestUserCreation:

    def setUp(self):
        self.testing_salt = Authenticator.generate_salt()


    def test_gather_user_credentials_called(self):
        '''
        This function will test if we are correctly calling the gather_user_creation_details.
        '''
        userbase = UserManager()
        creator = UserCreation(userbase)

        creator.gather_user_creation_details = MagicMock(return_value=False)
        creator.create()
        creator.gather_user_creation_details.assert_called_once()

    def test_create_new_user(self):
        '''
        This function will test if we can correctly create a new user.
        '''
        userbase = UserManager()

        username = "chad"
        password = "password"
        salt = Authenticator.generate_salt()

        creator = UserCreation(userbase,username,password,salt)
        creator.gather_user_creation_details = MagicMock(return_value=True)
        creator.create()
        assert(userbase.is_existing_user(username) == True)

    def test_create_many_users(self):
        '''
        This test case will ensure that multiple users can be created in one session.
        '''
        userbase = UserManager()
        usernames = ["chad","jay","dylan","ellen","pat","jon"]
        passwords = ["password","hockey","cooking","teaching","painting","swimming"]
        salts = [Authenticator.generate_salt()] * 6

        for xx in range(0, len(usernames)):
            creator = UserCreation(userbase,usernames[xx],passwords[xx],salts[xx])
            creator.gather_user_creation_details = MagicMock(return_value = True)
            creator.create()
            assert(userbase.is_existing_user(usernames[xx]) == True)

        assert(userbase.get_total_users() == len(usernames))

    def test_create_duplicate_new_users(self):
        '''
        This test case will ensure that only 1 unique user exists per username.
        '''
        userbase = UserManager()
        usernames = ["chad","chad"]
        passwords = ["password","hockey"]
        salts = [Authenticator.generate_salt()] * 2

        for xx in range(0, len(usernames)):
            creator = UserCreation(userbase,usernames[xx],passwords[xx],salts[xx])
            creator.gather_user_creation_details = MagicMock(return_value = True)
            creator.create()

        assert(userbase.get_total_users() == len(usernames)-1)
