from dcf_valuation import BalanceSheetQ
from dcf_valuation import YahooFin
from flask import Flask
from flask import render_template
from flask import url_for
from forms import TickerForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f8392ef05f0080c78dd92a7d1c5d623b'



@app.route("/")
@app.route("/home")
def home():
	ticker = 'AAPL'
	bal_sheet = BalanceSheetQ(ticker)
	data = bal_sheet.to_df()
	data = data.set_index('endDate')
	data = data.applymap(lambda x: x / 1000000000)
	return render_template('home.html',tables=[data.to_html(classes='dates')],
    titles = ['BalanceSheetQ', ticker])

@app.route("/about")
def about():
	return render_template('about.html')




if __name__ == '__main__':
	app.run(debug=True)