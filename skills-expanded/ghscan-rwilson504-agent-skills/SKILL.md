---
name: n8n-build-workflow
description: Design and author n8n workflow JSON files. Use when user says "build an n8n workflow", "design a workflow", "wire these nodes", "add a trigger", "convert this requirement into n8n", "set up a Schedule/Webhook trigger", "build an AI workflow", "use the AI Agent node", "add a Switch/IF/Merge/Loop Over Items", "split into sub-workflows", "add error handling", "create an error workflow", "build a webhook that responds to the caller", or asks for a runnable workflow JSON. Covers workflow JSON schema, node/connection wiring, the n8n data structure (array-of-items), triggers (Manual, Webhook, Schedule, Form, App triggers, Error Trigger), flow logic (IF/Switch/Merge/Loop Over Items/Wait), expressions and the `={{ }}` template, AI cluster nodes (Agent + Chat Model + Memory + Tools + Vector Store), sub-workflows, and import/export. Do NOT use for executing workflows at runtime, building community node packages (use n8n-create-nodes), Code-node scripting (use n8n-code-node), or hosting setup (use n8n-self-host).
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["n8n", "workflow", "automation", "ai-workflows", "json", "low-code"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/n8n", "emoji": "🟧" } }
---

# n8n Workflow Builder

Design and author production-quality n8n workflows by emitting valid workflow
JSON the user can import directly (Editor → Workflow menu → Import from File /
Import from URL / paste).

**References:** [WORKFLOW_JSON.md](references/WORKFLOW_JSON.md) | [NODE_CATALOG.md](references/NODE_CATALOG.md) | [EXPRESSIONS.md](references/EXPRESSIONS.md) | [DATA_STRUCTURE.md](references/DATA_STRUCTURE.md) | [AI_WORKFLOWS.md](references/AI_WORKFLOWS.md) | [PATTERNS.md](references/PATTERNS.md)

**Lessons:** [LESSONS_LEARNED.md](LESSONS_LEARNED.md) — read before non-trivial work.

**Authoritative docs:** <https://docs.n8n.io/workflows/>

---

## Before you start

1. **Identify the trigger.** Every n8n workflow needs at least one trigger
   node. Ask what kicks off the workflow if it isn't obvious. Common choices:

   | Trigger | When to use |
   |---|---|
   | Manual Trigger | Dev/testing only — user clicks Execute Workflow |
   | Schedule Trigger | Cron-style time-based runs |
   | Webhook | External HTTP callers (synchronous response option available) |
   | n8n Form Trigger | User-facing form submission |
   | Chat Trigger | AI chat workflows (LangChain bundle) |
   | App triggers (Slack, GitHub, Gmail, etc.) | Event push from a SaaS |
   | Email Trigger (IMAP) | Polling a mailbox |
   | Error Trigger | A dedicated workflow that fires when ANOTHER workflow errors |
   | Execute Sub-workflow Trigger | Entry point for a workflow called by another |

2. **Identify the destination(s).** Where does the data end up — Slack, DB,
   another workflow, a webhook response, nowhere (just side effects)?

3. **Identify the data shape.** n8n moves an **array of items** between nodes.
   Each item is `{ json: {...}, binary?: {...}, pairedItem?: {...} }`. Read
   [DATA_STRUCTURE.md](references/DATA_STRUCTURE.md) before authoring any
   non-trivial workflow.

4. **Identify edition constraints.** Some features are Enterprise/Cloud only:
   sub-workflows in some plans, RBAC, External Secrets, Source Control, Log
   Streaming. Don't propose Enterprise features without confirming the user's
   edition.

---

## Workflow JSON minimum shape

```json
{
  "name": "My Workflow",
  "nodes": [
    {
      "parameters": {},
      "id": "11111111-1111-4111-8111-111111111111",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "values": {
          "string": [{ "name": "greeting", "value": "hello" }]
        }
      },
      "id": "22222222-2222-4222-8222-222222222222",
      "name": "Set",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [460, 300]
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [
        [{ "node": "Set", "type": "main", "index": 0 }]
      ]
    }
  },
  "active": false,
  "settings": { "executionOrder": "v1" },
  "pinData": {}
}
```

**Critical rules — get any of these wrong and import breaks:**

- **Each node needs a UUID `id`.** Use proper UUID v4. Never reuse IDs.
- **Each node needs a unique `name`.** Connections key on names. Renaming a
  node requires rewriting every connection entry that references the old name.
- **`type` is `<package>.<nodeName>`** — almost always `n8n-nodes-base.<name>`
  for built-in nodes, or `@n8n/n8n-nodes-langchain.<name>` for AI cluster
  nodes. Look up the exact id at
  <https://docs.n8n.io/integrations/builtin/node-types/>.
- **`typeVersion` matters.** Older typeVersions accept different parameter
  shapes. When in doubt, use the highest documented version for that node.
- **`connections.<sourceName>.main[outputIndex]`** is an array of arrays — the
  inner arrays group connections going to the same output port (allowing
  fan-out to multiple downstream nodes).
- **`position` is `[x, y]` pixel coords** on the editor canvas. Spacing of
  ~220 px horizontally and ~160 px vertically reads well.
- **`settings.executionOrder: "v1"`** is the modern execution order. Always
  set this; the legacy mode is deprecated.

See [WORKFLOW_JSON.md](references/WORKFLOW_JSON.md) for the complete schema
including `pinData`, `staticData`, `versionId`, credentials references, and
sub-workflow `meta.templateCredsSetupCompleted`.

---

## Connection wiring patterns

### Linear (most common)

```json
"connections": {
  "Trigger": { "main": [[{ "node": "Step 1", "type": "main", "index": 0 }]] },
  "Step 1":  { "main": [[{ "node": "Step 2", "type": "main", "index": 0 }]] },
  "Step 2":  { "main": [[{ "node": "Step 3", "type": "main", "index": 0 }]] }
}
```

### Fan-out (one source, two parallel branches)

```json
"connections": {
  "Trigger": {
    "main": [[
      { "node": "Branch A", "type": "main", "index": 0 },
      { "node": "Branch B", "type": "main", "index": 0 }
    ]]
  }
}
```

### Two outputs (IF node — true on `[0]`, false on `[1]`)

```json
"connections": {
  "IF": {
    "main": [
      [{ "node": "True Branch",  "type": "main", "index": 0 }],
      [{ "node": "False Branch", "type": "main", "index": 0 }]
    ]
  }
}
```

### AI cluster wiring (Agent node uses non-`main` ports)

```json
"connections": {
  "OpenAI Chat Model": {
    "ai_languageModel": [[{ "node": "AI Agent", "type": "ai_languageModel", "index": 0 }]]
  },
  "Window Buffer Memory": {
    "ai_memory":        [[{ "node": "AI Agent", "type": "ai_memory",        "index": 0 }]]
  },
  "HTTP Request Tool": {
    "ai_tool":          [[{ "node": "AI Agent", "type": "ai_tool",          "index": 0 }]]
  }
}
```

AI cluster connection types: `ai_languageModel`, `ai_memory`, `ai_tool`,
`ai_outputParser`, `ai_embedding`, `ai_vectorStore`, `ai_document`,
`ai_textSplitter`. See [AI_WORKFLOWS.md](references/AI_WORKFLOWS.md).

---

## Expressions — the `={{ }}` template syntax

n8n parameters accept two modes per field:

- **Fixed value** — a literal string/number/boolean.
- **Expression** — starts with `=` and contains `{{ ... }}` JS-evaluated
  templates referencing built-in variables.

Common built-ins inside `{{ }}`:

| Variable | What it is |
|---|---|
| `$json` | The current item's `.json` payload |
| `$binary` | The current item's `.binary` payload |
| `$input.item` | Wraps the current item (use to access `.pairedItem`) |
| `$input.all()` | Array of all incoming items |
| `$input.first()` / `$input.last()` | First/last incoming item |
| `$('Node Name').item` | Single item from a previously-executed node |
| `$('Node Name').all()` | All items output by that node |
| `$('Node Name').first()` / `.last()` | Self-explanatory |
| `$node["Node Name"].json` | Legacy alternative to `$('Node Name').item.json` |
| `$workflow` | Workflow metadata (id, name, active) |
| `$execution` | Execution metadata (id, mode, resumeUrl) |
| `$env` | Hosting env vars (only if `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`) |
| `$now` / `$today` | Luxon DateTime helpers |
| `$jmespath()` | JMESPath query helper |
| `$secrets.<vault>.<key>` | External Secrets (Enterprise) |

**Example: pull a field from a prior node into a Slack message:**

```
=Hi {{ $('Webhook').item.json.body.username }}, new order #{{ $json.orderId }}
```

See [EXPRESSIONS.md](references/EXPRESSIONS.md) for the full reference
including string/array/object/date helpers, the `$()` accessor's rules around
nodes that haven't executed yet, and gotchas with multi-item references.

---

## The flow-logic node toolbox

| Node | Use it for |
|---|---|
| **IF** (`n8n-nodes-base.if`) | Two-way branch on a single condition |
| **Switch** (`n8n-nodes-base.switch`) | N-way branch on rules or on a value matching cases |
| **Filter** (`n8n-nodes-base.filter`) | Drop items that don't match a rule (no second branch) |
| **Merge** (`n8n-nodes-base.merge`) | Combine inputs (Append, Combine by Key, Combine by Position, SQL Query) |
| **Loop Over Items** / Split In Batches (`n8n-nodes-base.splitInBatches`) | Iterate the array of items in chunks; has a "done" output |
| **Wait** (`n8n-nodes-base.wait`) | Pause N seconds, resume at time, or resume on Webhook |
| **Stop and Error** (`n8n-nodes-base.stopAndError`) | Throw to halt the workflow with a custom message |
| **No Operation** (`n8n-nodes-base.noop`) | Join branches visually without changing data |
| **Execute Sub-workflow** (`n8n-nodes-base.executeWorkflow`) | Call another workflow (returns items) |
| **Execute Sub-workflow Trigger** | Entry point in the called workflow |

See [PATTERNS.md](references/PATTERNS.md) for proven recipes:

- **Loop with rate limit** — Loop Over Items + Wait
- **Aggregate then summarize** — Aggregate + Summarize
- **Error workflow handoff** — Error Trigger → Slack/PagerDuty
- **Webhook → process → respond synchronously** — Webhook (Respond: "Using
  Respond to Webhook Node") → ... → Respond to Webhook
- **Long-running webhook** — Webhook (Respond: Immediately) → background work
- **Idempotency** — Remove Duplicates + Data Tables
- **Pagination** — HTTP Request with built-in Pagination options OR Loop with
  cursor stored in `getWorkflowStaticData('global')`

---

## AI workflows (cluster nodes)

The LangChain bundle (`@n8n/n8n-nodes-langchain.*`) adds **root nodes**
(Agent, Chains, Vector Store roots, Information Extractor, Text Classifier,
Sentiment Analysis) plus **sub-nodes** (Chat Models, Memory, Tools, Output
Parsers, Embeddings, Text Splitters, Document Loaders, Retrievers, Rerankers).

Sub-nodes attach to root nodes via **non-`main` connection types** listed
above. They don't process items in the normal data-flow sense — they
configure the root node.

Common stacks:

- **Chat Agent:** Chat Trigger → AI Agent + OpenAI Chat Model + Window Buffer
  Memory + (one or more Tools)
- **RAG QA:** Question and Answer Chain + OpenAI Chat Model + Vector Store
  Retriever + Vector Store + Embeddings + Document Loader + Text Splitter
- **Information Extractor:** Source → Information Extractor + Chat Model +
  Structured Output Parser → downstream

See [AI_WORKFLOWS.md](references/AI_WORKFLOWS.md) for full topologies, the
`fromAI()` function for tool parameters, evaluations, and human-in-the-loop
patterns.

---

## Procedure (every workflow-build request)

1. **Clarify trigger + destination + data shape** (one short paragraph back to
   the user) if not obvious from the request.
2. **Read existing JSON if any.** Don't blindly overwrite. Preserve unrelated
   nodes, keep node IDs, keep credential references.
3. **Plan node graph on paper first.** List nodes, their types, and the
   connection topology. Catch missing merges or unwired branches NOW, not
   after generating JSON.
4. **Generate the JSON.** Use the patterns above. Use real UUIDs (`uuidgen`,
   `crypto.randomUUID()`, or any UUID v4 generator).
5. **Hand the user copy/paste-ready JSON.** Tell them: "Import this via
   Workflow menu → Import from File (or paste into a new tab via Ctrl/Cmd-A,
   Ctrl/Cmd-V on the canvas)."
6. **Call out credentials they need to attach.** Workflow JSON includes a
   `credentials` reference per node by name+id, but the actual credential
   values live in the n8n instance. The user must select credentials for any
   node that needs them after import.
7. **Mention activation gotchas:** for Webhook/Schedule/Form/App triggers,
   workflows only fire on the **Production URL / production schedule** after
   the user toggles "Inactive → Active" in the top bar.
8. **Update `LESSONS_LEARNED.md`** if you discovered anything per the agent's
   continuous-learning rules.

---

## Best practices

**Do:**
- Set `settings.executionOrder` to `"v1"` always.
- Name nodes descriptively. The name is what shows up in expressions
  (`$('My Descriptive Name').item.json...`).
- Add **Sticky Notes** (`n8n-nodes-base.stickyNote`) to document non-obvious
  sections. They cost nothing at runtime and survive export/import.
- Use **Edit Fields (Set)** liberally to shape data into the schema the next
  node expects. Better than complex expressions everywhere.
- Use **Sub-workflows** for any logic shared by 2+ workflows or for blocks
  that exceed ~15 nodes.
- Add an **Error Workflow** at the instance level for production work — set
  it as `errorWorkflow` in the workflow settings, and build a separate
  workflow whose trigger is the Error Trigger node.
- Use `Loop Over Items` (Split In Batches) when calling rate-limited APIs;
  pair it with the Wait node.
- Use `Remove Duplicates` keyed on a stable ID for idempotent processing of
  upstream feeds.
- For long-running webhooks, set Webhook → Respond: "Immediately" and do work
  in the background.

**Don't:**
- Don't fan out into 5+ parallel branches that all hit the same API — you'll
  rate-limit yourself. Sequence with Loop Over Items + Wait instead.
- Don't use Manual Trigger in production workflows. It won't fire on
  schedule/webhook/event.
- Don't put secrets in node parameters as plain text — use Credentials, or
  for Enterprise, External Secrets.
- Don't depend on item order across branches that merged — order is
  preserved within a branch but not across merges (use Merge → Combine by
  Key when order matters).
- Don't forget to handle the "no items" case in Loop Over Items — if the
  input is empty, the loop never runs and downstream nodes may not execute.

---

## Common mistakes (read [PATTERNS.md](references/PATTERNS.md) for full list)

| Symptom | Likely cause | Fix |
|---|---|---|
| "Cannot read properties of undefined (reading 'json')" | Referencing a node that hasn't run on this branch | Use `$('Node').first()?.json.field ?? 'fallback'` |
| Workflow runs once then nothing | Manual Trigger only fires on Execute Workflow | Replace with Schedule/Webhook/App trigger |
| Webhook returns empty body to caller | Default Webhook responds with "When last node finishes" but workflow doesn't return data | Use Respond to Webhook node and set Webhook → Respond: "Using Respond to Webhook Node" |
| IF/Switch sends nothing downstream | Confused which output port is true vs false | IF: index 0 = true, 1 = false. Switch: order matches rule order |
| `$json` in Code node returns wrong shape | Code node runs ONCE for all items by default | Set "Mode: Run Once for Each Item" or iterate `$input.all()` |
| Pairing breaks after a Code node | Code node didn't set `pairedItem` on returned items | See [n8n-code-node](../n8n-code-node/SKILL.md) for the canonical pattern |
| Imported workflow can't run | Credentials weren't selected post-import | After import, open each node with a yellow warning triangle and pick credentials |

---

## Continuous learning

If during this session you discovered:
- A node-specific quirk that wasn't documented
- A wiring pattern that solved a non-obvious problem
- A version-specific behavior change
- A workaround for an n8n bug

… append a dated entry to [LESSONS_LEARNED.md](LESSONS_LEARNED.md) using the
[Lesson entry template](../../agents/n8n.agent.md#lesson-entry-template) from
the agent file. Brief is better than nothing.
