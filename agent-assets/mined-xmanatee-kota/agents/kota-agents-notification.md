# Notification Module

This module owns shared notification delivery primitives used by notification channel modules (slack, webhook).

- `postWithRetry` is the core primitive: policy-aware HTTP POST with
  exponential-backoff retry. Tests inject the outbound request port, not a
  parallel fetch implementation.
- Notification channel modules that use shared delivery declare this module as a dependency.

## Boundaries

- Does not own channel-specific formatting, config, or event subscriptions (those belong in each channel module).
- Does not own SMTP delivery (the email module handles that independently).
