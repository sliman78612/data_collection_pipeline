from turtle import delay
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

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
        self.product_info_dict = {'Name':[],'Serving Size':[], 'Cost per serving':[],'Product cost':[],'Amount':[],}

        

    def load_and_get_links(self):

        driver = webdriver.Chrome()
        driver.get('https://www.myprotein.com/nutrition/protein.list')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@class="emailReengagement show"]')))        
        x_button = driver.find_element(by=By.XPATH,value='//button[@class="emailReengagement_close_button"]')
        x_button.click()

        while True:
            link_buttons = driver.find_elements(by=By.XPATH,value='//div[@class="athenaProductBlock_imageContainer"]/a[@class="athenaProductBlock_linkImage"]')
            for tag in link_buttons:
                link = tag.get_attribute('href')
                self.link_list.append(link)
            next_button = driver.find_element(by=By.XPATH, value='//button[@class="responsivePaginationNavigationButton paginationNavigationButtonNext"]')
            try:
                if next_button.get_attribute('data-direction') == 'next':
                    next_button.click()
                    time.sleep(10)
                else:
                    break
            except AttributeError:
                break
        print(self.link_list)
        return driver


        

    def get_info(link_list, driver:webdriver.Chrome()):

        pass


data = scraper()
print(data.link_list)
data.load_and_get_links()


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