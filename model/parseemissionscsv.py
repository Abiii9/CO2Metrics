import sqlite3
import csv
pointer = 0
#connecting to countries database to fetch all entries from it
conn = sqlite3.connect('model/emission-data.db')
cur = conn.cursor()
countries = cur.execute("SELECT * FROM countries").fetchall()
country_list = []
for country in countries:
	country_list.append(country[0])
conn.close()

#connecting to industries database to fetch all values from it.
conn = sqlite3.connect('model/emission-data.db')
cur = conn.cursor()
industries = cur.execute("SELECT * FROM industries").fetchall()
industry_list = []
for industry in industries:
	industry_list.append(industry[0])
conn.close()
#connecting to emissions database to insert values to it.
conn = sqlite3.connect('model/emission-data.db')
cur = conn.cursor()

with open("model/emissionsSchema.sql") as f:
	conn.executescript(f.read())
rows = []
with open("model/Emission.csv") as f:
	reader = csv.reader(f,delimiter=',')
	next(reader)
	for row in reader:
		rows.append(row)

for country in country_list:
	for (i,industry) in enumerate(industry_list):
		Unit = rows[i+pointer][0]
		Indicator = rows[i+pointer][1]
		F2008 = float(rows[i+pointer][2])
		F2009 = float(rows[i+pointer][3])
		F2010 = float(rows[i+pointer][4])
		F2011 = float(rows[i+pointer][5])
		F2012 = float(rows[i+pointer][6])
		F2013 = float(rows[i+pointer][7])
		F2014 = float(rows[i+pointer][8])
		F2015 = float(rows[i+pointer][9])
		F2016 = float(rows[i+pointer][10])
		F2017 = float(rows[i+pointer][11])
		F2018 = float(rows[i+pointer][12])
		cur.execute("INSERT INTO emissions VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (country, industry,Unit,Indicator,F2008,F2009,F2010,F2011,F2012,F2013,F2014,F2015,F2016,F2017,F2018))
		conn.commit()
	pointer += len(industry_list)
	
conn.close()