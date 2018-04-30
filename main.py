from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import getpass

LOGIN_PAGE = 'https://streaming.settrade.com/realtime/streaming-login/login.jsp?noPopUp=true'

uid = input("User ID: ")
pwd = getpass.getpass("Password: ")

# Initialize driver
driver = webdriver.Firefox()

# LOGIN
driver.get(LOGIN_PAGE)
loginForm      = driver.find_element_by_xpath("//form[@id='loginFrm']")
loginForm.find_element_by_xpath("//span[@class='ng-arrow']").click()
loginForm.find_element_by_xpath("//input[@autocomplete='off']").send_keys('CIMB' + Keys.RETURN)
idField        = loginForm.find_element_by_name('txtLogin').send_keys(uid)
passwdField    = loginForm.find_element_by_name('txtPassword').send_keys(pwd)
button         = loginForm.find_element_by_id('submitBtn').click()
print("Login Successfully")

# Streaming Page
driver.close()                                      # Close current page
driver.switch_to_window(driver.window_handles[0])   # Switch to streaming page

