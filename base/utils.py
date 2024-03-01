from django.db import connections
import traceback


def print_exception(func):
    """
    Decorator that prints exception.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(traceback.format_exc())
            raise e
    return wrapper


def reconnect_to_database():
    """
    Reconnects to database if it falls.
    """

    # Get the default database connection
    db_connection = connections['default']

    # Close the existing connection
    db_connection.close()

    # Reopen the connection
    db_connection.connect()
