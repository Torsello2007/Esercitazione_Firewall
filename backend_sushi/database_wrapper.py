import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseWrapper:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "port": int(os.getenv("DB_PORT", 3306)),
            "database": os.getenv("DB_NAME"),
            "cursorclass": pymysql.cursors.DictCursor
        }
        self._setup_db()

    def _execute(self, query, params=None, fetch=True):
        conn = pymysql.connect(**self.config)
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                if fetch: return cur.fetchall()
                conn.commit()
                return cur.lastrowid
        finally: conn.close()

    def _setup_db(self):
        self._execute("CREATE TABLE IF NOT EXISTS categorie (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(50))", fetch=False)
        self._execute("CREATE TABLE IF NOT EXISTS prodotti (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100), prezzo DECIMAL(10,2), immagine TEXT, id_categoria INT)", fetch=False)
        self._execute("CREATE TABLE IF NOT EXISTS ordini (id INT AUTO_INCREMENT PRIMARY KEY, tavolo VARCHAR(10), cliente VARCHAR(50), stato VARCHAR(20) DEFAULT 'in attesa')", fetch=False)
        if not self._execute("SELECT id FROM prodotti"):
            self._execute("INSERT INTO categorie (nome) VALUES ('Sushi')", fetch=False)
            self._execute("INSERT INTO prodotti (nome, prezzo, immagine, id_categoria) VALUES ('Nigiri Salmone', 4.00, 'https://via.placeholder.com/150', 1), ('Uramaki Phil', 8.00, 'https://via.placeholder.com/150', 1)", fetch=False)

    def get_prodotti(self): return self._execute("SELECT * FROM prodotti")
    def add_ordine(self, t, c): return self._execute("INSERT INTO ordini (tavolo, cliente) VALUES (%s, %s)", (t, c), fetch=False)
    def get_ordini(self): return self._execute("SELECT * FROM ordini")
    def set_stato(self, id, s): return self._execute("UPDATE ordini SET stato=%s WHERE id=%s", (s, id), fetch=False)

db = DatabaseWrapper()
