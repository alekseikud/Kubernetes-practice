import requests
import psycopg
from dotenv import load_dotenv
import os
import time 
import json

load_dotenv()


def server_connect() -> psycopg.Connection | None:
    try:
        db_name = os.getenv("DB")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        connection: psycopg.Connection = psycopg.connect(
            dbname=db_name, user=user, password=password, host=host,port=port
        )
        return connection
    except Exception as _ex:
        raise ConnectionError(f"Exception {_ex} ocurred during connection to server")


def server_disconnect(connection: psycopg.Connection | None) -> None:
    if connection:
        connection.close()

if __name__=="__main__":
    connection:psycopg.Connection|None=server_connect()
    if not connection:
        raise
    connection.autocommit=True
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS prices \
                       (id SERIAL PRIMARY KEY,\
                       price NUMERIC(10,5) NOT NULL,\
                       created_at TIMESTAMPTZ DEFAULT NOW())")
        while True:
            time.sleep(10)
            request=requests.get("http://price-manager:8000/number")
            price=json.loads(request.text)["conversion_rate"]
            cursor.execute("INSERT INTO prices(price) VALUES (%s)",(round(price,5),))