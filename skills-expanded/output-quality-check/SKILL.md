---
name: output-quality-check
description: "When the user wants an independent quality check of an artifact produced by a PMM skill, such as a brief, strategy, plan, or asset. Checks the output against the originating skill's own explicit requirements and routes failures back for correction. For company-message alignment use messaging-consistency-audit; for SKILL.md structure use repository validation or skill specification review."
metadata:
  version: 1.0.0
---

# Output Quality Check

Independently answer: did the originating skill produce an output that meets
the quality standard declared by that skill? The originating skill owns the
domain standard. This skill reads and applies it without adding a universal PMM
rubric.

## Scope boundary

- Verify output quality against the originating skill's explicit requirements.
- Do not decide whether an asset matches company messaging. That belongs to
  `messaging-consistency-audit` and the canonical SSOT.
- Do not audit whether a `SKILL.md` is well structured. Use repository
  validation or the applicable skill-spec review process.
- Do not silently edit the artifact. Report corrections and route them back to
  the originating skill.

An artifact can pass both reviews, fail either one, or fail both. Keep their
findings and statuses separate. For a market-facing asset, the useful flow is
`originating skill → artifact → output-quality-check → messaging-consistency-audit →
approval or remediation`. The messaging audit is not required for internal
artifacts where it is irrelevant.

## Inputs and standard discovery

Accept the artifact and its claimed originating skill or infer the skill from
artifact metadata, format, or user context. If origin remains ambiguous, ask
which skill produced it. If the artifact is absent, request it. Never verify a
summary in place of the complete artifact when the full version is available.

Read the originating skill's current `SKILL.md` before evaluating the artifact.
Extract all explicit, applicable criteria from its declared:

- required output and sections;
- process or workflow requirements that leave observable evidence in the output;
- output rules and format constraints;
- quality gates, verification criteria, and checklists;
- evidence, traceability, safety, and approval requirements.

Use only requirements actually stated by that skill or by a shared reference it
explicitly requires. Follow referenced shared standards, such as
`../_shared/evidence-gaps.md`, when applicable. Do not import criteria from a
neighboring skill, this verifier's preferences, or generic notions of good PMM
work. If the skill declares no explicit verifiable criteria, report that
limitation and mark the affected check UNVERIFIABLE. Do not invent a rubric.

Read the entire artifact. Evaluate each requirement independently and cite the
artifact location or quote that supports the finding. A claim that a step was
completed is not evidence when the required source or artifact is unavailable.

For audience-dependent work, apply the persona-consumption requirements in
`../_shared/ssot-consumption.md` when required by the originating skill.
Inspect whether relevant intelligence supports the material choices in the output
and preserves source access, evidence status and uncertainty. Existing rationale
or annotations suffice; no separate audience table or exhaustive attributes are
required. Shared treatment may be valid when evidence supports shared needs.
Non-audience tasks are exempt. Missing nonessential metadata is not a failure;
unavailable essential evidence is UNVERIFIABLE. Do not invent persona differences
or certify unsupported application. Route failures to the originating owner;
message-to-canon alignment remains a separate messaging review.

## Finding statuses

Assign each applicable requirement exactly one result:

| Result | Use |
|---|---|
| `PASS` | Observable artifact evidence meets the originating skill's requirement. |
| `FAIL` | The artifact contradicts or omits a requirement that can be checked. |
| `NOT_APPLICABLE` | The originating skill permits a conditional requirement and the artifact provides a valid reason it does not apply. |
| `UNVERIFIABLE` | Required evidence/input is unavailable, or a claimed requirement cannot be independently confirmed. Do not count this as PASS. |

Overall status is `PASS` only when every applicable criterion is PASS or
NOT_APPLICABLE and none is UNVERIFIABLE. Otherwise use `NEEDS_CORRECTION`.
Report UNVERIFIABLE separately from actual FAIL findings. Do not imply that
absence of evidence proves the underlying claim false.

## Verification workflow

1. Identify the artifact, claimed/inferred originating skill, and artifact
   version. Record the verification date when available.
2. Load that skill's current `SKILL.md` and any shared references it explicitly
   requires for the artifact. Record the standard's source and version/status.
3. Extract the complete set of explicit applicable requirements. Preserve
   conditional branches. Do not add requirements.
4. Read the artifact in full and check each requirement. Record evidence with
   locations. Mark unsupported claims UNVERIFIABLE when verification depends on
   unavailable inputs or sources.
5. Assign stable finding IDs for FAIL or UNVERIFIABLE results, such as
   `MV-[skill]-001`. Preserve IDs on re-verification when the same requirement
   remains unresolved. Close only after inspecting the corrected artifact.
6. Route every failure to the originating skill for correction. If the
   originating skill cannot satisfy its own requirement because canonical
   context appears outdated or contradictory, route the evidence through
   `ssot-context-loop` and its human approval gates. Never change canon.
7. For market-facing messaging alignment, separately route the artifact to
   `messaging-consistency-audit` where relevant. Do not combine its outcome
   with this verification status.

## Required output

### Output quality verification: [artifact]

- Originating skill: `[skill]`
- Overall status: `PASS` or `NEEDS_CORRECTION`
- Standard inspected: `[SKILL.md path/version or available revision]`

| Requirement | Source in SKILL.md | Result | Evidence in artifact | Finding / correction |
|---|---|---|---|---|

Include all applicable requirements, including passing checks. Cite section
headings or line/page/slide/email locations when available. Use
`NOT_APPLICABLE` only when allowed and explained. Use `UNVERIFIABLE` when the
artifact claims compliance but evidence/input cannot be inspected.

### Required corrections

List only actual FAIL findings, prioritized by impact. For each include finding
ID, violated requirement, artifact location, why it fails, required correction,
and route to the originating skill. List UNVERIFIABLE items separately with the
missing source or input needed. Do not frame them as proven errors.

If no corrections are needed, say so. Re-verification inspects the revised
artifact and updates each existing ID to PASS, NOT_APPLICABLE, FAIL, or
UNVERIFIABLE. Do not close an item based only on a correction description.

## Safety and boundaries

- Verification is read-only. Do not rewrite, patch, or approve the artifact.
- Do not inspect or compare canon to decide messaging consistency. If the
  originating skill requires canon use as part of its own deliverable, verify
  only that the artifact records the required inputs and follows its declared
  process; route actual message-to-canon claims to the messaging auditor.
- Do not treat output-quality-check as a check of skill specification structure.
- Repeated failures that expose a gap in a skill's own requirements can be
  reported as a proposed skill improvement, routed to that skill's owner. Do not
  amend skill standards during artifact verification.

## Related skills

- `messaging-consistency-audit`: vertical SSOT and horizontal messaging checks.
- `ssot-context-loop`: governed canonical context and approval workflow.
- `events`: event strategy and downstream asset orchestration.
