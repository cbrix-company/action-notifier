# Cbrix Notifier

This action accepts a message from [cbrix-company/action-messages](https://github.com/cbrix-company/action-messages) and notifies on the specified communication channel.

Supported channels:
* Slack

## Example usage

```yaml
- name: Parse Bandit output
  id: bandit-message
  uses: cbrix-company/action-messages@v1
  with:
    tool: bandit
    input-file: 'bandit.json'
    message-type: slack
    repo-name: $GITHUB_REPOSITORY

- name: Nofify about Bandit findings
  uses: cbrix-company/action-notifier@v1
  with:
    message: steps.bandit-message.outputs.message
    message-type: slack
    slack-token: ${{ secrets.SLACK_TOKEN }}
    slack-channel: ${{ secrets.SLACK_CHANNEL_ID }}
```
