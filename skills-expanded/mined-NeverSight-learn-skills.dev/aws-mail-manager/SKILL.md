---
name: aws-mail-manager
description: Process, route, filter, and archive inbound email with Amazon SES Mail Manager. Use when building email ingress pipelines, spam/IP filtering, compliance archiving, SMTP relay forwarding, address allow/block lists, or any inbound email processing workflow. Covers ingress points, traffic policies, rule sets, relays, archives, and address lists.
license: Apache-2.0
compatibility: Requires AWS credentials (IAM user, role, or environment variables) and an AWS account with Amazon SES Mail Manager enabled. Python SDK — boto3 with client name 'mailmanager'. Available in all commercial AWS regions where SES is offered (27 regions as of December 2025). See https://aws.amazon.com/about-aws/whats-new/2025/12/ses-mail-manager-10-regions/ for the latest availability.
metadata:
  author: aws
  version: "1.0"
  service: mailmanager
  revision: 1
  updated-on: "2026-03-20"
  source: maintainer
  tags: "ses,mail-manager,email,smtp,ingress,archive,relay,traffic-policy,rule-set"
---

# Amazon SES Mail Manager

Amazon SES Mail Manager is an email processing service for inbound email. It receives email via SMTP ingress points, applies traffic policies and rule sets, then routes messages to archives, relays, S3, SNS, WorkMail, or drops them.

## Key Capabilities

- **Ingress Points** — SMTP endpoints (OPEN, AUTH, or MTLS) that receive email. Point your MX records here. Configurable TLS policy: `REQUIRED`, `OPTIONAL`, or `FIPS`.
- **Traffic Policies** — Connection-level filtering by sender IP, recipient, or TLS version. Evaluated before message body is received.
- **Rule Sets** — Message-level processing with conditions (SPF/DKIM verdicts, headers, size, IP) and actions (archive, bounce, relay, S3, SNS, Lambda, drop).
- **SMTP Relays** — Forward email to external SMTP servers with optional authentication.
- **Archives** — Durable email storage with async search and export. Configurable retention from 3 months to permanent.
- **Address Lists** — Managed allow/block lists used in rule conditions. Supports bulk CSV/JSON import.
- **Add-ons** — Third-party integrations (spam filtering, threat analysis) attachable to rule sets.

## When to Use This Skill

- Setting up an inbound email processing pipeline
- Walking a developer through Mail Manager configuration decisions step by step
- Filtering spam or blocking senders/IP ranges before email reaches your systems
- Archiving email for compliance, legal hold, or eDiscovery
- Routing email to different destinations based on recipient, sender, or content
- Forwarding email to on-premises or third-party SMTP servers
- Building allow/block lists for email filtering
- Enforcing TLS requirements on inbound connections

## What This Skill Does NOT Cover

- **Outbound email sending** — Use the Amazon SES V2 API (`sesv2` client) for sending email.
- **SES core features** — Identity verification, DKIM/SPF/DMARC setup, configuration sets, suppression lists. See the `aws-ses` skill.
- **WorkMail setup** — Mail Manager can deliver to WorkMail mailboxes, but WorkMail provisioning is a separate service.

## Common Mistakes (Quick Reference)

| Mistake | Fix |
|---------|-----|
| Using `ses` or `sesv2` client | Use `boto3.client('mailmanager')` |
| Creating ingress point first | Create traffic policy + rule set first |
| `RecipientCondition` in traffic policy | Use `StringExpression` with `Attribute: RECIPIENT` |
| `Values` in TlsExpression | Use singular `Value` for TLS expressions |
| Missing `DefaultAction` on traffic policy | Always set `DefaultAction: ALLOW` or `DENY` |
| `SOURCE_IP` in traffic policy | Traffic policies use `SENDER_IP`; rule sets use `SOURCE_IP` |
| Updating rule set without fetching first | `update_rule_set` replaces ALL rules — fetch first |
| DNS before ingress point is ACTIVE | Poll `get_ingress_point` until `Status == ACTIVE` |
| `Evaluate` field in DmarcExpression | DmarcExpression has no `Evaluate` — just `Operator` + `Values` |
| Archive ARN in `TargetArchive` | Use archive ID (`a-xxxx`), not ARN — 66-char limit enforced by API |
| CFN `!GetAtt Archive.ArchiveId` returns ARN | Extract ID: `!Select [1, !Split ["/", !GetAtt Archive.ArchiveArn]]` |
| Archive name collision after rollback | Append `${AWS::AccountId}` — names persist through `PENDING_DELETION` |
| FIPS TLS policy can't be changed | `FIPS` is immutable after creation — delete and recreate to change |
| TLS policy default varies by region | `FIPS` in US/CA, `REQUIRED` elsewhere — set explicitly |

See [Agent Instructions](references/agent-instructions.md) for detailed explanations, full condition/action syntax, and the complete common mistakes list.

## Resource Links

- [Agent Instructions](references/agent-instructions.md) — Full workflow patterns, condition/action reference, agent instructions
- [Getting Started Guide](references/setup/getting-started.md)
- [Traffic Policy Guide](references/traffic-policies/traffic-policy-guide.md)
- [Rule Set Guide](references/rule-sets/rule-set-guide.md)
- [Archive Guide](references/archives/archive-guide.md)
- [Relay Guide](references/relays/relay-guide.md)
- [Address List Guide](references/address-lists/address-list-guide.md)
- [Cleanup Guide](references/cleanup/cleanup-guide.md)
- [Troubleshooting Guide](references/troubleshooting/troubleshooting-guide.md)
- [Guided Setup Decision Tree](references/workflows/guided-setup.md)
- [Event-Driven AI Pipeline](references/workflows/event-driven-ai-pipeline.md)
- [SES v2 + Mail Manager API Index](references/api/ses-api-index.md)
- [Examples](examples/README.md)
- [Mail Manager Developer Guide](https://docs.aws.amazon.com/ses/latest/dg/mail-manager.html)
- [API Reference](https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_Operations_Amazon_SES_Mail_Manager.html)

## Summary

This skill provides the context AI agents need to work with Amazon SES Mail Manager correctly — the right API client, condition/action syntax, resource dependency order, and common pitfalls. Start with the [Agent Instructions](references/agent-instructions.md) for the full reference, or use the [Guided Setup](references/workflows/guided-setup.md) for an interactive walkthrough.
