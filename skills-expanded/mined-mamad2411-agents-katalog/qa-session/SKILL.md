---
name: qa-session
description: Run a QA session for a unit of work (milestone, task, diff, PR) against any surface — Website, Docker Compose, HTTP API, gRPC, MCP, GraphQL. Derives the user experience the work should deliver, confirms it, probes the running surface, delivers a verdict report. Triggers include "QA this", "QA session", "verify the milestone", "verify this PR", "acceptance check", "does this deliver", "check user experience".
---

Run the QA session as four steps. Each ends on its completion criterion; do not advance early.

## 1. Bound the work

Identify the work unit and what changed in it: read the milestone/task/diff/PR description and the actual changes (diff, files, commits). Ground facts in the repo; note claims the description makes that the diff does not show.

Completion: one paragraph — what changed, what it claims to deliver.

## 2. Derive the UX contract

From the work unit, state the user experiences that should be observable on the surface. For each expectation write: who the user is, what they do, what they must see or get. Expectations are outcome statements, not implementation steps.

Then confirm with the user via `ask`: present the contract, ask them to correct, add, or drop expectations. Do not probe before confirmation — a QA session against the wrong contract produces a confident wrong verdict.

Completion: user-confirmed list of expectations. This list is the source of truth for the verdict.

## 3. Probe the surface

Load the reference for the surface the user named, read it, then probe:

- Website → `skill://qa-session/references/website.md`
- HTTP API → `skill://qa-session/references/http.md`
- gRPC API → `skill://qa-session/references/grpc.md`
- MCP server → `skill://qa-session/references/mcp.md`
- GraphQL API → `skill://qa-session/references/graphql.md`
- Docker Compose → `skill://qa-session/references/compose.md`

If the surface is not running, bring it up first (compose.md covers startup for stack surfaces). Probe every confirmed expectation. Each expectation MUST end with a verdict and captured evidence — a screenshot, a response body, a log line, a measured value. An expectation without evidence is unprobed, not passed.

Completion: every expectation has verdict + evidence, or is explicitly marked blocked with the reason (surface unreachable, prerequisite missing).

## 4. Verdict report

Deliver:

```
## QA Verdict: <work unit> — <N>/<total> pass

PASS <expectation> — <evidence one-liner>
FAIL <expectation> — <what diverged>, <evidence one-liner>
BLOCKED <expectation> — <why>

Blocking: <count> — <the failures that break the core experience>
```

Classify a failure blocking when it breaks the experience a normal user hits on the happy path. Divergences on edge cases, cosmetics, or contract details are non-blocking unless the work unit explicitly claims them. Cite evidence verbatim; never summarize a response you did not capture.
