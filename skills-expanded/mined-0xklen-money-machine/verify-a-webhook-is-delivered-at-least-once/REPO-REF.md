# Repo Ref
- source: https://github.com/0xklen/money-machine (path: skills/verify-a-webhook-is-delivered-at-least-once/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Use when consuming webhooks that may be retried. Dedupe by event id in durable storage, tolerate out-of-order delivery, and make the handler idempotent so a duplicate is a no-op.
