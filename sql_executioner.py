import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_tables():
    connection = get_connection()

    query = """
            UPDATE cameras
            SET
                status = 'offline',
                vision_status = 'offline'
            WHERE id = 1;
            """

    try:
        with connection.cursor() as cursor:

            cursor.execute(query)

        connection.commit()

    finally:
        connection.close()