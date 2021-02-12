# Chad J Lewis, 2/12/2021

# This program will run the program and drive the UI mainly.
# It will also control calling certain classes and functions to implement
# core fucntionality, e.g. creating a user.
from UserCreation import UserCreation
from UserManager import UserManager

def main():
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
        show_ui_options()
        option_functions[gather_user_input()](userbase)

        #UI formatting to clear up space.
        print("\n\n\n\n\n\n")




def create_new_user(userbase: UserManager) -> bool:
    '''
    In this function, we create a new UserCreation object, then utilize that
    object to create a new user. This will require the use of an Authenticator
    Static Method, that is the Hash Function.
    '''
    creator = UserCreation(userbase)
    creator.create()

def login_existing_user(userbase: UserManager):
    print('login')

def logout_current_user(userbase: UserManager):
    print('logout')

def exit_application(userbase: UserManager):
    userbase.exit_routine()
    exit()






def show_ui_options():
    '''
    This function swiftly prints options for UI usage.
    '''

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

def input_error():
    print("Please enter a valid option")

if __name__ == '__main__':
    main()
