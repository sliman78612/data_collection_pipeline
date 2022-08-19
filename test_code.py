from json import load
from lib2to3.pgen2 import driver
from multiprocessing.connection import wait
import requests
from bs4 import BeautifulSoup
# page = requests.get('http://pythonscraping.com/pages/page3.html')
# html = page.text # Get the content of the webpage
# soup = BeautifulSoup(html, 'html.parser') # Convert that into a BeautifulSoup object that contains methods to make the tag searcg easier
# #print(soup.prettify())

# fish = soup.find(name='tr', attrs={'id': 'gift3', 'class': 'gift'}) # If it doesn't find anything it returns None

# fish_row = fish.find_all('td') 
# title = fish_row[0].text
# description = fish_row[1].text
# price = fish_row[2].text
# print(title)
# print(description)
# print(price)

# parrot = fish.find_next_sibling()
# parrot_children = parrot.findChildren()
# print(parrot_children[0].text)

from selenium import webdriver 
from selenium.webdriver.common.by import By
import time

def load_and_accept_cookies() -> webdriver.Chrome:
    driver = webdriver.Chrome()

    URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
    driver.get(URL)
    time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot

    try:
        driver.switch_to_frame('gdpr-consent-notice')
        accept_cookies_brn = driver.find_element_by_xpath(by = By.XPATH, value = '\\*[@id="save"]')
        accept_cookies_brn.click

    except AttributeError:
        driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
        accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
        accept_cookies_button.click()

    except:
        pass 
    return driver

def get_links(driver:webdriver.Chrome):

    '''
    Returns list of links from first page of zoopla
    ---------------------
    
    driver:webdriver.Chrome
        Driver contianing information about current page
    ------------------------

    Returns
    -------
    link_list:list
        A list of link from first page
    '''

    house_property = driver.find_element(by=By.XPATH, value = '//*[@id="listing_62220157"]')
    a_tag = house_property.find_element(by = By.TAG_NAME, value='a')
    link = a_tag.get_attribute('href')

    prop_container = driver.find_elements(by=By.XPATH, value='//div[@data-testid="search-result"]')
    link_list = []
    for container in prop_container:
        a_tag = container.find_element(by=By.TAG_NAME, value='a')
        link_list.append(a_tag.get_attribute('href'))

    return link_list

def get_info(link_list):
    properties_dict = {'Price':[],'Address':[], 'Bedrooms':[],'Square Footage':[],'Description':[]}
    for link in link_list:
        driver.get(link)
        time.sleep(2)
        price = driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]')
        address = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]')
        #bedrooms = driver.find_element (by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-kQvhQW-centered-true c-PJLV-iPJLV-css"]')
        bedrooms = driver.find_elements(by=By.XPATH ,value = '//div[@class = "c-PJLV c-PJLV-kQvhQW-centered-true c-PJLV-iPJLV-css"]')
        description = driver.find_element(by=By.XPATH ,value = '//div[@data-testid="truncated_text_container"]/div[@class="css-14s800p e1am2vkf3"]')


        properties_dict['Price'].append(price.text)
        properties_dict['Address'].append(address.text)
        properties_dict['Bedrooms'].append(bedrooms[-3].text)
        properties_dict['Square Footage'].append(bedrooms[-1].text)
        properties_dict['Description'].append(description.text)

    return properties_dict


driver = load_and_accept_cookies()
time.sleep(2)
get_info(get_links())
print(properties_dict['Price'])