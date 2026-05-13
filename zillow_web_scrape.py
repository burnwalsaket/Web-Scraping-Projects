import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
zillow_clone="https://appbrewery.github.io/Zillow-Clone/"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}
response=requests.get(zillow_clone, headers=header)
soup=BeautifulSoup(response.content,"html.parser")
price_cards=soup.find_all(class_="PropertyCardWrapper")
price_list=[]
for price_card in price_cards:
    price=price_card.getText()
    price_list.append(price.strip())
print(price_list)
address_cards=soup.find_all(name="address")
address_list=[]
for address_card in address_cards:
    address=address_card.getText()
    address_list.append(address.strip())
print(address_list)
link_cards=soup.find_all(name="a",class_="property-card-link")
link_list=[]
for link_card in link_cards:
    link=link_card.get("href")
    link_list.append(link)
print(link_list)

# Lets fill the data into google form
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
# Lets fill the data into google form
google_form = "https://docs.google.com/forms/d/e/1FAIpQLSf4lu-LsAf7OyIA82-Qg8wVL8EpMeSVNboQPB-3wt4GHs2HQQ/viewform"

# LOOP THROUGH ALL LISTS TOGETHER
for n in range(len(link_list)):
    driver.get(google_form)
    time.sleep(2)

    # ADDRESS FIELD
    address_in_form = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

    # PRICE FIELD
    price_in_form = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')

    # LINK FIELD
    link_in_form = driver.find_element(
        By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    # SUBMIT BUTTON
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address_in_form.send_keys(address_list[n])
    price_in_form.send_keys(price_list[n])
    link_in_form.send_keys(link_list[n])

    # SUBMIT BUTTON

    submit_button.click()
