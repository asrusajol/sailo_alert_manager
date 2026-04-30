from dotenv import load_dotenv
import os
import psycopg2
from datetime import datetime

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = 5432


conn = psycopg2.connect(
    host = DB_HOST,
    database = DB_NAME,
    user = DB_USER,
    password = DB_PASS,
    port = DB_PORT
)

cursor =conn.cursor()

def store_sensor_state(data):
    try:
        query = """
                INSERT INTO sensor_states (time, device_name, sensor_states)
                VALUES (%s, %s, %s)
                """

        values = (
            datetime.now().astimezone(),
            data["device_name"],
            int(data["sensor_states"])
        )
        cursor.execute(query, values)
        conn.commit()
        print(data)
        print(f"Data have been saved in Database")

    except Exception as e:
        print("Error: ", e)
        conn.rollback()