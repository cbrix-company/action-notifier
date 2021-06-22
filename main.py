import argparse
import logging
import sys

from notifiers import message_slack


logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--message-type', type=str, dest='message_type', help='message type', choices=['slack'], required=True)
    parser.add_argument('--message', type=str, dest='message', help='parser message from action-message', required=True)
    parser.add_argument('--slack-token', type=str, dest='slack_token', help='slack token', required=False)
    parser.add_argument('--slack-channel-id', type=str, dest='slack_channel_id', help='slack channel id', required=False)

    params = parser.parse_args()

    if params.message_type == 'slack':
        message_slack(params.slack_token, params.slack_channel_id, params.message)
    else:
        sys.exit(f"'{params.message_type}' is not a supported message type")
