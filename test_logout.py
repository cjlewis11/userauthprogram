'''
This module will handle all testing related to logging out of an active user.
'''
import UserCreation
from UserCreation import UserCreation
from UserManager import UserManager
from Authenticator import Authenticator

import pytest
from unittest import mock
from unittest.mock import MagicMock
from io import StringIO

class TestUserLogin:

    def setUp(self):
        self.testing_salt = Authenticator.generate_salt()


    def test_logout_while_not_logged_in(self):
        '''
        This function will test that we can "logout" while not in an active
        session and no failures will occur.
        '''
        active_token = ""
        userbase = UserManager()
        assert(userbase.logout_user(active_token) == "")

    def test_logout_while_logged_in(self):
        '''
        This function will test that we can "logout" while in an active
        session and no failures will occur.
        '''

        userbase = UserManager()

        username = "chad"
        password = "password"
        salt = Authenticator.generate_salt()

        # Create a new user
        creator = UserCreation(userbase,username,password,salt)
        creator.gather_user_creation_details = MagicMock(return_value=True)
        creator.create()
        assert(userbase.is_existing_user(username) == True)

        # Login to that user
        salt = userbase.get_user_salt(username)
        auther = Authenticator(userbase,username,password,salt)
        auther.collect_user_credentials = MagicMock(return_value=True)
        token = auther.login()
        auther.collect_user_credentials.assert_called_once()


        assert(token is not None)
        assert(token != "")
        assert(userbase.get_user_from_token(token) == username)

        token = userbase.logout_user(token)
        assert(token == "")
