import sqlite3
'''A testing file just to test the values in the database'''
conn = sqlite3.connect("model/emission-data.db")
cur= conn.cursor()
dbdata = cur.execute("SELECT * FROM emissions").fetchall()
print(dbdata)