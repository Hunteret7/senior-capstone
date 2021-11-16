import psycopg2 as db_con  # Manage the connection to databse
import os  # Fetch credentials from the environment
from sys import stderr, argv # Print errors to stderr
from flask import Flask, json, request  # The framework for backend & dev server
from gevent.pywsgi import WSGIServer  # The production server for backend
from decimal import Decimal  # Allow override for decimal type in json serialization
import re # Regular expression for validation of input
import hashlib  # For hashing passwords


app = Flask(__name__)  # Create the flask app
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Pretty print json with newlines


class DatabaseConnection():
    def __init__(self):
        try:
            # Fetch credentials from the environment
            self.host_name = os.environ["DB_HOST_NAME"]
            self.db_user   = os.environ["DB_USER"]
            self.db_pass   = os.environ["DB_PASS"]
            self.db_name   = os.environ["DB_NAME"]
        except KeyError:
            # If >= 1 of the credentials are missing,
            print("Set environment variables DB_HOST_NAME, DB_USER, DB_PASS, DB_NAME", file=stderr)
            exit(1)
        
        # Connect to the database
        self.connection = db_con.connect(
            host=self.host_name, 
            user=self.db_user, 
            password=self.db_pass, 
            database=self.db_name)
        self.cursor = self.connection.cursor()
        # Set the override for decimal type (maybe datetimes in future?)
        json.JSONEncoder.default = self.default
    def execute_query(self, query, user_input="", include_headers=False):
        # Execute the query and return the results
        user_input = [self.clean_query(i) for i in user_input]            
        self.cursor.execute(query, user_input)
        if include_headers:
            columns = [column[0] for column in self.cursor.description]
            return columns, self.cursor.fetchall()
        return self.cursor.fetchall()
    def execute_insert(self, query : str, user_input : list):
        # Execute the query and return the results
        user_input = [self.clean_query(i) for i in user_input]
        self.cursor.execute(query, user_input)
        self.connection.commit()
    def get_password_hash(self, username):
        # Get the password hash for a user
        username = self.clean_query(username)
        print(f'{username=}')
        self.cursor.execute("SELECT password_hash FROM rev2.users WHERE user_name = %s", [username])
        try:
           return self.cursor.fetchone()[0]
        except TypeError:
            return None
    def close_connection(self):
        self.connection.close()
    def clean_query(self, query):
        # Very basic attempt at cleaning up the query
        # I believe psycopg2 does a fair bit of protection
        # but I'm sure it's not 100%
        if isinstance(query, str):
            return query.replace("'", "''")
        return query
    def default(self, o):
        # Override the default json serialization for decimal type
        if isinstance(o, Decimal):
            return float(o)



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
