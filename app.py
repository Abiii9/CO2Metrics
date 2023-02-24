from flask import Flask,render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    return render_template('metrics.html')