import logging
from doctest import debug

from flask import Flask
from routes import phone_tracker_rout
from init_db import init_driver


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['LOGGING_LEVEL'] = logging.DEBUG

app.register_blueprint(phone_tracker_rout)

if __name__ == '__main__':
    with app.app_context():
        init_driver("bolt://neo4j:7687", "neo4j", "password")
    app.run(host='0.0.0.0', port=5000, debug=True)