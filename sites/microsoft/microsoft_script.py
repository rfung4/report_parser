import re
from runner import run_script
from sites.script import Script
from util.utility import extract_monetary_value


class Microsoft(Script):

    report_url = 'https://www.microsoft.com/en-us/Investor/earnings/FY-2020-Q3/press-release-webcast'

    rev_regex = re.compile('Revenue was \\$[0-9]+\\.[0-9]+ billion')
    net_income_regex = re.compile('Net income was \\$[0-9]+\\.[0-9]+ billion')
    eps_regex = re.compile('Diluted earnings per share was \\$[0-9]+\\.[0-9]+')

    def __init__(self):
        super().__init__('Microsoft')

    def get_report(self):
        self.report = self.make_soup_requests(self.report_url)

    def parse_net_income(self):
        income_string = self.net_income_regex.search(self.report.text).group()
        self.values[self.NET_INCOME_TAG] = extract_monetary_value(income_string)

    def parse_revenue(self):
        rev_string = self.rev_regex.search(self.report.text).group()
        self.values[self.REV_TAG] = extract_monetary_value(rev_string)

    def parse_cash_flow(self):
        #cf_table = self.report.find('')
        pass

    def parse_EPS(self):
        eps_string = self.eps_regex.search(self.report.text).group()
        self.values[self.EPS_TAG] = extract_monetary_value(eps_string)

    def cleanup(self):
        pass


if __name__ == '__main__':
    run_script(Microsoft())