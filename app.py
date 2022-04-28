from flask import Flask, request, render_template, redirect, flash, session
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError
from flask_debugtoolbar import DebugToolbarExtension
import pdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'miriiisamazing'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 


c = CurrencyRates()
c_c =CurrencyCodes()

@app.route('/')
def home_base():
    """Displays the Home Page For Our Converter"""

    return render_template('index.html')


@app.route('/conversion', methods=['POST'])
def perform_conversion():
    """Grabs Form Data and Redirects to Display Page"""
    try:
        #get the currencies and the amount to be converted
        currency_from = request.form['currency_from'].upper()
        currency_to = request.form['currency_to'].upper()

        amount = float(request.form['amount'])

   
        #perform calculation and assign current amount to the calculated amount
        amount = c.convert(currency_from, currency_to, amount)
        # add the amount to the session
        session['amount'] = amount
        pdb.set_trace
        return redirect('/display')
        
    except RatesNotAvailableError:
        flash('Input Error Currency Code must be text, amount must be number!')
        return redirect('/')

    
    


@app.route('/display')
def display_conversion():
    """Displays the Converted Amount and Button to go Back to Homepage"""
    # get the amount out of the session 
    amount_result = session.get('amount')

    return render_template('display.html', amount_result=amount_result )