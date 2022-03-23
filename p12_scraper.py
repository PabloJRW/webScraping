import requests
from bs4 import BeautifulSoup
import re

def getHomePage(HOME_URL):
    """Recibe el enlace de la página y hace la consulta"""
    
    try:
        response = requests.get(HOME_URL) # Consulta a la página a scrapear
        if response.status_code == 200:
            home_soup = BeautifulSoup(response.content, 'lxml')
            return home_soup
        
    except Exception as e:
        print(e)


def getNavSections(home_soup):
    """Recibe la sopa de la página principal, retorna los enlaces de las secciones"""
    
    nav_sect_soup = home_soup.find('ul', attrs={'class':'horizontal-list main-sections hide-on-dropdown'}).find_all('li')
    nav_sections = [section.a.get('href') for section in nav_sect_soup]
    return nav_sections


def getSectionNewsLinks(sections):
    """Recibe los enlaces de las secciones, retorna los enlaces de las noticias en ellas """
    
    links_to_news = []
    for section in sections:
        section_response = requests.get(section) # Consulta las secciones
        
        try:
            if section_response.status_code == 200:
                section_soup = BeautifulSoup(section_response.content, 'lxml')
                articles = section_soup.find('div', attrs={'id':'main-content'}).find_all('article')
                news_links = [i.a.get('href') for i in articles]
                links_to_news.append(news_links)
                
        except Exception as e:
            print(e)   
            
    return links_to_news


def getInfo(HOME_URL, sections_news_links):
    
    info = []
    for list_section_links in sections_news_links:
        for article in list_section_links:
        
            news_response = requests.get(HOME_URL + article)
            
            try:
                if news_response.status_code == 200:
                    article_soup = BeautifulSoup(news_response.content, 'lxml')
                    
                    # Título de la noticia
                    title = article_soup.find('title').get_text() 
                    title = re.sub(r'Página12', '', title)
                    
                    # Fecha de publicación
                    date = article_soup.find('span').get_text()
                    
                    #Resumen de la noticia
                    summary = article_soup.find('div',attrs={'class':'col 2-col'}).find('h3').get_text()
                    
                    # Cuerpo de la noticia
                    body = article_soup.find('div', attrs={'class':'article-main-content article-text'}).find_all('p')
                    body = [p.get_text() for p in body]
                    
                    info.append({'title': title, 
                                 'date': date
                                 'summary': summary,
                                 'body' : body})
                    
                    print(body)
                    
            except Exception as e:
                print(e)
                    
    return info