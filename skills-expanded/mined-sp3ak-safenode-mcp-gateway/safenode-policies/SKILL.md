---
name: safenode-policies
description: Design and write SafeNode policies that decide which AI agent actions are allowed, warned, held for human review, or denied, for MCP tools behind the SafeNode MCP Gateway or actions sent through the SafeNode SDKs. Use when the user asks what their agent should be allowed to do, wants to block deletes or writes outside a folder, require approval for payments or bulk changes, stop secrets or card numbers in tool arguments, cap spend, or restrict vendors or regions. Also use when a policy isn't firing the way they expected.
---

# Writing SafeNode policies

SafeNode evaluates each proposed action and returns `allow`, `warn`, `review` or `deny`. A policy
is a JSON definition with **hard rules** (any failure denies) and **soft rules** (each one adds
risk, and the total score is banded into a decision). The user edits policies in the SafeNode
dashboard under **Policy**: each policy has versions, and **Set active** on a version makes it the
one evaluations use.

Your job: turn "what should my agent be allowed to do" into rules, explain each one in plain words,
and hand the user JSON they can paste.

## Step 1: Inventory the actions

List what the agent can actually do, then sort it into tiers with the user:

| Tier | Examples | Usual decision |
| --- | --- | --- |
| Read-only | `read_file`, `list_*`, `search_*`, `get_*` | allow |
| Reversible writes | create a task, write inside the project folder | allow or warn |
| Costly or external | send email, create invoice, open a PR, payment | review |
| Destructive | `delete_*`, drop table, force push, `rm` | deny |

Ask which tier any unclear tool belongs in. Don't guess for anything that costs money or can't
be undone.

## Step 2: Know what the policy can see

Every evaluation carries an `action_type`, a `payload` (the arguments) and a `context`.

**Through the MCP gateway, every call has `action_type: "mcp_tool_call"`.** The tool is identified
in context, not in the action type:

| Context key | Value |
| --- | --- |
| `tool_name` | The tool's name on the downstream server |
| `exposed_tool_name` | The name the agent sees (with a `<server>__` prefix if names collided) |
| `server_name` | The gateway's name for the downstream server |
| `session_id` | One per gateway process |
| anything you add | From `context` in the gateway config: globally, per server or per tool (they merge) |

So rules like `action_type_match` on `delete_*` **do nothing behind the gateway**. Target tools with
context: either an allowlist on `tool_name`, or a tag you attach per tool in the gateway config
(see the patterns below).

**Through the SDKs**, the developer sets `action_type` themselves (`send_email`, `delete_customer`
and so on), so action-type rules work directly.

## Step 3: Pick rules

| Rule `type` | Hard/soft | Does | Key `params` |
| --- | --- | --- | --- |
| `action_type_match` | hard | Deny when `action_type` matches | `action_types` (exact), `patterns` (globs like `delete_*`), `message` |
| `context_match` | hard | **Deny unless** `context[context_key]` is in the list (an allowlist) | `context_key`, `values`, `message` |
| `action_type_context_threshold` | soft | Add risk when the action matches and a numeric context value passes a threshold | `action_types`/`patterns`, `context_key`, `gt` or `gte`, `factor_scores`, `message` |
| `action_type_business_hours` | soft | Add risk outside working hours | `action_types`/`patterns`, `timezone`, `start_hour`, `end_hour`, `weekdays_only` |
| `sensitive_data` | either | Match payload values or keys | `patterns`, `forbidden_keys`, `field_names` |
| `redaction_metadata` | hard | Act on what the client reports it redacted | `forbidden_types`, `max_counts`, `allowed_payload_modes`, `require_full_payload` |
| `spend_threshold` | either | Context `cost_estimate` (or `spend`) above a limit | `max_amount` |
| `blocked_vendor` | hard | Context `vendor_id`/`vendor_slug` is blocked | `blocked_slugs` |
| `unapproved_region_geo` | hard | Context `geo_country`/`country_code` | `allowed_countries` or `blocked_countries` |
| `unapproved_region_cloud` | hard | Context `region`/`cloud_region` | `allowed_regions` or `blocked_regions` |

