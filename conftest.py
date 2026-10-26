import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from config import BASE_URL, HEADLESS, DEFAULT_TIMEOUT

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def driver():
    options = Options()
    if HEADLESS or os.getenv("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(45)
    yield browser
    browser.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, DEFAULT_TIMEOUT)
