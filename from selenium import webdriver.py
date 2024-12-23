from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# BrowserStack credentials
USERNAME = 'prathamm_854lVN'
ACCESS_KEY = '36qoAQ7r67ZkBK5BF3cW'

# BrowserStack hub URL
URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Platforms configurations
platforms = [
    {
        "os": "Windows",
        "osVersion": "10",
        "browserName": "Chrome",
        "browserVersion": "120.0",
        "browserstack.local": "true",
        "project": "BrowserStack Sample",
        "build": "browserstack-build-1",
        "name": "Windows Chrome Test"
    },
    {
        "deviceName": "Xiaomi Redmi Note 9",
        "osVersion": "10.0",
        "browserName": "chrome",
        "deviceOrientation": "portrait",
        "browserstack.local": "true",
        "project": "BrowserStack Sample",
        "build": "browserstack-build-1",
        "name": "Mobile Chrome Test - Portrait"
    }
]

# Test URL
test_url = "https://elpais.com/opinion/2024-12-23/la-descarbonizacion-se-frena.html"

# Test function
def run_test(platform):
    driver = None  # Initialize driver to None to avoid UnboundLocalError
    try:
        # Create options object and add capabilities
        options = Options()
        for key, value in platform.items():
            options.set_capability(key, value)

        # Add BrowserStack credentials to capabilities
        options.set_capability("browserstack.user", USERNAME)
        options.set_capability("browserstack.key", ACCESS_KEY)

        # Create WebDriver session
        driver = webdriver.Remote(
            command_executor=URL,
            options=options
        )

        # Open the test URL
        driver.get(test_url)
        print(f"Testing on: {platform.get('name', 'Unknown Platform')}")
        time.sleep(3)  # Wait for the page to load

        # Extract title as an example
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h1").text
            print(f"Page Title: {title}")
        except Exception as e:
            print(f"Error extracting title: {e}")

    except Exception as e:
        print(f"Error during BrowserStack session: {e}")
    finally:
        # Safely quit the driver only if it was successfully initialized
        if driver:
            driver.quit()

# Run tests on all platforms
if __name__ == "__main__":
    for platform in platforms:
        run_test(platform)
