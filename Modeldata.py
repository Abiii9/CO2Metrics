'''Import sqlite3 for database interaction'''
import sqlite3

'''Creating a class Modeldata to interact with the database.
This class has been created in order to prevent direct interaction to the database from the app.py.
This can be considered as an API to the emission-data database.'''

class Modeldata:
    def __init__(self,name):
        self.name = name
        self.conn = False
    def open_connection(self):
        self.conn = sqlite3.connect("model/emission-data.db")
        return self.conn
    def get_table_headings(self):
        self.conn = sqlite3.connect("model/emission-data.db")
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        values = cur.execute(f"SELECT * FROM {self.name}").fetchone()
        value = values.keys()
        self.conn.close()
        return value
    def get_table_values(self):
        cur = self.conn.cursor()
        values = cur.execute(f"SELECT * FROM {self.name}").fetchall()
        return values
    def left_outer_join(self,query):
        cur = self.conn.cursor()
        keysQuery = list(list(query.values())[1].keys())
        if(len(keysQuery) == 1):
            values = cur.execute(f"SELECT {query['colnames']} FROM emissions LEFT OUTER JOIN industries ON emissions.Industry_id = industries.Industry_id WHERE {keysQuery[0]} = ?",[query['condition']['country_id']]).fetchall()
        else:
            values = cur.execute(f"SELECT {query['colnames']} FROM emissions LEFT OUTER JOIN industries ON emissions.Industry_id = industries.Industry_id WHERE {keysQuery[0]} = ? AND emissions.{keysQuery[1]} = ?",(query['condition']['country_id'],query['condition']['industry_id'])).fetchone()
        return values
    def select_one_column(self,query):
        keysQuery = list(list(query.values())[1].keys())
        valQuery = list(list(query.values())[1].values())
        cur = self.conn.cursor()
        values = cur.execute(f"SELECT {query['colname']} FROM {self.name} WHERE {keysQuery[0]} = ?", [valQuery[0]]).fetchone()
        return values
    def close_connection(self):
        self.conn.close()


'''Creating objects for each of the tables in the database.'''
countries = Modeldata('countries')
industries = Modeldata('industries')
emissions = Modeldata('emissions')
