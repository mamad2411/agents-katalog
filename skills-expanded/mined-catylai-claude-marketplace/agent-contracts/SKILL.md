---
name: agent-contracts
description: "Use when writing or checking a review agent's JSON artifact, or building a pipeline that consumes one. The JSON finding contract: document keys, the ten finding keys, id format and enums. Not for general schema design (use agent-craft:output-contracts)."
user-invocable: false
license: MIT
---

# Agent output contract

A review agent writes two things: a JSON artifact the pipeline acts on, and a Markdown companion a
person reads. The pipeline decides from the JSON only, so the prose can stay readable while the gate
stays reliable.

**Source of truth.** In code-review-core the contract is executable:
`pipeline/schemas/agent-contract.schema.json` is generated from `pipeline/contract.py`, and
`contract.py` alone defines when a finding blocks. When this page and those files disagree, the
files win; report the drift. A new pipeline imports or vendors `contract.py` rather than
re-implementing it from prose.

This page owns the keys, the id format and the enums. What each severity, scope and confidence value
means is owned by `code-review-standards`; the causation test behind `in_diff` by `file-scope-rules`.

## The document

| Key | Required | Value |
| --- | --- | --- |
| `agent` | yes | your agent name, non-empty |
| `category` | yes | your artifact name, e.g. `SEMANTIC`, `TESTING`, `ARCHITECTURE`, `CLAUDE_CONFIG`; `SCAN` and `VALIDATED` belong to the pipeline |
| `findings` | yes | array of findings, `[]` when you found nothing |
| `source_branch`, `target_branch`, `reviewed_sha` | no | strings, copied from the review context |
| `coverage` | judges: yes | object: `gaps_covered`, `gaps_not_covered`, `files_read` (string arrays), `reads_used` (integer), `notes` (string) |
| `scan_triage` | `SEMANTIC` only | array of `{id, decision, severity?, confidence?, reason}`, one per scanner finding triaged |
| `verdict` | no | `APPROVE` \| `REQUEST_CHANGES` \| `INCOMPLETE`; nothing reads a specialist's own verdict |
| `metrics` | no | integer `total`, `blocker`, `major`, `minor`, `nit`, `ux_impact_count`; `coverage_pct` number or null |

Extra keys are allowed. `rejected_count`, `blocking_reason_ids`, `blocking_floor`,
`incomplete_inputs` and `contract_health` appear only in `VALIDATED.json`, which
`contract.py finalize` writes; an agent never writes them.

```json
{
  "agent": "review-semantic",
  "category": "SEMANTIC",
  "source_branch": "feature/x",
  "target_branch": "main",
  "reviewed_sha": "<sha>",
  "findings": [],
  "coverage": {"gaps_covered": [], "gaps_not_covered": [], "files_read": [], "reads_used": 0, "notes": ""}
}
```

## A finding

All ten keys are required, spelled exactly:

| Key | Value |
| --- | --- |
| `id` | `<PREFIX>-<SEVERITY>-<n>`, e.g. `SEM-MAJOR-2`; the severity token equals `severity`, and the id stays stable across runs |
| `severity` | `BLOCKER` \| `MAJOR` \| `MINOR` \| `NIT` |
| `category` | non-empty string |
| `location` | one `path:line` string, a line you verified (not `file` + `line`) |
| `title` | one line, 1–300 characters (not `summary`) |
| `evidence` | the code itself, raw, not fenced |
| `recommendation` | a concrete fix; `""` when you have none |
| `ux_impact` | boolean: an end user would notice |
| `in_diff` | boolean: this change introduced or worsened it |
| `confidence` | `HIGH` \| `MEDIUM` \| `LOW` |

Judge agents add `lens`, the name of the lens that raised the finding.

Enums are closed and upper-case. Emit exactly these values; a near miss such as `"High"` or `"INFO"`
is repaired or escalated by the pipeline rather than trusted. A finding missing `id`, `severity`,
`location` or `title` asserts nothing: the pipeline drops it from the author's list and records it in
`contract_health` for the tooling owner.

## How the verdict follows

`contract.py` computes it, in `finding_blocks`, `finding_escalates` and `rollup_verdict`; agents
supply honest values. In one line: an in-diff, non-`NIT` finding at or above the blocking floor (or
with `ux_impact`) blocks at `HIGH` confidence and escalates the review to `INCOMPLETE` below it.
Read those functions for anything finer, rather than inferring from this sentence.

## Completion trailer

Owned by `code-review-core:judge-protocol`.

## Verify

Parse the artifact and check it against the schema, for example
`python3 -c 'import json,sys; json.load(open(sys.argv[1]))' .code-review/<CATEGORY>.json`, then
confirm every finding has all ten keys and every id's severity token equals its `severity`. Without a
checkout, check pasted JSON against the tables above.
