import requests
import random


port = 5440

class UserGenerator:
    def __init__(self, port):
        self.port = port
        self.add_users(10)
    def make_username():
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(random.randint(5, 10)))

    def make_name():
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(random.randint(5, 10))).capitalize()

    def make_password():
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(random.randint(5, 20)))

    def make_email(username):
        return "{}@{}.com".format(username, random.choice(["gmail", "yahoo", "hotmail"]))

    def add_users(num_users):
        for i in range(num_users):
            name = self.make_name()
            username = self.make_username()
            password = self.make_password()
            email = self.make_email(username)
            data = {
                "name": name,
                "username": username,
                "password": password,
                "email": email
            }
            print("Adding user #{}:\n".format(i+1), data)
            req = requests.post("http://localhost:{}/u/register".format(port), data=data)
            print(req.text)
