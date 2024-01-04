import requests
import csv
from bs4 import BeautifulSoup
import time


class CSV:

    def read_csv():

        csv_data = []

        # Specify the path to your CSV file
        csv_file_path = 'company_list.csv'  # Replace 'your_file.csv' with the actual file path

        # Read the CSV file and store its contents in the list
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            for row in csv_reader:
                if row[0].rfind("#") == -1:
                    csv_data.append(row)

        return csv_data

    def write_elements(elements):
        with open('./result.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(elements)

class ScrapingHTML():

    def __init__(self, stock_no):
        self.stock_no = stock_no

    def get_html(self):

        r = requests.get("https://www.nikkei.com/nkd/company/kessan/?scode=" + str(self.stock_no))        
        soup = BeautifulSoup(r.content, "html.parser")

        return soup

stocks = CSV.read_csv()

for stock_code in stocks:

    if stock_code[0].find("＃") == 0:
        continue

    time.sleep(1) 

    try:
        cStock = ScrapingHTML(stock_code[0])
        soup =  cStock.get_html()

        write_elem = []

        stock_code = soup.select("span.m-companyCategory_text")[0]
        write_elem.append(stock_code.text.replace("\r\n        ",""))
        scock_name = soup.select("h1.m-headlineLarge_text")[0]
        write_elem.append(scock_name.text)

        trs = soup.select("tr")

        for tr in trs:

            th= tr.select("th")


            if len(th) == 0:
                continue

            # print(th[0].text)

            if th[0].text == "売上高（解説）":

                tds = tr.select("td")

                for td in tds:

                    print(td.text)
                    write_elem.append(td.text)


            if th[0].text == "営業利益（解説）":

                tds = tr.select("td")

                for td in tds:

                    print(td.text)
                    write_elem.append(td.text)

            if th[0].text == "経常利益（解説）":

                tds = tr.select("td")

                for td in tds:

                    print(td.text)
                    write_elem.append(td.text)    

        CSV.write_elements(write_elem)
    except:
        pass