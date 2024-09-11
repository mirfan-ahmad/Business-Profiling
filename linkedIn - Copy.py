import os
import time
import random
import datetime
import pandas as pd
import streamlit as st
from business_profiling import WebScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class LinkedIn():
    def __init__(self, RUN_SELF=False, FILE_PATH=None, selected_designation=None):
        st.header("Scrape LinkedIn")
        self.Scraped = 0
        self.GUI(RUN_SELF=RUN_SELF, FILE_PATH=FILE_PATH, selected_designation=selected_designation)


    def start_driver(self):
        option = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        except:
            self.driver = webdriver.Chrome(service=Service("chromedriver/chromedriver.exe"), options=option)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)


    # Private Wrapper/Helper Method
    def __wrapper_find_element(self, company, idx, des, link, lst, description=None):
        try:
            try:    
                name = lst[0].strip()
                designation = lst[1].strip()
            except:
                return
            
            # write data into file
            def write_into_file(file):
                row = ''
                for col in self.df.columns:
                    try:
                        self.dictionary[col].append(self.df.at[idx, col])
                        row += f"{str(self.df.at[idx, col]).replace(',', ' ')},"
                    except:
                        try:
                            file.write(f"{company},{str(des).replace(',', ' ').capitalize()},{str(name).replace(',', ' ').capitalize()},{link.split('#')[0].replace(',', ' ')},{description.find_element(By.TAG_NAME, 'div').text.replace(',', ' ')}\n")
                        except:
                            file.write(f"{company},{str(des).replace(',', ' ').capitalize()},{str(name).replace(',', ' ').capitalize()},{link.split('#')[0].replace(',', ' ')},{description}\n")
                        return
                
                file.write(f"{row[:len(row)-1]},{str(des).replace(',', ' ').capitalize()},{str(name).replace(',', ' ').capitalize()},{link.split('#')[0].replace(',', ' ')},{description.find_element(By.TAG_NAME, 'div').text.replace(',', ' ')}\n")
            
            # print(company.replace(' ', '').capitalize(), lst[-1].replace(',', '').replace(' ', '').capitalize())
            # print(company.replace(' ', '').capitalize() in lst[-1].replace(',', '').replace(' ', '').capitalize())
            
            # print(company.capitalize().replace(' ', ''), name.replace(',', '').replace(' ', '').capitalize())
            # print(company.capitalize().replace(' ', '') in name.replace(',', '').replace(' ', '').capitalize())
            
            # print(company.capitalize().replace(' ', ''), designation.replace(',', ' ').replace(' ', '').capitalize())
            # print(company.capitalize().replace(' ', '') in designation.replace(',', ' ').replace(' ', '').capitalize())
            
            # print(company.replace(' ', '').replace('and', '&').capitalize(), lst[-1].replace(',', '').replace(' ', '').capitalize())
            # print(company.replace(' ', '').replace('and', '&').capitalize() in lst[-1].replace(',', '').replace(' ', '').capitalize())
            
            # print(company.capitalize().replace(' ', '').replace('and', '&'), name.replace(',', '').replace(' ', '').capitalize())
            # print(company.capitalize().replace(' ', '').replace('and', '&') in name.replace(',', '').replace(' ', '').capitalize())
            
            # print(company.capitalize().replace(' ', '').replace('and', '&'), designation.replace(',', ' ').replace(' ', '').capitalize())
            # print(company.capitalize().replace(' ', '').replace('and', '&') in designation.replace(',', ' ').replace(' ', '').capitalize())
            
            # print(lst[-1].replace(',', '').replace(' ', '').capitalize(), company.replace(' ', '').capitalize())
            # print(lst[-1].replace(',', '').replace(' ', '').capitalize() in company.replace(' ', '').capitalize())
            
            # print(name.replace(',', '').replace(' ', '').capitalize(), company.capitalize().replace(' ', ''))
            # print(name.replace(',', '').replace(' ', '').capitalize() in company.capitalize().replace(' ', ''))
            
            # print(lst[-1].replace(',', '').replace(' ', '').capitalize().split('.')[0], company.replace(' ', '').replace('and', '&').capitalize())
            # print(lst[-1].replace(',', '').replace(' ', '').capitalize().split('.')[0] in company.replace(' ', '').replace('and', '&').capitalize())
            
            # print(name.replace(',', '').replace(' ', '').capitalize().split('.')[0], company.capitalize().replace('and', '&').replace(' ', ''))
            # print(name.replace(',', '').replace(' ', '').capitalize().split('.')[0] in company.capitalize().replace('and', '&').replace(' ', ''))
            
            # open the file with the dictionary
            if (link.split('#')[0].replace(',', ' ')) not in self.dictionary['LinkedIn'] and 'post' not in link:

                if company.replace(' ', '').capitalize() in lst[-1].replace(',', '').replace(' ', '').capitalize() or\
                        company.capitalize().replace(' ', '') in name.replace(',', '').replace(' ', '').capitalize() or\
                            company.capitalize().replace(' ', '') in designation.replace(',', ' ').replace(' ', '').capitalize() or\
                                company.replace(' ', '').replace('and', '&').capitalize() in lst[-1].replace(',', '').replace(' ', '').capitalize() or\
                                    company.capitalize().replace(' ', '').replace('and', '&') in name.replace(',', '').replace(' ', '').capitalize() or\
                                        company.capitalize().replace(' ', '').replace('and', '&') in designation.replace(',', ' ').replace(' ', '').capitalize() or\
                                            lst[-1].replace(',', '').replace(' ', '').capitalize() in company.replace(' ', '').capitalize() or\
                                                name.replace(',', '').replace(' ', '').capitalize() in company.capitalize().replace(' ', '') or\
                                                    lst[-1].replace(',', '').replace(' ', '').capitalize().split('.')[0] in company.replace(' ', '').replace('and', '&').capitalize() or\
                                                        name.replace(',', '').replace(' ', '').capitalize().split('.')[0] in company.capitalize().replace('and', '&').replace(' ', ''):
                    
                    # print(des.upper().replace(' ', ''), designation.replace(',', ' ').replace(' ', '').upper())
                    # print(des.upper().replace(' ', ''), name.replace(',', ' ').replace(' ', '').upper())
                    
                    if des.upper().replace(' ', '') in designation.replace(',', ' ').replace(' ', '').upper() or\
                        des.upper().replace(' ', '') in name.replace(',', ' ').replace(' ', '').upper():

                        with open(os.path.join('Scraped_Files', f'{self.query}_{self.date}.csv'), 'a') as file:
                            write_into_file(file)
                        
                        print(f'Found linkedIn Info of {name} working in {company} as {designation}')
                        self.dictionary['Company Name'].append(company)
                        self.dictionary['LinkedIn'].append(str(link.split('#')[0]).replace(',', ' '))
                        self.dictionary['Designation'].append(str(des).replace(',', ' '))
                        self.dictionary['Name'].append(str(name).replace(',', ' '))
                        
                        try:
                            self.dictionary['Description'].append(description.find_element(By.CSS_SELECTOR, 'div.LEwnzc').text.replace(',', ' '))
                        except:
                            self.dictionary['Description'].append('Not Found')
                        
                        self.Scraped += 1
                        self.container.empty()
                        self.container.write(f'Scraped Leads: {self.Scraped}')
                        file.close()
        
        except NoSuchElementException as e:
            print('Error from wrapper:', e)
            raise e
        
        except IndexError as e:
            print('Index Error', e)
            pass


    def Find_Elements(self, company, idx, des, base=0):
        try:
            self.FLAG = False
            try:
                elements = [self.driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/block-component/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/span/a')]
            except:
                self.FLAG = True
                elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.kb0PBd:nth-child(1)')
                descriptions = self.driver.find_elements(By.CSS_SELECTOR, 'div.kb0PBd:nth-child(2)')
                
            if len(elements) == 0:
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="recaptcha"]')
                    print('Got Recaptcha, Solving..')
                    self.__SolveCaptcha()
                except:
                    pass
                
            for idxx, element in enumerate(elements):
                if self.FLAG:
                    description = descriptions[idxx]
                    anchor = element.find_element(By.CSS_SELECTOR, 'div > div > span > a')
                else:
                    description = None
                    anchor = element
                link = anchor.get_attribute('href')
                
                if 'linkedin.com/in/' in link:
                    text = anchor.find_element(By.TAG_NAME, 'h3').text
                    lst = text.split('-')
                    self.__wrapper_find_element(company, idx, des, link, lst, description=description)

        except NoSuchElementException as e:
            print('Got captcha')
            pass
            
        except Exception as e:
            print('Error: %s' % e)
            if base == 2:
                return
            self.driver.refresh()
        

    def Scrape(self, RUN_SELF=False):
        print('In Scrape')
        if RUN_SELF:
            self.scrape = True
        if self.scrape:
            print('In Scrape.')
            progress_bar = st.progress(0)
            self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.query = 'LinkedIn'

            if not os.path.exists('Scraped_Files'):
                os.makedirs('Scraped_Files')
            self.start_driver()
            
            # Write the header into file
            def write_into_file(file):
                columns = ','.join([col for col in self.df.columns])
                file.write(columns+',Designation,Name,LinkedIn,Descriptions\n')

            # Open the file    
            with open(os.path.join('Scraped_Files', f'{self.query}_{self.date}.csv'), 'w') as file:
                write_into_file(file)
        
            # initiate the scraping process
            increment = 1
            for idx, company in enumerate(self.company_names):
                for idxx, designation in enumerate(self.selected_designations):
                    link = f"https://www.google.com/search?q={company.replace(' ', '+').replace('&', '%26')}+in+{str(self.locations[idx]).replace(' ', '+')}+-+{designation.replace(' ', '+')}+linkedIn+accounts"
                    self.driver.get(link)
                    
                    time.sleep(random.random() * random.randint(1, 3))
                    self.Find_Elements(company, idx, designation.capitalize())
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                    progress_bar.empty()
                    progress_bar.progress(increment / (len(self.company_names)*len(self.selected_designations)))
                    increment += 1
            st.write(f'Scraped Leads: {self.Scraped}')
        return True


    def GUI(self, RUN_SELF=False, FILE_PATH=None, selected_designation=None):
        # Temporary Solution for Hybrid App
        if RUN_SELF:
            self.selected_designations = selected_designation
            try:
                self.df = pd.read_csv(FILE_PATH)
            except:
                self.df = pd.read_excel(FILE_PATH)
            self.__dictionary()
                
            self.company_names = self.df['Company Name']
            self.locations = self.df['City']
            if self.Scrape(RUN_SELF=RUN_SELF):       # Scrape the LinkedIn Info from the file
                self.__save_file()
                try:
                    st.write(self.dataframe)
                except:
                    pass
                return True
                
        st.write('Scrape the LinkedIn Info. Which Option do you want to choose:')
        options = ('Scrape LinkedIn Info from File', 'Scrape LinkedIn Info from Keyword')

        selected_option = st.radio('Select Option:', options)
        if selected_option == options[0]:
            file = st.file_uploader('Upload File', type=['csv', 'xls'])
            if file:
                content_type = file.type
                if 'csv' in content_type:
                    self.df = pd.read_csv(file)
                else:
                    try:
                        self.df = pd.read_excel(file)
                    except:
                        st.write('Only CSV file type is supported.')
                        return False

                company_name = st.text_input('Enter the Columns containing Company Name:').strip()
                location = st.text_input('Enter the Location, where to Search').strip()
                self.company_names = self.df[company_name]
                self.locations = self.df[location]

                self.__designation()
                self.selected_designations = st.multiselect('Select Designations:', self.designation_options)
                self.__dictionary()
                self.scrape = st.button('Scrape LinkedIn')
                self.container = st.empty()
                
                if self.scrape:
                    if self.Scrape():       # Scrape the LinkedIn Info from the file
                        self.__save_file()
                        st.write(self.dataframe)
                        return True

        elif selected_option == options[1]:
            self.company_names = [st.text_input('Enter the Keyword to Search')]
            self.locations = [st.text_input('Enter the Location, where to Search')]
            self.df = pd.DataFrame(columns=['Company Name'])
            
            self.__designation()
            self.selected_designations = st.multiselect('Select Designations:', self.designation_options)
            self.__dictionary()
            self.scrape = st.button('Scrape LinkedIn')
            
            if self.scrape:
                self.container = st.empty()
                if self.Scrape():
                    self.__save_file()
                    try:
                        st.write(self.dataframe)
                    except:
                        pass
                    return True


    # Private Methods
    def __dictionary(self):
        self.dictionary = {}
        for column in self.df.columns:
            self.dictionary[column] = []
        
        self.dictionary['Designation'] = []
        self.dictionary['Name'] = []
        self.dictionary['LinkedIn'] = []
        self.dictionary['Description'] = []
        
    
    def __save_file(self):
        try:
            print(self.dictionary)
            self.dataframe = pd.DataFrame(self.dictionary)
        except ValueError:
            st.write('DataFrame has been saved into the file.')


    def __designation(self):
        with open('Designations.txt', 'a') as file:
            new = st.text_input('Add New Designation:')
            if st.button('Add New Designation'):
                file.write(f"\n{new}")
        
        with open('Designations.txt', 'r') as file:
            self.designation_options = file.read().split('\n')
    
    
    def __SolveCaptcha(self, link):
        sitekey = self.driver.find_element(By.XPATH, '//*[@id="recaptcha"]').get_attribute('outerHTML')
        print(sitekey)
        sitekey_clean = sitekey.split('"data-callback')[0].split('data-sitekey="')[1]
        print(sitekey_clean)
        
        self.API_KEY = "b4cd1819720f4dc426596bc9d1e8ad4b"
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(self.API_KEY)
        solver.set_website_url(link)
        solver.set_website_key(sitekey_clean)
        
        g_response = solver.solve_and_return_solution()
        if g_response!= 0:
            print("g_response"+g_response)
        else:
            print("task finished with error"+solver.error_code)

        self.driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

        self.driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", g_response)
        self.driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
        
        self.driver.find_element(By.XPATH, '//*[@id="recaptcha-verify-button"]').click()
        time.sleep(random.random() * random.randint(1, 3))
