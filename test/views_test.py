from flask import Flask
from flask_testing import TestCase

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from view import view
from room_manager import SCECRET_KEY

class TestViews(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["SECRET_KEY"] = SCECRET_KEY
        app.config['TESTING'] = True
        app.register_blueprint(view)
        return app
    
    def test_home_get(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('home.html')
    