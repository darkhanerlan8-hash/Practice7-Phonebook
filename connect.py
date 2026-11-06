
import psycopg2
from getpass import getpass
from config import DB_CONFIG

def connect():
    password = getpass("PostgreSQL password: ")
    return psycopg2.connect(**DB_CONFIG, password=password)
