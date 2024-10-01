from dotenv import load_dotenv
import psycopg2
import os
load_dotenv()

DATABASE = os.environ['DATABASE']
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PWD']
HOST = os.environ['DB_HOST']
PORT = os.environ['DB_PORT']

class ResumeDB(object):
    def __init__(self):
        self.conn = self.get_connection()
        pass

    def get_connection(self):
        conn = psycopg2.connect(database=DATABASE,
                                user=USER,
                                password=PASSWORD,
                                host=HOST,
                                port=PORT)
        return conn

    def insert(self, query, data):
        self.conn.cursor().execute(query, data)
        self.conn.commit()
        self.conn.close()

    def select_all(self, query, where=None):
        with self.conn.cursor() as cur:
            cur.execute(query, where)
            rows = cur.fetchall()
            return rows

    def update(self, query, where):
        with self.conn.cursor() as cur:
            cur.execute(query, where)
            self.conn.commit()
            self.conn.close()

