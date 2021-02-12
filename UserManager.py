'''
Chad Lewis 2/12/2021

The assumption is that all user information must be stored locally.
Doing so, we are assuming that there is no use of Databases allowed.
Therefore this class acts as a "database" by using a file system that is updated
whenever a user is added. It utlizies a dictionary data structure to ensure
that there are no duplicate users and the file is loaded into a dictionary when
initialized. In any other context, a database would be preferred for security
and optimization purposes.
'''
import csv

class UserManager:
    def __init__(self):
        self.__filename = "storage.csv"
        self.__userStorage = {}
        self.__createDictionary()

    def __createDictionary(self):
        '''
        This method will create a dictionary structure based on the
        file set in the initialization of this class.
        '''
        with open(self.__filename, newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                self.__userStorage[row[0]] = {
                                                "salt": row[1],
                                                "hash": row[2]
                                             }

    def is_existing_user(self, username):
        return username in self.__userStorage

    def store_new_user(self, username, salt, passHash):
        print(username)
        self.__userStorage[username] = {
                                        "salt":salt,
                                        "hash": passHash
                                      }
        print(self.__userStorage)

    def exit_routine(self):
        rows = []
        for key in self.__userStorage.keys():
            temp = []
            temp.append(key)
            entries = self.__userStorage[key]
            temp.append(entries["salt"])
            temp.append(entries["hash"])
            rows.append(temp)

        print(rows)

        with open(self.__filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ')
            for row in rows:
                writer.writerow(row)
