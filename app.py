from flask import Flask, render_template, request
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ihHIethina462Ha'

@app.route('/', methods=['GET', 'POST'])
def currency_home():
    '''Render form for currency conversion and display results once submitted'''

    if request.method == 'POST':
        '''Once form is posted, handle data, return the result at the top of the form'''

        c = CurrencyRates()
        code = CurrencyCodes()

        conv_from = request.form.get('convert-from').upper()
        conv_to = request.form.get('convert-to').upper()
        amount = request.form.get('amount')
        symb = code.get_symbol(conv_to)

        # convert amount value to a float. If a nonnumerical value is passed in it will raise a Value error
        # if either currency is not valid it will raise RatesNotAvailableError
        # convert currency using form data then round to 2 decimal places before passing back to the webpage
        try:
            converted = round(c.convert(conv_from, conv_to, float(amount)), 2)
            result = f"{amount} {conv_from} = {symb} {converted} {conv_to}"

        except ValueError:
            result = "Make sure the amount is a valid number"

        except RatesNotAvailableError:
            result = "Recheck your currency codes"

        finally:
            return render_template("home.html", result= result)

    return render_template("home.html")
