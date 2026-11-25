---
name: context-load-scan
description: What actually loads — CLAUDE.md and @import budget, AGENTS.md not imported, rule tokens, ai/ budget, oracle age.
kind: skill
pack: learning
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: context-load-scan

## Premise

Context has a cost and a ceiling. Long context degrades retrieval (Context Rot, Chroma 2025; Lost in the Middle, TACL 2024; LongCodeBench, 2025), and context files raised agent cost by more than 20% with no significant success gain in Gloaguen et al. (2026). What matters is not how long a file is but **what the host actually loads**, and every loader has its own rule:

- Claude Code loads `CLAUDE.md`, `.claude/CLAUDE.md` and `CLAUDE.local.md` at launch, strips block-level HTML comments first, and loads every `@import` up to 4 hops, relative to the importing file (memory docs, code.claude.com/docs/en/memory, fetched 2026-10-19). Its target is under 200 lines per `CLAUDE.md`.
- A rule in `.claude/rules/` without `paths:` loads every session; `globs:` is not a field Claude Code reads (Refract platform facts, verified 2026-10-05 on Claude Code 2.1.236).
- `AGENTS.md` is read by Claude Code only when no `CLAUDE.md` or `CLAUDE.local.md` exists at or above the working directory. On a real NestJS + React monorepo, a 657-line `AGENTS.md` sits beside a `CLAUDE.md` that never imports it: Claude Code loads none of it.
- MEMORY.md loads only its first 200 lines or 25 KB; Copilot code review reads the first 4,000 characters of an instruction file (GitHub docs, fetched 2026-10-19).

`scripts/load-budget.py` (this skill) owns: §1 the loader-truth budget (KN-31), §2 `CLAUDE.md` / `AGENTS.md` selection (KN-32), §3 the vague-lexicon advisory (KN-33, never a Finding), §4 the extraction oracle's freshness and approval (KN-19; KN-16 and KN-18 counts for their baseline owner), §5 the context-file list security reads (KN-34/35 are security's).

**Every finding cites the file + what loads (effective lines, the import closure, the always-on token estimate, the bytes a loader reads) + the budget and its source + the remedy (path-scope a rule, move detail to an on-demand `ai/` doc, add `@AGENTS.md`, re-extract the oracle).** "Context within budget" is never printed without the class-coverage block.

## The rule

A row is a finding when all four hold:

1. **The loader really loads it.** Effective lines after HTML block comments (P-21); imports counted because they load at launch; rules counted only without `paths:` (P-22); `AGENTS.md` counted for Claude Code only through an import or a symlink (P-16).
2. **A sourced budget applies.** Every threshold above names its source; a budget with no source is not checked.
3. **The breach is measured, not estimated by eye.** Lines and bytes from the files; tokens as bytes ÷ 4, the convention `audit-setup.sh` C2u uses, labelled an estimate.
4. **The remedy moves content to where it loads on demand**, never just into an `@import` (which loads too).

## Boundaries

- **What the loaded files say** — dead references, wrong facts, stale anchors → `knowledge-ref-scan` and `knowledge-fact-scan`. This skill measures load, not truth.
- **Refract's own setup budgets at install time** → `audit-setup.sh` C2x (CLAUDE.md), C2u (rule tokens), C2v (oracle check 7) and `/setup-project-health` check 4. §1 re-measures the same budgets after setup, when no setup command runs; the two must agree, and the health command stays the record of setup health.
- **A secret in a context or memory file** (KN-34) → security `secret-scan-method` (its AI-context-file step); **hidden Unicode or injection-shaped instructions** (KN-35) → security `sast-scan` (trojan-source lane), when the security pack is installed (its pre-flight 6 reads context files). §5 prints the file list and a handoff count; without the security pack the rows are `N/A (owner pack security not installed)` with the list attached.
- **Unmarked oracle claims and approval stamps** (KN-16, KN-18) → `/setup-project-health` checks 11 and 9. §4 prints counts only.
- **Retrieval quality of `/recall`** → `/eval` cases; product RAG retrieval → ai-engineering `retrieval-eval`, when installed.

