import os  # Fetch credentials from the environment
from sys import argv # Print errors to stderr
from flask import Flask, json, request  # The framework for backend & dev server
from gevent.pywsgi import WSGIServer  # The production server for backend
import re # Regular expression for validation of input
import hashlib  # For hashing passwords

from database_man import DatabaseConnection


app = Flask(__name__)  # Create the flask app
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Pretty print json with newlines






class BackendRESTAPI():
    def __init__(self, port_num=5440):
        self.db_connection = DatabaseConnection()
        self.port_number    = port_num
        self.host           = "localhost"
        self.devenv         = True
        try:
            self.pepper = os.environ["PEPPER"]
        except KeyError:
            self.pepper = ""
        
        @app.route("/", methods=["GET"])
        def index():
            header, res = self.db_connection.execute_query(
                "SELECT * FROM rev2.users", include_headers=True)
            return json.jsonify({"header": header, "data": res})

        @app.route("/q/<query>", methods=["GET"])
        def query(query):
            header, res = self.db_connection.execute_query(query, include_headers=True)
            return json.jsonify({"header": header, "results": res})

        @app.route("/q/<query>/<user_input>", methods=["GET"])
        def query_with_input(query, user_input):
            header, res = self.db_connection.execute_query(query, user_input, include_headers=True)
            return json.jsonify({"header": header, "results": res})
        
        @app.route("/u/login", methods=["POST"])
        def login():
            # Validate the login
            re.match(r"\$a-zA-Z0-9_]{1,20}", request.form["username"])
            re.match(r"\$a-zA-Z0-9_]{1,20}", request.form["password"])
            un = request.form["username"]
            pw = request.form["password"]
            # Execute the query
            password_hash = self.db_connection.get_password_hash(un)
            if password_hash is None:
                return json.jsonify({"error": "Incorrect password or username"})
            print("nice")
            try:
                salt, hashed_password = password_hash.split("$")
                hash_val = hashlib.sha256((self.pepper + salt + request.form["password"]).encode()).hexdigest()
                if hash_val == hashed_password:
                    return json.jsonify({"success": True})
            except:
                pass
            return json.jsonify({"success": False})

        @app.route("/u/register", methods=["POST"])
        def register():
            try:
                # Validate the registration
                if not re.fullmatch(r"([a-zA-Z0-9_]{1,20}$)", request.form["username"]):
                    return json.jsonify({"error": "Invalid char or length in username"})
                if not re.fullmatch(r"([a-zA-Z0-9_]{1,20}$)", request.form["password"]):
                    return json.jsonify({"error": "Invalid char or length in password"})
                if not re.fullmatch( r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form["email"]):
                    return json.jsonify({"error": "Bad email"})

                """everything below this is super gross
                please make sure to include these fields in your form
                and post requests so i can delete this """
                try:
                    request.form["name"]
                except:
                    return json.jsonify({"error": "No name provided"})
                try:
                    bio = request.form["bio"]
                except:
                    bio = ""
                try:
                    phone = request.form["phone_number"]
                except:
                    phone = "0"
                try:
                    website = request.form["website"]
                except:
                    website = ""
                try:
                    role_type = request.form["user_role_type"]
                except:
                    role_type = "0"
                
                # Create the salt
                salt = os.urandom(16).hex()
                # Hash the password
                hash_val = hashlib.sha256((self.pepper + salt + request.form["password"]).encode()).hexdigest()
                password_hash = salt + "$" + hash_val
                # Execute the query
                try:
                    self.db_connection.execute_insert("INSERT INTO rev2.users\
                        (user_name,                bio, email,                 phone_number, website, name,                 user_role_type, password_hash) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                        (request.form["username"], bio, request.form["email"], phone,        website, request.form["name"], role_type,      password_hash))
                    return json.jsonify({"success": True})
                except db_con.errors.UniqueViolation:
                    return json.jsonify({"error": "Username already exists"})
            except KeyError:
                return json.jsonify({"success": False})


        # Start the server
        if self.devenv:
            # Development server
            app.run(host=self.host, port=self.port_number, debug=True, use_reloader=True)
        else:
            # Production server
            http_server = WSGIServer((self.host, self.port_number), app)
            http_server.serve_forever()


def main():
    # May change argv passing to env variables
    if len(argv) > 1:
        BackendRESTAPI(int(argv[1]))
    else:
        BackendRESTAPI()


if __name__ == "__main__":
    main()
