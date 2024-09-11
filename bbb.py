import os
import random
import datetime
import pandas as pd
import streamlit as st
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from webdriver_manager.chrome import ChromeDriverManager


class BBB:
    def __init__(self):
        self.TITLES = {'BBB File Opened:': 'BBB File Opened',
                  'Years in Business:': 'Years in Business',
                  'Business Started:': 'Business Started',
                  'Business Incorporated:': 'Business Incorporated',
                  'Accredited Since:': 'Accredited Since',
                  'Type of Entity:': 'Type of Entity',
                  'Alternate Business Name': 'Alternate Business Name',
                  'Business Management': 'Business Management',
                  'Additional Contact Information': 'Additional Contact Information',
                  'Business Categories': 'Business Categories'}
        self.DATA = []
        self.GUI()
        if st.button('Scrape'):
            self.Scrape()
            try:                
                converter = self.DataFrameConverter(self.DATA, self.business)
                df = converter.convert_into_df()
                st.write(df)
            except Exception as e:
                print('Error converting', e)
                st.write('Got Error while converting to DataFrame')
            
    
    def start_driver(self, link):
        option = webdriver.ChromeOptions()
        option.add_argument("--incognito")
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        except:
            self.driver = webdriver.Chrome(service=Service("chromedriver/chromedriver.exe"), options=option)
        self.driver.maximize_window()
        self.driver.get(link)
        
    
    def Scrape_Pages(self, BUSINESSES, page):
        for i in range(1, 19):
            try:
                BUSINESSES.append(self.driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div/div[1]/div[2]/div[{i}]/div/div[1]/div/h3/a').get_attribute('href'))
            except NoSuchElementException:
                pass
        
        if page == 0:
            try:
                if self.pages == 0:
                    return
                return self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div[1]/nav/a[1]').get_attribute('href')
            except:
                return

        else:
            try:
                return self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div[1]/nav/a[3]').get_attribute('href')
            except NoSuchElementException:
                print('Element not Found')

    def __scrape_address(self, COLUMNS):
        location = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div[1]/div/div/dl/div[1]/dd').text.split('\n')[0]
        COLUMNS['Full Address'] = location
        
        address = location.split(',')
        if len(address) == 3:
            COLUMNS['Address'] = address[0]
            COLUMNS['City'] = address[1]
            state_zip = address[2].split(' ')
            COLUMNS['State'] = state_zip[1]
            try:
                COLUMNS['Zip Code'] = state_zip[2].split('-')[0]
            except:
                COLUMNS['Zip Code'] = 'Not Found'
        else:
            COLUMNS['Address'] = 'Not Found'
            COLUMNS['City'] = address[0]
            state_zip = address[1].split(' ')
            COLUMNS['State'] = state_zip[1]
            try:
                COLUMNS['Zip Code'] = state_zip[2].split('-')[0]
            except:
                COLUMNS['Zip Code'] = 'Not Found'
        return COLUMNS
    
    def __scrape_phone_website(self, COLUMNS):
        anchor = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div[2]/div[1]/div[2]/a')
        if anchor.text == 'Visit Website':
            COLUMNS['Website'] = anchor.get_attribute('href')
        elif anchor.text[:5] != 'Email':
            COLUMNS['Website'] = 'Not Found'
            COLUMNS['Phone Number'] = anchor.text
        else:
            COLUMNS['Website'] = 'Not Found'

        try:
            phone_or_email = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div[2]/div[1]/div[2]/a').text
            if phone_or_email[:5] not in ['Email', 'Visit']:
                COLUMNS['Phone Number'] = phone_or_email
            else:
                phone = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div[2]/div[1]/div[3]/a').text
                if phone[:5] not in ['Email', 'Visit']:
                    COLUMNS['Phone Number'] = phone
                else:
                    phone = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div[2]/div[1]/div[4]/a').text
                COLUMNS['Phone Number'] = phone
        except:
            COLUMNS['Phone Number'] = 'Not Found'
        return COLUMNS


    def Scrape_details(self, COLUMNS, link):
        ## Scraping Business Details
        Company = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div/h1').text.split('\n')[1]
        COLUMNS['Company'] = Company
        
        COLUMNS = self.__scrape_address(COLUMNS)
        COLUMNS = self.__scrape_phone_website(COLUMNS)
    
        ## Scraping Remaining Details
        for i in range(2, 17):
            try:
                element = self.driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div[1]/div[1]/div/div/dl/div[{i}]')
                if element.find_element(By.TAG_NAME, 'dt').text == 'Additional Contact Information':
                    elements = element.find_elements(By.CSS_SELECTOR, 'dd > div')
                    for ele in elements:
                        try:
                            COLUMNS[f"Alt {ele.find_element(By.TAG_NAME, 'p').text}"] = ele.find_element(By.CSS_SELECTOR, 'ul>li>span').text
                        except NoSuchElementException:
                            pass
                        
                        for idx, anchor in enumerate(ele.find_elements(By.CSS_SELECTOR, 'ul>li')):
                            if anchor.find_element(By.TAG_NAME, 'a').text != 'Email this Business':
                                COLUMNS[f"Alt {ele.find_element(By.TAG_NAME, 'p').text} {idx+1}"] = anchor.find_element(By.TAG_NAME, 'a').text
                
                elif element.find_element(By.TAG_NAME, 'dt').text == 'Business Categories':
                    categories = ''
                    anchors = element.find_elements(By.TAG_NAME, 'a')
                    for anchor in anchors:
                        categories+= anchor.text + ', '
                    COLUMNS['Business Categories'] = categories
                
                elif element.find_element(By.TAG_NAME, 'dt').text == 'Business Management':
                    elements = element.find_elements(By.CSS_SELECTOR, 'dd > ul > li')
                    
                    for idx, ele in enumerate(elements):
                        complete_name = ele.text.split('. ')[1].split('. ')
                        COLUMNS[f'Person {idx+1}'] = complete_name[0].split(', ')[0]
                        COLUMNS[f'Desgination {idx+1}'] = complete_name[0].split(', ')[1]
                
                elif element.find_element(By.TAG_NAME, 'dt').text == 'Social Media':
                    elements = element.find_elements(By.CSS_SELECTOR, 'dd > ul > li')
                    for idx, ele in enumerate(elements):
                        COLUMNS[f"{ele.find_element(By.TAG_NAME, 'a').text} {idx+1}"] = ele.find_element(By.TAG_NAME, 'a').get_attribute('href')
                
                elif element.find_element(By.TAG_NAME, 'dt').text in self.TITLES:
                    COLUMNS[self.TITLES[element.find_element(By.TAG_NAME, 'dt').text]] = element.find_element(By.TAG_NAME, 'dd').text
                    
            except Exception as e:
                pass
        
        COLUMNS['BBB Profile Link'] = link
        
        return COLUMNS
            
    
    def Scrape_Business(self, links, progress_bar, total):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        for idx, link in enumerate(links):
            sleep(1)
            try:
                self.driver.get(f'{link}/details')
                data = self.Scrape_details({}, link)
                if data not in self.DATA:
                    self.DATA.append(data)
                
                progress_bar.empty()
                progress_bar.progress((self.PAGE+idx) / total)
            except:
                pass
        
        self.PAGE = idx
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return
        
        
    def Scrape(self):
        BUSINESSES = []
        
        self.start_driver(f'https://www.bbb.org/search?find_country={self.state}&find_loc={self.city.replace(',', '%2C').replace(' ', '%20')}&find_text={self.business.replace(' ', '%20')}')
        
        try:
            self.PAGE = 1
            progress_bar = st.progress(0)
            for page in range(self.pages):
                next_page = self.Scrape_Pages(BUSINESSES, page)
                sleep(2)
                self.Scrape_Business(BUSINESSES, progress_bar, (self.pages*len(BUSINESSES)))
                BUSINESSES = []
                
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.get(next_page)
                
                sleep(random.random() * random.randint(0, 5))

        except NoSuchWindowException:
            st.write('Window has been closed, Restart the Scrapper.')
            return True

        except Exception as e:
            print('Exception Raised:', e)
            self.driver.quit()
            return True
        
        self.driver.quit()
        return True
    
    class DataFrameConverter:
        def __init__(self, data, business):
            self.business = business
            self.DATA = data

        def __find_max_keys_dict(self, data):
            max_keys_dict = max(data, key=lambda x: len(x.keys()))
            return max_keys_dict

        def convert_into_df(self):
            order = list(self.__find_max_keys_dict(self.DATA).keys())

            all_keys = set()
            for entry in self.DATA:
                all_keys.update(entry.keys())

            ordered_all_keys = [key for key in order if key in all_keys] + [key for key in all_keys if key not in order]

            rows = []
            for entry in self.DATA:
                row = {key: entry.get(key, 'Not Found') for key in ordered_all_keys}
                rows.append(row)

            df = pd.DataFrame(rows, columns=ordered_all_keys)
            date_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            os.makedirs('Scraped_Files', exist_ok=True)
            df.to_csv(f'Scraped_Files/{self.business}_{date_time}.csv', index=False)
            return df
        
    def GUI(self):
        # st.set_page_config(layout="wide")
        st.title('Better Buesiness Bureau')
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            self.business = st.text_input('Enter Business name:')
        with col2:
            self.city = st.text_input('Enter City:')
        with col3:
            self.state = st.selectbox('State', ['US', 'Canada'])
            self.state = 'USA' if self.state == 'US' else 'CAN'
        with col4:
            self.pages = int(st.text_input('Pages:', 0))