## Adapt to the codebase — the loader lanes

| Loader | Loads at launch | Budget (source) | Trap |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md` + `@import` closure (4 hops) + `.claude/rules/**` without `paths:` | 200 lines per CLAUDE.md (memory docs); rules ~12,000 tokens (C2u) | HTML block comments are stripped (P-21); `globs:` is ignored, so a `globs:`-only rule is always on (P-22); README.md and `_*.md` in rules load too |
| **Claude Code auto memory** | MEMORY.md (first 200 lines / 25 KB), topic files on demand | 200 lines / 25,600 bytes (memory docs) | outside the repo: read only with `--memory-dir` (O-3) |
| **Codex, OpenCode, Cursor, Copilot agents** | nearest `AGENTS.md` | — | Claude Code ignores it beside a CLAUDE.md unless imported (P-16) |
| **GitHub Copilot** | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` (`applyTo`) | code review reads 4,000 characters per file (GitHub docs) | the rule a reviewer must see belongs in the first 4,000 characters |
| **Cursor** | `.cursor/rules/*.mdc` (`alwaysApply`, `globs`, `description`) | < 500 lines per rule (Cursor docs, undated) | team > project > user precedence (P-15) |
| **Refract knowledge layer** | `ai/**` on demand; `ai/_session-digest.md` at session start | ai/ ≤ 50 files, ai/<file> ≤ 300 lines non-ADR, rules ≤ 30 files (`/setup-project-health` check 4) | history files count toward the file budget; report them separately |

## Pre-flight

Run as **one** bash script from the repo root. Step **N** feeds detector **§N**. Every `rg` names its path; any `rg` exit 2 is `blocked`.

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (arrays and PIPESTATUS are bash-only)"; exit 2; }
KS="${KS:-.claude/skills}"        # installed engines; in the Refract repo itself: templates/packs/learning/skills
RUN="${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/knowledge.XXXXXX")}"; mkdir -p "$RUN"; echo "RUN=$RUN"
export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true

# 1-5. The engine: effective lines, import closure, rule frontmatter, loader budgets, AGENTS.md selection,
#      vague lexicon (advisory), oracle census sha vs HEAD, approval stamp, hidden-Unicode handoff.
python3 -I "$KS/context-load-scan/scripts/load-budget.py" . > "$RUN/load.tsv" 2> "$RUN/load.ledger"
echo "load-budget exit $? (0 clean · 1 rows · 2 blocked)"; cat "$RUN/load.ledger"; cut -f1-7 "$RUN/load.tsv"
#    Opt-in, never by default (O-3): add --memory-dir="$HOME/.claude/projects/<encoded>/memory" for MEMORY.md.
python3 -I "$KS/context-load-scan/scripts/load-budget.py" . --security-list > "$RUN/context-files.txt"   # §5: security's input

# Cross-checks.
# 1a. @imports in the CLAUDE files (the engine follows each to 4 hops).
for c in CLAUDE.md .claude/CLAUDE.md CLAUDE.local.md; do [ -f "$c" ] && { rg -n --pcre2 '(?<![\w`@/])@(?:\.{1,2}/|[\w-]+/)?[\w./-]+\.md\b' "$c"; echo "rg 1a $c exit $?"; }; done
# 1b. Rule scoping as written: `paths:` scopes, `globs:` does not (P-22).
[ -d .claude/rules ] && { rg -l '^paths:' -g '*.md' .claude/rules | wc -l; rg -l '^globs:' -g '*.md' .claude/rules; echo "rg 1b exit $?"; }
# 2. Is AGENTS.md imported?
[ -f AGENTS.md ] && [ -f CLAUDE.md ] && { rg -n '@AGENTS\.md' CLAUDE.md; echo "rg 2 exit $? (1 = not imported; check for a symlink: ls -l CLAUDE.md AGENTS.md)"; }
# 5. Bidi overrides and zero-widths in context files (a handoff count; LRM/RLM in RTL text is legitimate, P-26).
rg -n --pcre2 '[\x{202A}-\x{202E}\x{2066}-\x{2069}\x{200B}-\x{200D}\x{2060}\x{FEFF}]' -g '*.md' -g '*.mdc' . -g '!**/node_modules/**' > "$RUN/g5.txt"
echo "rg 5 exit $? ($(wc -l < "$RUN/g5.txt" | tr -d ' ') lines; handed to security, never graded here)"
```

Read the ledger first: which CLAUDE files exist, the import closure size, each file's effective lines (and how many HTML-comment lines were stripped), the rule split (always-loaded with its token estimate, path-scoped, `globs:`-only), the `ai/` totals (history counted separately), MEMORY.md (`NOT READ` without `--memory-dir`), the oracle and stamp state, and the context-file count for security.

**Measured** (2026-10-19), read-only on a real NestJS + React monorepo (0.5 s; 0 files written):
- §1: `CLAUDE.md` 118 effective lines (125 raw, 7 in HTML block comments) — within 200; its 8 imports load **673 lines across 9 files** at launch (a row: imports are not a saving); 9 always-loaded rules ≈ **12,644 tokens** against 12,000 (a row; the research measured ≈ 12.6k), 17 path-scoped, 0 `globs:`-only (rg 1b: 18 files carry a `paths:` line, 17 in frontmatter); `ai/` holds **380 files** against 50 (165 of them history) and 48 files over 300 lines (36 history) → 12 rows for the live ones, the top 10 printed (a 2,141-line parity ledger, a 948-line runbook).
- §2: `AGENTS.md`, 657 lines, not imported and not a symlink (rg 2 exit 1) — Unconfirmed, because the user setting that would load it is not in the repo.
- §3: 8 vague-lexicon lines in loaded files, 5 printed as advisory.
- §4: `.claude/_extracted-codebase.md` **absent** (every consumer of the oracle reads nothing); `codebase-profile.md` carries no approval stamp (routed to health check 9) and was last edited 135 commits ago.
- §5: 408 context files listed; 1 U+202E (right-to-left override) in a pattern doc, handed to security.
- On `benchmarks/fixtures/*` (24 trees): no tree has a CLAUDE.md over budget or an AGENTS.md beside one. 10 trees carry `.claude/codebase-profile.md` without the oracle and print the §4 "oracle absent" row — true against the setup contract, which `audit-setup.sh` C2b fails the same way; the other 14 print `N/A (no knowledge layer installed)` (the first run flagged all 24). The self-test seeds 12 rows (205-line CLAUDE.md, a dead import, rules over a budget, a `globs:`-only rule, a 4,100-character Copilot file, `ai/` over its file budget and a 320-line file, MEMORY.md at 210 lines, an unimported AGENTS.md, an absent oracle, a vague line, a U+202E) and 5 decoys (a 260-line CLAUDE.md whose 80 lines are an HTML comment, an `@AGENTS.md` import, a `paths:`-scoped rule, an RLM inside Arabic text, a CLAUDE.md and a MEMORY.md of exactly 200 lines).
- On `stale-knowledge` (the seeded fixture): `CLAUDE.md` at 205 effective lines (242 raw, a 37-line HTML comment stripped; a final newline ends the last line, it adds none), 4 always-on rules (~273 tok), 1 `paths:`-scoped, 1 `globs:`-only; 6 rows, **4 of 4 seeds** (CLAUDE.md over budget, the `globs:` rule, `AGENTS.md` not imported, the oracle 3 commits behind its census sha) plus 2 routed rows (the KN-18 stamp, a U+202E handoff); KN-16 as a ledger count; 34 context files listed for security. Decoys: 0 of 26. On the one-commit copy the census check prints `sha not in this history`.

## The 3,000-hit path

Load rows are few; the volume is in §1's per-file `ai/` budget and §5's handoff list.

1. **Separate history from live**: the ledger counts history files apart; archive history out of the loaded tree before trimming live files (`/recall` still finds archived files).
2. **Rank by load frequency**: always-on rules and the import closure first, the session digest next, then `ai/` files commands read by name.
3. **One remedy per root cause**: a rule set over budget is one path-scoping change, not one row per rule.
4. **Ledger the rest** as `Live, unreviewed (k files)`; the engine prints the top 10 over-budget files and the count beyond.

## Scans for

| § | Class | Default |
|---|---|---|
| 1 | KN-31 loader-truth budget breach | M; H for MEMORY.md truncation; L for a single `ai/` file |
| 2 | KN-32 `AGENTS.md` beside `CLAUDE.md`, not imported or linked | M, Unconfirmed |
| 3 | KN-33 vague rule text in loaded files | advisory only (O-4) |
| 4 | KN-19 oracle absent or older than the code it cites | M |
| 5 | KN-34/35 context files for security | handoff (owner: security) |

### 1. Loader-truth budget (KN-31)

```
BAD:   CLAUDE.md 205 effective lines · 9 always-loaded rules ≈ 12,644 tok (budget 12,000) · a `globs:`-only rule
       MEMORY.md 210 lines (the tail never loads) · copilot-instructions.md 4,100 characters
GOOD:  a 260-line CLAUDE.md whose 80 lines are an HTML block comment (P-21) · a `paths:`-scoped rule (P-22)
```
**Read the code:** Which lines load every session, and which belong in an on-demand `ai/` doc or a path-scoped rule? Is a big rule cross-cutting (keep) or about a slice of the tree (scope it)? Does a `globs:` rule mean `paths:`? **Finding when** a loader's measured load exceeds its sourced budget. **Proof:** tier S + V507 — the re-measured load (`load-budget.py` quiet on that row) after the move; the moved content still reachable on demand.

### 2. `CLAUDE.md` / `AGENTS.md` selection (KN-32)

```
BAD:   AGENTS.md (657 lines) + CLAUDE.md with no `@AGENTS.md` and no symlink — "Read AGENTS.md" in prose is not an import
GOOD:  CLAUDE.md containing `@AGENTS.md` · CLAUDE.md symlinked to AGENTS.md (P-16) · a nested AGENTS.md with no CLAUDE.md above it
```
**Read the code:** Does the team maintain `AGENTS.md` for other tools only (then say so in `CLAUDE.md`), or expect Claude Code to follow it? Would importing it breach §1? **Finding when** both exist on one path and nothing makes Claude Code load `AGENTS.md`. Unconfirmed always: the user or managed setting `claude-md-and-agents-md` is not visible in the repo. **Proof:** V508 — `/memory` in Claude Code lists `AGENTS.md` after the import is added.

### 3. Vague rule text (KN-33)

```
ADVISORY:  "Keep code clean" · "use best practices" · "be careful with migrations"   (no path, command or number)
GOOD:      "Run `pnpm lint` before committing; `no-restricted-imports` bans `axios`"
```
Specific instructions are followed more consistently (Anthropic guidance); judge precision on vagueness is too low to grade, so this class never produces a Finding (O-4). The rows name the line and suggest the file, command or number that would make it actionable.

### 4. Oracle freshness (KN-19)

```
BAD:   .claude/_extracted-codebase.md absent — every consumer of the oracle reads nothing
       census sha a1b2c3d; 50 commits since touched 31 cited paths
GOOD:  a census sha with no commit since on the cited paths · a repo with no knowledge layer (N/A)
```
**Read the code:** Was the oracle cleaned up after setup, or never written? Does the digest claim freshness the oracle does not have? Is the approval stamp's hash still the body's (health check 9)? **Finding when** the oracle is absent in an installed knowledge layer, or commits since its census sha touched the paths it cites. **Proof:** V509 — after `/refresh-knowledge`, the recorded census sha equals HEAD and the engine is quiet.

### 5. Context files for security (KN-34/35)

`--security-list` prints every context and memory file (`CLAUDE*.md`, `AGENTS.md`, `GEMINI.md`, `.cursor/rules`, Copilot files, `ai/**`, `.claude/rules/**`, the memory dir when given). The run adds one handoff row when a bidi override, isolate or zero-width character sits outside RTL text (P-26). Security's `secret-scan-method` and `sast-scan` grade them; this skill never does.

## Proof

Oracles: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Learning — V507 (re-measured load under budget), V508 (the import added; `/memory` lists the file), V509 (oracle census sha = HEAD after refresh). The engine re-run is the before/after probe.

## Output

```
context-load-scan — CLAUDE.md (118 effective / 125 raw) · import closure 9 files, 673 lines · rules 9 always (~12,644 tok), 17 scoped

1. .claude/rules:0                                                        [report-with-fix]   medium
   §1 KN-31 — 9 always-loaded rules ≈ 12,644 tokens (bytes/4) against 12,000 (audit-setup.sh C2u).
   Fix: path-scope the rules that govern a slice of the tree with `paths:`. Proof: re-measure under budget.
2. AGENTS.md:1                                                            [report-flagged]    medium
   §2 KN-32 — 657 lines, CLAUDE.md never imports it: Claude Code does not load it. Unproven: the user setting.
   Settling probe: /memory. Fix: `@AGENTS.md` in CLAUDE.md (then re-check §1).
3. .claude/_extracted-codebase.md:0                                       [report-with-fix]   medium
   §4 KN-19 — oracle absent: every consumer reads nothing. Fix: /refresh-knowledge writes it with a census sha.

Verification: 16 candidates → 14 findings · 1 unconfirmed · 1 hardening · 0 pre-existing · 0 refuted

Class coverage:
  §1  KN-31 loader budget      checked (3 loaders read; MEMORY.md NOT READ — opt-in) → 13 rows
  §2  KN-32 selection          checked (1 AGENTS.md → 1 unconfirmed)
  §3  KN-33 vague text         advisory (8 lines)
  §4  KN-19 oracle             checked (absent)
  §5  KN-34/35 handoff         408 files listed · 1 hidden character → security
```

`[report-with-fix]`: the load is measured and the budget sourced, and the remedy moves content to an on-demand place. `[report-flagged]`: the user-level setting or a loader version is unknown. The coverage block lists **all five** classes on every run: `checked`, `advisory`, `N/A (<reason>)` (no CLAUDE.md, no knowledge layer, memory dir not given), or `blocked (<reason>)`.

## False positives / precedents

The verifier reads [`precedents/learning.md`](../../../../snippets/precedents/learning.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. The ones this skill meets most: § 15 nested precedence, § 16 import or symlink, § 21 HTML block comments, § 22 path-scoped rules and `globs:`, § 25 gitignored session files, § 26 bidi marks in RTL text, § 32 an oracle that was never written.

## When to run

- On any diff that edits `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md`, `.claude/rules/**`, Copilot or Cursor instruction files, adds files under `ai/`, or changes the extraction oracle: the `/audit-knowledge` dispatch signal.
- After `/setup-project --refresh`, `/refresh-knowledge`, or a rules change (`scope-rules.sh`).
- On every whole-repo `/audit-knowledge`, reporting all five classes.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10, with [`precedents/learning.md`](../../../../snippets/precedents/learning.md)). Under `/audit-knowledge` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Never state a budget without its source, and never present a token estimate as measured: it is bytes ÷ 4, labelled.
- Never report §3 as a Finding, and never grade §5: security owns it.
- Never read the host memory directory without `--memory-dir` (O-3); never write into the scanned repository.
- Never print "context within budget" without the coverage block. A loader that was not read is `N/A` or `NOT READ`, never within budget.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `scripts/load-budget.py` (this skill): §1–§5, `--memory-dir`, `--rule-budget`, `--claude-max`, `--ai-max-files`, `--ai-max-lines`, `--security-list`, `--self-test`; imports `kn_common.py` from the knowledge-ref-scan skill (its scripts directory). Stdlib only, `python3 -I` safe; nothing is written under the scanned root.
- `audit-setup.sh` C2x / C2u / C2v and `/setup-project-health` checks 4, 9, 11 (Refract baseline): the setup-time checks of record. `/audit-knowledge` dispatches this skill; `/refresh-knowledge` re-extracts the oracle.
- security `secret-scan-method` and `sast-scan` (when installed) read the §5 list.
