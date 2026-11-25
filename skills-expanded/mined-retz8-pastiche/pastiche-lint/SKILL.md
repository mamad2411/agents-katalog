---
name: pastiche-lint
description: Use to re-validate `pastiche/{config.yaml, FACT.md, KNOWLEDGE.md, WISDOM.md}` after hand-editing any of them outside the mutator skills. Thin manual wrapper around the bundled lint script; reports drift and schema violations.
---

# Pastiche — lint

Manual entry point for the lint script. The four mutator skills (`/pastiche-sync`, `/pastiche-setup`, `/pastiche-write-knowledge`, `/pastiche-write-wisdom`) invoke the same script internally at the end of their mutations; `/pastiche-lint` exists for the hand-edit case.

## Run

Invoke `pastiche-lint` with cwd = the user's repo root. Print stdout and stderr verbatim.

Do not interpret violations, group them by document, suggest remediation, or point at other skills — the script's output already includes a summary and `OK` / `FAILED — N violation(s)` line.

Do not pre-check for `pastiche/` or its files. The script's own sentinels handle the missing-state case with a user-facing message.

Do not pass arguments. The script takes none.

Do not chain into another skill.
