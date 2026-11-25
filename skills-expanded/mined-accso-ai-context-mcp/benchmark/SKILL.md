---
name: benchmark
description: >
  Use when the user asks to run/start/execute a retrieval benchmark session,
  or mentions comparing ai-context vs idea-mcp vs baseline tooling on a
  target repo. Drives exactly one isolated arm of the 3-arm .ai-context
  retrieval benchmark (ai-context | idea-mcp | baseline), instrumented with
  bench.js, and writes its report/CSV into
  .ai-context/docs/benchmark/sessions/.
---

# Benchmark — Retrieval Toolset Comparison

This skill runs **one isolated arm** of a 3-arm benchmark that compares three
ways of answering the same real codebase questions against a target repo:

- **ai-context** — this repo's `<project>-context_*` MCP tools only
- **idea-mcp** — JetBrains/idea-mcp tools only
- **baseline** — no special tooling, generic `find`/`grep`/read only

Each arm must be run in a **brand-new session/context that has not yet
explored the target repository** — that isolation is the entire point of the
benchmark. Never run more than one arm in the same context, and never let one
arm see another arm's reference document or results.

## Step 0 — Ask which arm to run

Before doing anything else, **ask the user which session to start**:
`ai-context`, `idea-mcp`, or `baseline`. Do not guess or default — it decides
which reference document governs the rest of this session, and the three are
mutually exclusive within one context.

## Step 1 — Read the matching reference document, and only that one

| Session | Reference document (read this one, ignore the other two) |
|---|---|
| `ai-context` | `references/benchmark-session-ai-context.md` |
| `idea-mcp` | `references/benchmark-session-idea-mcp.md` |
| `baseline` | `references/benchmark-session-baseline.md` |

Also read the frozen query-set file the operator provides (not shipped in this repo) — the query set and
pre-written ground truth shared by all three arms. Do not invent queries and
do not explore the repo to build your own list; use this file verbatim.

## Step 2 — Ask clarifying questions before you start

Confirm with the operator whatever the chosen reference document's "For the
Benchmark Operator" table asks for (target repository, date, approximate
file/folder counts, primary language(s), executing model, IDE/idea-mcp
version if running that arm) — fill it into your final report's Metadata
table. Don't start Step 4 until you have these.

## Step 3 — Clean up this arm's previous output (that arm only)

Before answering any query, delete only the files belonging to the session
you are about to run from `.ai-context/docs/benchmark/sessions/` — **never
touch the other two arms' files**, they may still be needed for comparison:

- `<session>_summary.csv` (e.g. `ai-context_summary.csv`, `idea-mcp_summary.csv`, `baseline_summary.csv`)
- any prior `benchmark-session-<A|B|C>-<session>-*.md` report for this same
  arm (filename includes the target-repo name and run date, so match by the
  `<session>` segment, e.g. `*-ai-context-*.md`)

If nothing exists yet for this arm, there's nothing to remove — proceed.

## Step 4 — Run the session strictly per the reference document

Follow the reference document from Step 1 **completely and in order** — it
already contains the full instructions for:

- which tools are allowed for this arm (and that using anything outside that
  list invalidates the query's data point),
- mandatory `bench.js` instrumentation
  (`.ai-context/docs/benchmark/bench.js`, relative to the repo root) —
  `wrap` for single shell commands, `start`/`stop` for MCP/IDE tool calls;
  any action not logged this way cannot be scored,
- per-query scoring (tool-call count, tokens, token quality, time, response
  quality vs. ground truth),
- the exact final report structure and filename.

Do not skip, shorten, or reinterpret any of that — this skill only routes
you to it and handles cleanup/output location; the reference document is the
actual protocol.

## Step 5 — Save results

At the end of the reference document's Step 3 ("Report"), you will have run
`bench.js report --session <session> --csv <session>_summary.csv`. Save
**both** outputs into `.ai-context/docs/benchmark/sessions/`:

- the Markdown report, named exactly as the reference document specifies
  (e.g. `benchmark-session-A-ai-context-<repo-name>-<date>.md`)
- the `<session>_summary.csv` file `bench.js report` produced

Include the printed `bench.js report` output in your session write-up, as
the reference document's instrumentation section requires.
