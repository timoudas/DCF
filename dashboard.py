# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from dcf_valuation import BalanceSheetQ
from dcf_valuation import YahooFin




# def gen_data(ticker):
#   bal_sheet = BalanceSheetQ(ticker)
#   data = bal_sheet.to_df()
#   data = data.set_index('endDate')
#   data = data.applymap(lambda x: x / 1000000000)
#   return data

# def generate_table(dataframe, max_rows=10):
#     return dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in df.columns],
#     data=df.to_dict('records'),
# )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

ticker_default = 'AAPL'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    dcc.Input(
        id='ticker', 
        value='AAPL', 
        type="text"
    ),

    html.Button(
        'Submit', 
        id='button'
    ),

    html.Div(
        id='ticker_header'
    ),
    # html.Div('DCF_valuation' +' '+ ticker_default, id='ticker_header')
     html.Div(
        id='table',
        
    )
])

@app.callback(
    [
    Output('ticker_header', 'children'),
    ],
    [

        Input('button', 'n_clicks'),

    ],
    [
        State('ticker', 'value'),
        #State(component_id='ticker_header', component_property='value'),

    ]
)
def update_ticker_header(n_clicks, ticker):
    return [html.H1('DCF Valuation ' + f'{ticker}')]

@app.callback(
    [
    Output('table', 'children'),
    ],
    [

        Input('button', 'n_clicks'),

    ],
    [
        State('ticker', 'value'),
        #State(component_id='ticker_header', component_property='value'),

    ]
)
def update_ticker_header(n_clicks, ticker):
    try:
        df = BalanceSheetQ(ticker).to_df()
        print(df)
        columns = [{'name': col, 'id': col} for col in df.columns]
        data = df.to_dict('rows')
        return [dash_table.DataTable(
                    data=data, 
                    columns=columns,
                    style_table={'overflowX': 'auto'},
                    )]
    except KeyError as e:
        return [html.H2('There is not ticker: ' f'{ticker}')]


if __name__ == '__main__':
    app.run_server(debug=True)