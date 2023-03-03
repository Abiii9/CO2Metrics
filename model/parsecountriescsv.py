'''Import the required modules'''
import csv
import sqlite3
'''Connecting to the database file'''
conn = sqlite3.connect("model/emission-data.db")
'''Executing the sql file'''
with open("model/countriesSchema.sql") as f:
	conn.executescript(f.read())
cur = conn.cursor()
'''Reading values from the countries.csv file and adding it to the database tables.'''
with open('model/Countries.csv') as f:
    reader = csv.reader(f,delimiter=',')
    #Skipping the header line
    next(reader)
    for row in reader:
        print(row)
        ISO3 = row[0]
        CountryName = row[1]
        cur.execute("INSERT INTO countries VALUES (?,?)",(ISO3,CountryName))
        conn.commit()
print("Data parsed successfully.")
conn.close()