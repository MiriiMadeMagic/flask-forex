"""Sample test suite for testing demo."""

from unittest import TestCase
from app import app
from flask import session

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class ForexAppTest(TestCase):
    """Testing Forex Flask App"""

    def test_root_route(self):
        with app.test_client() as client:
            # get root route and piece of html to verify
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Convert Me! </h1>', html)

    def test_currency_submit(self):
        with app.test_client() as client:
            resp = client.post('/conversion',
                           data={'currency_from': 'USD', 'currency_to': 'EUR', 'amount' : 75})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn('<h1> Your Result is! </h1>', html)


    def test_redirection(self):
        with app.test_client() as client:
            resp = client.get("/conversion")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")

    def test_redirection_followed(self):
        with app.test_client() as client:
            resp = client.get("/display", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Your Result is! </h1>', html)

