---
name: n8n-code-node
description: Write JavaScript or Python in the n8n Code node correctly. Use when user says "write a Code node", "transform data in n8n", "use the Code node to...", "JavaScript in n8n", "Python in n8n", "$json in code node", "$input vs $json", "item linking in code node", "pairedItem", "use Luxon in n8n", "use JMESPath in n8n", "binary data in code node", "AI Code Tool", "Code Tool for agent", "external libraries in code node", "fetch in code node", or pastes Code-node JS/Python. Covers the two run modes ("Run Once for All Items" vs "Run Once for Each Item"), the canonical pairedItem-preserving pattern, $json/$input/$node/$execution semantics, binary data access via helpers, Luxon (DateTime), JMESPath, the Pyodide-based Python runtime, $getWorkflowStaticData persistence, and external library use. Do NOT use for building community node packages (use n8n-create-nodes), designing the broader workflow (use n8n-build-workflow), or debugging non-code-node failures (use n8n-debug-workflow).
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["n8n", "code-node", "javascript", "python", "pyodide", "luxon", "item-linking"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/n8n", "emoji": "🟧" } }
---

# n8n Code Node

Write JavaScript or Python in the Code node (`n8n-nodes-base.code`) that
preserves item linking, plays nicely with downstream nodes, and avoids the
half-dozen ways the Code node silently misbehaves.

**References:** [JAVASCRIPT.md](references/JAVASCRIPT.md) | [PYTHON.md](references/PYTHON.md) | [BUILTIN_HELPERS.md](references/BUILTIN_HELPERS.md) | [ITEM_LINKING_CODE.md](references/ITEM_LINKING_CODE.md) | [BINARY_DATA.md](references/BINARY_DATA.md)

**Lessons:** [LESSONS_LEARNED.md](LESSONS_LEARNED.md) — read before non-trivial work.

**Authoritative docs:** <https://docs.n8n.io/code/code-node/>

---

## The two run modes (always confirm which one)

The Code node has a **Mode** parameter — `runOnceForAllItems` (default) or
`runOnceForEachItem`. The semantics are NOT subtle and getting it wrong is
the #1 cause of Code-node bugs.

### `runOnceForAllItems`

- Code runs ONCE.
- Receives ALL incoming items.
- `$json` refers to the **first** item only.
- Use `$input.all()` to access the full array.
- You MUST manually return an array of items in `{ json, binary?, pairedItem? }` shape.
- You MUST manually set `pairedItem` to preserve item linking (see [ITEM_LINKING_CODE.md](references/ITEM_LINKING_CODE.md)).

```js
const items = $input.all();
return items.map((item, index) => ({
  json: { processed: item.json.value * 2 },
  pairedItem: { item: index }
}));
```

### `runOnceForEachItem`

- Code runs N times, once per input item.
- `$json` refers to the current item.
- Return a SINGLE item object `{ json: { ... } }` (n8n collects them into an array).
- `pairedItem` is auto-set to the current item's index.

```js
return {
  json: {
    processed: $json.value * 2
  }
};
```

**Rule of thumb:** Use `runOnceForEachItem` when transformation is
1-to-1 and per-item. Use `runOnceForAllItems` when you need cross-item logic
(aggregation, joining, batching, splitting).

---

## Returning items — the contract

### JavaScript

```js
// runOnceForAllItems — return an array
return [
  { json: { name: 'alice' }, pairedItem: { item: 0 } },
  { json: { name: 'bob' },   pairedItem: { item: 1 } }
];

// runOnceForEachItem — return a single item object
return { json: { name: 'alice' } };
```

### Python (via Pyodide)

```python
# runOnceForAllItems
return [
  { "json": { "name": "alice" }, "pairedItem": { "item": 0 } },
  { "json": { "name": "bob" },   "pairedItem": { "item": 1 } }
]

# runOnceForEachItem
return { "json": { "name": "alice" } }
```

### Rules

- **Every returned item MUST have a `json` field.** Bare objects (without
  `json` wrapping) cause "Output item is not in valid format" errors.
- **`pairedItem` is optional but strongly recommended** in
  `runOnceForAllItems` mode (auto-set in `runOnceForEachItem`).
- **Don't mutate `$json` in place** — mutating the upstream item's data
  corrupts the execution history view. Spread first: `{ ...item.json, x: 1 }`.
- **Don't return `null`, `undefined`, or a non-array** in
  `runOnceForAllItems` — n8n throws "Expected an array".

---

## Built-in variables (most common)

| Variable | Notes |
|---|---|
| `$json` | Current item's `.json` (in `runOnceForEachItem`) or first item's `.json` (in `runOnceForAllItems`) |
| `$binary` | Current item's `.binary` map (in `runOnceForEachItem`) |
| `$input.all()` | Array of incoming items (in `runOnceForAllItems`) |
| `$input.first()` / `$input.last()` | Self-explanatory |
| `$input.item` | Current item with `.pairedItem` preserved (in `runOnceForEachItem`) |
| `$('Node Name').first()` / `.last()` / `.all()` / `.item` | Access prior node outputs (same rules as expressions — see [BUILTIN_HELPERS.md](references/BUILTIN_HELPERS.md)) |
| `$workflow` | `{ id, name, active }` |
| `$execution` | `{ id, mode, resumeUrl, customData }` |
| `$env` | Host env vars (if `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`) |
| `$now` | Luxon `DateTime` (JS only) — use `from datetime import datetime` in Python |
| `$today` | `$now.startOf('day')` (JS only) |
| `$jmespath(obj, expr)` | JMESPath query (JS only — Python uses native dict/list) |
| `$getWorkflowStaticData('global')` / `'node'` | Persistent KV between executions |
| `this.helpers.*` | Node helper API (binary data, HTTP, etc.) — JS only |

---

## Canonical pairedItem pattern (memorize this)

```js
// runOnceForAllItems, 1-to-1 transformation
const items = $input.all();
return items.map((item, index) => ({
  json: { ...item.json, computed: item.json.value * 2 },
  pairedItem: { item: index }
}));
```

```js
// runOnceForAllItems, 1-to-N fan-out
const items = $input.all();
const out = [];
items.forEach((item, sourceIndex) => {
  for (const tag of item.json.tags) {
    out.push({
      json: { tag, source: item.json.id },
      pairedItem: { item: sourceIndex }
    });
  }
});
return out;
```

```js
// runOnceForAllItems, N-to-1 aggregation
const items = $input.all();
return [{
  json: {
    total: items.length,
    sum: items.reduce((acc, item) => acc + item.json.amount, 0)
  },
  pairedItem: items.map((_, i) => ({ item: i }))
}];
```

See [ITEM_LINKING_CODE.md](references/ITEM_LINKING_CODE.md) for variants
including multi-source pairing (after merges).

---

## Binary data — never base64 by hand

To read a binary attachment from an input item:

```js
// JavaScript, runOnceForEachItem
const binaryKey = 'data';
const buffer = await this.helpers.getBinaryDataBuffer(0, binaryKey);
// buffer is a Buffer — use buffer.toString('utf8') for text, .length for size, etc.
const text = buffer.toString('utf8');
return { json: { length: text.length, preview: text.slice(0, 100) } };
```

To write a binary output:

```js
const text = 'Hello, world!';
const binaryData = await this.helpers.prepareBinaryData(
  Buffer.from(text, 'utf8'),
  'greeting.txt',
  'text/plain'
);
return {
  json: { saved: true },
  binary: { data: binaryData }
};
```

Never construct binary by hand-base64-encoding into the `data` field — that
breaks filesystem-mode and S3-mode binary storage. Always use the helpers.

See [BINARY_DATA.md](references/BINARY_DATA.md) for streaming, MIME
detection, and converting between binary keys.

---

## Persistent state across executions

```js
const data = $getWorkflowStaticData('global'); // or 'node'
data.lastCursor = data.lastCursor || null;
const cursor = data.lastCursor;
// ... use cursor ...
data.lastCursor = newCursor; // n8n persists this on workflow save
return [{ json: { cursor } }];
```

- Scope `'global'` shared across the workflow; `'node'` per-node.
- Persisted to DB. Heavy or frequent writes hurt performance.
- Wiped on workflow duplicate or fresh import.
- DON'T use for hot state (high-frequency counter, queue). Use Redis or a
  DB instead.

---

## External libraries

### JavaScript

Default n8n installs ship with a small set of safe libraries pre-loaded:
**Luxon** (`DateTime`, `Duration`, `Interval`), **JMESPath** (`$jmespath`).

To import additional npm packages:

- **Self-hosted only.** Set env `NODE_FUNCTION_ALLOW_EXTERNAL=<csv of allowed packages>`.
  Example: `NODE_FUNCTION_ALLOW_EXTERNAL=lodash,uuid,axios`.
- Then in the Code node: `const _ = require('lodash');`
- Cloud doesn't allow arbitrary external packages — use the built-ins or
  build a community node instead.

### Built-in JS modules

Set `NODE_FUNCTION_ALLOW_BUILTIN=<csv>` (e.g. `crypto,url`) to allow Node.js
built-ins. By default they're blocked.

### Python (Pyodide)

The Python runtime is Pyodide running in a browser-like sandbox. Standard
library available, plus a curated set of scientific packages (numpy,
pandas, etc.) loadable on demand. Native packages requiring C extensions
don't work outside the Pyodide-supported list.

```python
# Loading a package
import micropip
await micropip.install('requests')
# ... but note: requests' socket layer doesn't work in Pyodide; use fetch instead
```

For HTTP from Python, prefer the n8n HTTP Request node ahead of the Code
node rather than fighting Pyodide's sandboxed fetch.

---

## Common Code-node mistakes

### 1. Forgot to wrap return in `json`

```js
// ✗ Wrong
return [{ name: 'alice' }];

// ✓ Right
return [{ json: { name: 'alice' } }];
```

### 2. Returned a single item in `runOnceForAllItems`

```js
// ✗ Wrong — returns one item, expected array
return { json: { foo: 'bar' } };

// ✓ Right
return [{ json: { foo: 'bar' } }];
```

### 3. Returned an array in `runOnceForEachItem`

```js
// ✗ Wrong — each-item mode expects a single item object, not array
return [{ json: { foo: 'bar' } }];

// ✓ Right
return { json: { foo: 'bar' } };
```

### 4. Mixed up `$input.all()` and `$json` in `runOnceForEachItem`

In each-item mode, `$input.all()` returns `[currentItem]` (length 1) — NOT
the full upstream array. Use `$('UpstreamNode').all()` instead.

### 5. Awaited helpers without `async`

`this.helpers.*` are async. The Code node body is treated as an async
function so top-level `await` works — no need to wrap in `(async () => { ... })()`.

### 6. Used `console.log` and expected to see it in execution data

`console.log` writes to the n8n server log, NOT the execution detail view.
To inspect values in the UI, return them in the output `json` or use
`$execution.customData.set('key', value)`.

### 7. Tried to mutate input items

```js
// ✗ Wrong — corrupts the upstream execution data record
const items = $input.all();
items[0].json.x = 1;
return items;

// ✓ Right
return $input.all().map(item => ({
  json: { ...item.json, x: 1 },
  pairedItem: item.pairedItem
}));
```

### 8. Forgot pairedItem after a fan-out

See [ITEM_LINKING_CODE.md](references/ITEM_LINKING_CODE.md). The most
common cause of "Could not find paired item" downstream.

### 9. `$now` used in Python

`$now` is a JavaScript helper (Luxon). In Python, use:

```python
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
```

### 10. Using `require()` for non-allowlisted packages

```js
// ✗ Throws "X is not allowed" unless package is in NODE_FUNCTION_ALLOW_EXTERNAL
const _ = require('lodash');
```

On Cloud, this never works. On self-hosted, set the env var.

---

## Code Tool (for AI Agents)

The **Code Tool** (`@n8n/n8n-nodes-langchain.toolCode`) is a Code-node-like
sub-node that an AI Agent can invoke as a tool. Same JS runtime, same
helpers, but the input/output contract differs:

- Input: the Agent's tool-call arguments (described by your tool
  description).
- Output: a string returned from the function body — that string becomes
  the tool's observation visible to the model.

```js
// Code Tool body
const { city } = JSON.parse($input.first().json.query);
const data = await this.helpers.httpRequest({ url: `https://api.weather.com/v1/forecast?city=${city}` });
return JSON.stringify({ temp: data.temp, summary: data.summary });
```

---

## Continuous learning

After every Code-node session that surfaced a new gotcha, append a dated
entry to [LESSONS_LEARNED.md](LESSONS_LEARNED.md). The Code node has lots of
quiet failure modes — your lesson today saves the next session an hour.
