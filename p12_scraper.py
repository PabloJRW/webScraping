import requests
from bs4 import BeautifulSoup
import os
import datetime

HOME_URL = 'https://www.pagina12.com.ar/'

XPATH_LINK_TO_ARTICLE = '//div[@class="story-box"]/h2/a/@href'
XPATH_TITLE = '//article/div[@class="article-header"]/h1/text()'
XPATH_SUMMARY = '//article/div[@class="article-header"]/div[@class="article-summary"]/text()'
XPATH_BODY = '//article/div[@class="article-content"]/p[not(@class)]/text()'

def parse_news(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            parsed = html.fromstring(response)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            # Home Page
            home_soup = BeautifulSoup(response.content, 'lxml')

            # Sections Navigator
            nav = home_soup.find('ul', attrs={'class':'horizontal-list main-sections hide-on-dropdown'}).find_all('li')
            nav_sections = [sect.a.get('href') for sect in nav_sections]

            

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        


def run():
    parse_home()


if __name__=='__main__':
    run()


