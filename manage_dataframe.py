import pandas as pd

class ManageDataFrame:

    def __init__(self, lists):

        self.dataf = pd.DataFrame(lists)

    def cut_range_col(self, start_col, end_col):
        return self.dataf.iloc[:, start_col:end_col]
