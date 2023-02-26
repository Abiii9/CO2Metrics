from flask import Flask,render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    conn = sqlite3.connect("model/countries.db")
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM countries").fetchall()
    conn.close()
    conn1 = sqlite3.connect("model/emissions.db")
    conn1.row_factory = sqlite3.Row
    cur = conn1.cursor()
    names = cur.execute("SELECT * FROM emissions").fetchone()
    name = names.keys()
    conn1.close()
    return render_template('metrics.html', rows=rows,names=name[5:])

@app.route('/metricsquery', methods=['GET'])
def metricsquery():
    country = request.args['country']
    year = request.args['year']
    conn = sqlite3.connect("model/countries.db")
    cur = conn.cursor()
    country_id = cur.execute("SELECT ISO3 FROM countries WHERE CountryName = ?", [country]).fetchone()
    conn.close()
    conn1 = sqlite3.connect("model/industries.db")
    cur=conn1.cursor()
    industries = cur.execute("SELECT IndustryName FROM industries").fetchall()
    conn1.close()
    conn2 = sqlite3.connect("model/emissions.db")
    conn2.row_factory = sqlite3.Row
    cur = conn2.cursor()
    names = cur.execute("SELECT * FROM emissions").fetchone()
    name = names.keys()
    emissions = cur.execute("SELECT * FROM emissions WHERE Country_id=?",country_id).fetchall()
    conn2.close()

    return render_template('result.html',emissions=emissions, names=name, industries=industries)