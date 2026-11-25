---
name: ec2-ttl-alert
description: Deploy or update a small EC2 TTL tag alert workflow using Lambda, SNS, and EventBridge. Use when you need daily alerts for missing, expired, or soon-to-expire `TTL=YYYY-MM-DD` tags on EC2 instances in a single AWS account.
---

# EC2 TTL Alert

Use this skill to deploy a simple daily EC2 TTL alert per account.

## Use when

- you want a lightweight daily TTL review for EC2
- you need alerts for expired, expiring, or missing `TTL` tags
- you want a small Lambda + SNS + EventBridge path without a full monitoring stack

## Do not use when

- you need cross-account scanning from one Lambda
- you need central inventory or automated stop/terminate actions
- you need a full policy/compliance platform

## Workflow

1. deploy the workflow to one account/profile at a time
2. confirm SNS email subscriptions
3. test invoke once
4. review the alert body and scheduled rule

## Important guardrails

- this skill is single-account by default
- do not claim multi-profile Lambda support unless assume-role logic is added
- keep outputs under:
  - `~/.AGENTS-temp/agent-skills/ec2-ttl-alert/`

## Main scripts

### Deploy

```bash
bash scripts/deploy-ec2-ttl-alert.sh <profile> [region]
```

Environment overrides:

- `TTL_ALERT_EMAILS`
  - space-separated email addresses
- `TTL_ALERT_WARN_DAYS`
  - default `3`
- `TTL_ALERT_FUNCTION_NAME`
  - default `ec2-ttl-checker`
- `TTL_ALERT_TOPIC_NAME`
  - default `ec2-ttl-alerts`
- `TTL_ALERT_RULE_NAME`
  - default `ec2-ttl-daily`

### Lambda source

- `scripts/ttl_checker.py`

## Expected behavior

The Lambda scans `running` and `stopped` instances in the current account and
alerts on:

- missing `TTL`
- invalid `TTL`
- expired `TTL`
- `TTL` expiring within the warning window

## Output location

Keep packaging and test outputs under:

```bash
~/.AGENTS-temp/agent-skills/ec2-ttl-alert/
```
