import os
import re

import requests
from bs4 import BeautifulSoup

CHROME_DRIVER_PATH = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver.exe"
NUMBER_REGEX = re.compile('[0-9]+')

class Script:

    @staticmethod
    def make_soup_requests(url):
        return BeautifulSoup(requests.get(url).content, features='lxml')

    REV_TAG, NET_INCOME_TAG, CASH_TAG, EPS_TAG = 'Revenue', 'Net Income', 'Cash Flow', 'EPS'
    values = {t: '' for t in (REV_TAG, NET_INCOME_TAG, CASH_TAG, EPS_TAG)}

    def __init__(self, name):
        self.name = name
        self.driver = None
        self.report = None

    def set_driver(self, dm):
        self.driver = dm

    def get_report(self):
        pass

    def parse_net_income(self):     # Parses value & assigns to value dict
        pass

    def parse_revenue(self):
        pass

    def parse_cash_flow(self):
        pass

    def parse_EPS(self):
        pass









