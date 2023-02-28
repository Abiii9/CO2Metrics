from flask import Flask,render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/metrics')
def metrics():
    #try to refactor this
    conn = sqlite3.connect("model/emission-data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    names = cur.execute("SELECT * FROM emissions").fetchone()
    name = names.keys()
    conn.close()
    conn = sqlite3.connect("model/emission-data.db")
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM countries").fetchall()
    industries= cur.execute("SELECT * FROM industries").fetchall()
    conn.close()
    year = None
    noofcolumns = 0
    noofrows = 0
    industry = None
    if(request.args):
        country = request.args['country']
        year = None if request.args['year'] == "allyears" else request.args['year']
        industry = None if request.args['industry'] == "allindustries" else request.args['industry']
        conn = sqlite3.connect("model/emission-data.db")
        cur = conn.cursor()
        country_id = cur.execute("SELECT ISO3 FROM countries WHERE CountryName=?", [country]).fetchone()
        if(not year and not industry):
            data = cur.execute("SELECT emissions.Indicator,industries.IndustryName,emissions.F2008,emissions.F2009,emissions.F2010,emissions.F2011,emissions.F2012,emissions.F2013,emissions.F2014,emissions.F2015,emissions.F2016,emissions.F2017,emissions.F2018 FROM emissions LEFT OUTER JOIN industries ON emissions.Industry_id = industries.Industry_id WHERE Country_id = ?", country_id).fetchall()
            noofcolumns = 13
            noofrows = 45
        elif(year and not industry):
            data = cur.execute(f"SELECT emissions.Indicator,industries.IndustryName,emissions.{year} FROM emissions LEFT OUTER JOIN industries ON emissions.Industry_id = industries.Industry_id WHERE Country_id = ?", country_id).fetchall()
            noofcolumns = 3
            noofrows = 45
        elif(not year and industry):
            industry_id = cur.execute("SELECT Industry_id FROM industries WHERE IndustryName = ?", [industry]).fetchone()
            data = cur.execute(f"SELECT emissions.Indicator,industries.IndustryName,emissions.F2008,emissions.F2009,emissions.F2010,emissions.F2011,emissions.F2012,emissions.F2013,emissions.F2014,emissions.F2015,emissions.F2016,emissions.F2017,emissions.F2018 FROM emissions LEFT OUTER JOIN industries ON emissions.Industry_id = industries.Industry_id WHERE Country_id = ? AND emissions.Industry_id = ?",(country_id[0],industry_id[0])).fetchone()
            print(data)
            noofcolumns = 13
            noofrows = 1
        else:
            industry_id = cur.execute("SELECT Industry_id FROM industries WHERE IndustryName = ?", [industry]).fetchone()
            data = cur.execute(f"SELECT emissions.Indicator,industries.IndustryName,emissions.{year} FROM emissions LEFT OUTER JOIN industries ON emissions.Industry_id = industries.Industry_id WHERE Country_id = ? AND emissions.Industry_id = ?", (country_id[0],industry_id[0])).fetchone()
            noofcolumns = 3
            noofrows = 1
        conn.close()
    else:
        data=None
    return render_template('metrics.html', rows=rows,names=name[5:],data=data,industries=industries,year=year,columns=noofcolumns, industry=industry)

