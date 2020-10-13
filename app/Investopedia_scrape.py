import os
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
from itertools import cycle
import numpy as np 
# from kdriver import RemoteDriverStartService

# class RemoteDriverStartService():
#     options = webdriver.ChromeOptions()
#     # Set user app data to a new directory
#     options.add_argument("user-data-dir=C:\\Users\\Donley\\App Data\\Google\\Chrome\\Application\\User Data\\Kit")
#     options.add_experimental_option("Proxy", "null")
#     options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
#     # Create a download path for external data sources as default: 
#     options.add_experimental_option("prefs", {
#       "download.default_directory": r"C:\\Users\\Donley\\Documents\\GA_TECH\\SUBMISSIONS\\PROJECT2-CHALLENGE\\data\\external",
#       "download.prompt_for_download": False,
#       "download.directory_upgrade": True,
#       "safebrowsing.enabled": True
#     }),
#     # Add those optional features to capabilities
#     caps = options.to_capabilities()  
#     def start_driver(self):
#         return webdriver.Remote(command_executor='http://127.0.0.1:4444', 
#                                 desired_capabilities=self.caps)


#  # Set class equal to new capabilities:
# DesiredCapabilities = RemoteDriverStartService() 

def invsto_scrape():
    # Connect to MongoDB
    client =  MongoClient("mongodb://localhost:27017")
    db = client['investopedia']

    # # Set class equal to new capabilities:
    # DesiredCapabilities = RemoteDriverStartService() 

    # Create variables for scraping: 
    investo = "https://www.investopedia.com/top-communications-stocks-4583180"
    # Download data to paths, csv's, json, etc: 
        # for external data sources
    external = "../data/external/"
        # for processed data sources with ID's
    processed = "../data/processed/"

    # Locate Driver in system
    current_path = os.getcwd()

    # save the .exe file under the same directory of the web-scrape python script.
    # driver = webdriver.Firefox(executable_path='C:\Python\geckodriver.exe')
    Path = os.path.join(current_path, "geckodriver.exe")

    # Initialize Chrome driver and start browser session controlled by automated test software under Kit profile.
    # caps = webdriver.DesiredCapabilities.CHROME.copy()
    # caps['acceptInsecureCerts'] = True
    # caps = webdriver.DesiredCapabilities.CHROME.copy()
    # caps['acceptInsecureCerts'] = True
    # driver = webdriver.Chrome(options=options, desired_capabilities=caps)
    driver = webdriver.Firefox(executable_path= "geckodriver.exe")

    ##Step 3: Find the IDs of the items we want to scrape for [5]
    # Start Grabbing Information from investopedia: 
    driver.maximize_window()
    
    driver.get(investo)

    # Find an ID on the page and wait before executing anything until found: 
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "main_1-0")))
    except TimeoutException:
        driver.quit()

    ##Step 5: The full code that runs the scraper and save the data to .csv files
    itable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    itables  = pd.read_html(itable)
    communications_bv = itables[0]
    communications_bv.columns = ["Communictaions Best Value", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    communications_bv
    # Locate column containing ticker symbols: 
    communications_bv_df = communications_bv.iloc[1:]
    # Only keep tick information within parentheses:
    communications_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in communications_bv_df["Communictaions Best Value"]]
    communications_bv_ticks

    communications_fg = itables[1]
    communications_fg.columns = ["Communications Fastest Growing", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    communications_fg_df = communications_fg.iloc[1:]
    communications_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in communications_fg_df["Communications Fastest Growing"]]
    communications_fg_ticks

    communications_mm = itables[2]
    communications_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    communications_mm_df = communications_mm.iloc[1:]
    communications_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in communications_mm_df["Communications Most Momentum"]]
    del communications_mm_ticks[-2:]
    communications_mm_ticks

    discretionary = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(3) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "journey-nav-header_1-0")))
    except TimeoutException:
        driver.quit()

    discretionary[0].click() 

    dtable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    dtables  = pd.read_html(dtable)
    discretionary_bv = dtables[0]
    discretionary_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    discretionary_bv
    # Locate column containing ticker symbols: 
    discretionary_bv_df = discretionary_bv.iloc[1:]
    # Only keep tick information within parentheses:
    discretionary_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in discretionary_bv_df["tick"]]
    discretionary_bv_ticks

    discretionary_fg = dtables[1]
    discretionary_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    discretionary_fg_df = discretionary_fg.iloc[1:]
    discretionary_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in discretionary_fg_df["stock"]]
    discretionary_fg_ticks

    discretionary_mm = itables[2]
    discretionary_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    discretionary_mm_df = discretionary_mm.iloc[1:]
    discretionary_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in discretionary_mm_df["Communications Most Momentum"]]
    del discretionary_mm_ticks[-2:]
    discretionary_mm_ticks

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "Top Consumer Staples Stocks")))
    except TimeoutException:
        driver.quit()

    staples = driver.find_elements(By.NAME, "Top Consumer Staples Stocks")
    staples[0].click()


    stable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    stables  = pd.read_html(stable)
    staples_bv = stables[0]
    staples_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    staples_bv
    # Locate column containing ticker symbols: 
    staples_bv_df = staples_bv.iloc[1:]
    # Only keep tick information within parentheses:
    staples_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in staples_bv_df["tick"]]
    staples_bv_ticks

    staples_fg = stables[1]
    staples_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    staples_fg_df = staples_fg.iloc[1:]
    staples_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in staples_fg_df["stock"]]
    staples_fg_ticks

    staples_mm = stables[2]
    staples_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    staples_mm_df = staples_mm.iloc[1:]
    staples_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in staples_mm_df["Communications Most Momentum"]]
    del staples_mm_ticks[-2:]
    staples_mm_ticks

    energy = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(5) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/div[1]/div/div[1]/ul/li[2]/ul/li[5]/a")))
    except TimeoutException:
        driver.quit()
    energy[0].click()
    

    etable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    etables  = pd.read_html(etable)
    energy_bv = etables[0]
    energy_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    energy_bv
    # Locate column containing ticker symbols: 
    energy_bv_df = energy_bv.iloc[1:]
    # Only keep tick information within parentheses:
    energy_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in energy_bv_df["tick"]]
    energy_bv_ticks

    energy_fg = etables[1]
    energy_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    energy_fg_df = energy_fg.iloc[1:]
    energy_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in energy_fg_df["stock"]]
    energy_fg_ticks

    energy_mm = etables[2]
    energy_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    energy_mm_df = energy_mm.iloc[1:]
    energy_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in energy_mm_df["Communications Most Momentum"]]
    del energy_mm_ticks[-2:]
    energy_mm_ticks

    financial = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(6) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "journey-nav-header_1-0")))
    except TimeoutException:
        driver.quit()
    financial[0].click()

    

    ftable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    ftables  = pd.read_html(ftable)
    financial_bv = ftables[0]
    financial_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    financial_bv
    # Locate column containing ticker symbols: 
    financial_bv_df = financial_bv.iloc[1:]
    # Only keep tick information within parentheses:
    financial_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in financial_bv_df["tick"]]
    financial_bv_ticks

    financial_fg = ftables[1]
    financial_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    financial_fg_df = financial_fg.iloc[1:]
    financial_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in financial_fg_df["stock"]]
    financial_fg_ticks

    financial_mm = itables[2]
    financial_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    financial_mm_df = financial_mm.iloc[1:]
    financial_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in financial_mm_df["Communications Most Momentum"]]
    del financial_mm_ticks[-2:]
    financial_mm_ticks

    healthcare = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(7) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "journey-nav-header_1-0")))
    except TimeoutException:
        driver.quit()
    healthcare[0].click()
    

    htable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    htables  = pd.read_html(htable)
    healthcare_bv = htables[0]
    healthcare_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    healthcare_bv
    # Locate column containing ticker symbols: 
    healthcare_bv_df = healthcare_bv.iloc[1:]
    # Only keep tick information within parentheses:
    healthcare_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in healthcare_bv_df["tick"]]
    healthcare_bv_ticks

    healthcare_fg = htables[1]
    healthcare_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    healthcare_fg_df = healthcare_fg.iloc[1:]
    healthcare_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in healthcare_fg_df["stock"]]
    healthcare_fg_ticks

    healthcare_mm = htables[2]
    healthcare_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    healthcare_mm_df = healthcare_mm.iloc[1:]
    healthcare_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in healthcare_mm_df["Communications Most Momentum"]]
    del healthcare_mm_ticks[-2:]
    healthcare_mm_ticks

    industrial = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(8) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "journey-nav-header_1-0")))
    except TimeoutException:
        driver.quit()
    industrial[0].click()
    

    intable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    intables  = pd.read_html(intable)
    industrial_bv = intables[0]
    industrial_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    industrial_bv
    # Locate column containing ticker symbols: 
    industrial_bv_df = industrial_bv.iloc[1:]
    # Only keep tick information within parentheses:
    industrial_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in industrial_bv_df["tick"]]
    industrial_bv_ticks

    industrial_fg = intables[1]
    industrial_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    industrial_fg_df = industrial_fg.iloc[1:]
    industrial_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in industrial_fg_df["stock"]]
    industrial_fg_ticks

    industrial_mm = intables[2]
    industrial_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    industrial_mm_df = industrial_mm.iloc[1:]
    industrial_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in industrial_mm_df["Communications Most Momentum"]]
    del industrial_mm_ticks[-2:]
    industrial_mm_ticks

    materials = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(9) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "journey-nav-header_1-0")))
    except TimeoutException:
        driver.quit()
    materials[0].click()

    

    motable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    motables  = pd.read_html(motable)
    materials_bv = motables[0]
    materials_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    materials_bv
    # Locate column containing ticker symbols: 
    materials_bv_df = discretionary_bv.iloc[1:]
    # Only keep tick information within parentheses:
    materials_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in materials_bv_df["tick"]]
    materials_bv_ticks

    materials_fg = motables[1]
    materials_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    materials_fg_df = materials_fg.iloc[1:]
    materials_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in materials_fg_df["stock"]]
    materials_fg_ticks

    materials_mm = motables[2]
    materials_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    materials_mm_df = materials_mm.iloc[1:]
    materials_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in materials_mm_df["Communications Most Momentum"]]
    del materials_mm_ticks[-2:]
    materials_mm_ticks

    real_estate = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(10) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "journey-nav-header_1-0")))
    except TimeoutException:
        driver.quit()
    real_estate[0].click()

    retable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    retables  = pd.read_html(retable)
    real_estate_bv = retables[0]
    real_estate_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    real_estate_bv
    # Locate column containing ticker symbols: 
    real_estate_bv_df = real_estate_bv.iloc[1:]
    # Only keep tick information within parentheses:
    real_estate_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in real_estate_bv_df["tick"]]
    real_estate_bv_ticks

    real_estate_fg = retables[1]
    real_estate_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    real_estate_fg_df = real_estate_fg.iloc[1:]
    real_estate_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in real_estate_fg_df["stock"]]
    real_estate_fg_ticks

    real_estate_mm = retables[2]
    real_estate_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    real_estate_mm_df = real_estate_mm.iloc[1:]
    real_estate_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in real_estate_mm_df["Communications Most Momentum"]]
    del real_estate_mm_ticks[-2:]
    real_estate_mm_ticks

    tech = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(11) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "journey-nav-header_1-0")))
    except TimeoutException:
        driver.quit()
    tech[0].click()

    tetable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    tetables  = pd.read_html(tetable)
    tech_bv = tetables[0]
    tech_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    tech_bv
    # Locate column containing ticker symbols: 
    tech_bv_df = tech_bv.iloc[1:]
    # Only keep tick information within parentheses:
    tech_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in tech_bv_df["tick"]]
    tech_bv_ticks

    tech_fg = tetables[1]
    tech_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    tech_fg_df = tech_fg.iloc[1:]
    tech_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in tech_fg_df["stock"]]
    tech_fg_ticks

    tech_mm = tetables[2]
    tech_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    tech_mm_df = discretionary_mm.iloc[1:]
    tech_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in tech_mm_df["Communications Most Momentum"]]
    del tech_mm_ticks[-2:]
    tech_mm_ticks

    utilities = driver.find_elements(By.CSS_SELECTOR, '#journey-nav__sublist_1-0 > li:nth-child(12) > a')
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "journey-nav-header_1-0")))
    except TimeoutException:
        driver.quit()
    utilities[0].click()

    utable = driver.find_element_by_id("main_1-0").get_attribute('outerHTML')
    utables  = pd.read_html(utable)
    utilities_bv = utables[0]
    utilities_bv.columns = ["tick", "Price", "Market Cap", "12-Month Trailing P/E Ratio"]
    utilities_bv
    # Locate column containing ticker symbols: 
    utilities_bv_df = utilities_bv.iloc[1:]
    # Only keep tick information within parentheses:
    utilities_bv_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in utilities_bv_df["tick"]]
    utilities_bv_ticks

    utilities_fg = utables[1]
    utilities_fg.columns = ["stock", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    utilities_fg_df = utilities_fg.iloc[1:]
    utilities_fg_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in utilities_fg_df["stock"]]
    utilities_fg_ticks

    utilities_mm = utables[2]
    utilities_mm.columns = ["Communications Most Momentum", "Price", "Market Cap", "12-Month Trailing Total Return (%)"]
    utilities_mm_df = utilities_mm.iloc[1:]
    utilities_mm_ticks = [tick[tick.find("(")+1:tick.find(")")] for tick in utilities_mm_df["Communications Most Momentum"]]
    del utilities_mm_ticks[-2:]
    utilities_mm_ticks

    lists=[communications_bv_ticks,communications_fg_ticks,communications_mm_ticks, discretionary_bv_ticks,discretionary_fg_ticks,discretionary_mm_ticks,staples_bv_ticks,staples_fg_ticks,staples_mm_ticks,energy_bv_ticks,energy_fg_ticks,energy_mm_ticks, financial_bv_ticks,financial_fg_ticks,financial_mm_ticks,healthcare_bv_ticks,healthcare_fg_ticks,healthcare_mm_ticks,industrial_bv_ticks,industrial_fg_ticks,industrial_mm_ticks,tech_bv_ticks,tech_fg_ticks,tech_mm_ticks,materials_bv_ticks,materials_fg_ticks,materials_mm_ticks,real_estate_bv_ticks,real_estate_fg_ticks,real_estate_mm_ticks,utilities_bv_ticks,utilities_fg_ticks,utilities_mm_ticks]
    stock_list = [item for sublist in lists for item in sublist]
    
    sector_collection = db['sector_stock_list']
    # Insert collection
    sector_collection.update_many({}, {"$set": {"Sector Stocks": stock_list}}, upsert = True)

    sp500_df=pd.read_csv('../data/external/sp500.csv')
    sector_l=sp500_df["S&P 500 & Sectors"].drop(sp500_df.index[0])
    sector_l = sector_l.reset_index().drop(columns='index')
    sector_list=sector_l["S&P 500 & Sectors"]
    type(sector_l)

    new_sector_df=pd.DataFrame()
    new_sector_df["ids"]=sector_l["S&P 500 & Sectors"]
    new_sector_df["labels"]=sector_l["S&P 500 & Sectors"]
    new_sector_df


    perf_df= pd.DataFrame(np.arange(1,34), columns=['ids'])
    seq = cycle(['Best Value','Fastest Growth','Most Momentum'])
    perf_df['labels'] = [next(seq) for count in range(perf_df.shape[0])]

    lists1=[]
    for i in range(len(sector_list)):
        
        
        seq1 = cycle([sector_list[i]])
        lists1.append([next(seq1) for count in range(3)])

    combined = [item for sublist in lists1 for item in sublist]
    perf_df['ids']=combined 
    perf_df['parents']=combined
    perf_df['ids']=perf_df['ids'] + '-' + perf_df['labels']
    perf_df

    stocks_df=pd.DataFrame()
    perf_l=perf_df["labels"]
    lists2=[]
    for i in range(len(perf_l)):
        
        
        seq = cycle([perf_l[i]])
        lists2.append([next(seq) for count in range(3)])

    combined = [item for sublist in lists2 for item in sublist]
    stocks_df['ids']=combined 
    stocks_df['labels']=stock_list

    lists3=[]
    for i in range(len(sector_list)):
        
        
        seq3 = cycle([sector_list[i]])
        lists3.append([next(seq3) for count in range(9)])
    combined2= [item for sublist in lists3 for item in sublist]
    stocks_df['parents']=combined2
    stocks_df['parents']=stocks_df['parents'] + '-'+ stocks_df['ids']
    stocks_df['ids']=stocks_df['ids'] + '-' + stocks_df['labels']
    stocks_df

    sector_perf_df=new_sector_df.append(perf_df)
    sunburst_df=sector_perf_df.append(stocks_df)
    sunburst_df

    sunburst_collection = db['sunburst']
    sunburst_df.reset_index(inplace=True)
    sunburst_dict = sunburst_df.to_dict("records")
    # Insert collection
    sunburst_collection.update_many({}, sunburst_dict, upsert= True)

    sunburst_df.to_csv('../data/external/sunburst_scrape.csv',index=False)
    driver.quit()

invsto_scrape()





