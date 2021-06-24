# Cbrix Notifier

This action accepts a message from [cbrix-company/action-messages](https://github.com/cbrix-company/action-messages) and notifies on the specified communication channel.

Supported channels:
* Slack

## Example usage

```yaml
- name: Render Bandit output for slack
  id: bandit-to-slack
  uses: cbrix-company/action-messages@v1
  with:
    tool: bandit
    input-file: 'bandit_output.json'
    renderer: slack

    repository: ${{ github.repository }}
    ref: ${{ github.ref }}
    actor: ${{ github.actor }}
    run_id: ${{ github.run_id }}
    sha: ${{ github.sha }}


- name: Nofify about Bandit findings
  uses: cbrix-company/action-notifier@v1
  with:
    message-type: slack
    message-file: steps.bandit-message.outputs.output-file
    slack-token: ${{ secrets.SLACK_TOKEN }}
    slack-channel: ${{ secrets.SLACK_CHANNEL_ID }}
```
