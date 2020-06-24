import re

from runner import run_script
from sites.script import Script
from util.utility import extract_monetary_value


class Nvidia(Script):

    report_url = 'https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2021'

    rev_regex = re.compile('Revenue of \\$[0-9]+\\.[0-9]+ billion')
    eps_regex = re.compile('GAAP earnings per diluted share for the quarter were \\$[0-9]+\\.[0-9]+')

    income_table_regex = re.compile('CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS')
    cash_table_regex = re.compile('RECONCILIATION OF GAAP TO NON-GAAP FINANCIAL MEASURES')

    def __init__(self):
        super().__init__('Nvidia')

    @staticmethod
    def get_income_table(soup):
        for table in soup.findAll('table'):
            if Nvidia.income_table_regex.search(str(table)):
                return table

    @staticmethod
    def get_cash_table(soup):
        for table in soup.findAll('table'):
            if Nvidia.cash_table_regex.search(str(table)):
                return table

    @staticmethod
    def get_table_row_with_text(table, text):
        for row in table.findAll('tr'):
            if text in str(row):
                return row

    def get_report(self):
        self.report_soup = self.make_soup_requests(self.report_url)

    def parse_net_income(self):
        cf_table = self.get_income_table(self.report_soup)
        inc_row = self.get_table_row_with_text(cf_table, 'Net income')
        self.values[self.NET_INCOME_TAG] = "".join(["$", inc_row.findAll('td')[2].text, ' million'])

    def parse_revenue(self):
        rev_string = self.rev_regex.search(self.report_soup.text).group()
        self.values[self.REV_TAG] = extract_monetary_value(rev_string)

    def parse_cash_flow(self):
        cf_table = self.get_cash_table(self.report_soup)
        cash_row = self.get_table_row_with_text(cf_table, 'Free cash')
        self.values[self.CASH_TAG] = "".join(["$", cash_row.findAll('td')[2].text, ' million'])

    def parse_EPS(self):
        eps_string = self.eps_regex.search(self.report_soup.text).group()
        self.values[self.EPS_TAG] = extract_monetary_value(eps_string)

    def cleanup(self):
        pass


if __name__ == '__main__':
    run_script(Nvidia())
