from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables from .env file
load_dotenv()

# Fetch LinkedIn credentials from environment variables
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

# Check if the LinkedIn credentials are available
if not linkedin_username or not linkedin_password:
    raise ValueError("LinkedIn credentials not found in environment variables.")

# Set up Chrome options to disable GPU hardware acceleration
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
chrome_options.add_argument('--no-sandbox')  # Disable sandboxing (useful in some cases)
chrome_options.add_argument('--headless')  # Run in headless mode if needed
chrome_options.add_argument('--disable-software-rasterizer')  # Disable software rasterizer
chrome_options.add_argument('--remote-debugging-port=9222')  # Disable remote debugging to avoid logging issues
chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage in headless mode
chrome_options.add_argument('--disable-extensions')  # Disable extensions for a cleaner environment

# Use webdriver_manager to automatically handle the ChromeDriver path
service = Service(ChromeDriverManager().install())

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open LinkedIn login page
driver.get("https://www.linkedin.com/login")

# Find and interact with the login elements
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")

# Enter LinkedIn credentials
username_field.send_keys(linkedin_username)
password_field.send_keys(linkedin_password)

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for login to complete (use explicit wait for better practice)
try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.global-nav__me-text"))
    )
    print("Login successful!")
except Exception as e:
    print(f"Error during login: {e}")

# Example: Print page title to verify you're logged in
print(driver.title)

# Close the driver after the actions are completed
driver.quit()
