import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ria.com/newauto/marka-mercedes-benz/'
HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/98.0.4758.109 Safari/537.36', 'accept':'*/*'}
HOST = 'https://auto.ria.com'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

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

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
        return cars
    else:
        print("Error")

print(parse())
