import requests
from bs4 import BeautifulSoup


class Script:

    @staticmethod
    def make_soup_requests(url):
        return BeautifulSoup(requests.get(url).content, features='lxml')

    REV_TAG, NET_INCOME_TAG, CASH_TAG, EPS_TAG = 'Revenue', 'Net Income', 'Cash Flow', 'EPS'
    values = {t: 'N/A' for t in (REV_TAG, NET_INCOME_TAG, CASH_TAG, EPS_TAG)}

    def __init__(self, name):
        self.name = name
        self.driver = None

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

    def cleanup(self):
        pass