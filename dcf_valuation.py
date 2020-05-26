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

    def extract_raw(func):
      """Decorator to remove keys from from json data 
      that is retreived from the yahoo-module
      """
      def wrapper_extract_raw(self, *args, **kwargs):
        sheet = func(self)
        for items in sheet:
            for key, value in items.items():
                if type(value) == dict and 'fmt' in value:
                    del value['fmt']
                if type(value) == dict and 'longFmt' in value:
                    del value['longFmt']
        return sheet
      return wrapper_extract_raw

    def create_dict(self):
        balance_sheet = []
        temp_data = self._dict
        for d in temp_data:
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

class BalanceSheetQ(YahooFin):

  def __init__(self, ticker):
    super().__init__(ticker)
    self._module = 'balanceSheetHistoryQuarterly'
    self._url = (f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'
                    f'{self.ticker}?'
                    f'modules={self.module}')
    self._dict = self._balance_sheet()
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

  @YahooFin.extract_raw
  def _balance_sheet(self):
      data = self.data()
      query =  data[0]
      balance_sheet_qty = query['balanceSheetHistoryQuarterly']
      balance_sheet_statements = balance_sheet_qty['balanceSheetStatements']
      return balance_sheet_statements



class IncomeStatementQ(YahooFin):

  def __init__(self, ticker):
        super().__init__(ticker)
        self._module = 'incomeStatementHistoryQuarterly'
        self._url = (f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'
                    f'{self.ticker}?'
                    f'modules={self.module}')
        self._dict = self._income_statement()
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

  @YahooFin.extract_raw
  def _income_statement(self):
      data = self.data()
      query =  data[0]
      income_statement_qty = query['incomeStatementHistoryQuarterly']
      income_statement_statements = income_statement_qty['incomeStatementHistory']
      return income_statement_statements


if __name__ == '__main__':
    data = IncomeStatementQ('INVE-B.ST')
    print(data.to_df())

