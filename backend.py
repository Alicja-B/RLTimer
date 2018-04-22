import sqlite3

class Database:

    def __init__(self, db):
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, start_date text, end_date text, description text, duration text, surplus INTEGER)")
        self.conn.commit()

    def insert(self, start_date, end_date, description, duration, surplus):
        self.cur.execute("INSERT INTO sessions VALUES (NULL,?,?,?,?,?)",(start_date, end_date, description, duration, surplus))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM sessions")
        rows=self.cur.fetchall()
        return rows

    def view_since(self, start_date):
        self.cur.execute("SELECT * FROM sessions WHERE start_date >= ?", (start_date,))
        rows=self.cur.fetchall()
        return rows

    def delete(self,id):
        self.cur.execute("DELETE FROM sessions WHERE id=?",(id,))
        self.conn.commit()

    def update(self, start_date, end_date, description, duration, surplus):
        self.cur.execute("UPDATE book SET start_date=?, end_date=?, description=?, duration=? WHERE id=?",(start_date, end_date, description, duration, surplus))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
#database = Database("sessions.db")
#database.delete(5)
#database.delete(4)
#database.insert("2018-04-22 08:12:53", "2018-04-22 08:18:34", "1 EXP 6:00", "0:05:41", 18)
#database.insert("2018-04-22 11:02:48", "2018-04-22 11:34:48", "3 EXP 6:18, 2 EXP 01:00, 3 local 03:48, 1 EXP 01:18", "0:32:00", 90)
#database.insert("2018-04-22 11:58:55", "2018-04-22 12:15:59", "1 EXP 6:18, 6 SxS 02:00", "0:17:03", 70)
