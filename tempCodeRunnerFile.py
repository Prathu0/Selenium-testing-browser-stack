import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator  # Using Deep Translator for translation
from selenium.webdriver.chrome.options import Options

# List of URLs to scrape
urls = [
    "https://elpais.com/espana/2024-12-23/sanchez-se-muestra-dispuesto-a-reunirse-con-puigdemont-antes-de-que-se-le-aplique-la-amnistia.html",
    "https://elpais.com/espana/2024-12-23/sanchez-se-muestra-dispuesto-a-reunirse-con-puigdemont-antes-de-que-se-le-aplique-la-amnistia.html",
    "https://elpais.com/espana/catalunya/2024-12-23/illa-confia-en-que-la-nueva-etapa-en-cataluna-deje-atras-el-sufrimiento-y-no-descarta-reunirse-con-puigdemont.html",
    "https://elpais.com/internacional/2024-12-23/macron-nombra-un-gobierno-continuista-en-un-nuevo-intento-de-sacar-a-francia-del-bloqueo-politico.html",
    "https://elpais.com/espana/madrid/2024-12-20/madrid-llega-ya-al-millon-de-latinos-uno-de-cada-siete-habitantes.html"
]

# BrowserStack capabilities
caps = {
    "browserstack.local": "true",
    "buildName": "bstack-demo",
    "projectName": "BrowserStack Sample",
    "debug": "true",
    "consoleLogs": "info"
}

def run_test():
    driver = None  # Initialize driver to None to handle any errors in driver creation
    try:
        # Create a ChromeOptions instance and set the capabilities
        options = Options()
        for key, value in caps.items():
            options.set_capability(key, value)

        # Initialize WebDriver with options instead of capabilities
        driver = webdriver.Remote(
            command_executor='https://prathamm_854lVN:36qoAQ7r67ZkBK5BF3cW@hub-cloud.browserstack.com/wd/hub',
            options=options  # Use 'options' instead of 'capabilities'
        )

        for url in urls:
            # Open each article URL
            driver.get(url)

            # Wait for the page content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/article/div[2]/p"))
            )

            try:
                # Extract the article title
                title = driver.find_element(By.TAG_NAME, "h1").text
                
                # Translate the title from Spanish to English
                translated_title = GoogleTranslator(source='auto', target='en').translate(title)
                
                # Extract the content of the article
                content = driver.find_element(By.XPATH, "/html/body/article/div[2]/p").text

                # Find image URLs within the article (if any)
                images = driver.find_elements(By.TAG_NAME, 'img')
                image_urls = [img.get_attribute('src') for img in images]
                
                # Display the extracted information
                print(f"URL: {url}")
                print(f"Original Title: {title}")
                print(f"Translated Title: {translated_title}")
                print(f"Content: {content[:200]}...")  # Displaying first 200 characters of content
                print(f"Image URLs: {image_urls}")
                print("-" * 50)

            except Exception as inner_e:
                print(f"Error processing article {url}: {inner_e}")
                continue

        # Mark test as passed if everything works
        executor_object = {
            'action': 'setSessionStatus',
            'arguments': {
                'status': "passed",
                'reason': "Fetched and translated articles successfully"
            }
        }
        driver.execute_script('browserstack_executor: {}'.format(json.dumps(executor_object)))

    except Exception as e:
        if driver:
            # Mark test as failed
            executor_object = {
                'action': 'setSessionStatus',
                'arguments': {
                    'status': "failed",
                    'reason': str(e)
                }
            }
            driver.execute_script('browserstack_executor: {}'.format(json.dumps(executor_object)))
        print(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_test()
