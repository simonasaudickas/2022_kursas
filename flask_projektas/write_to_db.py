import psycopg2
import pandas as pd
import datetime
from sqlalchemy import create_engine
"""
picu_csv = pd.read_csv('/home/simonas/Documents/picu_pardavimai_csv_202202241858.csv', encoding='utf-8')
print(picu_csv)

engine = create_engine("postgresql+psycopg2://simonas:kursas@localhost/kursas")
picu_csv.to_sql('picu_pardavimai', engine, schema='puslapiui', if_exists='replace',index=False)
"""

conn = psycopg2.connect(
    host="localhost",
    database="kursas",
    user="simonas",
    password="kursas")
c= conn.cursor()
c.execute("select * from puslapiui.picu_pardavimai")
picos_pardavimai=c.fetchall()

if __nane__=='__main__':
    print(picos_pardavimai)