"""
Demo script that starts a server which exposes liver segmentation.

Based off of https://github.com/morpheus-med/vision/blob/master/ml/experimental/research/prod/model_gateway/ucsd_server.py
"""

import logging.config
import yaml
import numpy
import pydicom
from PIL import Image

from chexnet.chexnet import Xray
from utils import tagged_logger

# ensure logging is configured before flask is initialized

with open('logging.yaml', 'r') as f:
    conf = yaml.safe_load(f.read())
    logging.config.dictConfig(conf)

logger = logging.getLogger('inference')

from gateway import Gateway


def handle_exception(e):
    logger.exception('internal server error %s', e)
    return 'internal server error', 500


def get_empty_response():
    response_json = {
        'protocol_version': '1.0',
        'parts': []
    }
    return response_json, []


def get_prediction_covid(dicom_instances):
    response_json = {
        'protocol_version': '1.0',
        'parts': []
    }
    for dicom_file in dicom_instances:

        dcm = pydicom.read_file(dicom_file)
        dataset = dcm.pixel_array
        img = Image.fromarray(dataset)
        result_data = x_ray.predict(img)
        if result_data['result'] == 'RANDOM':
            response_json['parts'].append(
                {
                    'result': "Invalid Image"
                }
            )
        else:
            response_json['parts'].append(
                {
                    'result': result_data['result'],
                    'type': result_data['type'],
                    'probability': str(round(result_data['probability'], 2))
                }
            )

    return response_json, []


def request_handler(json_input, dicom_instances, input_digest):
    """
    A mock inference model that returns a mask array of ones of size (height * depth, width)
    """
    transaction_logger = tagged_logger.TaggedLogger(logger)
    transaction_logger.add_tags({'input_hash': input_digest})
    transaction_logger.info('mock_model received json_input={}'.format(json_input))

    if json_input['inference_command'] == 'covid19':
        return get_prediction_covid(dicom_instances)
    else:
        return get_empty_response()


if __name__ == '__main__':
    x_ray = Xray()
    app = Gateway(__name__)
    app.register_error_handler(Exception, handle_exception)
    app.add_inference_route('/', request_handler)

    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=True)
