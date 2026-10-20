# Architecture Decision Records

## Summary

**One-sentence:** Produces an ADR (context + decision + alternatives + consequences + status lifecycle) stored in-repo so significant architecture choices outlive the team's memory and stop the same debates from recurring.

**Ефективно для:** Solo devs and small teams who keep re-debating 'why did we pick Postgres over MongoDB' every six months because nobody wrote it down.

**One-paragraph:** ADRs capture significant architectural decisions with context, alternatives, and consequences. Storing them in version control (not wikis) preserves the why alongside the code. This methodology pins each ADR to 1-2 pages, enforces the Nygard status lifecycle (Proposed → Accepted → Deprecated | Superseded), and requires ≥2 genuine alternatives. Output is consumed by design-docs-patterns and code-review-cycle.

## Applies If (ALL must hold)

- Significant architectural decision (database, framework, language, deployment target).
- Decision will be revisited or questioned within 18 months.
- Multiple alternatives exist (≥2 genuine, not strawmen).
- Repo has a docs/adr/ or .aidocs/decisions/ folder.

## Skip If (ANY kills it)

- Operational tweaks (CDN cache TTL, log level).
- Decisions reversible inside a single sprint.
- One-person hobby project with no future readership.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| decision title | string | author |
| ≥2 genuine alternatives | array | team |
| context paragraph | string | author |
| ADR index file | markdown | repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/design-docs-patterns` | Sibling — ADRs extract from design docs once locked. |
| `solo/sdd/sdd/living-documentation` | Parent — ADRs live in docs-as-code repo. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/architecture-decision-records.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/architecture-decision-records.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-architecture-decision-records.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[design-docs-patterns]] — related methodology.
- [[design-docs-big-tech]] — related methodology.
- [[code-review-cycle]] — related methodology.
- [[living-documentation]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/architecture-decision-records.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/architecture-decision-records.json",
  "title": "Architecture Decision Records Output Contract",
  "type": "object",
  "required": [
    "adr_id",
    "title",
    "status",
    "context",
    "decision",
    "alternatives",
    "consequences",
    "supersedes",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "adr_id": {
      "type": "string",
      "description": "stable id (ADR-001..)"
    },
    "title": {
      "type": "string",
      "description": "decision title"
    },
    "status": {
      "type": "string",
      "description": "Proposed | Accepted | Deprecated | Superseded"
    },
    "context": {
      "type": "string",
      "description": "background paragraph"
    },
    "decision": {
      "type": "string",
      "description": "what was decided"
    },
    "alternatives": {
      "type": "array",
      "description": "\u22652 with rationale",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "consequences": {
      "type": "object",
      "description": "{positive: [...], negative: [...]}"
    },
    "supersedes": {
      "type": "string",
      "description": "ADR id this replaces (or null)"
    },
    "owner": {
      "type": "string",
      "description": "named author"
    },
    "version": {
      "type": "string",
      "description": "semver"
    },
    "last_reviewed": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    }
  },
  "additionalProperties": true
}
```

### `templates/_smoke-test.json`

```json
{
  "adr_id": "sample-adr_id",
  "title": "sample-title",
  "status": "sample-status",
  "context": "sample-context",
  "decision": "sample-decision",
  "alternatives": [
    {
      "k": "v"
    }
  ],
  "consequences": {
    "k": "v"
  },
  "supersedes": "sample-supersedes",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
