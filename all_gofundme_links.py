from bs4 import BeautifulSoup
from multiprocessing import Pool
import psycopg2
import random
from requests import get
import pandas as pd
import re
import logging
import optparse
import time


def scrape_page(url):
    resp = get(url)
    soup = BeautifulSoup(resp.content, "lxml", from_encoding="utf-8")
    return soup


def get_links(results, element_name):
    links = []
    for result in results:
        link = result.find(
            'a', {'data-gfm-analytics-element': element_name})
        links.append(link.attrs['href'])
    return links

def save_to_db(links, page_num, country_name, cur, conn):
    for l in links:
        try:
            cur.execute("INSERT INTO gofundme (url, page_num, country_term) VALUES (%s, %s, %s)",
                        (l, page_num, country_name))
            conn.commit()
        except:
            conn.rollback()


def process_country_term(country_name):
    # Setup the DB Connection
    conn = psycopg2.connect(
        "dbname='lumos' user='lumos' host='localhost' password='lumos'")
    cur = conn.cursor()

    base_url = "https://www.gofundme.com/mvc.php?route=category&term="
    search_url = base_url + country_name
    page_num = 1

    body = scrape_page(search_url)

    header = body.find('div', {'class': 'header-tile'})
    num_results = header.find('h2').text
    logging.info("Total number of results for {}: {}".format(
        country_name, num_results))
    results = body.findAll('div', {'class': 'js-fund-tile'})
    links = get_links(results, "btn_category_fund_tile_description")
    save_to_db(links, page_num, country_name, cur, conn)

    while True:
        page_num += 1
        url = "https://www.gofundme.com/mvc.php?route=category/loadMoreTiles&page={}&term={}&country=MX&initialTerm=".format(
            page_num, country_name)
        new_body = scrape_page(url)
        if new_body == body:  # Stop when no new content
            logging.info("No new content")
            cur.execute(
                "SELECT COUNT(*) FROM gofundme WHERE country_term = '{}'".format(country_name))
            num_rows = cur.fetchone()[0]
            logging.info("Total rows for {}: {}".format(
                country_name, num_rows))
            break
        else:
            body = new_body
        results = body.findAll('div', {'class': 'js-fund-tile'})
        links = get_links(results, "_fund_tile_description")
        save_to_db(links, page_num, country_name, cur, conn)
        if page_num % 50 == 0:
            cur.execute(
                "SELECT COUNT(*) FROM gofundme WHERE country_term = '{}'".format(country_name))
            num_rows = cur.fetchone()[0]
            logging.info("Total rows for {}: {}".format(
                country_name, num_rows))
        time.sleep(random.choice([0.5, 1, 1.5, 1.7]))
    return

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    # Load countries
    with open("Data/countries.txt", "r") as f:
        countries = f.read().splitlines()
    terms = ['', 'children shelter', 'children', 'orphanage', 'orphans', 'orphan', 'street children']
    country_terms = []

    for country in countries:
        for term in terms:
            country_term = ' '.join([term, country]).strip()
            country_terms.append(country_term)

    country_terms = country_terms[::-1]
    with Pool(20) as p:
        p.map(process_country_term, country_terms)
