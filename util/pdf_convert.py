import tabula
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


class PdfConverter:

    @staticmethod
    def extract_tables_to_csv(pdf_path, output_path=None):
        tabula.convert_into(pdf_path, output_path if output_path else'tables.csv', pages='all')

    @staticmethod
    def convert_pdf_to_txt(file_path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()

        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        fp = open(file_path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        return str

    # convert pdf file text to string and save as a text_pdf.txt file
    @staticmethod
    def save_convert_pdf_to_txt():
        content = PdfConverter.convert_pdf_to_txt()
        txt_pdf = open('text_pdf.txt', 'wb')
        txt_pdf.write(content.encode('utf-8'))
        txt_pdf.close()


if __name__ == '__main__':
    print(PdfConverter.convert_pdf_to_txt('../sites/amd/report.pdf'))
