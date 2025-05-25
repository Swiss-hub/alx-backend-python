#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that fetches users in batches of `batch_size`."""
    connection = mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",
        password="your_mysql_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes each batch and filters users over age 25."""
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user["age"] > 25:
                print(user)  # still within 2 total loops
return()