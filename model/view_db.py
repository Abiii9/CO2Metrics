import sqlite3
conn = sqlite3.connect("model/emissions.db")
cur= conn.cursor()
dbdata = cur.execute("SELECT * FROM emissions WHERE Country_id='IND'").fetchall()
print(dbdata)