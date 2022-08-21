from imp import find_module
from itertools import product
from turtle import delay
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

import re
import uuid
from pathlib import Path
import json
  

class scraper:

    '''
        Parameters:
        -----------

        Attributes:
        -----------

        Methods:
        --------


    '''

    def __init__(self) -> None:

        self.link_list = []
        self.product_info_dict = {'Name':[],'ID':[],'UUID':[],'Serving Size':[], 'Cost per serving':[],'Product cost':[],'Amount':[],'Product link':[]}

        

    def load_and_get_links(self):

        driver = webdriver.Chrome()
        driver.get('https://www.myprotein.com/nutrition/protein.list')
        time.sleep(2)
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,'//div[@class="emailReengagement show"]')))        
            x_button = driver.find_element(by=By.XPATH,value='//button[@class="emailReengagement_close_button"]')
            x_button.click()
        except:
            pass

        while True:
            link_buttons = driver.find_elements(by=By.XPATH,value='//div[@class="athenaProductBlock_imageContainer"]/a[@class="athenaProductBlock_linkImage"]')
            for tag in link_buttons:
                link = tag.get_attribute('href')
                self.link_list.append(link)
            next_button = driver.find_element(by=By.XPATH, value='//button[@class="responsivePaginationNavigationButton paginationNavigationButtonNext"]')
            try:
                if next_button.get_attribute('data-direction') == 'next':
                    next_button.click()
                    time.sleep(2)
                else:
                    break
            except AttributeError:
                break
        print(self.link_list)
        return driver


        

    def get_info(self,link_list,driver:webdriver.Chrome):
     #   product_dict =  {'Name':[],'ID':[],'UUID':[],'Serving Size':[], 'Cost per serving':[],'Product cost':[],'Amount':[],'Product link':[]}
        for link in link_list:
            time.sleep(1)
            product_dict = {}

            # page = requests.get('http://pythonscraping.com/pages/page3.html')
            # html = page.text # Get the content of the webpage
            # soup = BeautifulSoup(html, 'html.parser') 
            # suggested_use = soup.find(name='div',attrs={'id':'product-description-content-lg-6'}).firs.findChild.findChildren[1]
            # print(suggested_use.text)

            driver.get(link)
            #Get product id
            id = re.search(r'(\d{8})(\.html)$',link)
            folder_path = (Path.cwd()/ Path(f'raw_data\{id.group(1)}'))
            folder_path.mkdir(exist_ok=True)
            product_dict['ID'] = id.group(1)
            product_dict['UUID'] = str(uuid.uuid4())
            product_dict['Product link'] = link

            cost = driver.find_element(by = By.XPATH, value = ('//p[@class="productPrice_price  "]')).text
            cost_float = re.search(r'\d+\.\d{2}',cost).group()
            name = driver.find_element(by = By.XPATH, value = ('//h1[@class="productName_title"]')).text
            amount = driver.find_element(by = By.XPATH, value = ('//button[@data-selected]')).text
            #suggested_use = driver.find_element(by = By.XPATH, value = ('//div[@data-tab-title="Suggested Use"]//parent::button/following-sibling::div/div/div/p'))
            # suggested_use_button = driver.find_element(by=By.XPATH, value='//div[@class="productDescription_contentPropertyListItem  productDescription_contentPropertyListItem_suggestedUse "]/button')
            # suggested_use_button.click()
            #WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//div[@id="product-description-content-lg-6"]/div/div/p')))
            try:
                #suggested_use = driver.find_elements(by = By.XPATH, value = ('//div[@id="product-description-content-lg-6"]/div/div/p'))[0].get_attribute('innerHTML')
                suggested_use = driver.find_element(by=By.XPATH,value=('//div[@id="product-description-content-6"]')).get_attribute('innerHTML')
            except:
                pass
            try:
                serving_size = re.search(r'(\d{1,2})g',suggested_use)
                cost_per_serving = round(float(cost_float)/float(serving_size.group(1)),2)
                print(serving_size.group())
                product_dict['Serving Size'] = serving_size.group()

            except:
                product_dict['Serving Size']= 'Sample Size'
                cost_per_serving = 'Sample'

            product_dict['Name'] = name
            product_dict['Cost per serving'] = cost_per_serving
            product_dict['Product cost'] = cost
            product_dict['Amount'] = amount
            
            with open(f'{folder_path}\data.json', 'w', encoding='utf-8') as f:
                json.dump(product_dict, f, ensure_ascii=False, indent=4)
            #
            
if __name__ == "__main__":
    data = scraper()
    data.get_info(data.link_list,(data.load_and_get_links()))


#            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gdpr-consent-notice"]')))
#            print("Frame Ready!")
#            driver.switch_to.frame('gdpr-consent-notice')
#            accept_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="save"]')))
   

# driver = webdriver.Chrome()

# driver.get("http://www.python.org")
# time.sleep(2)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# search_bar = driver.find_element(by=By.XPATH, value='//*[@id="id-search-field"]')
# search_bar.click()
# search_bar.send_keys("method")
# search_bar.send_keys(Keys.RETURN)

# time.sleep(2)