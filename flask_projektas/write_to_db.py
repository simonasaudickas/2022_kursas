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
c.execute("select * from puslapiui.video")
picos_pardavimai=c.fetchall()
def get_videos(id):
    cur = c
    cur.execute("select * from puslapiui.video where vartotojas_id = {}".format(id))
    #print(cur.fetchall())
    return cur.fetchall()


if __name__=='__main__':
    #print(picos_pardavimai)
    print(get_videos(10))