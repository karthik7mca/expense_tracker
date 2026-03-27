# db_connect.py
import oracledb
from config import DB_USER, DB_PASSWORD, DB_DSN

def get_connection():
    connection = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )
    return connection