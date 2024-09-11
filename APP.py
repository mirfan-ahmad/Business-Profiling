from selenium.common.exceptions import WebDriverException
from linkedIn import LinkedIn
from business_profiling import WebScraper
from bbb import BBB
from how_to_use import How_to_Use
import streamlit as st


def SideBar():
    st.sidebar.markdown('---')
    st.sidebar.subheader('Contact Developer')
    st.sidebar.write('For questions or feedback, please contact:')
    st.sidebar.write('Email: irfanahmad2959@gmail.com')
    st.sidebar.write('Phone: [Contact](tel:+923177102959)')

    st.sidebar.subheader('Feedback')
    st.sidebar.write('Have feedback or found a bug?')
    st.sidebar.write('[Provide Feedback](irfanahmad2959@gmail.com)')

    st.sidebar.subheader('Version Information')
    st.sidebar.write('Version: 1.2.0')
    st.sidebar.write('Last Updated: May 01, 2024')

    st.sidebar.subheader('Copyright')
    st.sidebar.write('© 2024 DevNest Solutions. All rights reserved.')
    
def render_page(page):
    if page == 'Business Listing':
        business_profiling = WebScraper()
        if business_profiling.button:
            try:
                business_profiling.scrape_data()
                st.write(business_profiling.dataframe)
            except WebDriverException:
                st.write('Internet connection is not stable, please try again.')
                st.stop()
            except Exception as e:
                try:
                    st.write(business_profiling.dataframe)
                except:
                    st.write('Scrapped Data is saved in the CSV file.')
        else:
            pass

    elif page == 'Lead Generation':
        try:
            st.title('Lead Generation')
            business_profiling = WebScraper(RUN_SELF=True)
            designation_options = designation()
            selected_designations = st.multiselect('Select Designations:', designation_options)
            if st.button('Scrape'):
                business_profiling.scrape_data()
                business_profiling.driver.quit()
                st.write(business_profiling.dataframe)
                linkedin = LinkedIn(RUN_SELF=True, FILE_PATH=business_profiling.file_name, selected_designation=selected_designations)
                linkedin.driver.quit()
                    
        except WebDriverException:
            st.write('Internet connection is not stable, please try again.')
            st.stop()
        
    elif page == 'LinkedIn':
        try:
            linkedin = LinkedIn()
        except WebDriverException:
            st.stop()
        except Exception as e:
            print(e)
            st.empty()
            st.stop()
    elif page == 'Better Business Bureau (BBB)':
        BBB()
        
    elif page == 'Guidelines':
        How_to_Use()


def designation():
    with open('Designations.txt', 'a') as file:
        new = st.text_input('Add New Designation:')
        if st.button('Add New Designation'):
            file.write(f"\n{new}")
    
    with open('Designations.txt', 'r') as file:
        return file.read().split('\n')


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    col1, col2, col3, col4 = st.sidebar.columns(4, gap="small")
    col1.image('logo.jpeg', width=70)
    col2.title('Scalease')

    pages = ["Lead Generation", "Business Listing", "LinkedIn", "Better Business Bureau (BBB)", "Guidelines"]
    st.sidebar.markdown('---')
    selected_page = st.sidebar.selectbox("Select a Page", pages)

    render_page(selected_page)
    SideBar()
