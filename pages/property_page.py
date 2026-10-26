from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PropertyPage(BasePage):
    BOOK_BUTTONS = [
        (By.XPATH, "//a[contains(translate(normalize-space(.),'BOOK NOW','book now'),'book now')]"),
        (By.XPATH, "//button[contains(translate(normalize-space(.),'BOOK NOW','book now'),'book now')]"),
        (By.XPATH, "//a[contains(translate(normalize-space(.),'BOOK ROOM','book room'),'book room')]"),
        (By.XPATH, "//button[contains(translate(normalize-space(.),'BOOK ROOM','book room'),'book room')]"),
    ]
    NAME = [(By.ID, "txtCustomerName"), (By.NAME, "customer_name"), (By.NAME, "name"), (By.XPATH, "//input[contains(@placeholder,'Name')]")]
    MOBILE = [(By.ID, "txtCustomerMobile"), (By.NAME, "mobile"), (By.NAME, "phone"), (By.XPATH, "//input[contains(@placeholder,'Mobile') or contains(@placeholder,'Phone')]")]
    EMAIL = [(By.ID, "txtCustomerEmail"), (By.NAME, "email"), (By.XPATH, "//input[@type='email']")]

    def click_book(self):
        return self.click_first(self.BOOK_BUTTONS)

    def booking_form_visible(self):
        return any(self.first_visible(items) for items in [self.NAME, self.MOBILE, self.EMAIL])

    def fill_booking_form(self, name, mobile, email):
        return (
            self.type_first(self.NAME, name),
            self.type_first(self.MOBILE, mobile),
            self.type_first(self.EMAIL, email),
        )

    def validation_messages(self):
        messages = self.driver.find_elements(By.XPATH, "//*[contains(@class,'error') or @role='alert' or self::small]")
        return " ".join(m.text for m in messages if m.is_displayed())
