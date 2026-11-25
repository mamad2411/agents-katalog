---
name: xero-chart-of-accounts-manager
description: Safely inspect and manage a Xero Chart of Accounts. Use when listing accounts, finding account codes, preparing new accounts, or creating accounts through an authenticated Xero integration.
disable-model-invocation: true
---

# Xero Chart of Accounts Manager

Use this skill to inspect a Xero organisation's Chart of Accounts and to
prepare or create accounts with an authenticated Xero integration.

## Guardrails

- Treat account creation as a financial-system change. Show the proposed
  account code, name, type, tax type, and description, then obtain explicit
  confirmation before creating it.
- Never expose, request in chat, log, or commit Xero client secrets, access
  tokens, refresh tokens, tenant IDs, or exported account data unless the user
  has supplied it through an approved secret-handling mechanism.
- Select the target organisation explicitly when more than one Xero tenant is
  connected. State the selected organisation before performing a write.
- Do not modify, archive, delete, merge, or reclassify accounts with this
  skill. Explain that those actions require a separate, reviewed workflow.
- Do not infer a tax type or account type when the user has not specified one.
  Ask for the missing information or direct them to their accountant.
- This skill helps operate Xero; it does not provide accounting, tax, or legal
  advice.

## Prerequisites

Before accessing Xero, verify that an approved Xero integration is available
and authenticated with the least-privilege scopes needed to read accounts. A
write additionally needs permission to create accounts. If the integration is
not connected, direct the user to complete the organisation's approved OAuth
connection flow rather than asking them to paste credentials or tokens.

## Workflow

### 1. Establish the request

Identify whether the user wants to:

- list all accounts;
- find accounts by code, name, type, or status; or
- create a new account.

For listing and searching, ask for structured criteria. Do not accept or
execute arbitrary expressions as filters. Report results in a stable table or
CSV with account code, name, type, tax type, description, status, and account
ID when available.

### 2. Inspect before changing

For a request to create an account:

1. Select the Xero tenant explicitly.
2. Search existing accounts for the requested code and a similar name.
3. Report any conflict or likely duplicate and stop for the user's decision.
4. Validate that the requested account type and tax type are supported by the
   connected Xero organisation.
5. Present the complete proposed account as a reviewable summary.

### 3. Confirm and create

Create an account only after the user explicitly confirms the exact summary.
After a successful creation, report the returned account code, name, and ID.
If creation fails, report the error without exposing credentials, tokens, or
other sensitive response data. Do not retry a write automatically.

## Information to collect for a new account

| Field | Required | Notes |
| --- | --- | --- |
| Account code | Yes | Must be unique in the selected organisation. |
| Account name | Yes | Check for similar existing names first. |
| Account type | Yes | Use a Xero-supported type for the organisation. |
| Tax type | No | Obtain the user's or accountant's direction when relevant. |
| Description | No | Keep it clear enough for future operators. |
| Tenant | Yes when multiple are connected | Never silently use an ambiguous organisation. |

## Attribution

This skill adapts the Chart of Accounts use case from
[xero-fin-ops](https://github.com/Cogni-AI-OU/xero-fin-ops), specifically its
`scripts/xero_coa_manager.py` utility, by Cogni AI OÜ. The upstream project is
licensed under the MIT License; the complete license and copyright notice are
preserved in [LICENSE](LICENSE). See [ATTRIBUTION.md](ATTRIBUTION.md) for the
source version and adaptation details.
