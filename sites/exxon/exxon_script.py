import re

from runner import run_script
from sites.script import Script
from util.utility import extract_monetary_value, format_value_millions


class Exxon(Script):

    report_url = 'https://corporate.exxonmobil.com/News/Newsroom/News-releases/2020/0501_ExxonMobil-reports-results-for-first-quarter-2020'

    income_regex = re.compile('estimated (first|second|third|fourth) quarter 20[0-9]{2} (gain|loss) of \\$[0-9]+ million')
    cash_flow_regex = re.compile('Cash flow from operating activities was \\$[0-9]+\\.[0-9]+ billion')
    eps_regex = re.compile('\\$[0-9]+\\.[0-9]+ per share')

    def __init__(self):
        super().__init__('Exxon')

    def get_report(self):
        self.report_soup = self.make_soup_requests(self.report_url)

    def parse_net_income(self):
        inc_raw = self.income_regex.search(str(self.report_soup)).group()
        self.values[self.NET_INCOME_TAG] = extract_monetary_value(inc_raw)

    def parse_revenue(self):
        for row in self.report_soup.findAll('tr'):
            if 'Total revenues' in str(row):
                total_rev_value = row.findAll('td')[1].text  # First non-header column
                self.values[self.REV_TAG] = format_value_millions(total_rev_value.replace(',', '').strip().replace("\n", ''))
                break

    def parse_cash_flow(self):
        cf_raw = self.cash_flow_regex.search(str(self.report_soup)).group()
        self.values[self.CASH_TAG] = extract_monetary_value(cf_raw)

    def parse_EPS(self):
        eps_raw = self.eps_regex.search(str(self.report_soup)).group()
        self.values[self.EPS_TAG] = extract_monetary_value(eps_raw)

    def cleanup(self):
        pass


if __name__ == '__main__':
    run_script(Exxon())
