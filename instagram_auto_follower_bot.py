import time

from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

similar_account="saketgokhale"
username="ksaket2332026"
password="Apple@2024"

class InstaFollower:
    def __init__(self):
        # ✅ Create Options object FIRST
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        # ✅ Then pass options to WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
    def login(self):
        self.driver.get("https://www.instagram.com")
        username_button=self.driver.find_element(By.XPATH, '//*[@id="_R_1h5l6n6pcldcpbn6b5ipamH1_"]')
        username_button.click()
        username_button.send_keys(username)
        password_button=self.driver.find_element(By.XPATH, '//*[@id="_R_1hll6n6pcldcpbn6b5ipamH1_"]')
        password_button.click()
        password_button.send_keys(password)
        time.sleep(2)
        log_in_button=self.driver.find_element(By.XPATH,'//*[@id="login_form"]/div/div[1]/div/div[3]/div/div/div')
        log_in_button.click()
        pass
        time.sleep(40)
        save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
        if save_login_prompt:
            save_login_prompt.click()
        time.sleep(5)
        notifications_prompt = self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]')
        if notifications_prompt:
            notifications_prompt.click()
    def find_followers(self):
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{similar_account}/followers")
        time.sleep(5)
        follower=self.driver.find_element(By.XPATH,'//*[@id="mount_0_0_ip"]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/section/main/div/div/header/div/section[2]/div/div[3]/div[2]/a')
        follower.click()
        time.sleep(2)



    def follow(self):
        buttons = self.driver.find_elements(By.CSS_SELECTOR,"div.x1dm5mii > div > div > div > div > div > button")
        for button in buttons:
            try:
                print(button.text)
                button.click()
                time.sleep(2)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_button.click()

bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
