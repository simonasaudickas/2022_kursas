import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="kursas",
    user="simonas",
    password="kursas")
c = conn.cursor()
c.execute("select * from puslapiui.picu_pardavimai")
picos_pardavimai = c.fetchall()


df = pd.DataFrame(picos_pardavimai)
header = (i[0] for i in c.description)
df.columns = header
total_sales = df['kiekis'].sum()
average_sales = int(round(df['kiekis'].mean(), 0))


df['dt'] = pd.to_datetime(df['dt']).dt.strftime("%Y-%m")
picos = df.groupby(by=['dt']).sum()
picos.reset_index(inplace=True)
rec = picos.to_records(index=False)
picos = list(rec)




sales = [("2022-01-01", 15), ("2022-01-02", 30), ("2022-01-03", 25), ("2022-01-04", 55),
("2022-01-05", 64),
("2022-01-06", 34),
("2022-01-07", 46),
("2022-01-08", 32),
("2022-01-09", 23),
("2022-01-10", 47),
("2022-01-11", 44),
("2022-01-12", 33),
("2022-01-13", 46),
("2022-01-14", 48),
("2022-01-15", 67),
("2022-01-16", 56),
("2022-01-17", 49),
("2022-01-18", 24),
("2022-01-19", 54),
("2022-01-20", 36)]


if __name__ == '__main__':
    print(picos_pardavimai)
    print(picos)
