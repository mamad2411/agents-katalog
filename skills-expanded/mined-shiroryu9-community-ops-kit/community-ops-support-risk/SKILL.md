---
name: community-ops-support-risk
description: Use when triaging community support issues, payment or access problems, moderation incidents, trust and safety concerns, permission/role changes, complaints, escalation paths, public-risk copy, evidence gaps, or operations that could affect user rights, privacy, rewards, discounts, webhooks, bots, or official claims.
---

# Community Ops Support Risk

Use this skill when a community issue touches support, safety, payments, permissions, public claims, moderation, privacy, rewards, discounts, roles, DMs, webhooks, bots, or official account actions.

## Project Inputs

Get the issue type, severity, confirmed facts, timestamps, minimum necessary user or record reference, evidence paths or IDs, applicable policy, desired resolution, and public/private boundary from the user or an approved source.

The skill supplies triage and escalation structure. It does not include a community's policy, compensation rules, account state, payment facts, moderation history, or permission data. Missing evidence remains missing. Do not import outcomes from examples, and do not request secrets, full private-message histories, payment details, or unrelated personal data.

## Triage First

Classify the issue:

- access/role/permission;
- payment/discount/entitlement;
- support bug or product issue;
- moderation/safety/rules;
- reward/winner/benefit dispute;
- public copy or official claim risk;
- privacy or sensitive user data.

## Risk Rule

Use the minimum access and user data needed to understand the issue. Do not execute public messaging, DMs, mentions, financial actions, rewards, discounts, role/channel/permission changes, bot/webhook changes, deletions, or official claims without explicit confirmation. When evidence is missing, ask for it or mark the item blocked.

## Output Pattern

```md
**Issue Type**
[Category and severity.]

**Confirmed Facts**
- [Who/what/where/when/evidence.]

**Missing Evidence**
- [IDs, screenshots, links, logs, policy, owner decision, etc.]

**Recommended Action**
| Priority | Action | Owner | Public/private | Risk |
|---|---|---|---|---|

**Do Not Do Yet**
- [Any send, role edit, reward, discount, DM, public claim, webhook/bot change, or deletion that needs confirmation.]

**User-Facing Draft**
[Only if requested; keep it factual and low-commitment.]
```

## Guardrails

Do not invent policy, compensation, blame, timelines, or official product status. Do not store secrets, webhook URLs, raw private messages, personal profiles, or unnecessary sensitive data. Preserve evidence paths and timestamps when available.
