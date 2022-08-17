import requests
import csv
import subprocess, sys
from bs4 import BeautifulSoup

HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/98.0.4758.109 Safari/537.36', 'accept':'*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('section', class_='proposition')

    cars = []
    for item in items:
        uah_price = item.find('span', class_='size16')
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'Цену уточняйте!'
        cars.append({
            'title':item.find('span', class_='link').get_text(strip=True),
            'link': HOST + item.find('a', class_='proposition_link').get('href'),
            'usd_price':item.find('span', class_='green').get_text(strip=True),
            'uah_price': uah_price,
            'city':item.find('span', class_='item region').get_text(strip=True)

        })
    return cars

def save_file(items, path):
    with open(path, 'w', encoding = 'utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Brand', 'Link', 'USD Price', 'UAH Price', 'City'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])


def parse():
    URL = input('Enter a url: ').strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f"Parsing of page {page} out of {pages_count}...")
            html = get_html(URL, params={'page':page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)

        if len(cars) > 1:
            print(f"Got {(len(cars))} cars!")
        else:
            print(f"Got 1 car!")

        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, FILE])
    else:
        print("Error")

parse()
