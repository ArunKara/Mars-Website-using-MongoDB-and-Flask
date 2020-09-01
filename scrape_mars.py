from splinter import Browser
from bs4 import BeautifulSoup
import time


def init_browser():
    # @ Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver'}
    return Browser("chrome", **executable_path) 


def scrape():

    browser = init_browser()

    dictionary = {}

    news_titles, news_p = news_mars()

    dictionary["titles"] = news_titles
    dictionary["paragraph"] = news_p
    dictionary["main_image"] = main_image()
    dictionary["mars_facts"] = mars_facts()
    dictionary["mars_hemispheres"] = mars_hemis()
    browser.quit()
    return dictionary




def news_mars():

    browser = init_browser()

    url = ('https://mars.nasa.gov/news/')

    browser.visit(url)

    time.sleep(1)

    url_html = browser.html
    soup = BeautifulSoup(url_html, 'html.parser')

    try:
        element = soup.select_one('ul.item_list li.slide')

        news_titles = element.find('div', class_="content_title").get_text()

        news_p = element.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    browser.quit()

    return news_titles, news_p

def main_image():

    browser = init_browser()

    website_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    core_url = 'https://www.jpl.nasa.gov'

    browser.visit(website_url)

    time.sleep(1)

    element_full_image = browser.find_by_id("full_image")
    element_full_image.click()

    browser.is_element_present_by_text('more info', wait_time = 1)
    element_more_info = browser.links.find_by_partial_text('more info')
    element_more_info.click()

    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')

    image_url_final = image_soup.select_one('figure.lede a img').get('src')
    #image_url_final



    final_url = core_url + image_url_final
    #final_url

    browser.quit()

    return final_url

def mars_facts():
    browser = init_browser()

    mars_info = 'https://space-facts.com/mars/'
    table = pd.read_html(mars_info)

    mars_info_df = table[0]
    mars_info_df.columns = ["Info", "Value"]
    mars_info_df.set_index(["Info"], inplace=True)
    
    info_html = mars_info_df.to_html()
    info_html = info_html.replace("\n","")
    info_html
    
    browser.quit()

    return info_html

def mars_hemis():
    browser = init_browser()

    cerberus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    response = requests.get(cerberus_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    cerberus_image = soup.find_all('div', class_="wide-image-wrapper")

    for image in cerberus_image:
        picture = image.find('li')
        full_image = picture.find('a')['href']
    print(full_image)
    cerberus_title = soup.find('h2', class_='title').text
    cerberus_hem = {"Title": cerberus_title, "url": full_image}

    schiaparelli_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'

    response = requests.get(cerberus_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    schiaparelli_image = soup.find_all('div', class_="wide-image-wrapper")

    for image in schiaparelli_image:
        picture = image.find('li')
        full_image2 = picture.find('a')['href']
    
    schiaparelli_title = soup.find('h2', class_='title').text
    schiaparelli_hem = {"Title": schiaparelli_title, "url": full_image2}

    syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'

    response = requests.get(syrtis_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    syrtis_image = soup.find_all('div', class_="wide-image-wrapper")

    for image in syrtis_image:
        picture = image.find('li')
        full_image3 = picture.find('a')['href']
    syrtis_title = soup.find('h2', class_='title').text
    syrtis_hem = {"Title": syrtis_title, "url": full_image3}

    valles_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    response = requests.get(valles_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    valles_image = soup.find_all('div', class_="wide-image-wrapper")
    for image in valles_image:
        picture = image.find('li')
        full_image4 = picture.find('a')['href']
    valles_title = soup.find('h2', class_='title').text
    valles_hem = {"Title": valles_title, "url": full_image4}

    mars_hemispheres = [{"Title": cerberus_title, "url": full_image},
                   {"Title": schiaparelli_title, "url": full_image2},
                   {"Title": syrtis_title, "url": full_image3},
                   {"Title": valles_title, "url": full_image4}]

    browser.quit()
    return mars_hemispheres


