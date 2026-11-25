---
name: code-review
description: >-
  Structured 3-phase peer review of a diff or PR — intent, issues by severity,
  then pointed merge-readiness questions and a verdict. Use for general code
  review. Not for AI workflow self-fix-and-edit (ai-systems-review) or
  no-edit devil's-advocate threat models (adversarial-challenge). Phase 3 asks
  questions only; it is not the adversarial-challenge skill.
---

# code-review

Senior peer review of a change. Challenge correctness, find breaks and subtle
bugs. Ends with a verdict — does not edit code.

**Not this skill:**
- Self-review AI workflow code and **apply fixes** → `ai-systems-review`
- Devil’s advocate / threat model with **hypotheticals only** → `adversarial-challenge`
- Preferred AI sequence: `adversarial-challenge` → decide → `ai-systems-review`

## Phase 1: Understand the Change

In 2–4 sentences, state:

- What the change does (functional intent)
- What it touches (files, modules, APIs, data structures)
- Any assumptions the code appears to make

Do not speculate beyond what the code shows. If intent is unclear, say so.

## Phase 2: Issue Review

For each issue:

- **Location**: file/function/line
- **Severity**: Bug | Logic Error | Edge Case | Performance | Security | Style | Maintainability
- **Description**: what’s wrong, one sentence
- **Evidence**: the code/pattern that causes it
- **Suggested fix**: concrete change — not “consider improving”

Skip empty categories. Do not manufacture issues.

## Phase 3: Merge questions

Ask 3–5 pointed questions the author must answer for a safe merge. Tailor to this
diff — no generic checklists. Each question cites a specific part of the code.
(This is not `adversarial-challenge`; questions only, no threat-model writeup.)

## Operating Rules

- Three phases with headers, in order
- Do not restate the code beyond Phase 1
- Skip Phase 3 on trivial diffs (e.g. typo) and say so
- End with **Verdict**: `Approve` | `Approve with nits` | `Request changes` | `Block` — one-sentence justification
