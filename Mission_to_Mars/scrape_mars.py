from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # ################################
    # first scrape
    # set up splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL for the first scrape:
    url = 'https://redplanetscience.com'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find the correct div classes
    all_titles = soup.find_all('div', class_='content_title')
    all_news_p = soup.find_all('div', class_='article_teaser_body')

    # store in a variable that grabs the first item in the list and takes just the text
    first_title = all_titles[0].text
    first_p = all_news_p[0].text

    # ################################
    # second scrape
    # New url for the 2nd scrape:
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find featured image and assign to variable
    featured_image = soup.find(class_='headerimage', src=True)

    # extract src from image, build and assign url to variable
    featured_image_url = url + '/' + featured_image.get('src')

    # ################################
    # third scrape
    # New URL for the 3rd scrape
    url = 'https://galaxyfacts-mars.com/'

    # read_html returns a list of tables from the URL
    tables = pd.read_html(url)

    # we want the second table from this and set it equal to a variable
    mars_planet_profile = tables[1]
    mars_planet_profile

    # now convert the table into a HTML string
    html_table = mars_planet_profile.to_html()

    # ################################
    # fourth scrape
    # extract src from image, build and assign url to variable
    hemis = ['cerberus','schiaparelli','syrtis','valles']
    url_list = []

    for each in hemis:
        url = 'https://marshemispheres.com/' + each + '.html'
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_link = soup.find(class_='wide-image', src=True)
        featured_image_url = 'https://marshemispheres.com/' + image_link.get('src')
        url_list.append(featured_image_url)


    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": url_list[0]},
        {"title": "Schiaparelli Hemisphere", "img_url": url_list[1]},
        {"title": "Syrtis Major Hemisphere", "img_url": url_list[2]},
        {"title": "Valles Marineris Hemisphere", "img_url": url_list[3]}
    ]
    
    scraped_data = {}
    scraped_data["Headline"] = first_title
    scraped_data["NewsBlurb"] = first_p
    scraped_data["Image_URL"] = featured_image_url
    scraped_data["HTML_table"] = html_table
    scraped_data["Hemis_URL"] = hemisphere_image_urls
    
    # quit the browser
    browser.quit()
    
    return scraped_data

