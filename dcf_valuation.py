from datetime import datetime


import matplotlib.pyplot as plt
import pandas as pd
import requests

from matplotlib.backends.backend_pdf import PdfPages

from pprint import pprint


class YahooFin():
    BASE_URL = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'

    def __init__(self, ticker):
        self.ticker = ticker

    def make_request(self, url):
        """Makes a GET request"""
        return requests.get(url)

    def get_data(self):
        return self.make_request(self.url).json()

    def data(self):
        data_temp = self.get_data()
        try:
            return data_temp.get('quoteSummary').get("result")
        except KeyError as e:
            print("Something went wrong")

    def convert_timestamp(self, raw):
        return datetime.utcfromtimestamp(raw).strftime('%Y-%m-%d')

    def _save_all_plots(self, df):
        for column in df:
            with PdfPages('foo.pdf') as pdf:
                fig=df.plot(x='endDate', y=column).get_figure()
                pdf.savefig(fig)







class BalanceSheetQ(YahooFin):

    def __init__(self, ticker):
        super().__init__(ticker)
        self._module = 'balanceSheetHistoryQuarterly'
        self._url = (f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'
                    f'{self.ticker}?'
                    f'modules={self.module}')
        self._df = None
                    
    @property
    def module(self):
        return self._module

    @property
    def url(self):
        return self._url

    @property
    def df(self):
        return self._df
    

    def _balance_sheet(self):
        data = self.data()
        query =  data[0]
        balance_sheet_qty = query['balanceSheetHistoryQuarterly']
        balance_sheet_statements = balance_sheet_qty['balanceSheetStatements']
        return balance_sheet_statements

    def extract_raw(self):
        balance_sheet = self._balance_sheet()
        for items in balance_sheet:
            for key, value in items.items():
                if type(value) == dict and 'fmt' in value:
                    del value['fmt']
                if type(value) == dict and 'longFmt' in value:
                    del value['longFmt']
        return balance_sheet

    def create_dict(self):
        balance_sheet = []
        temp_balance_sheet = self.extract_raw()
        for d in temp_balance_sheet:
            temp_dict = {}
            for key, value in d.items():
                if type(value) == dict and 'raw' in value:
                    v = value['raw']
                    temp_dict[key] = v
            balance_sheet.append(temp_dict)
        return balance_sheet


    def to_df(self):
        self._df = pd.DataFrame.from_dict(self.create_dict())
        for index, row in self._df.iterrows():
            self._df.loc[index, 'endDate'] = self.convert_timestamp(self._df.at[index, 'endDate'])
        self._df = self._df.iloc[::-1]
        return self._df

    def plot(self):
        self._save_all_plots(self._df)



if __name__ == '__main__':
    data = BalanceSheetQ('INVE-B.ST')
    df = data.to_df()
    data.df.plot()

