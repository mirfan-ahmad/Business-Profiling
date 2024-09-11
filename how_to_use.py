import streamlit as st


def How_to_Use():
    st.title('How to Setup')

    st.write("To set up the application on a new machine, ensure that the machine meets the following prerequisites:")
    st.write("1. Python should be installed. You can download Python from [here](https://www.python.org/downloads/).")
    st.write("2. Download ChromeDriver. Update Google Chrome to the latest version, then find the current version of the browser and download Chrome WebDriver from [here](https://googlechromelabs.github.io/chrome-for-testing/).")

    st.write("Now, let's proceed with setting up the application:")
    st.write("1. Unzip the downloaded Chrome WebDriver and place the folder along with the application files.")
    st.write("2. Make sure you have the folder name and binary file inside folder with 'chromedriver'")
    st.write("3. Open the Terminal/Bash/Command Prompt in the application folder from address bar.")
    st.write("4. Run the following command and create virtual environment:")
    st.code("python3 -m venv env")
    st.write("5. Activate Virtual Environment via following command:")
    st.code("env\\Scripts\\activate")
    st.write("6. Download all requirements / dependencies:")
    st.code("pip3 install -r requirements.txt")
    st.write("7. After successfully installing all the dependencies, run the following command:")
    st.code("streamlit run APP.py")
    st.write("Once you have successfully set up the application for the first time, you only need to follow Step (5&7) for subsequent usage.")

    st.title('How to Use')

    st.write("This tool consists of Four pages:")

    st.header('1. Lead Generation:')
    st.write("This page is the concatenated version of the Business Listing and LinkedIn pages.")
    
    st.header('2. Business Listing:')
    st.write("This page contains a text input field where users can enter their query.")
    st.write("- Click the 'Scrape' button.")
    st.write("- The scraper will start searching for business profiles and scrape relevant information.")
    st.write("- The DataFrame will be loaded on the UI. Click the download icon to download the CSV file.")

    st.header('3. LinkedIn:')
    st.write("There are two options available:")

    st.subheader('Scrape LinkedIn Info from File (Option 1):')
    st.write("If you have a file containing company names generated from the Business Listing page.")
    st.write("  - Browse the file.")
    st.write("  - Enter the column name containing company names in the input cell.")
    st.write("  - Enter new designations if needed.")
    st.write("  - Select the designations from the dropdown menu.")
    st.write("  - Click the 'Scrape LinkedIn' button to start scraping. The progress will be shown via a progress bar.")
    st.write("  - The scraper will search for relevant LinkedIn information.")
    st.write("  - The DataFrame will be loaded on the UI. Click the download icon to download the CSV file.")

    st.subheader('Scrape LinkedIn Info from Keyword (Option 2):')
    st.write("If you want to search LinkedIn info against a specific company name.")
    st.write("  - Enter the company name in the input cell.")
    st.write("  - Enter new designations if needed.")
    st.write("  - Select the designations from the dropdown menu.")
    st.write("  - Click the 'Scrape LinkedIn' button to start scraping. The progress will be shown via a progress bar.")
    st.write("  - The scraper will search for relevant LinkedIn information.")
    st.write("  - The DataFrame will be loaded on the UI. Click the download icon to download the CSV file.")
    
    st.header('4. Better Business Bureau:')
    st.write("This page contains 3 text input field and 1 dropdown.")
    st.write("  - Enter the company name in the first input cell.")
    st.write("  - Enter the city in the second input cell.")
    st.write("  - Select the state from the dropdown menu.")
    st.write("  - Enter the number of pages in the third input cell.")
    st.write("  - Click the 'Scrape' button to start scraping. The progress will be shown via a progress bar.")