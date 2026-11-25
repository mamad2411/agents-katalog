---
name: squad-decompose
description: Decompose a squad spec into 3-7 captured items for triage. Takes a spec name; reads the spec; drafts items via squad_new; lands them in the inbox linked to the parent spec.
argument-hint: "<spec-name>"
allowed-tools:
  - mcp__squad__squad_decompose
  - mcp__squad__squad_new
  - Read
  - Edit
disable-model-invocation: true
---

You are decomposing a squad spec into draft items.

## Step 1: Get the prompt

Call the `squad_decompose` MCP tool with `{"spec_name": "$ARGS"}`. It returns a `prompt` string. Read that prompt carefully — it tells you exactly what to do.

## Step 2: Read the spec

The prompt will tell you the spec path (`/path/to/.squad/specs/<name>.md`). Read it end-to-end.

## Step 3: Draft items

Per the prompt, propose 3-7 claimable items that decompose the spec's acceptance criteria. For each item:
- title: ≤8 words, action-oriented
- area: a real area tag (look at .squad/items/ for existing examples)
- estimate: 30m / 1h / 4h / 1d (be honest)
- risk: low / medium / high

For each, call `squad_new` with:
```json
{
  "type": "feat",
  "title": "<the title>",
  "area": "<area>",
  "estimate": "<estimate>",
  "risk": "<risk>"
}
```

(Use `task` or `bug` instead of `feat` when the work is clearly that.) `squad_new` returns `{id, status, path}`. The `path` is the absolute path to the item file.

`squad_new` does not accept `parent_spec` as a top-level argument. After each call, use `Edit` on the returned `path` to insert `parent_spec: $ARGS` into the YAML frontmatter (add a new line under the existing frontmatter fields, between the opening and closing `---` markers).

Default status (captured) is correct. Do NOT pass `ready: true` — a human triages these via `squad inbox`.

## Step 4: Summarize

Print one line: "decomposed $ARGS into N items: ID-1, ID-2, ..."
