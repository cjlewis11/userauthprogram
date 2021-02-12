import bcrypt
from getpass import getpass

from UserManager import UserManager

class Authenticator:

    def __init__(self, userbase: UserManager):
        self.__username = ""
        self.__password = ""
        self.__salt = ""
        self.__userbase = userbase

    def login(self) -> str:
        if self.__collect_user_credentials():
            self.__verify_login()


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
            print(self.__salt)
        else:
            print("Username or password is incorrect. Try again")
            return False

        return True

    def __verify_login(self):
        self.__password = Authenticator.generate_hash(self.__password,self.__salt.encode())
        if self.__userbase.get_user_hash(self.__username) == self.__password:
            self.__userbase.generate_active_token()
        print("Actual Hash: {}".format(self.__userbase.get_user_hash(self.__username)))
        print("Generated Hash {}".format(self.__password))


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
