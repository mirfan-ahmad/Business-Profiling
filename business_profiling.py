import streamlit as st
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class WebScraper:
    def __init__(self):
        self.name = []
        self.number = []
        self.website = []
        self.address = []
        self.linkedIn = []
        self.designations = ['Principal', 'Project Manager']
        self.start()

    def scrape_data(self):
        st.write("Scraping data for:", self.query)
        query = self.query.replace(" ", "%20")
        link = f'https://www.google.com/localservices/prolist?g2lbs=AIQllVyNk2Pbqnph9O2BVURId3NUsNUzfgDLCKbpLww_PzyAgLK3hD-UysZ1_-oPaC3Rtu7bmcdKTQd3Qq5FwsvUTCe-LQAGbQt8u-mq0xyGbl3SBhdeR-w%3D&hl=en-PK&gl=pk&ssta=1&oq=salon%20in%20usa&src=2&sa=X&q={query}&ved=0&scp=Cg9nY2lkOnVuaXZlcnNpdHkqClVuaXZlcnNpdHk%3D'

        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(service='chromedriver', options=options)
        self.driver.get(link)

        self.wait = WebDriverWait(self.driver, 10)
        i, page = 1, 1

        while True:
            try:
                name = self.__company_name(i)
                print('Got Name of the Company', name)
                self.name.append(name)
                self.number.append(self.__phone_number())
                print('Got Phone Number of the Company', self.number[-1])
                self.website.append(self.__Website())
                print('Got Website of the Company', self.website[-1])
                self.address.append(self.__Address())
                print('Got Address of the Company', self.address[-1])

                i += 2
                sleep(random.random() * random.randint(0, 3))

            # If the element is not found, then click the next page button
            except Exception as e:
                try:
                    if page == 1:
                        st.write('Trying to click the next page button')
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
        self.driver.quit()
        data = {'Company Name': self.name,
                'Phone Number': self.number,
                'Website': self.website,
                'Address': self.address
                }

        df = pd.DataFrame(data)
        st.write(df)

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
            return self.driver.find_element(By.CSS_SELECTOR, 'div.eigqqc').text
        except:
            print('Phone Number not found')
            return 'Phone Number not found'

    def start(self):
        st.title("Scrape Business Profiles")
        st.write('Scrape all the details of business profiles')
        self.query = st.text_input("Enter Query")
        if st.button("Scrape"):
            self.scrape_data()
