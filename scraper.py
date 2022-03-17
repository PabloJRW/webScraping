import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'http://www.prensa.com/'

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
            parsed = html.fromstring(response.text)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_news)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_news:
                parse_news(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        


def run():
    parse_home()


if __name__=='__main__':
    run()


