'''
This module will handle all testing related to logging into a new user.
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


    def test_collect_user_credentials_called(self):
        '''
        This function will test if we are correctly calling the
        collect_user_credentials method
        '''
        userbase = UserManager()
        auther = Authenticator(userbase)

        auther.collect_user_credentials = MagicMock(return_value=False)
        auther.login()
        auther.collect_user_credentials.assert_called_once()


    def test_login(self):
        '''
        This function will test if we can login as an existing user.
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

    def test_bad_login(self):
        '''
        This test will check if we can login to an existing user with an
        incorrect password.
        '''
        userbase = UserManager()

        username = "chad"
        password = "password"
        wrong_pass = "Hello!"
        salt = Authenticator.generate_salt()

        # Create a new user
        creator = UserCreation(userbase,username,password,salt)
        creator.gather_user_creation_details = MagicMock(return_value=True)
        creator.create()
        assert(userbase.is_existing_user(username) == True)

        # Attempt to login to that user
        salt = userbase.get_user_salt(username)
        auther = Authenticator(userbase,username,wrong_pass,salt)
        auther.collect_user_credentials = MagicMock(return_value=True)
        token = auther.login()
        auther.collect_user_credentials.assert_called_once()


        assert(token is not None)
        assert(token == "")
        assert(userbase.get_user_from_token(token) == "")

    def test_many_bad_logins(self):
        '''
        This test will check if we can login to an existing user with an
        incorrect password.
        '''
        userbase = UserManager()

        username = "chad"
        password = "password"
        wrong_pass = "Hello!"
        salt = Authenticator.generate_salt()

        # Create a new user
        creator = UserCreation(userbase,username,password,salt)
        creator.gather_user_creation_details = MagicMock(return_value=True)
        creator.create()
        assert(userbase.is_existing_user(username) == True)

        # Try to login many times to the same user.
        for xx in range(0,10):
            salt = userbase.get_user_salt(username)
            auther = Authenticator(userbase,username,wrong_pass,salt)
            auther.collect_user_credentials = MagicMock(return_value=True)
            token = auther.login()
            auther.collect_user_credentials.assert_called_once()


            assert(token is not None)
            assert(token == "")
            assert(userbase.get_user_from_token(token) == "")


    def test_login_to_new_user_while_logged_in(self):
        '''
        This test will ensure that we can log into a new user while logged in as
        an old user. This should change the current session token.
        '''

        # Create many users.
        userbase = UserManager()
        usernames = ["chad","jay","dylan","ellen","pat","jon"]
        passwords = ["password","hockey","cooking","teaching","painting","swimming"]
        salts = [Authenticator.generate_salt()] * 6

        for xx in range(0, len(usernames)):
            creator = UserCreation(userbase,usernames[xx],passwords[xx],salts[xx])
            creator.gather_user_creation_details = MagicMock(return_value = True)
            creator.create()

        # login to one user
        salt = userbase.get_user_salt(usernames[0])
        auther = Authenticator(userbase,usernames[0],passwords[0],salt)
        auther.collect_user_credentials = MagicMock(return_value=True)
        token = auther.login()
        auther.collect_user_credentials.assert_called_once()

        # Ensure we've logged in correctly.
        assert(token is not None)
        assert(token != "")
        assert(userbase.get_user_from_token(token) == usernames[0])
        # store token to test against.
        old_token = token


        # Login to a new user.
        salt = userbase.get_user_salt(usernames[1])
        auther = Authenticator(userbase,usernames[1],passwords[1],salt)
        auther.collect_user_credentials = MagicMock(return_value=True)
        token = auther.login()
        auther.collect_user_credentials.assert_called_once()
        assert(token is not None)
        assert(token != "")
        assert(userbase.get_user_from_token(token) == usernames[1])
        assert(token != old_token)


    def test_bad_login_while_logged_in_as_user(self):
        '''
        This test will ensure that if we attempt to log into another account
        with the wrong credentials, while logged in our user will be logged out.
        '''

        # Create many users.
        userbase = UserManager()
        usernames = ["chad","jay","dylan","ellen","pat","jon"]
        passwords = ["password","hockey","cooking","teaching","painting","swimming"]
        salts = [Authenticator.generate_salt()] * 6

        for xx in range(0, len(usernames)):
            creator = UserCreation(userbase,usernames[xx],passwords[xx],salts[xx])
            creator.gather_user_creation_details = MagicMock(return_value = True)
            creator.create()

        # login to one user
        salt = userbase.get_user_salt(usernames[0])
        auther = Authenticator(userbase,usernames[0],passwords[0],salt)
        auther.collect_user_credentials = MagicMock(return_value=True)
        token = auther.login()
        auther.collect_user_credentials.assert_called_once()

        # Ensure we've logged in correctly.
        assert(token is not None)
        assert(token != "")
        assert(userbase.get_user_from_token(token) == usernames[0])
        # store token to test against.
        old_token = token


        # Fail to login to a new user.
        salt = userbase.get_user_salt(usernames[1])
        auther = Authenticator(userbase,usernames[1],"bad",salt)
        auther.collect_user_credentials = MagicMock(return_value=True)
        token = auther.login()
        auther.collect_user_credentials.assert_called_once()
        assert(token is not None)
        assert(token == "")
        assert(userbase.get_user_from_token(token) == "")
