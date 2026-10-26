from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import PACKAGES_URL

class PackagePage(BasePage):
    def load(self):
        self.open(PACKAGES_URL)
        return self

    def package_links(self):
        return self.driver.find_elements(By.XPATH, "//a[contains(@href,'package-details') or contains(translate(normalize-space(.),'BOOK NOW','book now'),'book now') or contains(translate(normalize-space(.),'VIEW DETAILS','view details'),'view details')]")

    def open_first_package(self):
        for link in self.package_links():
            if link.is_displayed():
                link.click()
                return True
        return False

    def departure_controls(self):
        return self.driver.find_elements(By.XPATH, "//select[contains(translate(@name,'DATE','date'),'date') or contains(translate(@id,'DATE','date'),'date')] | //input[@type='date']")
