from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import DEFAULT_TIMEOUT

class BasePage:
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        return self

    def first_visible(self, locators):
        """Try locator alternatives; return the first visible element or None."""
        for by, value in locators:
            try:
                elements = self.driver.find_elements(by, value)
                for element in elements:
                    if element.is_displayed():
                        return element
            except Exception:
                continue
        return None

    def click_first(self, locators):
        element = self.first_visible(locators)
        if element:
            element.click()
            return True
        return False

    def type_first(self, locators, value):
        element = self.first_visible(locators)
        if element is None:
            return False
        element.clear()
        element.send_keys(str(value))
        return True

    def text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def page_has_error(self):
        body = self.text().lower()
        return any(term in body for term in ["internal server error", "502 bad gateway", "503 service unavailable"])
