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
    goal_container = main.find('h2', {'class': 'goal'})
    raised = goal_container.find('strong')
    if raised:
        raised = raised.text
    goal = goal_container.find('span')
    if goal:
        goal = goal.text.strip()
    raised_by = main.find('div', {'class': 'campaign-status'}).find('span')
    if raised_by:
        raised_by = raised_by.text
    date = main.find('div', {'class': 'created-date'})
    if date:
        date = date.text
    loc = main.find('a', {'class': 'location-name'})
    if loc:
        loc = loc.text.strip()
    content = main.find('div', {'class': 'co-story'})
    if content:
        content = content.text.strip()
    try:
        cur.execute("""INSERT INTO rawdata (url_id, goal, raised, raised_by, date_created, loc_name, content)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)""", (int(url_id), goal, raised, raised_by, date, loc, content))
        conn.commit()
    except:
        conn.rollback()

def process_url_id(url_id):
    conn = psycopg2.connect(
        "dbname='lumos' user='lumos' host='localhost' password='lumos'")
    cur = conn.cursor()
    cur.execute("""SELECT url FROM gofundme WHERE id = {};""".format(url_id))
    url = cur.fetchone()[0]
    main = get_page(url)
    if main:
        save_page(main, url_id, cur, conn)
        conn.close()
        time.sleep(random.choice([0.5, 1, 1.2, 1.3]))

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    conn = psycopg2.connect(
        "dbname='lumos' user='lumos' host='localhost' password='lumos'")
    cur = conn.cursor()
    # sql = """SELECT id FROM gofundme;"""
    sql = """SELECT g.id FROM gofundme g
            LEFT JOIN rawdata r ON g.id = r.url_id
            WHERE r.url_id IS NULL;"""
    cur.execute(sql)
    url_ids = np.array(cur.fetchall())
    url_ids = url_ids.reshape(url_ids.shape[0], )
    conn.close()

    with Pool(10) as p:
        p.map(process_url_id, url_ids)

