import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",  # or your db host
        database="WavPair",
        user="postgres",
        password="0251abkgtc"
    )
