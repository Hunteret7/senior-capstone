import psycopg2 as db_con  # Manage the connection to databse
import os  # Fetch credentials from the environment
from sys import stderr, argv # Print errors to stderr
from flask import Flask, json  # The framework for backend & dev server
from gevent.pywsgi import WSGIServer  # The production server for backend
from decimal import Decimal  # Allow override for decimal type in json serialization
import re # Regular expression for validation of input


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
        query = self.clean_query(query)
        self.cursor.execute(query, (user_input,))
        if include_headers:
            columns = [column[0] for column in self.cursor.description]
            return columns, self.cursor.fetchall()
        return self.cursor.fetchall()
    def close_connection(self):
        self.connection.close()
    def clean_query(self, query):
        # Very basic attempt at cleaning up the query
        # I believe psycopg2 does a fair bit of protection
        # but I'm sure it's not 100%
        return query.replace("'", "''").replace(";", "")
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
        
        # Start the server
        if self.devenv:
            # Development server
            app.run(host=self.host, port=self.port_number)
        else:
            # Production server
            http_server = WSGIServer((self.host, self.port_number), app)
            http_server.serve_forever()


def main():
    # May change argv passing to env variables
    if len(argv) > 1:
        api = BackendRESTAPI(int(argv[1]))
    else:
        api = BackendRESTAPI()


if __name__ == "__main__":
    main()
