import sqlite3
conn = sqlite3.connect("model/countries.db")
cur= conn.cursor()
dbdata = cur.execute("SELECT * FROM countries").fetchall()
print(dbdata)