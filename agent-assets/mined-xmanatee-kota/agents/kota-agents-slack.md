# Slack Module

This directory owns the Slack notification module — routes KOTA notification events to a Slack Incoming Webhook.

- No OAuth app or bot token required; only a Slack Incoming Webhook URL.
- Optional event filters must not suppress urgent owner/approval escalation
  notifications.
- Keep the subscription lists typed against the event bus so removed events fail
  in code rather than drifting in docs.
- Uses `postWithRetry` from the `notification` module for delivery with exponential-backoff retry.
- Declares a dependency on the `notification` module.

## Boundaries

- Does not own Telegram or generic webhook notification (those belong in `telegram/` and `webhook/`).
- Does not own inbound Slack interactions or slash commands.
- Does not own retry logic (that lives in the `notification` module).
