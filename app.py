from flask import Flask,render_template,request
import json 
from send import extract_stocks_data
from main import get_stocks
app = Flask(__name__)
with open('stocks.json', 'r') as file:
    stock_data = json.load(file)

@app.route("/")
def index():
    return render_template("first.html")



@app.route("/indian_stocks")
def indian_stocks():
    return render_template("indianstocks.html",stocks=stock_data)


@app.route('/output')
def output():
    extract_stocks_data()
    return render_template('output.html')



@app.route('/pricing', methods=['GET', 'POST'])
def pricing():
    return render_template('pricing.html',show_price=False)


@app.route('/stock_price',methods=['POST'])
def get_stock_price():
    if request.method == 'POST':
        stock_name = request.form['stock_name']
        company_name = request.form['company_name']
        stocks = get_stocks(stock_name,company_name)
    # Add logic to fetch and display the stock price for the given stock_name
        return render_template('pricing.html',show_price=True, stocks = stocks )  # Example stock price









if __name__ == "__main__":
    app.run()