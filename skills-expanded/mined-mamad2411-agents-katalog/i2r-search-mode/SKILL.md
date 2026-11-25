---
name: i2r-search-mode
description: Conditional evidence search producing 02b-evidence.json; informs terminology, constraints, and comparable patterns — never invents scope.
when_to_use: When i2r-evidence-researcher is activated by the L0 router (search_mode != "not_required"); skip entirely when the router marks search not_required.
user-invocable: false
---

# i2r-search-mode

## Role in the pipeline

`i2r-evidence-researcher` leans on this skill to produce `02b-evidence.json`
(schema: `schemas/02b-evidence.schema.json`). Every evidence card must carry a verifiable `source_ref` —
that is what the `i2r-citation-gate` hook actually enforces (it runs `i2r.py evidence.validate`).
Linking a downstream requirement back to an `EV-NNN` card is **author discipline**, not gate-enforced:
the gate does not verify requirement-level `evidence_ref`.

## Hard boundary (load-bearing)

Search evidence **informs** — it never decides scope and never overrides user intent.
The only things evidence is allowed to touch:

| Allowed `used_for` | Meaning |
|--------------------|---------|
| `context` | background / domain framing |
| `constraint` | regulatory, platform, or performance ceiling from an authoritative source |
| `nfr` | published SLA, compliance threshold, accessibility standard |
| `terminology` | canonical term to use in requirements text |
| `pattern` | comparable integration or architecture pattern |

Evidence is **not allowed** to:
- Add capabilities to `in_scope` (only intake + scope-architect may do that)
- Override a `stated` user decision
- Substitute for a missing clarification (surface as a `GAP` instead)

## Output contract

File: `.i2r/runs/<slug>/<run-id>/internal/stages/02b-evidence.json`
Owner agent: `i2r-evidence-researcher`
Must include `_meta.skills_used: ["i2r-search-mode"]`.

Required top-level fields (per schema):
- `search_mode` ∈ `{ local, web, mixed, unavailable }`
- `evidence[]` — zero or more cards (see `references/evidence-ledger-rules.md`)
- `gaps[]` — unanswered research questions (blocking or non_blocking)
- `research_questions[]` — optional, records what was asked

## Decision tree: search or not

```
L0 router decision
    |
    ├─ search_mode == "not_required"  → skip; 02b-evidence.json is NOT produced
    |
    ├─ search_mode == "local"         → search only raw/ + project docs
    |
    ├─ search_mode == "web"           → external sources per source-policy
    |
    ├─ search_mode == "mixed"         → local first, then web for gaps
    |
    └─ search_mode == "unavailable"   → record all questions as GAPs; produce
                                        empty evidence[], set all GAPs to
                                        non_blocking unless a specific constraint
                                        is truly unresolvable
```

## What the researcher does

1. Read `01-intake.json` and `02-context.json` to extract open research questions.
2. For each question, assign an `RQ-NNN` id and record in `research_questions[]`.
3. Search per `search_mode` and source ranking (see `references/source-policy.md`).
4. For each finding, produce an evidence card per `references/evidence-ledger-rules.md`.
5. For unanswered questions, produce a `GAP-NNN` record with `impact` classification.
6. Write `02b-evidence.json` and run `i2r.py validate --stage 2b`.

## What the researcher never does

- Fabricate a source or invent a citation
- Promote a `low`-confidence finding to a `stated` requirement
- Suggest new features or capabilities beyond what intake identified
- Call external skills at runtime (vendor-not-install, CONTRACT §0)

## References

- `references/evidence-ledger-rules.md` — evidence card shape, gap rules, when to search
- `references/source-policy.md` — source_type ranking, confidence assignment, scope guard

Vendored sources: SuperClaude research discipline; Anthropic multi-agent grounding guidance; claude-api source-grounding patterns.
