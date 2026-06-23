import mysql.connector
from mysql.connector import Error
DB_CONFIG = {
    "host": "localhost",       # MySQL server address (localhost = your own PC)
    "user": "root",            # your MySQL username
    "password": "your_password",  # <-- CHANGE THIS to your MySQL password
    "database": "attendance_db"   # name of the database we created using schema.sql
}
def get_connection():
    """
    Creates and returns a new connection to the MySQL database.
    Every function that needs to talk to the database calls this function
    first, so we don't repeat connection code everywhere.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        # If the connection fails, print a clear error message.
        print(f"[ERROR] Could not connect to MySQL database: {e}")
        return None
def close_connection(connection, cursor=None):
    """
    Safely closes the cursor (if given) and the database connection.
    Always call this after you are done using the connection to avoid
    leaving connections open (which can slow down or crash MySQL).
    """
    try:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"[ERROR] Could not close connection properly: {e}")
def test_connection():
    """
    Simple helper function to check whether the database connection works.
    Run this file directly (python db_connection.py) to test your setup.
    """
    conn = get_connection()
    if conn is not None and conn.is_connected():
        print("Connection to MySQL database successful!")
        close_connection(conn)
    else:
        print("Connection failed. Please check DB_CONFIG settings in db_connection.py")
if __name__ == "__main__":
    test_connection()
