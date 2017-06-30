import urllib
from bs4 import BeautifulSoup
import re
import json

BASE_URL = 'http://data-interview.enigmalabs.org'
COMPANY_REGEX = re.compile('^/companies/([A-Za-z-_0-9]+)')
COMPANY_NAME_REGEX = re.compile('.*Company Name.*')

def get_page(url):
    return urllib.urlopen(url)

def get_soup(url):
    html = get_page(url)
    return BeautifulSoup(html, 'html.parser')

def get_company_data(soup):
    table = soup.find('tbody')

    result = {}
    for cell in table.find_all('td'):
        id = cell.get('id')
        if id is None:
            continue

        result[id] = cell.text


    return result

def get_company_data_for_page(soup, result):
    company_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        regex_find_result = COMPANY_REGEX.findall(href)
        if len(regex_find_result) > 0:
            company_name = regex_find_result[0]
            company_links.append(href)

    for link in company_links:
        company_soup = get_soup(BASE_URL + link)
        data = get_company_data(company_soup)

        if data['name'] in result:
            print('Duplicate company data! Using new instance of data.')

        print('Got data for ' + data['name'])

        result[data['name']] = data

def get_next_page(soup):
    next_link = soup.find('li', class_='next')
    if 'disabled' in next_link.get('class'):
        return None

    next_page_url = next_link.find('a').get('href')
    return get_soup(BASE_URL + next_page_url)


result = {}
curr_soup = get_soup(BASE_URL + '/companies')
while True:
    get_company_data_for_page(curr_soup, result)
    curr_soup = get_next_page(curr_soup)

    if curr_soup is None:
        break

with open('solution.json', 'wb') as output:
    json.dump(result, output)
