from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from definitions import CHROME_DRIVER_PATH


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

    def get_soup(self, url):
        if not self.driver:
            self.get_driver()

        self.driver.get(url)
        return BeautifulSoup(self.driver.page_source, features='lxml')

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

