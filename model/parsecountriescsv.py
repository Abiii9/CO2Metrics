import csv
import sqlite3
conn = sqlite3.connect("countries.db")
with open("model/countriesSchema.sql") as f:
	conn.executescript(f.read())

cur = conn.cursor()
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