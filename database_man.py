import psycopg2 as db_con  # Manage the connection to databse
import os
from sys import stderr
from flask import json
from decimal import Decimal  # Allow override for decimal type in json serialization


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
