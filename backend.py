import sqlite3

class Database:

    def __init__(self, db):
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, start_date text, end_date text, description text, duration integer)")
        self.conn.commit()

    def insert(self, start_date, end_date, description, duration):
        self.cur.execute("INSERT INTO sessions VALUES (NULL,?,?,?,?)",(start_date, end_date, description, duration))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM sessions")
        rows=self.cur.fetchall()
        return rows

    def delete(self,id):
        self.cur.execute("DELETE FROM sessions WHERE id=?",(id,))
        self.conn.commit()

    def update(self, start_date, end_date, description, duration):
        self.cur.execute("UPDATE book SET start_date=?, end_date=?, description=?, duration=? WHERE id=?",(start_date, end_date, description, duration))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
