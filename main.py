import argparse
import json
import logging

import requests


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


CLASSIFICATION = {
    'UNDEFINED': 0,
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3,
}


def load_output(source_file):
    with open(source_file, 'r') as f_:
        return json.loads(f_.read())


def parse(output):
    distribution = {
        'UNDEFINED': 0,
        'LOW': 0,
        'MEDIUM': 0,
        'HIGH': 0,
    }

    results = []
    for idx, result in enumerate(output['results']):
        issue_severity = result['issue_severity']
        distribution[issue_severity] += 1
        issue_confidence = result['issue_confidence']
        results.append(
            (
                idx,
                CLASSIFICATION[issue_severity],
                CLASSIFICATION[issue_confidence],
                result['filename'],
                result['issue_text'],
                result['code'],
                result['line_number'],
                issue_severity,
            )
        )

    sorted_by_severity = sorted(results, key = lambda x: x[1], reverse=True)
    sorted_by_confidence = sorted(sorted_by_severity, key = lambda x: x[2], reverse=True)
    return sorted_by_confidence[:2], distribution

def build_slack_message(parsed_list, distribution, repo_name):
    header = (
        f"*Security Control:* Bandit\n"
        f"*Repo:* {repo_name}\n"
        f"*Run time:* 9/6/2021 18:20:12\n"
        f"*Output:* Link\n"
        f'*Findings:* High ({distribution["HIGH"]}), Medium ({distribution["MEDIUM"]}), Low ({distribution["LOW"]})\n\n\n'
        f"*Top Findings:*"
    )

    msg_data = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": header
            }
        },
        {
            "type": "divider"
        },
    ]

    for idx, finding in enumerate(parsed_list):
        name = finding[4]
        file_name = finding[3]
        line = finding[6]
        severity = finding[7]
        code = finding[5]
        block_text = f"*Finding #{idx+1}*\n\n*Name:* {name}\n*Filename:* {file_name}\n*Line number:* {line}\n*Severity:* {severity}\n```{code}```"

        block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": block_text
            }
        }

        msg_data.append(block)

    return msg_data


def message_slack(token, channel_id, msg):
    post_body = {
        'channel': channel_id,
        'blocks': msg,
    }

    url = 'https://slack.com/api/chat.postMessage'
    logger.info('POST {0}'.format(url))

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json; charset=utf-8',
    }

    response = requests.post(url, data=json.dumps(post_body), headers=headers)
    if response.status_code != 200:
        raise Exception(f'received \'{response.status_code}\' body: {response.content}')

    json_data = response.json()
    if not json_data['ok']:
        raise Exception(f'json response not ok: {json_data}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--slack-token', type=str, dest='slack_token', help='slack token')
    parser.add_argument('--slack-channel-id', type=str, dest='slack_channel_id', help='slack channel id')
    parser.add_argument('--output-file', type=str, dest='output_file', help='name of bandit output file')
    parser.add_argument('--repo-name', type=str, dest='repo_name', help='name of repo scanned')

    params = parser.parse_args()

    output = load_output(params.output_file)
    parsed_list, distribution = parse(output)
    if parsed_list:
        slack_message = build_slack_message(parsed_list, distribution, params.repo_name)
        message_slack(params.slack_token, params.slack_channel_id, slack_message)
