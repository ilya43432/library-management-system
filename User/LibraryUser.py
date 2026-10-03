import csv
from werkzeug.security import generate_password_hash, check_password_hash
from Logger.Logger import Logger
from Notifications.Observer import Observer


class LibraryUser(Observer):
    def __init__(self, user_file='users.csv'):
        self.user_file = user_file
        self.loads_user_file()
        self.logged_in_user = None
        self.notifications = []
        self.logger = Logger()

    def loads_user_file(self):
        try:
            with open(self.user_file, 'x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['username', 'password'])
        except FileExistsError:
            pass

    def register_user(self, username, password):
        if self.user_exists(username):
            self.logger.log_info("registered fail")
            return False

        hashed_password = generate_password_hash(password)
        with open(self.user_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_password])
            print(" user is been registered.")
        self.logger.log_info("registered successfully")
        return True

    def authenticate_user(self, username, password):
        with open(self.user_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    if check_password_hash(row['password'], password):
                        self.logged_in_user = username
                        self.logger.log_info("logged in successfully")
                        return True
                    else:
                        self.logger.log_info("logged in fail")
                        return False
        self.logger.log_info("logged in fail")
        return False

    def user_exists(self, username):

        with open(self.user_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    return True
        return False

    def logout(self):

        if self.logged_in_user:

            self.logger.log_info("log out successful")
            self.logged_in_user = None
        else:
            self.logger.log_info("log out fail")

    def update(self, message):

        self.notifications.append(message)
        print(f"Notification received: {message}")
