---
name: n8n-code-javascript
description: Write JavaScript code in n8n Code nodes. Use when writing JavaScript in n8n, using $input/$json/$node syntax, making HTTP requests with $helpers, working with dates using DateTime, troubleshooting Code node errors, or choosing between Code node modes.
---

# JavaScript Code Node

Expert guidance for writing JavaScript code in n8n Code nodes.
**JavaScript is recommended for 95% of n8n Code use cases** — full
`$helpers`, Luxon DateTime, no library limitations.

## When to use

- Writing or reviewing a JavaScript Code node in n8n.
- Using `$input` / `$json` / `$node` syntax.
- Making HTTP requests with `$helpers.httpRequest`.
- Date/time work with `DateTime` (Luxon).
- Querying JSON with `$jmespath`.
- Choosing between Code node modes (All Items vs Each Item).
- Debugging Code node errors (return shape, webhook nesting, undefined fields).

## Required input contract

Before writing or reviewing a JavaScript Code node, identify:

- **Mode** — "Run Once for All Items" (default, 95% of cases) vs "Run Once for Each Item".
- **Upstream node(s)** — which provides the input (webhook, HTTP, manual, prior Code node).
- **Required output cardinality** — single, list, empty, or filtered.
- **External calls** — does this node need `$helpers.httpRequest`?
- **Reason for Code node** — not solvable by Set / Filter / IF / HTTP Request nodes alone.

## n8n JavaScript Code node constraints

These constraints apply to every JavaScript Code node and must always be respected.

1. **Return shape**: every code path returns an array of objects each with
   a `json` key. Single returns wrapped in array. Empty result is `return []`.
2. **Webhook data nests under `.body`**. Use `$json.body?.<field>` or
   `$input.first().json.body`.
3. **Optional chaining + nullish coalescing** for nullable fields:
   `$json.body?.name ?? ""`.
4. **No `{{ }}` expression syntax inside the Code node body.** Code nodes
   execute pure JavaScript — use template literals or direct access.
5. **`$helpers.httpRequest` always inside `try`/`catch`.** Awaitable; throws on failure.
6. **`DateTime` time zones pinned explicitly** when crossing zones — never
   rely on the server default.
7. **Do not mutate `item.json` in place** — construct new objects
   (`{ json: { ...item.json, extra: v } }`).
8. **Do not return `$input.all()` raw** — map first to produce a fresh
   `{ json }` shape.
9. **Credentials live in n8n credential storage**, never in source.

## Workflow (compact)

1. **Mode**: All Items (default) vs Each Item.
2. **Read**: `$input.all()` / `.first()` / `.item` / `$node["..."].json`.
3. **Transform**: array methods (`map` / `filter` / `reduce`).
4. **Return**: `[{ json: {...} }, ...]` on every code path.
5. **Validate**: walk the gates (below).

Full workflow + mode examples + return-format matrix:
`references/javascript-code-workflow.md`.

## Decision logic

### Mode selection

| Mode | When | Data access |
|------|------|-------------|
| Run Once for All Items (default, 95%) | Aggregation, filtering, batch, API calls with all data | `$input.all()` / `items` |
| Run Once for Each Item | Item-specific logic, independent operations | `$input.item` / `$item` |

### Data access

| Accessor | When |
|----------|------|
| `$input.all()` | Arrays, batches, aggregations |
| `$input.first()` | Single objects, API responses |
| `$input.item` | Each-Item mode only |
| `$node["Name"].json` | Reference a non-immediate upstream node |

### When to use the Code node vs another node

| Situation | Use |
|-----------|-----|
| Complex multi-step transformations | Code node |
| Custom calculations / business logic | Code node |
| API response parsing with complex structure | Code node |
| Simple field mapping | **Set** node |
| Basic filtering | **Filter** node |
| Conditional routing | **IF** / **Switch** node |
| HTTP only, no transform | **HTTP Request** node |
| Need HTTP + custom logic in one node | Code node (JavaScript, with `$helpers.httpRequest`) |

