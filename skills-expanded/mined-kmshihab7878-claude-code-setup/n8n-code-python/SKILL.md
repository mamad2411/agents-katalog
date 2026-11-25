---
name: n8n-code-python
description: Write Python code in n8n Code nodes. Use when writing Python in n8n, using _input/_json/_node syntax, working with standard library, or need to understand Python limitations in n8n Code nodes.
---

# Python Code Node (Beta)

Expert guidance for writing Python code in n8n Code nodes.

## When to use

- Writing or reviewing a Python Code node in n8n.
- Using `_input` / `_json` / `_node` syntax.
- Selecting between Python (Beta) and Python (Native).
- Understanding what is and is not available in the n8n Python runtime.
- Switching between Python and JavaScript Code nodes.
- Debugging `ModuleNotFoundError`, `KeyError`, or empty-output issues.

## Required input contract

Before writing or reviewing a Python Code node, identify:

- **Mode** — "Run Once for All Items" (default, 95% of cases) vs "Run Once for Each Item".
- **Runtime** — Python (Beta, recommended) vs Python (Native, Beta).
- **Upstream node(s)** — which provides the input; webhook, HTTP, manual, or another Code node.
- **Required output cardinality** — single, list, empty, or filtered.
- **Reason for Python over JavaScript** — Python is justified only by stdlib needs, comfort, or list-comprehension fit.

## JavaScript first

Use **JavaScript for 95% of use cases**. Choose Python only when:

- You need a specific stdlib module (e.g., `statistics`).
- You are significantly more comfortable in Python.
- The transform maps cleanly to Python idioms.

JavaScript advantages: full `$helpers` (incl. `$helpers.httpRequest()`), Luxon
DateTime, no external-library limit, better n8n documentation.

## n8n Python Code node constraints

These constraints apply to every Python Code node and must always be respected.

1. **No external libraries.** `requests`, `pandas`, `numpy`, `bs4`, `lxml`,
   `httpx`, etc. produce `ModuleNotFoundError`. Standard library only.
2. **Available stdlib**: `json`, `datetime`, `re`, `base64`, `hashlib`,
   `urllib.parse`, `math`, `random`, `statistics`.
3. **Return shape**: every code path returns a list of dicts each with a
   `"json"` key. Single returns are wrapped in a list. Empty result is `return []`.
4. **Webhook data nests under `["body"]`**. Use `_json.get("body", {}).get(...)`.
5. **Dictionary access uses `.get()`** — fields may be missing.
6. **HTTP requests cannot originate inside the Code node.** Use the HTTP Request
   node upstream, or switch to JavaScript.
7. **Beta and Native runtimes have different variables** (`_input`/`_json`/`_node`
   vs `_items`/`_item`). Do not mix them.

## Workflow (compact)

1. **Language**: JavaScript first; Python only when justified.
2. **Mode**: All Items (default) vs Each Item.
3. **Runtime**: Beta (recommended) vs Native.
4. **Read**: `_input.all()` / `.first()` / `.item` / `_node["..."]["json"]`.
5. **Transform**: stdlib only; list comprehensions preferred.
6. **Return**: `[{"json": {...}}, ...]` on every code path.
7. **Validate**: walk the validation-gates checklist (below).

Full workflow + mode and runtime examples: `references/python-code-workflow.md`.

## Decision logic

### Mode selection

| Mode | When | Data access |
|------|------|-------------|
| Run Once for All Items (default, 95%) | Aggregation, filtering, batch | `_input.all()` |
| Run Once for Each Item | Item-specific logic, independent ops | `_input.item` |

### Runtime selection

| Runtime | Variables | Helpers |
|---------|-----------|---------|
| Python (Beta) — recommended | `_input`, `_json`, `_node` | `_now`, `_today`, `_jmespath()` |
| Python (Native, Beta) | `_items`, `_item` only | None |

### Data access

| Accessor | When |
|----------|------|
| `_input.all()` | Arrays, batches, aggregations |
| `_input.first()` | Single objects, API responses |
| `_input.item` | Each-Item mode only |
| `_node["Name"]["json"]` | Reference a non-immediate upstream node |

