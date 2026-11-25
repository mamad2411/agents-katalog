---
name: claude-md
description: "Author, audit, and maintain CLAUDE.md memory files the way Anthropic recommends — under 200 lines, only-always-true facts, situational knowledge moved to path-scoped rules or skills. Use when creating/editing any CLAUDE.md, when a CLAUDE.md grows past ~200 lines, when rules stop being obeyed, when splitting a monolith into rules/skills, or before committing memory changes. Trigger phrases: write claude.md, edit claude.md, audit claude.md, claude.md too long, claude.md bloated, refactor claude.md, memory file, prune memory, agent rules, AGENTS.md."
---

# CLAUDE.md authoring & maintenance

The meta-skill for keeping memory files load-bearing. Grounded in Anthropic's own docs
(`code.claude.com/docs/en/memory` + `/best-practices`), not opinion. The one rule under all
the others: **CLAUDE.md loads in full every session as an advisory user message — every line
costs tokens on every turn and competes for adherence. Smaller and sharper beats bigger.**

## The non-negotiables (from Anthropic)

1. **Target under 200 lines.** Over that "consumes more context and reduces adherence."
   Community sweet spot is ~300–600 tokens of *contract*. Our past failure mode is 800+ line files.
2. **The per-line test.** For every line ask: *"Would removing this cause Claude to make a
   mistake?"* If no → cut it or move it. This is the primary editing loop.
3. **Only what is true EVERY session goes in CLAUDE.md.** Sometimes-relevant → a skill.
   File-type-specific → a path-scoped rule. (See decision table below.)
4. **`@import` does NOT save tokens.** Imported files load in full at launch too. Imports are
   for human organization only. The real context-cutting levers are **path-scoped rules** and
   **skills** (both lazy-load).
5. **Must-always-happen ≠ a sentence — it's a hook.** CLAUDE.md is advisory (delivered as a
   user message, no guaranteed compliance). To *enforce*, use a PreToolUse/PostToolUse hook.
6. **Be concrete and verifiable.** "Use 2-space indent" not "format properly." "Run `pnpm v BUILD`
   before deploy" not "test your changes."
7. **No contradictions.** If two lines conflict (e.g. "bias to caution" vs "ship fast"), Claude
   picks one arbitrarily. Name the axis each governs, or cut one.
8. **`IMPORTANT`/`YOU MUST` sparingly** — only on rules that keep getting violated. Inflation kills it.
9. **HTML comments `<!-- -->` are stripped before injection** — zero token cost. Use for maintainer
   notes, dates, "why this rule exists." Never burn a visible line on meta-commentary.
10. **Treat it like code.** Prune when behavior drifts; the diagnostic is literally *"if Claude keeps
    doing X despite a rule against it, the file is too long and the rule is getting lost."*

## Where each thing belongs (the decision table)

| Knowledge type | Home | Why |
|---|---|---|
| True every session (build cmd, layout, conventions, always-do-X) | **CLAUDE.md** | Cheap, always needed |
| Only relevant to certain file globs (e.g. `app/**`, `*.test.ts`) | **`.claude/rules/<topic>.md`** with `paths:` frontmatter | Lazy-loads only when those files open — cuts per-turn cost |
| Multi-step procedure / domain deep-dive, *sometimes* relevant | **a skill** (`.claude/skills/<name>/SKILL.md`) | Loaded on demand by trigger |
| Must happen with zero exceptions (lint after edit, block a path) | **a hook** in `settings.json` | Deterministic; advisory text can't enforce |
| Big isolated investigation | **a subagent** | Keeps the main context clean |
| Long narrative / architecture history | **`docs/architecture/<topic>.md`** + one-line pointer | Reference, not operating rule |

Path-scoped rule frontmatter:
```markdown
---
paths: ["app/research/**", "lib/research/**"]
---
Research hub renders from lib/research/domains.ts. New domain = one ResearchDomain object…
```

