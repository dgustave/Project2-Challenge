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
