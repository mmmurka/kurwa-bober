from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverSingleton:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None or not cls._driver.session_id:
            chrome_options = Options()
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            cls._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None


