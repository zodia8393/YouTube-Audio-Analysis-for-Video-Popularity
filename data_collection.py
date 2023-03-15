from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def quit_chrome_driver(driver):
    driver.quit()


def get_video_urls_from_channel(driver, channel_url):
    driver.get(channel_url)

    video_urls = []
    video_elements = driver.find_elements_by_css_selector("a#video-title")
    for video_element in video_elements:
        video_urls.append(video_element.get_attribute("href"))

    return video_urls


def collect_video_metadata(driver, video_url):
    driver.get(video_url)

    wait = WebDriverWait(driver, 10)

    # Get video title
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title")))
    title = driver.find_element_by_css_selector("h1.title").text

    # Get video description
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#description yt-formatted-string")))
    description = driver.find_element_by_css_selector("div#description yt-formatted-string").text

    # Get view count
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.view-count")))
    view_count_text = driver.find_element_by_css_selector("span.view-count").text
    view_count = int(''.join(filter(str.isdigit, view_count_text)))

    # Get likes and dislikes
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "yt-formatted-string.ytd-toggle-button-renderer")))
    like_elements = driver.find_elements_by_css_selector("yt-formatted-string.ytd-toggle-button-renderer")
    likes = int(''.join(filter(str.isdigit, like_elements[0].get_attribute("aria-label"))))
    dislikes = int(''.join(filter(str.isdigit, like_elements[1].get_attribute("aria-label"))))

    # Get video tags
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "meta[name='keywords']")))
    tags = driver.find_element_by_css_selector("meta[name='keywords']").get_attribute("content").split(',')

    # Get video category
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "yt-formatted-string.ytd-metadata-row-renderer a")))
    category = driver.find_element_by_css_selector("yt-formatted-string.ytd-metadata-row-renderer a").text

    metadata = {
        "url": video_url,
        "title": title,
        "description": description,
        "view_count": view_count,
        "likes": likes,
        "dislikes": dislikes,
        "tags": tags,
        "category": category,
    }

    return metadata
