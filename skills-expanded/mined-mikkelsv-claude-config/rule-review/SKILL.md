---
name: rule-review
description: Critical single-pass triage of pending candidates AND existing rules. Promote drafts into rules; retire stale; propose prefix migrations.
---

# Rule Review

Triage candidates + audit existing rules in one critical pass. **Default stance: every rule must earn its keep.** Frame each item as "why does this stay?" — not "is this OK?"

## Steps

1. **Load inventory.**
   - Candidates: `<project>/.claude/local/rule-candidates/*.md` (pending, gitignored).
   - Existing global: `~/.claude/rules/*.md`.
   - Existing project: `<project>/.claude/rules/*.md` (committed, team-visible).

2. **Build queue.** Order: candidates first (fast decisions), then unprefixed rules (rename opportunities), then prefixed rules.

3. **Per-item critical review.** For each, surface:
   - **Dupes** — does another rule or candidate cover the same ground? Cross-reference all three locations.
   - **Earns-its-keep?** Under ~25 lines (per `wf-tight-claude-config`)? Actionable directive? Real enforcement signal (or just aspiration)?
   - **Naming.** Matches canonical prefix? Allowed: `arch-` `cq-` `wf-` `meta-`. Anything else → propose migration.

4. **Per-item AskUserQuestion** — options vary:
   - **Candidate:** Promote to global / Promote to project / Edit-then-promote / Keep pending / Discard.
   - **Existing rule (prefixed):** Keep / Edit (tighten) / Retire / Rename.
   - **Existing rule (unprefixed):** Propose prefix + migration plan — accept / skip / keep unprefixed.
   - **Dupe pair:** show both, ask: keep A / keep B / merge / keep both (with why).

5. **Apply edits.** Candidates are gitignored and therefore untracked, so promotion is a plain `mv` then `git add` — `git mv` fails on an untracked source. No rewrite needed (candidate files are already in rule format):
   - **Global (personal only)** → `mv .claude/local/rule-candidates/<slug>.md ~/.claude/rules/<slug>.md`, then `git -C ~/.claude add rules/<slug>.md`
   - **Project (team-visible)** → `mv .claude/local/rule-candidates/<slug>.md .claude/rules/<slug>.md`, then `git add .claude/rules/<slug>.md`. **Always confirm — this commits to the team's history.**
   - **Edit-then-promote** → rewrite first, then move and add.
   - **Retire** → `git rm` (confirm via `AskUserQuestion`).
   - **Rename** → `git mv <old> <new>`; grep-replace `<old>` references in `~/.claude/` and project `.claude/`.
   - **Discard candidate** → plain `rm` (the file is gitignored, no `git rm`).

6. **Summary.** N promoted to global, M promoted to project, K discarded, L retired, J renamed. Show the new canonical-prefix distribution.

## Canonical categories

- `arch-` — module boundaries, dependency direction, abstraction level.
- `cq-` — code quality: idiom, error handling, naming, control flow.
- `wf-` — workflow: how Claude behaves, when to ask, output format.
- `meta-` — config / tooling / file placement.

Resist new prefixes — split the namespace only when rules genuinely accumulate.

## Pre-flight

If `<project>/.claude/local/` is not present in `.gitignore`, surface a single warning at the start: "Add `.claude/local/` to `.gitignore` to keep drafts private." Accept user confirmation to do it, or proceed regardless.

## Rules

- One item at a time. Don't batch into a single mega-prompt.
- Confirm destructive ops (`git rm`, rename) via `AskUserQuestion`.
- Renames must update references — grep `~/.claude/` and the current project's `.claude/`.
- Stop at any time — user-driven, not autonomous.
- **Promote-to-project commits to the team's history** — always confirm before doing it.
