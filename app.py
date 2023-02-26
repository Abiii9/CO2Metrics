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
    conn.close()
    if(request.args):
        country = request.args['country']
        conn = sqlite3.connect("model/emission-data.db")
        cur = conn.cursor()
        country_id = cur.execute("SELECT ISO3 FROM countries WHERE CountryName=?", [country]).fetchone()
        data = cur.execute("SELECT * FROM emissions WHERE Country_id=?", country_id).fetchall()
        conn.close()
    else:
        data=None
    return render_template('metrics.html', rows=rows,names=name[5:],data=data)

