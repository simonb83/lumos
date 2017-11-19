from bs4 import BeautifulSoup
from requests import get
import random
import psycopg2
from multiprocessing import Pool
import logging
import numpy as np
import time


def get_page(url):
    resp = get(url)
    soup = BeautifulSoup(resp.content, "lxml", from_encoding="utf-8")
    main = soup.find('div', {'class': 'pg-campaign'})
    return main

def save_page(main, url_id, cur, conn):
    date = main.find('div', {'class': 'created-date'})
    if date:
        date = date.text
    try:
        cur.execute("""INSERT INTO temp (url_id, date_created)
                 VALUES (%s, %s)""", (int(url_id), date))
        conn.commit()
    except:
        conn.rollback()

def process_url_id(url_id):
    conn = psycopg2.connect('postgresql://simonbedford@localhost/lumos')
    cur = conn.cursor()
    cur.execute("""SELECT url FROM gofundme WHERE id = {};""".format(url_id))
    url = cur.fetchone()[0]
    main = get_page(url)
    if main:
        save_page(main, url_id, cur, conn)
        conn.close()
        time.sleep(random.choice([0.5, 0.3, 0.7]))

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    conn = psycopg2.connect('postgresql://simonbedford@localhost/lumos')
    cur = conn.cursor()
    # sql = """SELECT id FROM gofundme;"""
    sql = """SELECT g.id FROM gofundme g
            LEFT JOIN temp r ON g.id = r.url_id
            WHERE r.url_id IS NULL;"""
    cur.execute(sql)
    url_ids = np.array(cur.fetchall())
    url_ids = url_ids.reshape(url_ids.shape[0], )
    conn.close()

    with Pool(30) as p:
        p.map(process_url_id, url_ids)