## Minimal critical examples

### Quick Start

```javascript
const items = $input.all();
return items.map(item => ({
  json: {
    ...item.json,
    processed: true,
    timestamp: new Date().toISOString(),
  },
}));
```

### Webhook field access

```javascript
const name = $json.body?.name ?? "";
return [{ json: { name: name.trim() } }];
```

### HTTP from inside the Code node

```javascript
try {
  const res = await $helpers.httpRequest({
    method: "GET",
    url: "https://api.example.com/items",
  });
  return res.data.map(it => ({ json: { id: it.id, name: it.name } }));
} catch (err) {
  return [{ json: { ok: false, error: err.message } }];
}
```

### Return-format right/wrong

```javascript
return [{ json: { id: 1 } }];                            // RIGHT — single
return [{ json: { id: 1 } }, { json: { id: 2 } }];       // RIGHT — multiple
return [];                                               // RIGHT — empty
return { json: { id: 1 } };                              // WRONG — not wrapped
return [{ id: 1 }];                                      // WRONG — missing "json" key
return $input.all();                                     // WRONG — raw input
```

Worked end-to-end examples (webhook, API fetch + merge, group-by,
multi-node combine, regex extract, per-item conditional, date-range filter):
`references/examples.md`.

## Validation gates

Before deploying a JavaScript Code node:

- [ ] Code is not empty.
- [ ] Final `return` statement exists.
- [ ] Return shape is `[{ json: {...} }, ...]` on every code path.
- [ ] Data access uses only `$input.all()` / `$input.first()` / `$input.item` /
      `$node["..."].json`.
- [ ] No `{{ }}` expression syntax inside the Code node body.
- [ ] `?.` and `??` used for nullable fields.
- [ ] Webhook data accessed via `$json.body?.<field>`.
- [ ] `try`/`catch` wraps every `$helpers.httpRequest`.
- [ ] Mode is "All Items" unless per-item independence is required.
- [ ] Output consistent across every branch and exception path.
- [ ] `DateTime` time zones pinned explicitly when crossing zones.

Full top-5 mistakes, best practices, debugging playbook, anti-patterns:
`references/validation-troubleshooting-and-antipatterns.md`.

## Output expectations

When delivering a JavaScript Code node:

- Provide the full code block, ready to paste into the Code node.
- State the mode (All Items / Each Item).
- Note any required upstream nodes.
- Flag any branch that returns `[]` and what that means downstream.
- List required credentials if `$helpers.httpRequest` is used.

## Integration with other skills

- **n8n Expression Syntax** — expressions use `{{ }}` in other nodes; Code nodes use JavaScript directly.
- **n8n MCP Tools Expert** — find Code node via `search_nodes({query: "code"})`;
  configure via `get_node({nodeType: "nodes-base.code"})`; validate via
  `validate_node({nodeType: "nodes-base.code", config: {...}})`.
- **n8n Node Configuration** — mode and language selection are node properties.
- **n8n Workflow Patterns** — Code nodes in transformation steps; Webhook → Code → API; error handling.
- **n8n Validation Expert** — interpret validation errors, auto-fix.
- **n8n Code Python** — when to switch (rare); feature comparison.

## Reference map

| Need | Read |
|------|------|
| Mode selection + runtime + return-format full examples; workflow steps | `references/javascript-code-workflow.md` |
| 4 data access patterns, webhook body, 5 production patterns (aggregate / regex / transform / top-N / reduce) | `references/item-and-data-patterns.md` |
| `$helpers.httpRequest` (auth, retry, multi-request), DateTime / Luxon, `$jmespath`, integration decision table | `references/helpers-and-integrations.md` |
| Top 5 mistakes, best practices, validation gates, debugging playbook, anti-patterns | `references/validation-troubleshooting-and-antipatterns.md` |
| End-to-end worked examples | `references/examples.md` |
| Upstream comprehensive depth | `references/common-patterns.md`, `references/data-access.md`, `references/error-patterns.md`, `references/builtin-functions.md` |
