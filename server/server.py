"""  Server """

from flask import Flask
from server.blueprint.api import api


app = Flask(__name__)
app.register_blueprint(api)


def run_server():
    """

    :return:
    """
    app.run(host='0.0.0.0', port=8000)
