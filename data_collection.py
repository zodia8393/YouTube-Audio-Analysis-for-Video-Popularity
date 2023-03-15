from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def quit_chrome_driver(driver):
    driver.quit()

def collect_video_metadata(driver, video_url):
    driver.get(video_url)
    # Add your code here to collect metadata
    return metadata

def get_video_urls_from_channel(driver, channel_url):
    driver.get(channel_url)

    wait = WebDriverWait(driver, 10)

    # Wait for the video thumbnails to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#video-title")))

    # Scroll to load more videos
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.find_element_by_tag_name("body").send_keys(Keys.END)
        time.sleep(2)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

    # Get all video URLs
    video_elements = driver.find_elements_by_css_selector("#video-title")
    video_urls = [video_element.get_attribute("href") for video_element in video_elements]

    return video_urls
