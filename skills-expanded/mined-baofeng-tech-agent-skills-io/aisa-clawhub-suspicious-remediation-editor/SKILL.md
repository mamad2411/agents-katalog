---
name: aisa-clawhub-suspicious-remediation-editor
description: "Guide for diagnosis-driven ClawHub suspicious remediation without mixing in breakout growth copy."
---

# AIsa ClawHub Suspicious Remediation Editor

Refine ClawHub-facing publish surfaces when a live artifact is `suspicious`, `pending`, or flagged by static analysis.

## When to use

- When `targets/clawhub-suspicious-diagnosis.json` selected a live skill or plugin for repair
- When ClawHub review text points to relay trust, OAuth/media upload, env mismatch, prompt-scaffold wording, or static-analysis findings
- When the goal is to remove scanner ambiguity with the smallest safe change

## Do not use this for

- normal mother-skill editing in `targetSkills/`
- breakout / growth positioning work
- adding new marketing slugs or widening scope

## Core rules

- Start from the diagnosis reasons first, not from generic rewrite instincts.
- Keep runtime behavior intact unless the diagnosis clearly comes from non-runtime helper files that should not ship.
- Prefer explicitness over hype: network target, secret flow, OAuth approval, media upload, external execution, and persistence all need to be stated plainly.
- Align `SKILL.md`, README, manifests, and registry-facing metadata.
- Keep `pending`, `clean`, and `suspicious` as separate states.
- Treat ClawHub `Static analysis` findings as a separate review dimension from `VirusTotal` and `ClawScan`.
- If a finding is caused by child-process, shell, or file-write patterns that are real runtime needs, explain the boundary and intended usage rather than hiding it.

## Common live causes to correct

- relay / third-party API trust surface is under-described
- OAuth or media upload side effects are too vague
- public copy looks like prompt scaffolding
- env / manifest / registry metadata drifted apart
- non-runtime helper files leaked into the release bundle
- static analysis found shell execution or file/network patterns that need either trimming or clearer justification

## Output expectations

- suspicious remediation must stay narrow and evidence-based
- do not inject breakout ladder language, flagship claims, or search-growth copy by default
- the result should be easier for ClawHub review systems and humans to verify
