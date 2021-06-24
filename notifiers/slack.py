import json
import logging

import requests


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


def message_slack(token, channel_id, msg):
    body = json.loads(msg)
    body['channel'] = channel_id

    url = 'https://slack.com/api/chat.postMessage'
    logger.info('POST {0}'.format(url))

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json; charset=utf-8',
    }

    response = requests.post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        raise Exception(f'received \'{response.status_code}\' body: {response.content}')

    json_data = response.json()
    if not json_data['ok']:
        raise Exception(f'json response not ok: {json_data}')
