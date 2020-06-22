from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from definitions import CHROME_DRIVER_PATH
from bs4 import BeautifulSoup
import requests


class DriverWrapper:

    def __init__(self):
        self.driver = None

    def get_driver(self):
        if not self.driver:
            self.driver = self.create_chrome_driver()
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()

    @staticmethod
    def create_chrome_driver() -> WebDriver:
        """ Create & return ChromeDriver instance
        :return: ChromeDriver Instance
        """
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.implicitly_wait(10)
        return driver

