import requests
import random


port = 5440


class UserGenerator:
    def make_username():
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(random.randint(5, 10)))

    def make_name():
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(random.randint(5, 10))).capitalize()

    def make_password():
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(random.randint(5, 20)))

    def make_email(username):
        return "{}@{}.com".format(username, random.choice(["gmail", "yahoo", "hotmail"]))

    @classmethod
    def add_users(self, num_users):
        for i in range(num_users):
            name = UserGenerator.make_name()
            username = UserGenerator.make_username()
            password = UserGenerator.make_password()
            email = UserGenerator.make_email(username)
            data = {
                "name": name,
                "username": username,
                "password": password,
                "email": email
            }
            print("Adding user #{}:\n".format(i+1), data)
            req = requests.post("http://localhost:{}/u/register".format(port), data=data)
            print(req.text)

UserGenerator.add_users(1)
