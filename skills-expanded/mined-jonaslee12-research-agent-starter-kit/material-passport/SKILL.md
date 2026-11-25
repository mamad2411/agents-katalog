---
name: material-passport
description: Use before formal research writing or delivery to package source readiness, compliance or requirement evidence, citation boundaries, and unresolved confirmations for the artifact being moved forward.
---

# Material Passport

Use this skill when a formal research artifact is about to move from planning to drafting, drafting to review, or review to delivery.

## Purpose

Create a compact evidence passport for the artifact so the agent does not treat a polished draft as ready when sources, requirements, compliance, citations, or open confirmations are still weak.

## Activate For

- proposal, manuscript, thesis/dissertation section, report, grant, protocol, or reviewer/stakeholder-facing draft
- formal Word/PDF delivery
- citation-heavy or requirement-sensitive writing
- ethics, privacy, IRB, client, funder, journal, or institutional requirement claims
- any task entering `research-wiki/DOCUMENT_PIPELINE.md`

## Workflow

1. Identify the artifact, audience, purpose, and output status.
2. Choose passport scope:
   - `short`: internal planning or early draft movement; missing optional evidence becomes `WARN`.
   - `full`: reviewer-facing, stakeholder-facing, submission-facing, or final delivery; missing required evidence becomes `HOLD`.
3. Check the strongest available local evidence:
   - source-readiness record;
   - compliance or requirement tracker;
   - citation or claim-support report when citation-heavy;
   - runtime receipt, source map, and integrity preflight for full-scope delivery.
4. List unresolved `TO CONFIRM` items.
5. State the boundary clearly: the passport packages readiness evidence; it does not prove claim support, approval, acceptance, or official compliance.

## Local Tool

```bash
python3 scripts/material_passport.py --artifact <path> --scope short
python3 scripts/material_passport.py --artifact <path> --scope full --audience reviewer-facing
```

Add flags when relevant:

```bash
--requires-compliance
--requires-requirements
--citation-heavy
--citation-report <path>
--runtime-receipt <path>
--source-map <path>
--integrity-report <path>
--quality-gate <path>
--to-confirm "field or decision still unresolved"
```

## Failure Behaviour

- `PASS`: required evidence is present for the selected scope.
- `WARN`: short-scope passport has missing or non-blocking evidence.
- `HOLD`: full-scope or required evidence is missing.

If status is `HOLD`, do not call the artifact ready, client-ready, submission-ready, or publication-ready. Resolve the missing evidence, reduce the claim, or keep the artifact as a working draft.

## Boundaries

- A passport does not prove that cited sources support claims.
- A passport does not upgrade metadata-only sources.
- A passport does not replace compliance, ethics/IRB, journal, funder, client, supervisor, peer-review, or institutional approval.
- Retrieval tools, Obsidian, Zotero, and external metadata searches remain support tools, not evidence authorities.
