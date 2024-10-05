from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('HOST'),
            port=os.environ.get('PORT', 5432),  # default to 5432
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('UNAME'),
            password=os.environ.get('PASS')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn is None:
        return 'Error connecting to the database'

    cur = conn.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    cur.close()
    conn.close()
    return f'Database connected: {db_version}'

if __name__ == '__main__':
    app.run(host='0.0.0.0')