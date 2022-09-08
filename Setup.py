import sqlite3

conn = sqlite3.connect("Score.db")
c =conn.cursor()

c.execute("""CREATE TABLE score (
            id  integer,
            score integer
)""")

conn.commit()