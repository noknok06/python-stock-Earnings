import csv
import pandas as pd


class ManageCsv:

    def __init__(self):

        csv_data = []
        csv_file_path = 'result.csv'  # Replace 'your_file.csv' with the actual file path

        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)

            for row in csv_reader:
                csv_data.append(row)

        self.data = csv_data

    def read_csv():
        return pd.read_csv('result.csv')

    def cleansing(self):

        for row in self.data:
            for i in range(3, len(row)):
                try:
                    tmp = row[i].replace(",", "")
                    tmp = tmp.replace("－", "-")
                    if tmp == "-" or tmp == "None":
                        tmp = 0
                    row[i] = tmp
                except Exception as e:
                    print(e)

    # リストから１列だけ切り取る
    def cut_col(self, col_no):
        return [row[col_no] for row in self.data]
