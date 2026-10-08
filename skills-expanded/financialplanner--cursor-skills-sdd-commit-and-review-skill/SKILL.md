---
name: sdd-commit-and-review
description: Keeps commits and reviews aligned with FinancialPlanner docs/SPEC.md and AGENTS.md. Use when writing commit messages, PR descriptions, reviewing diffs, or when the user asks for merge readiness, changelog notes, or what to cite from the spec.
---

# Commit and review (SDD)

## Commits

- **Subject:** imperative mood, under ~72 characters.  
- **Body (when useful):** bullet list; cite **SPEC sections** (e.g. `SPEC §4.4: prepay keep EMI`).  
- One logical change per commit when possible: spec-only vs code-only vs test-only helps bisect.

## Pull requests

- **Summary:** what behaviour changed for the user or tester.  
- **Spec:** link or quote the governing **§** from `docs/SPEC.md`.  
- **Testing:** how §10 / Vitest / goldens were updated.  
- **Changelog:** user-visible changes under **`CHANGELOG.md` → `[Unreleased]`** (move to a dated version when merging to `main`).  
- **Screenshots:** only when UI changed meaningfully.

## Review checklist

- [ ] Behaviour matches **SPEC**; non-goals (§11) not violated  
- [ ] **`CHANGELOG.md`** updated for user-facing changes  
- [ ] **AGENTS.md** still accurate if workflow paths changed  
- [ ] **`.cursor/skills/`** descriptions updated if skill triggers changed  
- [ ] Footer / disclaimer (§14) intact if user-facing copy touched  

## Scope creep

If the diff does more than the spec describes, request a **SPEC** update first or split the PR.
