import argparse
import logging
import sys

from notifiers import message_slack


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--message-type', type=str, dest='message_type', help='message type', choices=['slack'], required=True)
    parser.add_argument('--message-file', type=str, dest='message_file', help='file containing the message', required=True)
    parser.add_argument('--slack-token', type=str, dest='slack_token', help='slack token', required=False)
    parser.add_argument('--slack-channel-id', type=str, dest='slack_channel_id', help='slack channel id', required=False)

    params = parser.parse_args()

    with open(params.message_file, 'r') as f:
        message = f.read()

    if params.message_type == 'slack':
        message_slack(params.slack_token, params.slack_channel_id, message)
    else:
        sys.exit(f"'{params.message_type}' is not a supported message type")
