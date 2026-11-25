---
name: graph-first
description: "Call BEFORE searching the code with grep or opening files at random. Trigger words (RU+EN): где определено, кто вызывает, что сломается от правки, где используется, найди в коде, зависимости модуля, точки входа / where is it defined, who calls it, what breaks on this edit, where is it used, find in code, module dependencies, entry points. Navigate by graph (graphify) instead of brute force. Boundary: the graph answers about functions and relations; for properties, strings and patterns use grep."
---

# The graph is the first search tool, not grep

Layers and a split by domains give many files; running over them by reading and grep is tokens down
the drain. The graph answers "where" and "what will break" in a single query.

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/retainer-graph.sh" explain "<entity name>"   # where it lives + who calls it + what it depends on
"${CLAUDE_PLUGIN_ROOT}/bin/retainer-graph.sh" path "<A>" "<B>"           # how A relates to B
```

`explain` and `path` walk the AST graph — deterministic and hit the target. Run the command from
the project tree, or pass `-C <project dir>`.

## Where the graph lives, and why it is never stale

The graph of a project lives in the engine's state home of that project, not in its tree: nothing
is committed, no gate reads it. Before answering, the command compares a fingerprint of the tree
(the index, the unstaged diff, the untracked files) with the one the graph was built from, and
rebuilds first when they differ — a few seconds once, then the answer in under a second. The first
query in a project builds the graph. Closing a task refreshes an existing graph in the background.

A failed rebuild exits 1 with graphify's own words, and its graph is not used for the answer; the
next query tries again. No graphify installed — exit 2 and the install command
(`uv tool install graphifyy`).

Searching for a function name with grep in a managed project brings a hint naming this command —
take it instead of reading the grep output.

## The graph answers about FUNCTIONS. About properties and templates — NO

Not a caveat but a measurement (checked on a live task):

```
explain "_attach_costs"        → Degree 9: showed every caller
explain "total_cost_per_year"  → Degree 2: only the class and the docstring,
                                 NOT A SINGLE caller
```

A model property is read as an **attribute** (`obj.total_cost_per_year`), not called — the AST
builds no edge for that. Templates (`{{ obj.total_cost_per_year }}`) do not enter the graph at all:
they are not Python.

| You seek | Tool |
|---|---|
| who calls a **function** | `retainer-graph.sh explain` ✅ |
| who reads a **property/model field** | **grep** — the graph does not know |
| use in **templates** | **grep** — the graph does not index them |
| how A relates to B | `retainer-graph.sh path` ✅ |
| "the code that does such-and-such" (you don't know the name) | **grep** |

**`graphify query "natural language"` without an LLM key — NOISE. Do not use.** It latches onto
single words and wanders into documents. Start with `explain`.

The graph says **where**, not **what**. The file is read before editing anyway.

An LLM key is needed only for NON-code (documents, images). Code goes through the AST, for free.
Without a key the code graph is complete; only `query` suffers.

## When NOT to apply

- **A question about properties and templates, not functions.** "Where else does this string
  appear", "what format are these files", "is there a TODO here" — that is grep, and the graph
  answers it worse.
- **An edit in a single file that is already open.** Building a path through the graph for a
  neighboring line costs more than reading it.
- **A one-off question about a foreign tree.** The first query builds the graph; for a tree you will
  not ask again, that build costs more than a grep.
