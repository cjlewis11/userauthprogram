'''
Chad J Lewis, 2/12/2021

This program will run the program and drive the UI mainly.
It will also control calling certain classes and functions to implement
core fucntionality, e.g. creating a user.
'''
from UserCreation import UserCreation
from UserManager import UserManager
from Authenticator import Authenticator

def main():
    '''
    This function is the driver function and runs the basic loop
    that controls program interaction.
    Functions are stored in a list for easy access via a UI input collector
    function.
    active_token is used to store the current active session token. Normal
    '''
    active_token = ""
    option_functions = {
                            "new_user": create_new_user,
                            "login": login_existing_user,
                            "logout": logout_current_user,
                            "input_error": input_error,
                            "exit": exit_application
                        }
    # Having no access to database usage, we use a class that manages our
    # userbase. We will pass this to all of our methods.
    userbase = UserManager()

    while(True):
        show_ui_options(active_token, userbase)
        active_token = option_functions[gather_user_input()](active_token, userbase)

        #UI formatting to clear up space.
        print("\n\n\n\n\n\n")




def create_new_user(active_token, userbase: UserManager) -> str:
    '''
    In this function, we create a new UserCreation object, then utilize that
    object to create a new user. This will require the use of an Authenticator
    Static Method, that is the Hash Function.
    '''
    creator = UserCreation(userbase)
    creator.create()
    if(userbase.is_active_token()):
        return active_token
    else:
        return ""

def login_existing_user(active_token, userbase: UserManager) -> str:
    '''
    In this function, we log the user in based on collected username and
    password. On success we recieve an active token, on failure we recieve no
    token. Prompts to user will be printed from class on failure.
    '''

    if userbase.is_active_token():
        userbase.logout_user(active_token)

    auther = Authenticator(userbase)
    return auther.login()

def logout_current_user(active_token, userbase: UserManager) -> str:
    '''
    This function will swiftly log the user out based on active_token usage.
    This removes the active token from the UserManager which is acting as our
    "server" in this case.
    '''

    if not userbase.is_active_token():
        print("There is no active session!")
        return ""

    return userbase.logout_user(active_token)

def exit_application(active_token, userbase: UserManager):
    '''
    Ends application runtime.
    '''
    exit()






def show_ui_options(active_token, userbase: UserManager):
    '''
    This function swiftly prints options for UI usage.
    '''

    if(active_token):
        username = userbase.get_user_from_token(active_token)
        print("Welcome {}, please enter the number of the options "
              "you'd like to use below.".format(username))
    else:
        print("Welcome, please enter the number of the options "
              "you'd like to use below.")
    print("1. Create a new user")
    print("2. Login as an existing user.")
    print("3. Logout from your current session.")
    print("4. Quit")


def gather_user_input():
    '''
    This function gathers user input then returns the key to the dictionary
    of functions stored in f
    '''
    choice = input("Choice: ")
    if choice == "1":
        return "new_user"
    elif choice == "2":
        return "login"
    elif choice == "3":
        return "logout"
    elif choice == "4":
        return "exit"
    else:
        return "input_error"

def input_error(active_token, userbase: UserManager):
    print("Please enter a valid option")

if __name__ == '__main__':
    main()
