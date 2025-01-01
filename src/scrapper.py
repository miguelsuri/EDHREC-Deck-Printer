from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
from urllib.parse import urljoin, urlparse
import time

# Create a directory to store images
os.makedirs('documents/images', exist_ok=True)

# Setup Selenium WebDriver (Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')  # Set a good window size
driver = webdriver.Chrome(options=options)

def clean_filename(url):
    # Parse the URL and get the path
    path = urlparse(url).path
    # Get just the filename from the path
    filename = os.path.basename(path)
    return filename

def download_image(deck_name, img_url, headers):
    try:
        response = requests.get(img_url, headers=headers, stream=True)
        response.raise_for_status()
        
        # Clean the filename
        filename = clean_filename(img_url)
        img_path = os.path.join(os.path.join('documents/images', deck_name), filename)
        
        with open(img_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Successfully downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")
        return False

def scrape(url):
    try:
        # Load the page
        print("Loading page...")
        driver.get(url)

        deck_name = url.split('/')[-1]
        print(deck_name)
        os.makedirs(os.path.join('documents/images', deck_name), exist_ok=True)
        
        # Wait for the page to load initial content
        print("Waiting for initial content...")
        time.sleep(5)  # Give it some time to start loading
        
        # Scroll slowly through the page multiple times to ensure everything loads
        print("Scrolling through page...")
        for _ in range(3):  # Scroll through 3 times
            # Scroll down slowly
            for i in range(10):
                driver.execute_script(f"window.scrollTo(0, {i * (driver.execute_script('return document.body.scrollHeight') / 10)});")
                time.sleep(0.5)
            
            # Scroll back to top
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        
        # Wait a bit more after scrolling
        time.sleep(2)
        
        print("Finding card containers...")
        # Find all card containers
        containers = driver.find_elements(By.CLASS_NAME, "CardImage_container__4_PKo")
        print(f"Found {len(containers)} containers")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://edhrec.com/'
        }

        downloaded_count = 0
        error_count = 0

        for idx, container in enumerate(containers, 1):
            try:
                # Wait for image to be present in this specific container
                wait = WebDriverWait(container, 10)  # Notice we're using the container now for the wait
                img = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='scryfall.io']"))
                )

                img_url = img.get_attribute('src')
                if img_url:
                    print(f"\nProcessing image {idx}/{len(containers)}")
                    print(f"Found image URL: {img_url}")

                    if download_image(deck_name, img_url, headers):
                        downloaded_count += 1
                    else:
                        error_count += 1

            except Exception as e:
                print(f"Error processing container {idx}: {e}")
                error_count += 1

        print(f"\nDownload Summary:")
        print(f"Total containers found: {len(containers)}")
        print(f"Successfully downloaded: {downloaded_count}")
        print(f"Errors: {error_count}")

    finally:
        print("Closing browser...")
        driver.quit()