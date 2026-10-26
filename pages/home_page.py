from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from config import HOME_URL

class HomePage(BasePage):
    # Public UI labels have changed in the past; update these alternatives after inspecting DevTools.
    DESTINATION_OPTIONS = [
        (By.XPATH, "//input[contains(@placeholder,'Destination')]"),
        (By.XPATH, "//select[contains(translate(@name,'DESTINATION','destination'),'destination')]"),
        (By.XPATH, "//label[contains(.,'Destinations')]/following::select[1]"),
    ]
    PRICE_OPTIONS = [
        (By.XPATH, "//label[contains(.,'Price Range')]/following::select[1]"),
        (By.XPATH, "//select[contains(translate(@name,'PRICE','price'),'price')]"),
    ]
    SEARCH_BUTTONS = [
        (By.ID, "search_hotel"),
        (By.XPATH, "//button[contains(translate(normalize-space(.),'SEARCH','search'),'search')]"),
        (By.XPATH, "//input[@type='submit']"),
    ]

    def load(self):
        self.open(HOME_URL)
        return self

    def select_filter(self, locators, value):
        element = self.first_visible(locators)
        if not element:
            # Some current filters are checkboxes rather than selects.
            candidate = self.driver.find_elements(By.XPATH, f"//*[self::label or self::a or self::span][contains(translate(normalize-space(.),'{value.upper()}','{value.lower()}'),'{value.lower()}')]")
            for item in candidate:
                try:
                    if item.is_displayed():
                        item.click()
                        return True
                except Exception:
                    pass
            return False
        tag = element.tag_name.lower()
        if tag == "select":
            select = Select(element)
            for option in select.options:
                if value.lower() in option.text.lower():
                    select.select_by_visible_text(option.text)
                    return True
            return False
        element.clear()
        element.send_keys(value)
        return True

    def search_destination(self, destination):
        return self.select_filter(self.DESTINATION_OPTIONS, destination)

    def search_price(self, price_range):
        return self.select_filter(self.PRICE_OPTIONS, price_range)

    def submit_search(self):
        return self.click_first(self.SEARCH_BUTTONS)

    def property_links(self):
        return self.driver.find_elements(By.XPATH, "//a[contains(translate(normalize-space(.),'SELECT PROPERTY','select property'),'select property') or contains(translate(normalize-space(.),'BOOK NOW','book now'),'book now')]")

    def open_first_property(self):
        links = self.property_links()
        if links:
            links[0].click()
            return True
        # Common fallback: property-card links
        links = self.driver.find_elements(By.XPATH, "//div[contains(@class,'item-title')]//a | //a[contains(@href,'property')]")
        for link in links:
            if link.is_displayed():
                link.click()
                return True
        return False
