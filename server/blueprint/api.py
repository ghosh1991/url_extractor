from flask import Blueprint, current_app, request
import logging
from flask_api import status
import json

from extract.url_data_extractor import Extractor


api = Blueprint('api', __name__)


@api.route('/url/', methods=['POST'])
def shorten_url():
    url = request.get_data().decode("utf-8")
    try:
        obj = Extractor(url)
        url_data = obj.extract_all_data()
        return json.dumps(url_data), status.HTTP_200_OK
    except OSError:
        logging.error('Error occurred while getting data from url')
        return "Web page parsing error", status.HTTP_500_INTERNAL_SERVER_ERROR


