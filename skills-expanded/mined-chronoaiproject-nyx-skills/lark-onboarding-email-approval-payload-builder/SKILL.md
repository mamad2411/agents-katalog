---
name: lark-onboarding-email-approval-payload-builder
version: "1.1"
description: Builds the connector-ready Lark approval instance payload for the onboarding email approval flow. Use after Aevatar has received a Lark/Base onboarding event and before calling the NyxID Lark approval connector.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - onboarding
    - lark-approval
    - payload-builder
  clawdbot:
    emoji: "mailbox_with_mail"
    files:
      - "references/*"
      - "scripts/*"
---

# Lark Onboarding Email Approval Payload Builder

Use this skill when an Aevatar-native onboarding flow needs to create the Lark approval instance payload for a new employee email account.

This skill does one thing: turn an onboarding event into a deterministic payload for `POST /open-apis/approval/v4/instances`. It does not fetch tenant tokens, store Lark credentials, submit the approval, or handle approval callbacks.

## When to use

Use for `lark-onboarding-email-approval` when the caller has an onboarding event with:

- Lark display name
- department
- onboarding date
- submitter/operator Lark user id

The original n8n flow is a short linear flow: webhook, format fields, get Lark tenant token, call approval instance API, respond. This skill replaces only the formatting step.

## Inputs

Required input keys, after alias normalization:

- `larkName`
- `department`
- `startDate`
- `operatorId`

Optional input keys:

- `approvalCode`
- `companyDomain`
- `requestDate`
- `autoSubmitLabel`

Field aliases, email generation rules, Lark widget ids, and output shape are defined in `references/onboarding-email-approval-contract.md`.

## Output

Return one JSON object with:

- `summary`
- `employee`
- `emailRequest`
- `requestDetail`
- `form`
- `lark.body`

The returned `lark.body` is connector-ready for:

```text
POST /open-apis/approval/v4/instances
```

## Determinism requirement

Follow `references/onboarding-email-approval-contract.md`. If executing code is allowed, use `scripts/build_onboarding_email_approval_payload.js` as the reference implementation. If executing code is not allowed, reproduce the same transformations exactly.

Do not invent employee data, Lark app credentials, tenant tokens, approval definitions, operator ids, or approvers.

## Failure behavior

If any required field is missing, return:

```json
{
  "needs_more_information": true,
  "missing": ["larkName"]
}
```