Soft-rule scores are combined and banded. The defaults are: up to 30 allow, up to 50 warn, up to 75
review, and above that deny. Tune with `decision_bands`, the rule's `weight` (0–100) and its
`factor_scores`. **Don't promise which band a soft rule lands in. Test it** (step 5).

### Pair `sensitive_data` with `redaction_metadata`

The gateway and SDKs redact payloads on the client by default, so a `sensitive_data` pattern looking
for card numbers sees `[REDACTED:credit_card]` and never matches. Your "block card numbers" rule
would silently pass everything. Add a `redaction_metadata` rule with `forbidden_types` alongside it,
so the policy acts on the reported count instead. Explain to the user that these counts are
self-reported: they raise the floor for honest clients and don't stop a hostile one.

## Patterns for the gateway

**Only these tools may run** (anything else is denied):

```json
{ "id": "tool-allowlist", "type": "context_match",
  "params": { "context_key": "tool_name",
              "values": ["read_file", "list_directory", "search_files", "write_file"],
              "message": "This tool is not on the approved list." } }
```

**Hold specific tools for approval.** Tag them in the gateway config:

```json
"tools": {
  "write_file":   { "context": { "risk_tier": 2 } },
  "move_file":    { "context": { "risk_tier": 3 } },
  "create_issue": { "context": { "risk_tier": 2 } }
}
```

Then add a soft rule on the tag:

```json
{ "id": "high-tier-review", "type": "action_type_context_threshold", "weight": 100,
  "params": { "action_types": ["mcp_tool_call"], "context_key": "risk_tier", "gte": 3,
              "message": "High-risk tool: needs approval." } }
```

**Block secrets and cards in arguments:**

```json
{ "id": "no-secrets-out", "type": "redaction_metadata",
  "params": { "forbidden_types": ["credit_card", "private_key", "api_key", "bearer_token"],
              "message": "Tool arguments contained a secret or card number." } }
```

## Patterns for the SDKs

```json
{
  "version": 1,
  "hard_rules": [
    { "id": "deny-deletes", "type": "action_type_match",
      "params": { "patterns": ["delete_*", "drop_*"], "message": "Destructive actions are denied." } }
  ],
  "soft_rules": [
    { "id": "bulk-review", "type": "action_type_context_threshold", "weight": 100,
      "params": { "action_types": ["bulk_create_task"], "context_key": "count", "gt": 5,
                  "message": "Bulk change over 5 items: review." } },
    { "id": "after-hours", "type": "action_type_business_hours", "weight": 50,
      "params": { "action_types": ["send_email"], "timezone": "America/Los_Angeles",
                  "start_hour": 9, "end_hour": 17, "weekdays_only": true } }
  ],
  "default_decision": "allow"
}
```

## Step 4: Explain before handing over

For each rule, give one line: what it stops, and what it would wrongly stop. Allowlists are safest
but break when a server adds a tool. Say so, and suggest reviewing the decision log after the first
day.

## Step 5: Test it

- Create a new version, **Set active**, then trigger one harmless call per rule (for example, a
  denied tool with no side effects).
- Check the gateway's `logFile` or the dashboard trace: each entry shows the decision and the
  matched rule's reasons.
- If a soft rule lands in the wrong band, adjust its `weight`/`factor_scores` or the
  `decision_bands`. Don't promote it to a hard rule just to make the test pass.
- Every evaluation counts against the account's monthly quota, so keep test runs small.

## Limits to tell the user

- There is no "deny if context equals X" rule. `context_match` is an allowlist only. To block one
  tool, either allowlist the others or tag it with a high `risk_tier` and add a soft rule.
- The policy judges the action, not the agent's reasoning. It won't detect prompt injection.
- The gateway decides whether a call is forwarded. It isn't a sandbox, so still scope each
  downstream server narrowly.
