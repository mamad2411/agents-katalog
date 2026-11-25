---
name: academic-integrity-preflight
description: Use before substantive formal research drafting and again before delivery to check concrete integrity risks such as prompt residue, placeholders, fake or unverified references, unsupported claims, unresolved compliance requirements, and AI-use disclosure boundaries.
---

# Academic Integrity Preflight

Use this skill for proposal, manuscript, report, methodology, ethics/IRB/compliance-facing, supervisor/PI/client/reviewer-facing, submission-facing, or citation-heavy research artifacts.

## Purpose

Catch concrete integrity and submission-readiness risks before style polishing or final delivery.

This is not an AI detector and must not be used to judge whether text was written by AI from style alone.

## When To Run

Run twice for formal-writing pipelines:

1. Early: after source-first and project-material checks, before substantive drafting or major revision.
2. Final: before delivery review, pre-delivery lock, formal delivery guard, Word/PDF delivery, or public sharing.

## Check

Look for:

- prompt residue or chatbot meta-text;
- placeholders such as `TO CONFIRM`, `SOURCE TO ADD`, `NEEDS VERIFICATION`, `xxx`, `TODO`, bracketed missing fields, or template instructions left in user-facing text;
- fake, incomplete, or unverified references;
- major claims without source-readiness or citation-support evidence;
- official requirement, rubric, journal, funder, client, deadline, word-count, or submission claims without requirement evidence;
- ethics, consent, withdrawal, recording, storage, privacy, or participant-facing claims without compliance evidence;
- AI-use disclosure claims that imply a formal requirement without source evidence;
- requests to hide, soften, remove, or invent AI-use disclosure statements.

## Local Tool

Use when checking a Markdown or text artifact:

```bash
python3 scripts/academic_integrity_preflight.py --target <path> --stage early
python3 scripts/academic_integrity_preflight.py --target <path> --stage final --strict
```

Use `--requires-ethics`, `--requires-rubric`, or `--citation-heavy` when the task type requires those gates.

## Failure Behaviour

- `HOLD`: prompt residue, user-facing placeholders, fake or unverified reference markers, unresolved compliance blockers, unverified official requirements, or unsupported major claims.
- `WARN`: low-risk wording concern, non-blocking reminder, or missing optional evidence.
- `PASS`: no concrete integrity issue found by this preflight.

If the preflight returns `HOLD`, do not describe the artifact as usable, approved, submission-ready, publication-ready, or client-ready. Fix the issue, downgrade the claim, mark `TO CONFIRM`, or record an explicit user risk override where the workflow allows it.

## Boundaries

- Do not claim a document is AI-generated from prose style.
- Do not promise lower AI-detection risk.
- Do not hide, soften, remove, or invent AI-use disclosure statements. Route detector-framed or disclosure-risk style requests to `authorial-voice-integrity`.
- Do not rewrite evidence, citations, participant facts, numbers, dates, or official rules for style.
- This skill complements document-quality gates; it does not replace source-first, citation claim-support audit, ethics/IRB/compliance review, requirement evidence, delivery review, pre-delivery lock, or formal delivery guard.
