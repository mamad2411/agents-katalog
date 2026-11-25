---
name: tool-scope-abuse-probe
description: >-
  Exercise each tool at the widest scope it was ever granted, using the correct
  identity and well-formed arguments, to find what it can do outside the job it
  was added for. Use when reviewing a tool manifest, an MCP server, or a tool
  that takes a query, a path or a command as a free-text argument.
allowed-tools: Read, Grep, Glob
---

# The tool was scoped for the widest job it ever does

Tool misuse needs no stolen credential and no malformed input. It is the
correct identity calling a familiar tool with well-formed arguments — for a
request the tool was never meant to serve. The defect is the **argument
surface**, not the caller.

## When to use this

Reviewing any tool whose argument is a language: SQL, a shell command, a file
path, a URL, a search query. Also after any change that widens a tool's scope
"temporarily".

## Procedure

**1 — List the tools and, for each, the job it was added for.** One sentence.
If nobody can produce that sentence, the tool has no scope to compare against
and that is the first finding.

**2 — Derive the granted surface from the implementation,** not the
description. A `run_query` tool that accepts arbitrary SQL grants every verb on
every table the connection can see, whatever the description says.

**3 — Probe the gap.** For each tool, construct a well-formed call that is
inside the granted surface and outside the stated job. Read a secret, touch a
table the feature never names, write where the job only reads.

**4 — Record what came back**, and whether anything refused. A refusal that
came from the downstream — a database permission, a bucket policy — is a real
control; a refusal that came from the tool's own docstring is not.

**5 — Propose the narrowing.** Name the verb and the resource, not the tool:
`SELECT on bookings` rather than `run_query`. A narrowing that cannot be
written in that form is not a narrowing.

## Example

**Input** — the fixture committed at the top of [`scripts/tool_scope_abuse_probe.py`](scripts/tool_scope_abuse_probe.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
intended use:
   how many invoices  -> {'rows': [{'id': 7, 'amount': 120}]}

same tool, same identity, same well-formed arguments:
   signing key        -> {'rows': [{'id': 1, 'value': 'prod-signing-key'}]}
   clean up secrets   -> {'deleted': 1, 'table': 'secrets'}

secrets table now: []
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "tools": [{"name": "str", "stated_job": "str", "granted_surface": "str", "unbounded": false}],
  "probes": [{"tool": "str", "call": "str", "outside_stated_job": true, "refused_by": "none|tool|downstream"}],
  "narrowing": [{"tool": "str", "verbs": ["str"], "resources": ["str"]}]
}
```

## Failure modes

- **Reading the description as the scope.** The description is what the tool is
  for; the implementation is what it can do.
- **Counting a docstring refusal as a control.** It is a comment.
- **Narrowing to the tool name.** `run_query` is not a permission; a verb on a
  resource is.
