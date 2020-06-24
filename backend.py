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

    def update(self, id, start_date, end_date, description, duration, surplus):
        self.cur.execute("UPDATE sessions SET start_date=?, end_date=?, description=?, duration=?, surplus=? WHERE id=?",(start_date, end_date, description, duration, surplus, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
#database = Database("sessions.db")
#database.delete(3238)
#database.delete(2676)
#database.delete(2677)
#database.delete(3368)
#database.insert("2018-11-05 07:41:09", "2018-11-05 08:53:18", "1 EXP 1:00 5 Local 07:30 3 SxS 08:00 3 SxS 03:30", "1:12:09", 49)
#database.insert("2020-01-02 21:36:00", "2020-01-02 22:20:00", "1 UO 05:00", "0:44:00", 0)
#database.update(3273, "2020-04-28 08:19:00", "2020-04-28 08:46:00", "5 EXP 10:00", "0:27:00", 0)
#database.update(2916, "2020-01-26 07:13:00", "2020-01-26 07:26:00", "1 SxS 15:00 2 SxS 8:00", "0:13:00", 0)
