import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase


class SimpleTest(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_main_route(self):
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
