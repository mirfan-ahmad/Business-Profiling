import os
import random
import datetime
import pandas as pd
import streamlit as st
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class WebScraper:
    def __init__(self, RUN_SELF=False):
        self.name = []
        self.number = []
        self.website = []
        self.address = []
        self.city = []
        self.linkedIn = []
        self.RUN_SELF = RUN_SELF
        self.dataframe = None
        self.start()
    
    
    def start_driver(self, link, path):
        option = webdriver.ChromeOptions()
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        except:
            self.driver = webdriver.Chrome(service=Service("chromedriver/chromedriver.exe"), options=option)
        self.driver.maximize_window()
        self.driver.get(link)
    
    
    def scrape_one_business(self, driver, query):
        try:
            element = driver.find_element(By.XPATH, '//*[@id="b_context"]/li/div[1]/div[2]/div/div/div[2]/div/div[1]/h2')
            self.name = element.text
            try:
                self.website = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except NoSuchElementException:
                self.website = 'Website Not Found'
            try:
                self.address = driver.find_element(By.XPATH, '//*[@id="IconItem_9"]/div/span/a').text
            except NoSuchElementException:
                self.address = 'Address Not Found'
            try:
                self.phone_number = driver.find_element(By.CSS_SELECTOR, '#IconItem_10 > a').text
            except NoSuchElementException:
                self.phone_number = 'Phone Number Not Found'
            print('Scraped Data:', self.name, self.website, self.address, self.phone_number)
        except NoSuchElementException as e:
            print('No Such Element Found', e)
            self.name, self.website, self.address, self.phone_number = query.replace('+', ' '), 'Webiste Not Found', 'Address Not Found', 'Phone Number Not Found'
            return
        
    
    def scrape_data(self):
        SCRAPED = 0
        st.write("Scraping data for:", self.query)
        query = self.query.replace(" ", "%20")
        link = f'https://www.google.com/localservices/prolist?g2lbs=AIQllVyNk2Pbqnph9O2BVURId3NUsNUzfgDLCKbpLww_PzyAgLK3hD-UysZ1_-oPaC3Rtu7bmcdKTQd3Qq5FwsvUTCe-LQAGbQt8u-mq0xyGbl3SBhdeR-w%3D&hl=en-PK&gl=pk&ssta=1&oq=salon%20in%20usa&src=2&sa=X&q={query}&ved=0&scp=Cg9nY2lkOnVuaXZlcnNpdHkqClVuaXZlcnNpdHk%3D'
        
        path = os.path.join('chromedriver', 'chromedriver.exe')
        self.start_driver(link, path)
        self.wait = WebDriverWait(self.driver, 10)
        i, page = 1, 1

        sleep(5)
        if not os.path.exists('Scraped_Files'):
            os.makedirs('Scraped_Files')
        
        container = st.empty()
        date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        self.file_name = os.path.join('Scraped_Files', f'{self.query}_{date}.csv')
        with open(self.file_name, 'w', encoding='utf-8') as file:
            file.write('Company Name,Phone Number,Website,Address,City\n')
            while True:
                try:
                    if self.profiles == 0:
                        self.__save_to_csv()
                        break
                    name = self.__company_name(i).replace(",", " ")
                    print('Got Name of the Company', name)
                    sleep(random.random() * random.randint(0, 3))
                    self.name.append(name.replace(",", " "))
                    self.number.append(self.__phone_number().replace(",", " "))
                    print('Got Phone Number of the Company', self.number[-1])
                    self.website.append(self.__Website().replace(",", " "))
                    print('Got Website of the Company', self.website[-1])
                    self.address.append(self.__Address().replace(",", " "))
                    print('Got Address of the Company', self.address[-1])
                    file.write(f"{name},{self.number[-1]},{self.website[-1]},{self.address[-1].replace(',', ' ')},{self.query.split('in ')[-1]}\n")
                    i += 2
                    SCRAPED += 1
                    self.profiles -= 1
                    container.empty()
                    container.text(f"Scraped Business: {SCRAPED}")
                
                except NoSuchWindowException:
                    st.write('No Such Window Exception!, Restart the process.')
                    return
                
                except Exception as e:
                    try:
                        if page == 1:
                            try:
                                self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[2]/div/div/button').click()
                            except:
                                self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[2]/div/div/button').click()
                            page += 1
                        else:
                            self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[2]/div[2]/div/button').click()

                        sleep(random.random() * random.randint(0, 3))
                        i = 1

                    # If the page is not found, then break the loop as all the pages have been scraped
                    except Exception as e:
                        self.__save_to_csv()
                        break

    def __save_to_csv(self):
        data = {'Company Name': self.name,
                'Phone Number': self.number,
                'Website': self.website,
                'Address': self.address
                }

        self.dataframe = pd.DataFrame(data)

    def __company_name(self, i):
        company_element = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[{i}]')))
        company_element.click()

        return self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div[3]/div[1]/c-wiz/div/c-wiz/div/div/div[3]/c-wiz[1]/div[1]/c-wiz/div'))).text

    def __Website(self):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, 'div.bfIbhd>div:nth-child(1)>div>a>div:nth-child(2)').text
        except NoSuchElementException:
            try:
                return self.driver.find_element(By.CSS_SELECTOR, 'div.bfIbhd>div:nth-child(2)>div>a>div:nth-child(2)').text
            except NoSuchElementException:
                try:
                    return self.driver.find_element(By.CSS_SELECTOR, 'div.bfIbhd>div:nth-child(3)>div>a>div:nth-child(2)').text
                except:
                    return 'Website not found'

    def __Address(self):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, 'div.bfIbhd>div:nth-child(2)>div>a>div>div:nth-child(2)>span').text
        except NoSuchElementException:
            try:
                return self.driver.find_element(By.CSS_SELECTOR, 'div.bfIbhd>div:nth-child(3)>div>a>div>div:nth-child(2)>span').text
            except NoSuchElementException:
                try:
                    return self.driver.find_element(By.CSS_SELECTOR, 'div.bfIbhd>div:nth-child(4)>div>a>div>div:nth-child(2)>span').text
                except NoSuchElementException:
                    try:
                        return self.driver.find_element(By.CSS_SELECTOR, 'div.bfIbhd>div:nth-child(5)>div>a>div>div:nth-child(2)>span').text
                    except NoSuchElementException:
                        try:
                            return self.driver.find_element(By.CSS_SELECTOR, 'div.bfIbhd>div:nth-child(6)>div>a>div>div:nth-child(2)>span').text
                        except:
                            return 'Not Found'

    def __phone_number(self):
        try:
            phone = self.driver.find_element(By.CSS_SELECTOR, 'div.eigqqc').text
            print('--Phone Number-- ', phone)
            return phone
        except:
            print('Phone Number not found')
            return 'Phone Number not found'

    def start(self):
        if not self.RUN_SELF:
            st.title("Scrape Business Profiles")
        st.write('Scrape all the details of business profiles')
        
        if self.RUN_SELF:
            col1, col2 = st.columns([4, 1])
            with col1:
                self.query = st.text_input("Enter Query")
            with col2:
                self.profiles = int(st.text_input("Profiles", 0))
                
        else:
            self.query = st.text_input("Enter Query")
            self.button = st.button("Scrape")