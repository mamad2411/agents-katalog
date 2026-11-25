---
name: budget-monitoring-variance-payload-builder
version: "1.4"
description: Builds deterministic Lark budget variance payloads and, when asked, runs the full budget monitoring flow through a NyxID service instead of direct Lark credentials.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - budget-monitoring
    - lark
    - nyxid-service-runner
    - payload-builder
  clawdbot:
    emoji: "bar_chart"
    files:
      - "references/*"
      - "scripts/*"
---

# Budget Monitoring Variance Payload Builder

Use this skill for budget-monitoring runs. It supports two modes:

1. **Payload-builder mode**: turn four provided record sets into a deterministic Lark interactive-card payload.
2. **NyxID service runner mode**: given a NyxID service slug, read the service-backed budget configuration, fetch Bitable records through NyxID proxy, build the payload, and send the Lark card through NyxID proxy.

Do not ask the user for raw Lark tokens, app secrets, tenant access tokens, or OAuth credentials. Use NyxID service/proxy access for all Lark I/O.

## When to use

Use for `budget-monitoring` when either:

- the caller already has four record arrays and needs a connector-ready Lark payload; or
- the caller provides a NyxID budget config service slug and wants the full read/build/send flow.

Do not use this skill to create Bitable tables or request Lark app permissions.

## Mode A: payload-builder

Use this mode when the caller provides records directly.

Required input keys:

- `coreBudgetRecords`
- `coreActualRecords`
- `aelfBudgetRecords`
- `aelfActualRecords`

Optional input keys:

- `period`
- `currency`
- `watchThresholdPercent`
- `alertThresholdPercent`
- `criticalThresholdPercent`
- `receiveId`
- `receiveIdType`

Return one JSON object with:

- `message_type: "interactive"`
- `summary`
- `severity`
- `period`
- `currency`
- `dataCutoff`
- `totals`
- `sections`
- `highlights`
- `lark.card`
- `lark.body` when `receiveId` is provided

The returned `lark.body` is connector-ready for:

```text
POST /open-apis/im/v1/messages?receive_id_type=<receiveIdType>
```

Record field aliases, cutoff rules, formulas, levels, and output shape are defined in `references/budget-variance-contract.md`.

## Mode B: NyxID service runner

Use this mode when the caller provides a NyxID service slug, for example:

```json
{
  "serviceSlug": "budget-monitoring-p2"
}
```

The NyxID service is the configuration and credential boundary. It must hold the Lark credential and budget-monitoring configuration. The runner must call Lark only through NyxID proxy for that service.

Expected NyxID service default headers are defined in `references/nyxid-service-runner-contract.md`.

Runner steps:

1. Resolve `serviceSlug` from input. If missing, return `needs_more_information` with `missing: ["serviceSlug"]`.
2. Read the NyxID service details, preferably with `nyxid service show <serviceSlug> --output json`.
3. Extract budget configuration from service default headers using `references/nyxid-service-runner-contract.md`.
4. Fetch all four Lark Bitable record sets through NyxID proxy using the same `serviceSlug`.
5. Build the payload using the payload-builder contract/reference implementation.
6. If `receiveId` is configured, send `lark.body` through NyxID proxy using the same `serviceSlug`.
7. Return JSON containing `sent`, `serviceSlug`, `dataCutoff`, `severity`, `summary`, `totals`, `highlights`, and the send response when a message was sent.

Never call Lark directly. Never send or log downstream credentials. Never ask the user to paste Lark secrets.

## Determinism requirement

For payload construction, follow `references/budget-variance-contract.md`. If executing code is allowed, use `scripts/build_budget_variance_payload.js` as the reference implementation. If executing code is not allowed, reproduce the same transformations exactly.

For the full NyxID-backed flow, use `scripts/run_budget_monitoring_nyxid_service.js` as the reference implementation when shell/Node execution is available.

Do not invent records, table ids, app tokens, receiver ids, credentials, schedules, or service slugs.

## Failure behavior

If any required record set is missing in payload-builder mode, return:

```json
{
  "needs_more_information": true,
  "missing": ["coreBudgetRecords"]
}
```

If any required NyxID service configuration key is missing in runner mode, return:

```json
{
  "needs_more_information": true,
  "missing": ["x-budget-core-budget-table-id"]
}
```
