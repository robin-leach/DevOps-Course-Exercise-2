import requests
import json
import logging

log = logging.getLogger('app')

def make_trello_request(method, endpoint, params):
    log.debug(
    f"""Sending HTTP request to Trello API.
        Method: {method.value}
        URL: {endpoint}
        Parameters: {json.dumps(params)}
    """
    )

    response = requests.request(method.value, endpoint, params=params)
    details = f'{len(response.json())} items found.' if method == "GET" else ''
    log.debug(f'Trello returned {response.status_code}.{details}')

    return response