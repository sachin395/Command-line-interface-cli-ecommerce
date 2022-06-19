import mysql.connector
from my_cart_app.app_config import *

db_connection = mysql.connector.connect(
    database=MYSQL_DB_NAME,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    autocommit=True
)

