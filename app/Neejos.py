from bs4 import BeautifulSoup
import requests

r = requests.get("https://api.scrapingdog.com/scrape?api_key=<your-api-key>&url=https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch").text

soup = BeautifulSoup(r,’html.parser’)

alldata = soup.find_all(“tbody”)

try:
 table1 = alldata[0].find_all(“tr”)
except:
 table1=None
try:
 table2 = alldata[1].find_all(“tr”)
except:
 table2 = None

l={}
u=list()

for i in range(0,len(table2)):
 try:
   table2_td = table2[i].find_all(“td”)
 except:
   table2_td = None
 l[table2_td[0].text] = table2_td[1].text
 u.append(l)
 l={}