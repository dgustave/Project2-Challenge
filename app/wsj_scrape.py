import os
import html5lib
import pandas as pd
from selenium import webdriver                   
from selenium.webdriver.common.keys import Keys   
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import date, timedelta, datetime as dt  
from pymongo import MongoClient 
# from kdriver import RemoteDriverStartService

class RemoteDriverStartService():
    options = webdriver.ChromeOptions()
    # Set user app data to a new directory
    options.add_argument("user-data-dir=C:\\Users\\Donley\\App Data\\Google\\Chrome\\Application\\User Data\\Kit")
    options.add_experimental_option("Proxy", "null")
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # Create a download path for external data sources as default: 
    options.add_experimental_option("prefs", {
      "download.default_directory": r"C:\Users\Donley\Documents\GA_TECH\SUBMISSIONS\PROJECT2-CHALLENGE\data\external",
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    }),
    # Add those optional features to capabilities
    caps = options.to_capabilities()  
    def start_driver(self):
        return webdriver.Remote(command_executor='http://127.0.0.1:4444', 
                                desired_capabilities=self.caps)


# Connect to MongoDB
client =  MongoClient("mongodb://localhost:27017")
db = client['WallStreet']
 


def wsjScrape():
        # Set class equal to new capabilities:
    DesiredCapabilities = RemoteDriverStartService() 

    # Create variables for scraping: 
    wsj = "https://www.wsj.com/market-data/stocks?mod=nav_top_subsection"
    # Download data to paths, csv's, json, etc: 
        # for external data sources
    external = "../data/external/"
        # for processed data sources with ID's
    processed = "../data/processed/"

    # Locate Driver in system
    current_path = os.getcwd()

    # save the .exe file under the same directory of the web-scrape python script.
    Path = os.path.join(current_path, "chromedriver")

    # Initialize Chrome driver and start browser session controlled by automated test software under Kit profile.
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    # caps = webdriver.DesiredCapabilities.CHROME.copy()
    # caps['acceptInsecureCerts'] = True
    # driver = webdriver.Chrome(options=options, desired_capabilities=caps)
    driver = webdriver.Chrome(executable_path='chromedriver', desired_capabilities=caps)

    # Get the URL
    driver.get(wsj)
    driver.maximize_window()

    # Give it time to search for ID and allow the page time to load:
    timeout = 30
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "root")))
    except TimeoutException:
        driver.quit()
        
    # Read Html to generate S&P 500 table: 
    table = driver.find_element_by_id("root").get_attribute('outerHTML')
    tables  = pd.read_html(table)
    tables

    # Get table 5 and rename columns:
    sp500_sectors_df = tables[5]
    sp500_sectors_df.columns = ["S&P 500 & Sectors", "% Change"]
    sp500_sectors_df.reset_index(drop=True, inplace=True)
    sp500_sectors_df


    sp500_sectors_df.to_csv(external+"sp500.csv", index=False)

    # Read data from CSV and load into a dataframe object
    data = pd.read_csv(external+"sp500.csv")
 


    sp500_sectors_html = sp500_sectors_df.to_html()
    sp500_sectors_table = str(sp500_sectors_html)
    sp500_sectors_table

    wsj_collection = db['SP500_Change']
    # Insert collection
    wsj_collection.update_many({},{"S&P 500": sp500_sectors_table}, upsert= True)




    # The index of the links needed
    # 0	S&P 500
    # 1	Communication Services
    # 2	Consumer Discretionary
    # 3	Consumer Staples
    # 4	Energy
    # 5	Financials
    # 6	Health Care
    # 7	Industrials
    # 8	Information Technology
    # 9	Materials
    # 10	Real Estate
    # 11	Utilities
    sp500_links = [(driver.find_elements_by_partial_link_text(sector)) for sector in sp500_sectors_df["S&P 500 & Sectors"]]

    # variable Links to individual sector pages: 
    sp500_link = [links.get_attribute("href") for links in sp500_links[0]]
    communication_link = [links.get_attribute("href") for links in sp500_links[1]]
    discretionary_link = [links.get_attribute("href") for links in sp500_links[2]]
    staples_link = [links.get_attribute("href") for links in sp500_links[3]]
    energy_link = [links.get_attribute("href") for links in sp500_links[4]]
    financials_link = [links.get_attribute("href") for links in sp500_links[5]]
    health_link = [links.get_attribute("href") for links in sp500_links[6]]
    industrials_link = [links.get_attribute("href") for links in sp500_links[7]]
    information_Technology_link = [links.get_attribute("href") for links in sp500_links[8]]
    materials_link = [links.get_attribute("href") for links in sp500_links[9]]
    real_estate_link = [links.get_attribute("href") for links in sp500_links[10]]
    utilities_link = [links.get_attribute("href") for links in sp500_links[11]]

    # list of links for sectors: 
    sector_links = [sp500_link, communication_link, discretionary_link, staples_link, energy_link, financials_link, health_link, industrials_link, information_Technology_link, materials_link, real_estate_link, utilities_link]
    sector_links

    wsjlink_collection = db['SP500_Links']
    wsjlink_collection.update_many({},{"Sector Links", sector_links}, upsert= True)

    # Get to Historical Data:
    driver.get(sp500_link[2])

    historical_data = driver.find_elements(By.CSS_SELECTOR, 'a.moreLink')
    historical_data

    # Get to historical data download page: 
    historical_data[1].click()

    # Todays date
    currentDate = date.today()
    today = currentDate.strftime('%m/%d/%Y')
    today

    # date 1 week ago from today
    five_days = currentDate - timedelta(days=365)
    five = five_days.strftime('%m/%d/%Y')
    five

    # Fill out Date to
    text_area2 = driver.find_element(By.CSS_SELECTOR, "#selectDateTo")
    text_area2.send_keys(Keys.CONTROL, "a")  # or Keys.COMMAND on Mac
    text_area2.send_keys(today)

    # Generate the data
    generate_data = driver.find_element(By.ID, "datPickerButton")

    generate_data.click()

    # Download as csv  
    download_sheet = driver.find_element(By.ID, "dl_spreadsheet")

    download_sheet.click()

    driver.quit()


wsjScrape()

