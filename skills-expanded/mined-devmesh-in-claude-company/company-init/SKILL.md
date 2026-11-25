---
name: company-init
description: Found or adopt the company - greenfield spec and architecture, or an existing-codebase audit that wires real gates and frozen defaults. The owner answers at most one question. Use when the user says /company-init or /onboard, or asks to set up claude-company in a fresh or existing repo. /company self-initializes too; this skill is the explicit founding or adoption pass.
---

# /company-init - found or adopt

The owner states what they want. The company generates the rest. Output is
a project where `/company` runs real work.

## 0. Verify the drop-in

`company/METHOD.md`, `COMPANY.md`, `.claude/agents/`, `.claude/hooks/`
must exist (installer). If not: stop, point at `install.sh`.

## Empty repo - found it

If the request already says what we are building, ask nothing. Otherwise
one question: "What are we building, and for whom?"

Then, in order:

1. You write the founding spec in `company/specs/` with FR/BR IDs and
   fallbacks, with the owner. If the client wants options first,
   `/brainstorm` already ran.
2. architect: the landed waist, ownership map, wave plan, frozen-surface
   entries, gate proposal.
3. You wire: `company/frozen-surfaces.json`, `company/gates.config`
   (`python3 .claude/hooks/gates_detect.py --write` once code exists; until
   then wire `python3 .claude/hooks/guard_models.py --check` so founding
   commits are honest), spawn facts in RESUME, conventions in `CLAUDE.md`,
   `git init` if needed.

Report one screen: what you decided, what they can veto. Then roll into
`/company` if they already asked to build.

## Existing codebase - adopt it

Ask nothing. Audit in parallel (architecture, tribal conventions, real
test/lint/build commands, load-bearing surfaces). Then:

- `python3 .claude/hooks/gates_detect.py --write`, reconcile with CI, run
  `bash company/run-gates.sh`. Red-today is debt in RESUME, not a silent pass.
- Freeze shipped migrations, schema, single-writer files. Owner can veto.
- Extend `CLAUDE.md` (never clobber) from evidence.
- Seed RESUME and WORRIES.

Findings memo, one screen: what you wired, current gate colors, worries.
Then `/company` is open.