### Python vs JavaScript

| Situation | Use |
|-----------|-----|
| HTTP request inside the node | JavaScript |
| Advanced date/time (Luxon, timezones) | JavaScript |
| Python `statistics` module | Python |
| Simple field mapping | Use **Set** node instead |
| Basic filtering | Use **Filter** node instead |
| Conditional routing | Use **IF** / **Switch** node instead |

## Minimal critical examples

### Quick Start

```python
from datetime import datetime

items = _input.all()
return [
    {"json": {**it["json"], "processed": True, "ts": datetime.now().isoformat()}}
    for it in items
]
```

### Webhook field access

```python
data = _json.get("body", {})
name = data.get("name", "")
return [{"json": {"name": name.strip()}}]
```

### Return-format right/wrong

```python
return [{"json": {"id": 1}}]   # RIGHT — single item
return [{"json": {"id": 1}}, {"json": {"id": 2}}]  # RIGHT — multiple
return []                       # RIGHT — empty
return {"json": {"id": 1}}      # WRONG — dict not wrapped
return [{"id": 1}]              # WRONG — missing "json" key
```

Worked end-to-end examples (webhook, aggregation, multi-node merge, regex
extract, checksum, per-item conditional): `references/examples.md`.

## Validation gates

Before deploying a Python Code node:

- [ ] Considered JavaScript first — Python is the right choice.
- [ ] Code is not empty.
- [ ] Final `return` statement exists.
- [ ] Return shape is `[{"json": {...}}, ...]` on every code path.
- [ ] Data access uses only `_input.all()` / `_input.first()` / `_input.item` /
      `_node["..."]["json"]`.
- [ ] No external library imports — stdlib only.
- [ ] `.get(key, default)` everywhere for dictionary access.
- [ ] Webhook data accessed via `_json.get("body", {})`.
- [ ] Mode is "All Items" unless per-item independence is required.
- [ ] Output is consistent across every branch and exception path.

Full top-5-mistakes catalog, best practices, debugging playbook, anti-patterns:
`references/validation-troubleshooting-and-antipatterns.md`.

## Output expectations

When delivering a Python Code node:

- Provide the full code block, ready to paste into the Code node.
- State the mode (All Items / Each Item) and runtime (Beta / Native).
- Note any required upstream nodes (HTTP Request, Webhook, etc.).
- List required stdlib imports at the top.
- Flag any branch that returns `[]` and what that means downstream.

## Integration with other skills

- **n8n Expression Syntax** — expressions use `{{ }}` in other nodes; Code
  nodes use Python directly, no `{{ }}`.
- **n8n MCP Tools Expert** — find Code node via `search_nodes({query: "code"})`;
  configure via `get_node({nodeType: "nodes-base.code"})`; validate via
  `validate_node({nodeType: "nodes-base.code", config: {...}})`.
- **n8n Node Configuration** — mode and language selection are node properties.
- **n8n Validation Expert** — interpret validation errors, auto-fix issues.
- **n8n Code JavaScript** — when to switch; feature comparison.

## Reference map

| Need | Read |
|------|------|
| Mode + runtime + return-format full examples; workflow steps | `references/python-code-workflow.md` |
| Data access patterns, webhook body, 5 production transform/filter/validate/stats patterns, stdlib quick reference | `references/item-and-data-patterns.md` |
| HTTP request strategy, auth, scraping, multiple-request orchestration, decision table | `references/api-requests-and-integrations.md` |
| Top 5 mistakes, best practices, no-library workarounds, debugging playbook, validation gates, anti-patterns | `references/validation-troubleshooting-and-antipatterns.md` |
| End-to-end worked examples (webhook, aggregation, multi-node merge, regex, checksum, per-item conditional) | `references/examples.md` |
| Upstream comprehensive depth | `references/common-patterns.md`, `references/data-access.md`, `references/error-patterns.md`, `references/standard-library.md` |
