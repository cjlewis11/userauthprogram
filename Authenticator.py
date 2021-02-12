import bcrypt

class Authenticator:

    @staticmethod
    def generate_salt():
        '''
        This function is used in generating the salt for the user password
        hash. We are using bcrypt to generate the hash.
        '''
        return bcrypt.gensalt()

    @staticmethod
    def generate_hash(password,salt,desired_key_bytes=32,rounds=100):
        print(password)
        print(salt)
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
