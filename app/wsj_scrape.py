import driver



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
sp500_sectors_df = wsj_tables[5]
sp500_sectors_df.columns = ["S&P 500 & Sectors", "% Change"]
sp500_sectors_df.reset_index(drop=True, inplace=True)
sp500_sectors_df

sp500_sectors_df.to_csv(external+"sp500.csv", index=False) 

sp500_sectors_html = sp500_sectors_df.to_html()
sp500_sectors_table = str(sp500_sectors_html)
sp500_sectors_table



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
