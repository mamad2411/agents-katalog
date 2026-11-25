---
name: rules-code-style
description: Binding personal rules for writing or refactoring code — load before writing handlers/helpers/async code, adding a helper, new state or a layer (KISS, reuse-first, pre-write gate), or reviewing code for anti-patterns.
---

# rules-code-style

These rules are binding (moved verbatim from ~/.claude/CLAUDE.md). Each heading names its full-text file in `~/.claude/rulebook/`: **Read that file before acting in its area** — the one-liners are the trigger, not the whole rule.

## Code Style — `14-…`, `15-…`, `16-…`, `17-…`
- Handlers read in one screenful; split 3+ concerns into verb-led single-purpose private helpers; ≤2 nesting levels; extract inline try/catch branches; refactors preserve behaviour exactly.
- DRY parallel flows: extract a config-driven shared helper before shipping the second copy; grep siblings/open PRs first; listener factories; repeated parse snippets (3+) → util.
- Prefer `map/filter/reduce/find/some/every/flatMap`; `for...of` for side effects or sequenced awaits (never `forEach` + async); pure callbacks; name intermediate stages.
- **Independent awaits → `Promise.all`** (comment when order matters non-obviously); skip calls whose result a branch discards; moved/ported code gets no exemption; self-check the diff for consecutive awaits before commit.

## KISS / STOP-BEFORE-WRITING / Lean Design — `24-…`, `25-…`, `26-…`
- Smallest change that fully solves the actual problem; size to severity both ways; no permanent tax for rare problems; YAGNI; layer/scope is co-owned with the user. Applies to this rulebook too.
- **Pre-write gate for any non-business-logic helper**: name the problem generically → a library exists; check the tree (often a transitive dep); search the problem domain; state the package used or why none fits. Helper crossing ~40 lines / extra error branch / custom timeout / retry loop → stop and re-search. Measure the perf trade-off; cheap deterministic check first.
- Before new persistent state or logic layer, reuse an existing field/mechanism (self-healing diffs, existing timestamps, one-off script); weigh permanence vs frequency; ship the smaller thing.

## Anti-patterns — `27-anti-patterns-to-avoid.md`
- No `NODE_ENV === 'production'` business gating (use flags/config); no assuming third parties are up; no `any` on config/DTOs from external data; new integrations get a config key with staging-safe default; never swallow errors silently (+ Sentry for money/contract/sync); no per-request state in module scope/static fields.
