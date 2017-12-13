# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:45:18 2017

@author: Ethan
"""

#### THIS IS FOR PERSONAL USE ONLY 
#### THIS IS NOT CREATED FOR MONETARY GAIN OR ADVANCEMENT

# SKELETON---------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create path to chromedriver
path_to_chromedriver = '' # change path as needed
# Open browser with path
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
time.sleep(2)

# Set surfline URL to ENSENADA
url_2 = 'http://www.surfline.com/surf-forecasts/northern-baja/ensenada_2158'
# Open URL in browser
browser.get(url_2)
time.sleep(2)

#Navigate to login by clickin on login link
login_click = browser.find_element_by_xpath('//*[@id="top-prefs"]/ul/li[4]/a/strong')
browser.execute_script("arguments[0].click();", login_click)
time.sleep(2)
# Set email and password information
email = browser.find_element_by_id("email")
time.sleep(1)
password = browser.find_element_by_id("password")
time.sleep(1)
# Use email and password information to login
email.send_keys("")
time.sleep(1)
password.send_keys("")
time.sleep(1)

# Click the login button after having entered email and password
login_attempt = browser.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[1]/form/div[3]/div/button')
time.sleep(1)
login_attempt.submit()
time.sleep(10)

# What region?-----------------------------------------------------------------
region = browser.find_element_by_xpath('//*[@id="regional-forecast-cf"]/div[1]/span/strong')
print(region.text)

# DAYS 1 to 6 -----------------------------------------------------------------

# Find the day text iteratively
for i in range(1, 7):
    day = browser.find_element_by_xpath('//*[@id="observed_component"]/div[3]/div[1]/div/div/div[%s]/div[1]/span' %(i))
    print(day.text)
    time.sleep(1)
    
# Find the day rating, iteratively
for i in range(1,7):
    rating = browser.find_element_by_xpath('//*[@id="observed_component"]/div[3]/div[1]/div/div/div[%s]/div[1]/strong' %(i))
    print(rating.text)
    time.sleep(1)
    
# Find the height description iteratively
for i in range(1,7):
    h_desc = browser.find_element_by_xpath('//*[@id="observed_component"]/div[3]/div[1]/div/div/div[%s]/div[3]/div/div[1]/span[2]' %(i))
    print(h_desc.text)
    time.sleep(1)

# Find the days description iteratively
for i in range(1,7):
    day_desc = browser.find_element_by_xpath('//*[@id="observed_component"]/div[3]/div[1]/div/div/div[%s]/div[3]/div/span' %(i))
    print(day_desc.text, ",")
    time.sleep(1)

# Find the wave heights for the first six days, put them into a list
one_to_six_tags = browser.find_elements_by_tag_name('h1')
time.sleep(10)

one_to_six_heights = []
for i in one_to_six_tags:
    if i.text != '':
        one_to_six_heights.append(i.text)
    print(i.text)

# Swell Direction
swell_day = browser.find_element_by_xpath('//*[@id="lola_component"]/div[3]/div[1]/div/div/div[1]/div[1]/p')
swell_day.text
swell_time = browser.find_element_by_xpath('//*[@id="lola_component"]/div[3]/div[1]/div/div/div[1]/div[2]/p')
swell_time.text
swell = browser.find_element_by_id('bar_swell_71563_1')
swell.get_attribute('alt')

# Wind
# While looping over days, loop over times
wind_day = browser.find_element_by_xpath('//*[@id="lola_component"]/div[3]/div[1]/div/div/div[1]/div[1]/p')
wind_day.text
wind_time = browser.find_element_by_xpath('//*[@id="wind_component"]/div[3]/div[1]/div/div/div[1]/div[2]/p')
wind_time.text
wind = browser.find_element_by_id('bar_wind_4238_1')
wind.get_attribute('alt')


# Find the wave heights for the second six days, put them into a list
 # iteratve over range(7, 13) instead of range(1, 6)
seven_to_twelve_click = browser.find_element_by_id('tab_one')
time.sleep(10)
browser.execute_script("arguments[0].click();", seven_to_twelve_click)
time.sleep(10)

seven_to_twelve_tags = browser.find_elements_by_tag_name('h1')
time.sleep(10)

seven_to_twelve_heights = []
for i in seven_to_twelve_tags:
    if i.text != '':
        seven_to_twelve_heights.append(i.text)
    print(i.text)

print(seven_to_twelve_heights)

# OR JUST PRINT THE WHOLE SLIDER CONTENTS
c = browser.find_element_by_class_name("day-slider-container")
c.text

# LOG OUT IS IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

browser.close()




# Send the email --------------------------------------------------------------
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("", "")

msg = str(seven_to_twelve_heights)
server.sendmail("", "", c.text)
server.quit()

