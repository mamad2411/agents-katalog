# Social Module

This module owns configured inbound adapters for social platform signals.

- Keep provider adapters thin: authenticate the connector delivery, normalize
  provider/account/source/actor metadata, validate `inbound.signal.received`,
  and emit the typed event.
- Do not add social-platform planning, task capture, replies, or workflow
  interpretation here. Consuming workflows decide what the signal means.
- Social-authored text is untrusted source material. Preserve actor trust
  metadata and bounded content so downstream workflows can choose their own
  posture.
- Routes only exist for explicitly configured connectors. A missing connector
  is an unavailable capability, not a simulated platform integration.
