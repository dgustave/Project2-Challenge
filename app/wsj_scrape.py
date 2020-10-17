#!/usr/bin/env python
# coding: utf-8

# # Step 1: Install Python packages

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
from pandas_profiling import ProfileReport





# Connect to MongoDB
client =  MongoClient("mongodb://localhost:27017")
db = client['WallStreet']



class RemoteDriverStartService():
    options = webdriver.ChromeOptions()
    # Set user app data to a new directory
    options.add_argument("user-data-dir=C:\\Users\\Donley\\App Data\\Google\\Chrome\\Application\\User Data\\Kit")
    options.add_experimental_option("Proxy", "null")
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # Create a download path for external data sources as default: 
    options.add_experimental_option("prefs", {
      "download.default_directory": r"C:\Users\Donley\Documents\GA_TECH\SUBMISSIONS\PROJECT2-CHALLENGE\data\processed",
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    }),
    # Add those optional features to capabilities
    caps = options.to_capabilities()  
    def start_driver(self):
        return webdriver.Remote(command_executor='http://127.0.0.1:4444', 
                                desired_capabilities=self.caps)
# Set class equal to new capabilities:
DesiredCapabilities = RemoteDriverStartService()  


def wsjScrape():
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


    # # Step 3: Find the IDs of the items we want to scrape for


    # Give it time to search for ID and allow the page time to load:
    timeout = 30
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "root")))
    except TimeoutException:
        driver.quit()
        


    # # Step 4: Techniques to make more human-like web-scrapers


    # If the website detects us as a web-scraper, it will cut our connection so we cannot pull more data and have to re-start our scraper. This largely impacts the efficiency of the scraper and involves a lot of manual interference. There are a few techniques we can use to make the scraper more human-like:
    # (1) Randomize the sleep time
    # This can be easily implemented as below wherever needed:
    #sleep for sometime between 5 and 8 seconds
    # time.sleep(random.uniform(5,8))
    # (2) Randomize the user agent for the web browser
    # This is also easy and can be added to the browser options as below:
    # ua = UserAgent()
    # userAgent = ua.random
    # Firefox_options = webdriver.FirefoxOptions()
    # Firefox_options.add_argument(f’user-agent={userAgent}’)
    # browser = webdriver.Firefox(executable_path = DRIVER_BIN, options=Firefox_options)
    # (3) Use dynamic proxy/IP
    # This requires more work than the above two. Usually free proxies are not stable and most of them don’t respond to requests, so we need to first a free proxy that responds to our requests. This website (also named as “url” in the script below) provides a lot of free proxies which we scrape down for our use. We will use Python BeautifulSoup package to scrape a list of proxies, and use Python requests package to test whether the proxy responds to our requests to the link.
    # def get_proxy(link):
    #     url = "https://www.sslproxies.org/"
    #     r = requests.get(url)
    #     soup = BeautifulSoup(r.content, 'html5lib')
    #     proxies_list = list(map(lambda x: x[0]+':'+x[1], list(zip(map(lambda x: x.text, soup.findAll('td')[::8]), map(lambda x: x.text, soup.findAll('td')[1::8])))))
    #     while 1:
    #         try:
    #             selected_ip = choice(proxies_list)
    #             proxy = {'https': selected_ip, 'http': selected_ip}
    #             headers = {'User-Agent': ua.random}
    #             print('Using proxy:{}'.format(proxy))
    #             r = requests.request('get', link, proxies=proxy, headers=headers, timeout=5)
    #             break
    #         except:
    #             pass
            
    #     return proxy
    # We then add the working proxy to the browser option, similar to how we added the fake user agent:
    # link = "https://www.expedia.com"
    # proxy = get_proxy(link)
    # Firefox_options.add_argument('--proxy-server=%s' % proxy)
    # browser = webdriver.Firefox(executable_path = DRIVER_BIN, options=Firefox_options)


    # # Step 5: The full code that runs the scraper and save the data to .csv files

    # Read Html to generate S&P 500 table: 
    table = driver.find_element_by_id("root").get_attribute('outerHTML')
    tables  = pd.read_html(table)
    tables



    # Generate List of tables on page:
    wsj_tables =[df for df in tables]


    # Get table 5 and rename columns:
    sp500_sectors_df = wsj_tables[5]
    sp500_sectors_df.columns = ["S&P 500 & Sectors", "% Change"]
    sp500_sectors_df.reset_index(drop=True, inplace=True)
    sp500_sectors_df



    sp500_sectors_df.to_csv(external+"sp500.csv", index=False) 



    sp500_sectors_html = sp500_sectors_df.to_html()
    sp500_sectors_table = str(sp500_sectors_html)
    sp500_sectors_table


    wsj_collection = db['SP500_Change']
    # Insert collection
    wsj_collection.update_many({},{"$set": {"S&P 500":sp500_sectors_table}})


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
    sector_dict = {"Top Sector Links": sector_links}



    wsjlink_collection = db['SP500_Links']
    wsjlink_collection.update_many({},{"$set": sector_dict} )



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



    # Fill out Date From Form
    text_area = driver.find_element(By.CSS_SELECTOR, "#selectDateFrom")
    text_area.send_keys(Keys.CONTROL, "a")  # or Keys.COMMAND on Mac
    text_area.send_keys(five)


    # Fill out Date to
    text_area2 = driver.find_element(By.CSS_SELECTOR, "#selectDateTo")
    text_area2.send_keys(Keys.CONTROL, "a")  # or Keys.COMMAND on Mac
    text_area2.send_keys(today)

    
    sp_df = pd.read_csv('../data/processed/HistoricalPrices.csv')



    sp_df.to_html()
    sp_df_table = str(sp_df)
    sp_df_table



    wsj_collection = db['S&P 500: Historical Prices']
    wsj_collection.update_many({},{"$set": {"Historical Prices":sp_df_table}})




    prof = ProfileReport(sp_df)


    prof.to_file(output_file='../app/templates/profile.html')




    # Generate the data
    generate_data = driver.find_element(By.ID, "datPickerButton")
    # try:
    #     WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "datPickerButton")))
    # except TimeoutException:
    #     driver.quit()


    generate_data.click()



    # Download as csv  
    download_sheet = driver.find_element(By.ID, "dl_spreadsheet")
    # try:
    #     WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "dl_spreadsheet")))
    # except TimeoutException:
    #     driver.quit()



    download_sheet.click()




    driver.quit()

wsjScrape()







