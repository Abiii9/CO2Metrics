import sqlite3
conn = sqlite3.connect("model/emission-data.db")
cur= conn.cursor()
dbdata = cur.execute("SELECT * FROM emissions").fetchall()
print(dbdata)