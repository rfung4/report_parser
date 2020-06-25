import re

from runner import run_script
from sites.script import Script
from util.utility import extract_monetary_value

class BeyondMeat(Script):

    report_url = 'https://investors.beyondmeat.com/news-releases/news-release-details/beyond-meatr-reports-first-quarter-2020-financial-results'

    cash_regex = re.compile('cash equivalents balance was \\$[0-9]+\\.[0-9]+.million')
    rev_regex = re.compile('Net revenues were \\$[0-9]+(\\.[0-9]+)? million')
    income_regex = re.compile('Net income was \\$[0-9]+(.[0-9]+)? million')
    eps_regex = re.compile('\\$[0-9]\\.[0-9]+ per common diluted share')

    def __init__(self):
        super().__init__('Beyond Meat')

    def get_report(self):
        self.report_text = self.make_soup_requests(self.report_url).text.replace(u'\xa0', ' ')

    def parse_net_income(self):
        income_string = self.income_regex.search(self.report_text).group()
        self.values[self.NET_INCOME_TAG] = extract_monetary_value(income_string)

    def parse_revenue(self):
        rev_string = self.rev_regex.search(self.report_text).group()
        self.values[self.REV_TAG] = extract_monetary_value(rev_string)

    def parse_cash_flow(self):
        cash_string = self.cash_regex.search(self.report_text)
        self.values[self.CASH_TAG] = extract_monetary_value(cash_string.group())

    def parse_EPS(self):
        eps_string = self.eps_regex.search(self.report_text)
        self.values[self.EPS_TAG] = extract_monetary_value(eps_string.group().strip()).strip()

    def cleanup(self):
        pass


if __name__ == '__main__':
    run_script(BeyondMeat())
