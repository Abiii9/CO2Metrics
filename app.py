'''Importing all the necessary packages'''
from flask import Flask,render_template, request,abort,send_file
import pandas as pd
import io
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
from Modeldata import *

matplotlib.use('SVG')
'''Providing initial values to variables'''
countryval = 'Enter a country'
indusval = 'Enter an industry'
'''initializing Flask app'''
app = Flask(__name__)
'''Fetching vaues from emissions_db database, using an API style'''
name = emissions.get_table_headings()
countries.open_connection()
rows = countries.get_table_values()
countries.close_connection()
industries.open_connection()
indus= industries.get_table_values()
industries.close_connection()

'''Error handlers for major errors'''
@app.errorhandler(404)
def pagenotfound(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internalservererror(error):
    return render_template('error_500.html'), 500

@app.errorhandler(400)
def bad_request(error):
    return render_template('error_400.html'),400

'''Route for index.html'''
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        abort(404)

'''Route for the metrics page'''
@app.route('/metrics')
def metrics():
    try:
        year = None
        noofcolumns = 0
        industry = None
        country = 'Select a country'
        '''Fetching values from the form request'''
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
            '''According to the input receievd, fetching values from the database API'''
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
        '''rendering the metrics page with the values supplied'''
        return render_template('metrics.html', rows=rows,names=name[5:],data=data,industries=indus,year=year,columns=noofcolumns, industry=industry,country=country)
    except:
        abort(500)
'''Initial value for the variable'''
dataList = []
'''Route for graph page.'''
@app.route('/graph')
def graph():
    try:
        global dataList
        '''Fetching values from the form request'''
        if(request.args):
            global countryval
            countryval = request.args['country']
            global indusval
            indusval = request.args['industry']
            '''Fetching data values from the database API'''
            countries.open_connection()
            country_id = countries.select_one_column({'colname': 'ISO3','condition': {"CountryName": f"{countryval}"}})
            countries.close_connection()
            industries.open_connection()
            industry_id = industries.select_one_column({'colname': 'Industry_id','condition': {"IndustryName": f"{indusval}"}})
            industries.close_connection()
            emissions.open_connection()
            data = emissions.left_outer_join({'colnames': "emissions.F2008,emissions.F2009,emissions.F2010,emissions.F2011,emissions.F2012,emissions.F2013,emissions.F2014,emissions.F2015,emissions.F2016,emissions.F2017,emissions.F2018",'condition':{"country_id":f"{country_id[0]}","industry_id": f"{industry_id[0]}"}})
            dataList = list(data)
            emissions.close_connection()
        '''rendering the graph page with the values supplied'''
        return render_template('graph.html',rows=rows,industries=indus,dataList=dataList,country=countryval,industry=indusval)
    except:
        abort(500)

'''Route for the image element from graph page'''
@app.route('/visualize') 
def visualize():
    try:
        '''Creating the figure element in matplotlib'''
        fig,ax=plt.subplots(figsize=(6,6))
        ax=sns.set(style="darkgrid")
        if(len(dataList) > 0):
            plotdata = {'years':['F2008','F2009','F2010','F2011','F2012','F2013','F2014','F2015','F2016','F2017','F2018'],'industries': dataList}
            df = pd.DataFrame(plotdata)
            '''Creating a Seaborn bar plot with scale values'''
            sns.barplot(data=df, x="years", y="industries")
            canvas=FigureCanvas(fig)
            '''Rendering the image'''
            img = io.BytesIO()
            fig.savefig(img)
            img.seek(0)
        else:
            plotdata = {'years': ['F2008','F2009','F2010'], 'industries': [8.77,9.77,5.67]}
            df = pd.DataFrame(plotdata)
            sns.barplot(data=df, x="years", y="industries")
            canvas=FigureCanvas(fig)
            img = io.BytesIO()
            fig.savefig(img)
            img.seek(0)
        '''Sending the rendered image to the graph page.'''
        return send_file(img,mimetype='img/png')
    except:
        abort(400)
    
'''Running Flask app'''
if(__name__) == "__main__":
    app.run()