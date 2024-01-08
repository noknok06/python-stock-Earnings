import requests
from bs4 import BeautifulSoup

class ScrapingHTML():

    def __init__(self, stock_no):
        self.stock_no = stock_no

    def get_html_kessan(self):

        r = requests.get("https://www.nikkei.com/nkd/company/kessan/?scode=" + str(self.stock_no))        
        soup = BeautifulSoup(r.content, "html.parser")

        return soup

    def get_html_gaiyo(self):

        r = requests.get("https://www.nikkei.com/nkd/company/gaiyo/?scode=" + str(self.stock_no))        
        soup = BeautifulSoup(r.content, "html.parser")

        return soup

    def get_html_quote(self):

        r = requests.get("https://finance.yahoo.co.jp/quote/" + str(self.stock_no) + ".T")
        soup = BeautifulSoup(r.content, "html.parser")

        return soup


