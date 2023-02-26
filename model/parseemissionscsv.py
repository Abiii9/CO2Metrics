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
with open("model/Emissions.csv") as f:
	reader = csv.reader(f,delimiter=',')
	next(reader)
	for row in reader:
		rows.append(row)

for country in country_list:
	for (i,industry) in enumerate(industry_list):
		Unit = rows[i+pointer][0]
		Indicator = rows[i+pointer][1]
		F1995 = float(rows[i+pointer][2])
		F1996 = float(rows[i+pointer][3])
		F1997 = float(rows[i+pointer][4])
		F1998 = float(rows[i+pointer][5])
		F1999 = float(rows[i+pointer][6])
		F2000 = float(rows[i+pointer][7])
		F2001 = float(rows[i+pointer][8])
		F2002 = float(rows[i+pointer][9])
		F2003 = float(rows[i+pointer][10])
		F2004 = float(rows[i+pointer][11])
		F2005 = float(rows[i+pointer][12])
		F2006 = float(rows[i+pointer][13])
		F2007 = float(rows[i+pointer][14])
		F2008 = float(rows[i+pointer][15])
		F2009 = float(rows[i+pointer][16])
		F2010 = float(rows[i+pointer][17])
		F2011 = float(rows[i+pointer][18])
		F2012 = float(rows[i+pointer][19])
		F2013 = float(rows[i+pointer][20])
		F2014 = float(rows[i+pointer][21])
		F2015 = float(rows[i+pointer][22])
		F2016 = float(rows[i+pointer][23])
		F2017 = float(rows[i+pointer][24])
		F2018 = float(rows[i+pointer][25])
		cur.execute("INSERT INTO emissions VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (country, industry,Unit,Indicator,F1995,F1996,F1997,F1998,F1999,F2000,F2001,F2002,F2003,F2004,F2005,F2006,F2007,F2008,F2009,F2010,F2011,F2012,F2013,F2014,F2015,F2016,F2017,F2018))
		conn.commit()
	pointer += len(industry_list)
	
conn.close()