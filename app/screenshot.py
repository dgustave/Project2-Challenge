from selenium import webdriver

DRIVER = 'chromedriver'
driver = webdriver.Chrome(DRIVER)
driver.get('https://www.spotify.com')
screenshot = driver.save_screenshot('my_screenshot.png')
driver.quit()