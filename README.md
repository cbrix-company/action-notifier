# Cbrix Bandit Slack Notifier

This action notifies based on Bandit json output to a slack channel

## Example usage

```yaml
- name: Bandit Notifier
  uses: cbrix-company/action-notifier@v1
  with:
    slack-token: ${{ secrets.SLACK_TOKEN }}
    slack-channel: ${{ secrets.SLACK_CHANNEL_ID }}
    output-file: 'bandit_output.json'
    repo-name: $GITHUB_REPOSITORY
```
