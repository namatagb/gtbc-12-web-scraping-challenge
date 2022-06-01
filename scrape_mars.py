from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #scrape title and pargraph of article sample
    mars_dict = {}
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    mars_dict['title'] = news_title
    mars_dict['paragraph'] = news_p

    #scrape main mars image
    url1 = 'https://spaceimages-mars.com/'
    browser.visit(url1)
    image_html = browser.html
    soup1 = bs(image_html, 'html.parser')
    image = soup1.find("div", class_='floating_text_area')
    href = image.a["href"]
    image_url = url + href

    mars_dict['image'] = image_url

    #scrape for mars facts
    url2 = 'https://galaxyfacts-mars.com/'
    browser.visit(url2)
    mars_table = pd.read_html(url2)
    mars_table = mars_table[0]
    mars_table = mars_table.drop(labels=0, axis=0)
    #mars_table.columns = mars_table.iloc[0]
    #mars_table = mars_table[1:]

    mars_table_out = mars_table.to_html('table.html')

    mars_dict['table'] = mars_table_out

    #scrape for mars hemisphere photos
    url3 = 'https://marshemispheres.com/'
    browser.visit(url3)
    html = browser.html
    soup = bs(html, 'html.parser')
    photos = soup.find('div', class_='result-list')
    hemispheres = photos.find_all("div", class_="description")
    image_list = []
    for hemis in hemispheres:
        image_dict = {}
        image_title = hemis.h3.text
        image_dict['title'] = image_title
        nav = hemis.find('a', class_="itemLink product-item")['href']    
        browser.visit(f"https://marshemispheres.com/{nav}")
        original = browser.find_by_text('Sample')['href']
        image_dict['img_url'] = url + original
        image_list.append(image_dict)

    mars_dict['hemispheres'] = image_list


    # Quit the browser
    browser.quit()

    return mars_dict
