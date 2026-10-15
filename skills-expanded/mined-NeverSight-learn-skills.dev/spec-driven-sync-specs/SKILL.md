---
skill_id: spec_driven_sync_specs
name: spec-driven-sync-specs
description: Scan code and specs for drift, create a dedicated spec-only change to synchronize them, and report the gaps in chat.
author: auto-spec-driven
type: agent_skill
version: 1.0.0
---

You are helping the user synchronize `.spec-driven/specs/` with behavior that
already exists in the repository.

## Prerequisites

The `.spec-driven/` directory must exist at the **project root**. Before
proceeding, verify:
```
ls .spec-driven/
```
If this fails, the project is not initialized. Run `/spec-driven-init` first.

## Steps

1. **Choose the scan scope** — determine whether the user wants:
   - a repository-wide scan
   - a scoped scan for a specific directory, module, or feature area

   If the user already gave a scope, use it. If not, ask whether to scan the
   whole repository or a narrower target.

2. **Read spec context first** — before deciding that any drift exists, read:
   - `.spec-driven/config.yaml`
   - `.spec-driven/specs/INDEX.md`
   - every main spec file that appears relevant to the chosen scan scope

3. **Read repository evidence in the chosen scope** — inspect the code, tests,
   and nearby documentation that define current observable behavior in that
   scope.
   - Prefer files that expose behavior directly: CLI commands, handlers,
     user-facing flows, tests, and docs
   - Do not treat internal implementation details as requirements

4. **Classify drift findings** — compare the repository evidence to the current
   specs and sort findings into:
   - confirmed behavior that exists in code but is missing from specs
   - existing requirements that appear outdated or incomplete
   - ambiguous findings that need human confirmation before they become specs
   - areas with no meaningful drift in the scanned scope

5. **Propose the sync change** — suggest a dedicated kebab-case change name for
   the spec sync work. Prefer names that reflect the scan scope, for example:
   - `sync-auth-specs`
   - `sync-cli-specs`
   - `sync-current-state-specs`

6. **Scaffold a dedicated spec-only change** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js propose <name>
   ```
   Then populate the normal five artifacts:
   - `proposal.md` — describe the scan scope, why the specs need catch-up, and
     unchanged behavior
   - `design.md` — describe how findings were derived from repository evidence
   - `tasks.md` — focus on reviewing and refining the generated spec sync change;
     do not add product-code implementation tasks
   - `questions.md` — record every ambiguity or doubtful inference here
   - `specs/` — create delta spec files aligned with `.spec-driven/specs/`

7. **Write delta specs from evidence** — for each confirmed gap:
   - choose the correct mirrored delta path under `changes/<name>/specs/`
   - use `## ADDED Requirements`, `## MODIFIED Requirements`, or
     `## REMOVED Requirements` as appropriate
   - describe observable behavior only
   - if no existing category or file fits, create the new relative path that
     should exist under `.spec-driven/specs/` after archive

8. **Record ambiguity instead of guessing** — if repository evidence is unclear,
   conflicting, or too implementation-specific:
   - add a question to `questions.md`
   - keep the in-chat report explicit about which findings are tentative
   - do not silently invent requirements

9. **Validate the sync change** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js verify <name>
   ```
   - Fix safe artifact-format problems immediately and rerun `verify`
   - If only open questions remain, surface them clearly as workflow blockers
   - If any non-question error remains, stop and report it instead of presenting
     the sync change as ready

10. **Report the drift summary in chat** — provide a concise summary covering:
    - the scan scope that was analyzed
    - confirmed gaps or outdated spec areas
    - which delta spec files were created or updated
    - any unresolved questions
    - any areas in scope where no meaningful drift was found

## Rules

- This is a planning/documentation skill only — do not change product code
- Read spec context before judging drift
- Respect the user-selected scope; do not imply full-repository coverage after a
  scoped scan
- Use code, tests, and nearby docs as evidence, but write only observable
  behavior into the specs
- Create a dedicated change instead of editing `.spec-driven/specs/` directly
- Do not write a standalone report file; the summary belongs in chat
