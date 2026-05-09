
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

PROMISED_DOWN = 30
PROMISED_UP = 30
TWITTER_EMAIL = "abcdef@gmail.com"
TWITTER_PASSWORD = "abcdef"

class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        button= self.driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div[2]/a')
        button.click()
        time.sleep(60)
        self.up=self.driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
        print(f"Up:{self.up.text}")
        self.down=self.driver.find_element(By.XPATH,'//*[@id="container"]/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
        print(f"Down:{self.down.text}")

    def tweet_at_provider(self):
        self.driver.get("https://x.com/")
        time.sleep(5)
        sign_in_button=self.driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div/main/div/div/div[1]/div/div/div[3]/div[4]/a')
        sign_in_button.click()
        time.sleep(5)
        click_to_write=self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
        click_to_write.click()
        click_to_write.send_keys(TWITTER_EMAIL)
        time.sleep(5)
        click=self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
        click.click()
        time.sleep(5)
        password_click=self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label')
        password_click.click()
        password_click.send_keys(TWITTER_PASSWORD)
        login_click=self.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div')
        login_click.click()
        time.sleep(5)
        twitter_compose=self.driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div')
        twitter_compose.click()
        tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        twitter_compose.send_keys(tweet)
        time.sleep(5)
        twitter_post=self.driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/button')
        twitter_post.click()
        time.sleep(5)
        self.driver.quit()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()
