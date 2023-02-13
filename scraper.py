from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import csv

class WebScrapper:
    def __init__(self, url):
        self.url = url
        self.scraped_datas = []
        self.listings = None
        self.driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
     
    def click_load_more(self):
        while True:   
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@data-aut-id="btnLoadMore"]')))
                self.driver.find_element(By.XPATH, '//*[@data-aut-id="btnLoadMore"]').click()
                print("Clicked 'Muat Lainnya'")
            except ( NoSuchElementException, TimeoutException, StaleElementReferenceException ):
                break
    
    def scrape(self):
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.click_load_more()
    
    def find_ul_element(self):
        ul_element = None
        all_ul_element = self.driver.find_elements(By.TAG_NAME, 'ul')
        for uls in all_ul_element:
            if uls.get_attribute("data-aut-id") == "itemsList":
                ul_element = uls
        self.listings =  ul_element.find_elements(By.TAG_NAME, "li")
    
    def loop_element(self):
        for listing in self.listings:
             if listing.get_attribute('data-aut-id') == 'itemBox':
                try:
                    ad_link = listing.find_element(By.XPATH, "./a").get_attribute("href")
                except NoSuchElementException:
                    print("No ad_link")
                    break
                try:
                    ad_details_card = listing.find_element(By.CLASS_NAME, "fTZT3")
                except NoSuchElementException:
                    print("No ad_details")
                try:
                    ad_price = ad_details_card.find_element(By.CSS_SELECTOR, "span[data-aut-id='itemPrice']").text
                except NoSuchElementException:
                    print("No ad_price")
                try:
                    ad_title = ad_details_card.find_element(By.CSS_SELECTOR, "span[data-aut-id='itemTitle']").text
                except NoSuchElementException:
                    print("No ad_title")
                try:
                    ad_details = ad_details_card.find_element(By.CSS_SELECTOR, "span[data-aut-id='itemDetails']").text
                except NoSuchElementException:
                    print("No ad_title")
                self.scraped_datas.append([ad_link, ad_price, ad_title,ad_details])
        
    def list_to_csv(self):
        with open(f'scraped_data/scraped_data.csv', 'w', newline='', encoding="utf-8") as file: 
            writer = csv.writer(file)
            headers = ['Ad Link','Price', 'Ad Title', 'Ad Location', 'Ad Details']
            writer.writerow(headers)
            for data in self.scraped_datas:
                writer.writerow(data)