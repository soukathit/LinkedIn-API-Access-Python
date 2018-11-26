from selenium import webdriver

driver = webdriver.Firefox(executable_path="/root/LinkedIn_API_Access/bin/geckodriver")

driver.get('https://www.google.com')

driver.close()
