---
name: n8n-node-configuration
description: Operation-aware node configuration guidance. Use when configuring nodes, understanding property dependencies, determining required fields, choosing between get_node detail levels, or learning common configuration patterns by node type.
---

# n8n Node Configuration

Expert guidance for operation-aware node configuration with property dependencies.

## Reference map

Reference material lives in `references/`. Load only what the current task needs.

| When | Read |
|---|---|
| Full step-by-step configuration walkthrough (HTTP Request 8-step example), get_node detail-level decision tree | [`references/configuration-workflow.md`](references/configuration-workflow.md) |
| displayOptions deep dive, dependency-finding code, conditional-requirement scenarios (HTTP body, IF singleValue) | [`references/property-validation.md`](references/property-validation.md) · [`DEPENDENCIES.md`](DEPENDENCIES.md) |
| Patterns 1–4 long code (Resource/Operation, HTTP, Database, Conditional), Slack / HTTP Request / IF operation-specific examples | [`references/node-patterns.md`](references/node-patterns.md) · [`OPERATION_PATTERNS.md`](OPERATION_PATTERNS.md) |
| Anti-patterns bad/good code, Best Practices full examples, validation-failure → fix recipes | [`references/troubleshooting.md`](references/troubleshooting.md) |
| End-to-end examples (Slack discovery, HTTP POST with expressions, IF unary auto-sanitize, Postgres insert, safe op-switch) | [`references/examples.md`](references/examples.md) |

---

## Configuration Philosophy

**Progressive disclosure**: start minimal, add complexity as needed.

- `get_node` with `detail: "standard"` is the most-used discovery pattern.
- 56 seconds average between configuration edits.
- Covers 95% of use cases with 1–2K tokens response.

**Key insight**: most configurations need only standard detail, not full schema.

---

## Core Concepts

### 1. Operation-Aware Configuration

**Not all fields are always required — it depends on operation.**

Example: a Slack node configured for `operation="post"` requires `channel` and `text`. The same node for `operation="update"` requires `messageId` and `text`, and **does not** require `channel`. Resource + operation determine which fields are required.

