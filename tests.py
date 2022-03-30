from app import app, RatesNotAvailableError
from unittest import TestCase

class get_tests(TestCase):
    '''Test for get status response and loading of the form'''

    def test_currency_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

        print("running get_test---------------------------------")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("<h1>Currency Converter</h1>", html)


class post_tests(TestCase):
    '''Test for post response, accurately returning a result of some sort and checking that the currency symbol is included'''

    def test_currency_home(self):
        with app.test_client() as client:
            resp = client.post('/', data={'convert-from': 'gBp', 'convert-to':'UsD', 'amount': '50.2'})
            html = resp.get_data(as_text=True)

        print('running post_test--------------------------------')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h2 id="result">', html)
        self.assertIn('$', html)


class currency_error_test(TestCase):
    '''Test for incorrect currency codes: If someone inserts incorrect code identifiers it should raise an error'''

    def test_currency_home(self):
        with app.test_client() as client:
            client.post('/', data={'convert-from': 'aete', 'convert-to':'USD', 'amount': '100'})

        print('running currency_error_test----------')
        self.assertRaises(RatesNotAvailableError)


class amount_error_test(TestCase):
    '''Test for incorrect answers in amount input: If someone inserts non-numeric values the app should raise a ValueError'''

    def test_currency_home(self):
        with app.test_client() as client:
            client.post('/', data={'convert-from': 'USD', 'convert-to':'GBP', 'amount': 'not a number'})

        print('running amount_error_test----------')
        self.assertRaises(ValueError)
