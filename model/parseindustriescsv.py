'''Importing the required modules'''
import csv
import sqlite3
conn = sqlite3.connect("model/emission-data.db")
'''executing the sql file'''
with open("model/industriesSchema.sql") as f:
	conn.executescript(f.read())

cur = conn.cursor()
'''Reading values from the industries.csv file and writing it to the database tables'''
with open('model/Industries.csv') as f:
    reader = csv.reader(f,delimiter=',')
    #Skipping the header line
    next(reader)
    for row in reader:
        IndustryName = row[0]
        print([IndustryName])
        cur.execute("INSERT INTO industries VALUES (NULL,?)",[IndustryName])
        conn.commit()
print("Data parsed successfully.")
conn.close()