Full Slack post/update/create-channel examples: [`references/node-patterns.md`](references/node-patterns.md#slack-node).

### 2. Property Dependencies

**Fields appear/disappear based on other field values via `displayOptions`.**

Example: HTTP Request `body` field shows only when `sendBody=true` AND `method` is POST/PUT/PATCH.

Full `displayOptions` mechanism, common dependency patterns (boolean toggle / operation switch / type selection), and dependency-finding workflow: [`references/property-validation.md`](references/property-validation.md).

### 3. Progressive Discovery — Pick the Right Detail Level

| Mode | When | Response size |
|---|---|---|
| `get_node({detail: "standard"})` — **default** | Starting configuration, 95% of needs | ~1–2K tokens |
| `get_node({mode: "search_properties", propertyQuery: "..."})` | Finding a specific field (auth, body, headers, etc.) | Small |
| `get_node({detail: "full"})` | Standard insufficient, need full schema | ~3–8K tokens |

Full decision tree: [`references/configuration-workflow.md`](references/configuration-workflow.md#get_node-detail-levels--when-to-use-which).

---

## Configuration Workflow

```
1. Identify node type and operation
   ↓
2. Use get_node (standard detail is default)
   ↓
3. Configure required fields
   ↓
4. Validate configuration
   ↓
5. If field unclear → get_node({mode: "search_properties"})
   ↓
6. Add optional fields as needed
   ↓
7. Validate again
   ↓
8. Deploy
```

Average 2–3 iteration cycles is normal. Full HTTP Request 8-step worked example: [`references/configuration-workflow.md`](references/configuration-workflow.md#example-configuring-http-request).

---

## Common Node Patterns

| Pattern | Examples | Shape | Key dependencies |
|---|---|---|---|
| **Resource/Operation** | Slack, Google Sheets, Airtable | `resource` + `operation` + op-specific fields | Op selection drives field set |
| **HTTP-Based** | HTTP Request, Webhook | `method` + `url` + `authentication` + method-specific | `sendBody`, `body`, credentials |
| **Database** | Postgres, MySQL, MongoDB | `operation` + query/table/values/where | `executeQuery`→query; `insert`→table+values; `update`→all three |
| **Conditional Logic** | IF, Switch, Merge | `conditions: { type: [{operation, value1, value2}] }` | Binary ops → `value1`+`value2`; unary ops → `value1` + `singleValue: true` |

Full per-pattern code recipes and Slack / HTTP Request / IF operation-specific examples: [`references/node-patterns.md`](references/node-patterns.md).

---

## Validation Rules

**Validation is mandatory** before deploying any node configuration.

- Always call `validate_node({ nodeType, config, profile: "runtime" })` before `n8n_update_partial_workflow`.
- Profiles: `runtime` (deployable), `ai-friendly`, `strict`.
- Treat validation errors as discovery — each cycle surfaces the next required field. Average 2–3 iterations.
- For conditional fields that "seem missing", use `get_node({mode: "search_properties", propertyQuery: "..."})` to find what controls visibility.
- **Trust auto-sanitization** for IF/Switch operator structure (`singleValue`, etc.). Don't fight it.

Full validation-failure → fix recipes: [`references/troubleshooting.md`](references/troubleshooting.md#common-validation-failure--fix-recipes).

---

## Anti-Patterns (don't)

1. **Don't over-configure upfront** — adding every optional field creates noise; start minimal and let validation guide additions.
2. **Don't skip validation** — never call `n8n_update_partial_workflow` without `validate_node` returning valid.
3. **Don't ignore operation context** — different operations on the same node require different fields; re-check `get_node` after every operation change.
4. **Don't jump straight to `detail="full"`** — try standard first; full is 3–8K tokens.
5. **Don't copy configs without understanding** — different operations need different fields; validate after copying.
6. **Don't manually fix auto-sanitization issues** — let the system handle operator structure.

Full bad/good code for each: [`references/troubleshooting.md`](references/troubleshooting.md#anti-patterns).

---

## Best Practices (do)

1. **Start with `get_node` (standard detail)** — covers 95% of needs.
2. **Validate iteratively** — configure → validate → fix → repeat (2–3 cycles typical).
3. **Use `search_properties` mode when stuck** — find what controls a missing field.
4. **Respect operation context** — re-check `get_node` after changing operation.
5. **Trust auto-sanitization** — IF/Switch structure is managed automatically.

Full guidance with examples: [`references/troubleshooting.md`](references/troubleshooting.md#best-practices--full-examples).

---

## Output Expectations

When configuring a node, the deliverable is a validated config object that:

- Includes all operation-required fields for the chosen `resource`/`operation`.
- Respects every active `displayOptions` constraint (no orphaned fields hidden by visibility rules).
- Passes `validate_node({ profile: "runtime" })` with no errors.
- Uses minimal optional fields — additions justified by use case.
- Uses n8n expression syntax (`={{ ... }}`) for dynamic values, not hard-coded data.

---

## Integration with Other Skills

- **n8n MCP Tools Expert** — how to use `search_nodes`, `get_node`, `validate_node` correctly.
- **n8n Validation Expert** — interpret validation errors, handle false positives, auto-fix.
- **n8n Expression Syntax** — configure expression fields with `={{ }}` (note: webhook data under `$json.body`).
- **n8n Workflow Patterns** — fit configured nodes into proven workflow shapes.
- **n8n Code JavaScript / Python** — when a node won't do, drop to a Code node.

---

## Summary

**Configuration strategy**:

1. Start with `get_node` (standard detail is default).
2. Configure required fields for the operation.
3. Validate configuration.
4. Search properties if stuck.
5. Iterate until valid (avg 2–3 cycles).
6. Deploy with confidence.

**Key principles**:

- **Operation-aware** — different operations require different fields.
- **Progressive disclosure** — start minimal, add as needed.
- **Dependency-aware** — understand `displayOptions` visibility rules.
- **Validation-driven** — let validation guide configuration.

## Detailed References

- [`references/configuration-workflow.md`](references/configuration-workflow.md) — full workflow walkthrough + detail-level decision tree
- [`references/property-validation.md`](references/property-validation.md) — displayOptions deep dive + conditional-requirement scenarios
- [`references/node-patterns.md`](references/node-patterns.md) — pattern recipes + Slack / HTTP / IF operation examples
- [`references/troubleshooting.md`](references/troubleshooting.md) — anti-patterns, best practices, validation-failure → fix recipes
- [`references/examples.md`](references/examples.md) — end-to-end worked examples
- [`DEPENDENCIES.md`](DEPENDENCIES.md) — comprehensive property-dependency reference
- [`OPERATION_PATTERNS.md`](OPERATION_PATTERNS.md) — comprehensive operation-pattern catalog
