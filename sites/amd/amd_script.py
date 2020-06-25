import os
import re
import requests
from runner import run_script
from sites.script import Script
from util.pdf_convert import PdfConverter
from util.utility import NUMBER_REGEX, format_value_millions


class AMD(Script):

    report_homepage = 'https://ir.amd.com/investor-overview'

    REV_REGEX = re.compile('quarter of 2020 of \\$[0-9]+\\.[0-9]+ (billion|million)')
    NET_INCOME_REGEX = re.compile('net income of \\$[0-9]+ million')
    EPS_REGEX = re.compile('diluted earnings per share of \\$[0-9]+\\.[0-9]+')

    def __init__(self):
        super().__init__('AMD')

    def get_report(self):
        homepage_soup = self.make_soup_requests(self.report_homepage)
        report_url = homepage_soup.find('a', text='Press Release')['href']

        response = requests.get(report_url)

        with open('report.pdf', 'wb') as f:
            f.write(response.content)

        report_file = open('report.pdf', 'rb')
        self.report_text = PdfConverter.convert_pdf_to_txt(report_file)

        PdfConverter.extract_tables_to_csv('report.pdf')
        report_file.close()

        return None     # Report is assigned to class variable

    def parse_net_income(self):
        res = self.NET_INCOME_REGEX.search(self.report_text).group()
        income = "".join(s for s in res.split() if '$' in s)
        self.values[self.NET_INCOME_TAG] = " ".join([income, 'million'])

    def parse_revenue(self):
        res = self.REV_REGEX.search(self.report_text).group()
        revenue = "".join(s for s in res.split() if '$' in s)
        self.values[self.REV_TAG] = revenue

    def parse_cash_flow(self):
        for row in open('tables.csv').readlines():
            if 'Free cash flow' in row:
                row_values = row.split(',', 1)[1]

                for v in row_values.split(","):
                    if NUMBER_REGEX.search(v):
                        cash_flow = v.replace("(", '').replace(")", '').replace("$", '').strip()
                        self.values[self.CASH_TAG] = format_value_millions(cash_flow)
                        return

    def parse_EPS(self):
        res = self.EPS_REGEX.search(self.report_text).group()
        eps = "".join(s for s in res.split() if '$' in s)
        self.values[self.EPS_TAG] = eps

    def cleanup(self):
        os.remove('tables.csv')
        os.remove('report.pdf')


if __name__ == '__main__':
    run_script(AMD())