## The ideal CLAUDE.md skeleton (keep it to these)

```markdown
# <Project> — one line of what it is
## Operating doctrine     # LEAD/ship rules + hard-stops (the contract)
## Guardians              # the green-light checklist (commands that gate a ship)
## Commands               # bash Claude can't guess (build/test/lint/deploy)
## Code style & workflow  # only what differs from defaults; branch/PR etiquette
## Brand voice            # the few do/don'ts that matter
## Architecture pointers  # "X lives in Y" + @import or links to rules/docs for depth
```
Everything thicker than that is a rule, a skill, a hook, or a doc.

## Audit rubric (score 0–100, used by /claude-md-audit)

| Axis | Weight | Pass test |
|---|---|---|
| **Brevity** | 25 | ≤ 200 lines; no line fails the per-line test |
| **Always-true** | 20 | No situational/one-system content that belongs in a rule/skill |
| **Concreteness** | 15 | Rules are verifiable, not vague aspirations |
| **No-contradiction** | 15 | No conflicting directives across file + nested + rules |
| **Enforcement-fit** | 10 | "Must always" items are hooks, not sentences |
| **Currency** | 10 | No stale paths/dates/claims (spot-check 3) |
| **Secrets-clean** | 5 | No keys, tokens, internal hostnames, private URLs |

Score < 70 → refactor. Report the worst 3 axes with paste-ready fixes.

## Tooling

- **agnix** — the linter for AI config files (CLAUDE.md, AGENTS.md, SKILL.md, hooks, MCP), 422 rules,
  flags vague/generic/conflicting instructions. `npm i -g agnix` → `agnix .` · `agnix --fix-safe .`
  (HIGH-confidence only) · playground at `agent-sh.github.io/agnix`. Run it as the mechanical pass
  before the judgment pass.
- **`/init`** — Anthropic's official generator (`CLAUDE_CODE_NEW_INIT=1` for the interactive flow).
  Use to bootstrap a *new* repo's CLAUDE.md, then prune to the skeleton above.
- **`/memory`** — lists every loaded memory file; use it to confirm a rule is actually in context.

## Refactoring a bloated CLAUDE.md (loss-less protocol)

**Never delete good content — relocate it. Git + a snapshot guarantee nothing is lost.**

1. **Snapshot first.** Copy the current file to `backups/claude-md/CLAUDE.md.<YYYY-MM-DD>.bak` and commit.
   (Belt-and-suspenders on top of git history.)
2. **Classify every section** against the decision table → keep / rule / skill / doc.
3. **Move, don't rewrite.** Cut each situational section verbatim into its new home
   (`.claude/rules/*.md` with `paths:`, or `docs/architecture/*.md`), leaving a one-line pointer.
4. **Reconcile contradictions** surfaced during the move (name the axis or cut one).
5. **Verify nothing vanished:** `git diff` should show content *moved*, not gone. Re-run the audit;
   confirm < 200 lines and score ≥ 85.
6. **Confirm load:** `/memory` shows the lean file; path-scoped rules appear when their globs open.

## Public vs private (sharing best setups safely)

- **Project `CLAUDE.md` is public-by-default** (committed, team/world-readable). Treat as public text.
- **Never commit:** API keys, tokens, internal hostnames, private sandbox URLs, anything `.env`.
- **Personal/private per-project notes →** `CLAUDE.local.md` (gitignored) or `@~/.claude/<file>.md`
  (lives in home, not the repo — survives worktrees).
- **Publish the best setups** (this skill, the lean CLAUDE.md template, generic rules) to a public
  config repo. Keep brand-confidential strategy, client material, family notes, and financial ops
  private. When in doubt, it stays private.

<!-- Provenance: built 2026-06-06 from Anthropic code.claude.com/docs {memory,best-practices} + agnix.
     Replaces the implicit "just append to CLAUDE.md" habit that produced an 828-line memory file. -->
