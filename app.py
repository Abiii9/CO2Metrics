from flask import Flask,render_template, request,abort
import sys
sys.path.append('C:\\Users\\S Elangovan\\OneDrive\\Documents\\CA4 - Advanced Programming\\CO2Metrics\\model')
from Modeldata import *

app = Flask(__name__)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internalservererror(error):
    return render_template('error_500.html'), 500


@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        abort(404)

    
@app.route('/metrics')
def metrics():
    try:
        #try to refactor this
        name = emissions.get_table_headings()
        countries.open_connection()
        rows = countries.get_table_values()
        countries.close_connection()
        industries.open_connection()
        indus= industries.get_table_values()
        industries.close_connection()
        year = None
        noofcolumns = 0
        industry = None
        if(request.args):
            country = request.args['country']
            year = None if request.args['year'] == "allyears" else request.args['year']
            industry = None if request.args['industry'] == "allindustries" else request.args['industry']
            if(industry):
                industries.open_connection()
                industry_id = industries.select_one_column({'colname': 'Industry_id','condition': {"IndustryName": f"{industry}"}})
                industries.close_connection()
            countries.open_connection()
            country_id = countries.select_one_column({'colname': 'ISO3','condition': {"CountryName": f"{country}"}})
            countries.close_connection()
            emissions.open_connection()
            if(not year and not industry):
                data = emissions.left_outer_join({'colnames': "emissions.Indicator,industries.IndustryName,emissions.F2008,emissions.F2009,emissions.F2010,emissions.F2011,emissions.F2012,emissions.F2013,emissions.F2014,emissions.F2015,emissions.F2016,emissions.F2017,emissions.F2018",'condition': {"country_id":f"{country_id[0]}"}})
                noofcolumns = 13
            elif(year and not industry):
                data = emissions.left_outer_join({'colnames': f"emissions.Indicator,industries.IndustryName,emissions.{year}",'condition': {"country_id":f"{country_id[0]}"}})
                noofcolumns = 3
            elif(not year and industry):
                data = emissions.left_outer_join({'colnames': "emissions.Indicator,industries.IndustryName,emissions.F2008,emissions.F2009,emissions.F2010,emissions.F2011,emissions.F2012,emissions.F2013,emissions.F2014,emissions.F2015,emissions.F2016,emissions.F2017,emissions.F2018",'condition':{"country_id":f"{country_id[0]}","industry_id": f"{industry_id[0]}"}})
                noofcolumns = 13
            else:
                data = emissions.left_outer_join({'colnames': f"emissions.Indicator,industries.IndustryName,emissions.{year}",'condition':{"country_id":f"{country_id[0]}","industry_id": f"{industry_id[0]}"}})
                noofcolumns = 3
            emissions.close_connection()
        else:
            data=None
        return render_template('metrics.html', rows=rows,names=name[5:],data=data,industries=indus,year=year,columns=noofcolumns, industry=industry)
    except:
        abort(500)

