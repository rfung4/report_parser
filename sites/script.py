import requests
from bs4 import BeautifulSoup


class Script:

    @staticmethod
    def make_soup_requests(url):
        """ Uses request module to create a BeautifulSoup object given a URL
        :param url: URL
        :return: BeautifulSoup object
        """
        return BeautifulSoup(requests.get(url).content, features='lxml')

    # Defined tags to ensure
    REV_TAG, NET_INCOME_TAG, CASH_TAG, EPS_TAG = 'Revenue', 'Net Income', 'Cash Flow', 'EPS'
    # Values initialized to N/A, to be set by implementing classes
    values = {t: 'N/A' for t in (REV_TAG, NET_INCOME_TAG, CASH_TAG, EPS_TAG)}

    def __init__(self, name):
        self.name = name

    def get_report(self):
        """
            Acquires the report, either through URL or by downloading the report PDF
        """
        pass

    def parse_net_income(self):    
        pass

    def parse_revenue(self):
        pass

    def parse_cash_flow(self):
        pass

    def parse_EPS(self):
        pass

    def cleanup(self):
        """
            Deletes temporary files used by the script during execution
        """
        pass
