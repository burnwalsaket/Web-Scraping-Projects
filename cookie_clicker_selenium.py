from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time

# Setup Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")

# Wait for page to load
sleep(3)

# -------------------- HANDLE LANGUAGE --------------------
try:
    language_button = driver.find_element(By.ID, "langSelect-EN")
    language_button.click()
    print("Language set to English")
    sleep(3)
except NoSuchElementException:
    print("Language selection not found")

# -------------------- HANDLE COOKIE CONSENT --------------------
try:
    consent_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "cc_btn_accept_all"))
    )
    consent_button.click()
    print("Accepted cookie consent")
    sleep(2)
except:
    print("No cookie popup found")

# -------------------- MAIN ELEMENTS --------------------
cookie = driver.find_element(By.ID, "bigCookie")

# Timers
wait_time = 5
timeout = time() + wait_time
end_time = time() + 60 * 5  # 5 minutes

# -------------------- GAME LOOP --------------------
while True:
    cookie.click()

    # Every 5 seconds → buy best item
    if time() > timeout:
        try:
            # Get cookie count
            cookies_text = driver.find_element(By.ID, "cookies").text
            cookies_count = int(cookies_text.split()[0].replace(",", ""))

            # Get all products
            products = driver.find_elements(By.CSS_SELECTOR, "div[id^='product']")

            best_item = None

            # Loop from most expensive to cheapest
            for product in reversed(products):
                if "enabled" in product.get_attribute("class"):
                    best_item = product
                    break

            # Buy item using JS click (fix for interception)
            if best_item:
                driver.execute_script("arguments[0].scrollIntoView();", best_item)
                sleep(0.2)
                driver.execute_script("arguments[0].click();", best_item)

                print(f"Bought: {best_item.get_attribute('id')}")

        except (NoSuchElementException, ValueError):
            print("Error finding items or cookies")

        # Reset timer
        timeout = time() + wait_time

    # Stop after 5 minutes
    if time() > end_time:
        print("Finished 5 minutes of gameplay")
        break

    # Small delay to stabilize loop
    sleep(0.01)

driver.quit()
