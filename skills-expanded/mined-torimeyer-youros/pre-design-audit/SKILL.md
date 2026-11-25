---
name: pre-design-audit
description: Run before proposing any new file, component, or service. Checks three signals (codebase literal, codebase semantic, git log, needles/specs) and produces a clearance report. MATCH FOUND or POSSIBLE MATCH blocks design until reuse or justification is written.
---

# Pre-design audit

Run this before creating any new file, component, or service. Catches things that already exist before the design conversation begins — including same-purpose components with different names.

## When to invoke

- Any time brainstorming or planning proposes a **new** file, component, service, or feature by name
- Before listing files under `Create:` in a writing-plans file structure section
- Before a subagent writes a new file to disk

## The four-signal check

Run the audit script for each proposed concept name:

```bash
python3 ~/.myos/pre-design-audit.py "<ConceptName>" --repo-root "$(git rev-parse --show-toplevel)"
```

The script checks:
1. **Codebase (literal)** — filename glob + grep in `app/src/`, `frontend/src/`, `api/` for the exact concept name (excluding test files)
2. **Codebase (semantic)** — splits the concept name into camelCase tokens, expands with synonyms, and searches filenames for same-purpose components with different names
3. **Git log** — last 30 commits on `origin/main` for the concept name
4. **Needles/Specs** — `docs/spec/` and `~/.myos/specs/` for any mention

## Clearance report format

The script outputs a table like this:

```
## Pre-design audit: `SourceBadge`

| Signal | Finding |
|--------|---------|
| Codebase (literal) | none |
| Codebase (semantic) | app/src/components/ClaimSourceChip.tsx [claim, chip, source] |
| Git log  | none |
| Needles/Specs | none |

POSSIBLE MATCH — a different-named component may serve the same purpose.
Review the semantic hits above and choose before proceeding:
- [ ] Reuse the existing component (state which file and how)
- [ ] Confirm these are genuinely different (state the distinction)
```

If a literal match exists: `MATCH FOUND` (hard block).
If only semantic hits exist: `POSSIBLE MATCH` (soft block requiring written review).
If no signals fire: `CLEAR — no existing equivalent found. Proceed with design.`

## How semantic matching works

The semantic signal splits the concept name at camelCase boundaries:
- `SourceBadge` → tokens `["source", "badge"]`
- `ClaimSourceChip` → tokens `["claim", "source", "chip"]`

Each token is expanded with synonyms (e.g., `badge` → `chip, pill, tag, indicator`). A file is a POSSIBLE MATCH when:
- Its filename stem contains **2+ expanded terms**, AND
- At least **1 original (un-expanded) token** is present in the stem

This prevents single-word coincidences from triggering false positives, while surfacing genuinely same-purpose components.

## Hard gate (MANDATORY)

**If the report says MATCH FOUND:**
- Do NOT proceed to clarifying questions, file-structure decisions, or code
- The checkbox (reuse or justify) must be resolved in writing FIRST
- Proposing a new file when a match exists without written justification = plan failure

**If the report says POSSIBLE MATCH:**
- Do NOT proceed to file-structure decisions or code
- Review each semantic hit; confirm whether it serves the same purpose
- The checkbox (reuse or confirm different) must be resolved in writing FIRST

**If the report says CLEAR:**
- Continue the normal workflow (brainstorming, writing-plans, implementation)

## Quick check (when audit script isn't available)

If the script can't be run (no shell access, offline), perform the check manually:

```
search(query="<ComponentName>", scope="code")
search(query="<purpose description>", mode="semantic", scope="code")
git fetch origin main && git log --oneline -30 origin/main | grep -i "<concept>"
grep -rl "<concept>" docs/spec/
```

Produce the same clearance table from the results. For the semantic check, search for synonyms of each camelCase token manually.

## Integration points

This skill is invoked by:
1. **Brainstorming** — at Step 1 ("Explore project context"), before asking clarifying questions
2. **Writing-plans** — before listing any file as `Create:` in the file structure section
3. **Subagent briefs** — before writing any new file to disk (per `feedback_subagent_prompt_template.md` Rule 6)
