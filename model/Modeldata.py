import sqlite3
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


countries = Modeldata('countries')
industries = Modeldata('industries')
emissions = Modeldata('emissions')
#print(countries.open_connection())
# print(emissions.left_outer_join({
#     'colnames': "emissions.Indicator,industries.IndustryName,emissions.F2008,emissions.F2009,emissions.F2010,emissions.F2011,emissions.F2012,emissions.F2013,emissions.F2014,emissions.F2015,emissions.F2016,emissions.F2017,emissions.F2018",
#     'condition': {"country_id":"IND","industry_id": 5}
# }))
# print(emissions.left_outer_join({
#     'colnames': f'emissions.Indicator,industries.IndustryName,emissions.{year}',
#     'condition': {"country_id":"IND","industry_id": 5}
# }))