from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import os


# STEP 1: Setup credentials and launch browser
ACCOUNT_EMAIL = "your_email@test.com"  # User login email
ACCOUNT_PASSWORD = "Honey@123"         # User login password
GYM_URL = "https://appbrewery.github.io/gym/"  # Target website

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keep browser open after script ends

# Create a persistent Chrome profile to maintain session/cookies
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# Launch Chrome driver
driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)  # Open the gym website


# STEP 2: Login to the application
Wait = WebDriverWait(driver, 2)  # Explicit wait (2 seconds max)

log_in_button = driver.find_element(By.ID, "login-button")  # Locate login button
log_in_button.click()  # Click login button

# Enter email
email = driver.find_element(By.ID, "email-input")
email.send_keys(ACCOUNT_EMAIL)

# Enter password
password = driver.find_element(By.ID, "password-input")
password.send_keys(ACCOUNT_PASSWORD)

# Submit login form
submit_button = driver.find_element(By.ID, "submit-button")
submit_button.click()

# Wait until schedule page loads after login
Wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

# Initialize counters for tracking results
booked_count = 0
waitlist_count = 0
already_booked_count = 0
processed_classes = []


# STEP 3: Find all class cards on schedule page
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

for class_card in class_cards:
    # Find parent day group (Tue, Wed, etc.)
    day_group = class_card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text  # Extract day text

    # Filter only Tuesday and Thursday classes
    if "Tue" in day_title or "Thu" in day_title:

        # Get class timing
        time_text = class_card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text

        # Filter only 6:00 PM classes
        if "6:00 PM" in time_text:

            # Get class name
            class_name = class_card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text

            # Find booking button
            book_button = class_card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
            print(f"BUTTON TEXT: '{book_button.text}'")

            class_info = f"{class_name} on {day_title}"  # Combine info

            # STEP 4: Handle booking logic based on button text
            if book_button.text == "Booked":
                # Already booked case
                print(f"✓ Already booked:  {class_info}")
                already_booked_count += 1
                processed_classes.append(f"[Booked]{class_info}")

            elif book_button.text == "Waitlisted":
                # Already waitlisted case
                print(f"Already on waitlist: {class_info}")
                already_booked_count += 1
                processed_classes.append(f"[Waitlisted]{class_info}")

            elif book_button.text == "Book Class":
                # Book the class
                book_button.click()
                print(f"Successfully booked:  {class_info}")
                booked_count += 1
                processed_classes.append(f"[New Booking]{class_info}")

            elif book_button.text == "Join Waitlist":
                # Join waitlist
                book_button.click()
                print(f"Joined waitlist for: {class_info}")
                waitlist_count += 1
                processed_classes.append(f"[New Waitlist]{class_info}")


# STEP 5: Print booking summary
print("--- BOOKING SUMMARY ---")
print(f"Classes booked : {booked_count}")
print(f"Waitlists joined : {waitlist_count}")
print(f"Already booked/waitlisted : {already_booked_count}")
print(f"Total Tuesday and Thursday 6pm classes processed : {booked_count + waitlist_count + already_booked_count}")

print("--- DETAILED CLASS LIST ---")

# Print all processed classes
for class_detail in processed_classes:
    print(f"  • {class_detail}")


# STEP 6: Calculate total bookings
total_booked = already_booked_count + waitlist_count + booked_count
print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")


# STEP 7: Verify bookings from "My Bookings" page
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

# Navigate to My Bookings page
my_bookings_link = driver.find_element(By.ID, "my-bookings-link")
my_bookings_link.click()

# Wait for bookings page to load
Wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

verified_booking = 0

# Get all booking cards
all_booking_cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")

for booking_card in all_booking_cards:
    try:
        # Find "When" section
        when_paragraph = booking_card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
        when_text = when_paragraph.text

        # Check for Tue/Thu at 6 PM bookings
        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
            class_name = booking_card.find_element(By.TAG_NAME, "h3").text
            print(f"Verified: {class_name}")
            verified_booking += 1

    except NoSuchElementException:
        # Skip cards that don't match expected structure
        pass


# STEP 8: Final verification result
print(f"--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} bookings")
print(f"Found: {verified_booking} bookings")

if verified_booking == total_booked:
    print("✅ SUCCESS: All Bookings Verified")
else:
    print(f"❌ MISMATCH: Missing {total_booked - verified_booking} bookings")
