# CO2Metrics v1.0 03-03-2023

## What is it
This application was developed as a part of coursework of the Advanced Programming Course at the University of Aberdeen. This application demonstrates the emission levels of carbon dioxide from different industries of 45+ countries. The data
can be viewed in two forms: tabular and graph form. This application aims at helping to monitor the carbon footprint of various countries. The Model-View-Controller architecture pattern has been followed. The database used in this application is SQLite3. 
Seaborn and Matplotlib packages have been used to perform data visualization.

## Where to get it

The source code is hosted on Render at: https://co2metrics.onrender.com and https://co2metrics-o392.onrender.com

## How to install and begin running the application

To get CO2Metrics up and running, you need to perform the following steps in your local environment.

~~~
pyenv install 3.11.0
py -3 -m venv .venv
source  venv/Scripts/activate
pip install --upgrade pip
pip install flask
export FLASK_APP=app.py
export FLASK_ENV=development
~~~

## Dependencies
There are a few dependency packages that need to be installed to complete setting up the application.

~~~
pip install selenium
pip install behave
python3 -m pip3 install -U matplotlib
pip install seaborn
pip install gunicorn
~~~
Once you have completed installing all the dependencies, you can run the flask app.
~~~
flask run
~~~

## How to use it
Here are a few features that help navigate CO2Metrics effectively.

- An interactive index page with options to choose metrics and graph views.
- A metrics page that contains a simple-to-use form. Users can customize their output by filtering what they need to see, including country, industry and year.
- A graph page that contains a simple-to-use form, with which the users can view the emissions made by a selective industry from a selective country over the period of 10 years, in the form of a bar plot.
- A home button that redirects the user to the home page.

## Maintenance
Please make sure to install the latest supported version of all the packages.
Contact information incase of any issues: abinayae19@gmail.com

## Credits
The data source for this application was taken from https://www.kaggle.com/datasets/prashant808/co2-emissions.
It contains a detailed table with countries, industries and their CO2 emission values from years 1995 to 2018.
The usage of Seaborn bar plot has been inspired from https://laptrinhx.com/how-to-visualize-with-seaborn-in-flask-3650608922/.
The clouds in the background image has been inspired from https://codepen.io/antonioescudero/pen/zrxGve.


## License 
MIT
