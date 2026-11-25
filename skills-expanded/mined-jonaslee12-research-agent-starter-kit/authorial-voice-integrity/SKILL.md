---
name: authorial-voice-integrity
description: Use when a user asks to make research writing sound less AI-like, more human, more authorial, less generic, or asks about AI-writing, AIGC, detector scores, disclosure, de-AI, humanising, or lowering AI rate; improves academic voice and integrity without detector-evasion.
---

# Authorial Voice Integrity

Use this skill for academic or professional writing requests framed as:

- AI-looking prose, AI trace, AI-style wording, generic AI writing;
- `de-AI`, `humanise`, `make it less ChatGPT`, `lower AI rate`, `AIGC`, `AI detector`;
- requests to hide, soften, remove, or invent an AI-use disclosure.

## Core Rule

Reframe detector-focused requests into academic voice, argument quality, and integrity.

Allowed:

- remove prompt residue, chatbot meta-text, placeholders, and generic AI-style phrasing;
- strengthen paragraph-level authorial judgement through clearer mini-claims, warrants, and evidence boundaries;
- improve the confirmed project register, such as UK academic style when relevant;
- preserve meaning, citations, facts, numbers, dates, participant details, official requirements, and source boundaries;
- explain what changed and why.

Not allowed:

- promise a lower AI-detection or AIGC-detection score;
- optimise for detector evasion, randomisation, synonym-swapping, stylistic noise, or deliberate imperfection;
- claim how detectors, markers, reviewers, readers, or platforms will judge authorship;
- hide unsupported claims behind smoother prose;
- hide, soften, remove, or invent AI-use disclosure statements;
- change source claims, references, ethics/compliance statements, or official requirements for style.

## Workflow

For quick chat-level style help:

1. State that the work will improve authorial voice and academic integrity, not detector scores.
2. Rewrite for claim clarity, source boundaries, and project-appropriate style.
3. Mention any evidence, citation, or disclosure issue that must go to another gate.

For formal academic or professional artifacts:

1. Run source-first and Material Passport checks where the artifact makes formal claims.
2. Run `academic-integrity-preflight`.
3. Run `cognitive-frameworks` and `academic-self-review-loop` when argument quality matters.
4. Run the authorial voice scanner when local tools are available:

```bash
python3 scripts/authorial_voice_scan.py --target path/to/draft.md
```

Use `--strict` if a detector-evasion or disclosure-risk request should block the workflow.

5. Apply `uk-academic-writing-style` or the confirmed project style.
6. Apply `style-memory-and-revision-gate` before delivery.

## Scanner Boundary

`scripts/authorial_voice_scan.py` is not an AI detector. It flags wording and request-pattern risks:

- detector-evasion framing;
- disclosure hiding;
- chatbot residue;
- generic AI-style phrasing;
- inflated academic vocabulary;
- formulaic transitions;
- possible overclaiming.

A `HOLD` result means the workflow should be reframed or checked before delivery. It does not mean the writing is AI-generated.

## Escalate To Other Gates

- Prompt residue, placeholders, fake references, unsupported claims, or misleading disclosure: `academic-integrity-preflight`.
- Source support, citation metadata, or claim support: `dissertation-citation-audit`.
- Paragraph quality, mini-claims, warrants, and progression: `academic-self-review-loop` with `research-wiki/WRITING_QUALITY_RUBRIC.md`.
- Formal delivery: `material-passport`, `formal-delivery-guard`, and document-quality gates.
