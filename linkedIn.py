from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import streamlit as st
import pandas as pd


class LinkedIn():
    def __init__(self):
        st.header("Scrape LinkedIn")
        self.main()

    def start_driver(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.minimize_window()
        self.driver.implicitly_wait(10)

    def Find_Elements(self, company):
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf')
        for element in elements:
            anchor = element.find_element(By.TAG_NAME, 'a')
            link = anchor.get_attribute('href')
            if 'linkedin.com/in/' in link:
                text = anchor.find_element(By.TAG_NAME, 'h3').text
                lst = text.split('-')
                try:
                    name = lst[0].strip()
                    designation = lst[1].strip()

                    if link not in self.dictionary['LinkedIn']:
                        self.dictionary['LinkedIn'].append(link)
                        self.dictionary['Designation'].append(designation)
                        self.dictionary['Name'].append(name)
                        self.dictionary['Company Name'].append(company)
                except IndexError:
                    pass

    def main(self):
        self.paused = False
        self.stop_requested = False

        st.write('Scrape the LinkedIn Info. Which Option do you want to choose:')
        options = ('Scrape LinkedIn from File', 'Scrape LinkedIn from Keyword')

        self.designation_options = ['Founder', 'Director', 'Owner', 'Principal', 'Project Manager']

        selected_option = st.radio('Select Option:', options)
        if selected_option == options[0]:
            file = st.file_uploader('Upload File', type=['csv', 'xls'])
            if file:
                if file.type == 'csv':
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

                company_name = st.text_input('Enter the Columns containing Company Name:').strip()
                if company_name:
                    self.company_names = df[company_name]
                    if self.Scrape():
                        self.save_file()

        elif selected_option == options[1]:
            self.company_names = [st.text_input('Enter the Keyword to Search')]
            if self.Scrape():
                self.save_file()

    def Scrape(self):
        self.new_designation = st.text_input('Add New Designation:')
        selected_designations = st.multiselect('Select Designations:', self.designation_options + [self.new_designation])
        self.dictionary = {'Company Name': [], 'Designation': [], 'Name': [], 'LinkedIn': []}
        INSIDE = False

        scrape = st.button('Scrape LinkedIn')
        if scrape:
            progress_bar = st.progress(0)
            INSIDE = True
            for company in self.company_names:
                self.start_driver()
                for idx, designation in enumerate(selected_designations):
                    link = f"https://www.google.com/search?q={company.replace(' ', '+')}+{designation.replace(' ', '+')}"
                    self.driver.get(link)
                    self.Find_Elements(company)
                        
                progress_bar.empty()
                progress_bar.progress((idx) / len(self.company_names))
                self.driver.quit()
        
        return INSIDE

    def save_file(self):
        df = pd.DataFrame(self.dictionary)
        st.write(df)