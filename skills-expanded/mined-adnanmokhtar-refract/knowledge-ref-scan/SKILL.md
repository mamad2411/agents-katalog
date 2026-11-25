---
name: knowledge-ref-scan
description: Dead paths, symbols, commands, ADR ids and anchor markers in the AI knowledge layer (CLAUDE.md, ai/, anchors).
kind: skill
pack: learning
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: knowledge-ref-scan

## Premise

The AI knowledge layer is read by an agent that acts on it without a human in between. A path that no longer exists is a file the agent opens, edits or re-creates. A renamed class is a symbol it imports. A package script that was removed is a command that errors. A slash command that is not installed is a step that silently does nothing. A pattern or ADR id with no file is a rule the agent is told to follow and cannot find. A corrupted `project-specific` marker makes the next setup run eat or duplicate content.

DOCER (Tan, Wagner, Treude, EMSE 2024) found an outdated code-element reference at HEAD in 28.9% of the top-1000 repositories, and ReCite (ASE 2026) found 869 stale function references in one kernel release. The same defect in an agent's context is one notch worse: it is loaded every session (precedents § Reading the gates).

`scripts/knowledge-refs.py` (this skill) owns six learning classes: §1 dead path (KN-01), §2 dead symbol (KN-02), §3 dead command, script, skill or agent (KN-03), §4 dead knowledge cross-reference (KN-04), §5 framework path leaked into an installed artifact (KN-05), §6 marker corruption (KN-15). The shared reader `scripts/kn_common.py` is imported by the other four learning detectors, so they agree on scope and resolution.

**Every finding cites the knowledge `file:line` + the reference as written + how it failed to resolve (RENAMED → the successor, DELETED in `<sha>`, never installed, uninstalled command) + the edit that closes it.** A regex hit is never a finding by itself, and "references clean" is never printed without the class-coverage block (§ Output).

## The rule

A reference is a finding when all four hold ([`precedents/learning.md`](../../../../snippets/precedents/learning.md), the claim restated):

1. **It is a live project claim.** The file loads or an agent is told to read it, and the line sits outside history (§ 3), outside an HTML block comment (§ 21), outside a `_template` (§ 4), and — in an installed pack artifact — inside the live anchor block (§ 10).
2. **It does not resolve.** Not exact, not relative to the citing file, not through a tsconfig `paths` alias or a workspace package name, not extension-less, not a unique tracked suffix (§ 6), not present on disk as an ignored or untracked output (§ 1, § 25).
3. **It once resolved here, or it names something the project must have.** Git history says RENAMED or DELETED (DOCER's filter). A path or symbol that never existed is Unconfirmed (§ 5, § 7), and another codebase's path is not a claim (§ 8).
4. **The fix is mechanical or named.** RENAMED → repoint to the successor; DELETED → delete the line or repoint by hand; uninstalled → install, or remove the instruction.

## Boundaries

- **Human docs** — README, `docs/**`, runbooks written for people, diagrams, external links — belong to documentation `doc-drift-scan` when the documentation pack is installed; it can call this engine with its own corpus (`--corpus=`), and the two runs dedupe by `file:line` (owner decision O-1). Without the documentation pack those files are out of scope here, listed as `N/A (owner pack documentation not installed)`.
- **A fact that is wrong but resolves** (MySQL where the lockfile says Postgres, a citation whose line moved) → `knowledge-fact-scan` (KN-07, 13, 14). **A citation inside a memory entry** → `memory-hygiene-scan` §1 (KN-20). **An ADR's own status and supersede links** → `decision-record-scan`. **An oracle file that was never written** (`_extracted-*.md`) is reported here as one KN-19 group and graded by `context-load-scan` §4.
- **A convention the code no longer follows** (KN-10) → align `convention-oracle` AL-04, when the align pack is installed; without it `/detect-drift`'s fallback agent.
- **Dead code** found while resolving → code-quality `dead-code-scan`, not a reference row.

## Adapt to the codebase — the resolution lanes

The engine needs no tool beyond `git` and Python 3.8. Read which lanes resolved what from the ledger (stderr), never assume.

| Lane | What resolves a reference | Read from | Trap |
|---|---|---|---|
| **Any repo** | `git ls-files` (case-sensitive), every parent directory, unique tracked suffix | the index, read-only (`GIT_OPTIONAL_LOCKS=0`) | no git → `census=find` (os.walk minus build dirs): RENAMED/DELETED cannot be classified, rows print `no-history` |
| **JS / TS monorepo** (pnpm, npm, yarn, bun workspaces; Nx, Turborepo) | every tracked `tsconfig*.json` / `jsconfig.json` `paths` (relative `extends` followed), workspace package names from every `package.json` | JSONC read by a string-aware scanner | a regex comment-stripper reads the `/*` in `"@/*"` as a comment and loses the whole alias table |
| **Python, Go, Ruby, PHP, JVM, .NET** | tracked paths and suffixes; symbols by tokenising every tracked source file | the tree | package import paths (`github.com/x/y`) are not repo paths unless the module path maps to a directory |
| **Commands** | `package.json` `scripts` of every workspace; `Makefile` / `justfile` targets; `.claude/{commands,skills,agents}`; `~/.claude/{commands,skills,agents}` and plugin manifests (P-23); Claude Code built-ins; the Refract pack catalog under `~/.claude/templates/packs` | disk | `--no-global` drops the global sets: a global command then reads as unknown, so use it only on a machine with no Refract install |
| **ADR ids** | the detected ADR home (an index's declaration, else the directory with most `NNNN-*.md`) | `kn_common.adr_home` | a hard-coded `ai/decisions/` reads 0 ADRs on a repo whose home is `docs/decisions/` (KN-29) |

## Pre-flight

Run as **one** bash script from the repo root. Step **N** feeds detector **§N**. Every `rg` names its paths (`"${ROOTS[@]}"`, built from the knowledge files that exist); any `rg` exit 2 is `blocked`, never zero hits. Includes first, exclusions last.

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (arrays and PIPESTATUS are bash-only)"; exit 2; }
KS="${KS:-.claude/skills}"        # installed engines; in the Refract repo itself: templates/packs/learning/skills
RUN="${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/knowledge.XXXXXX")}"; mkdir -p "$RUN"; echo "RUN=$RUN"
export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true
ROOTS=(); for p in CLAUDE.md CLAUDE.local.md AGENTS.md GEMINI.md ai .claude/rules .claude/agents .claude/commands .claude/skills \
  .claude/codebase-profile.md .cursor .github/copilot-instructions.md .github/instructions; do [ -e "$p" ] && ROOTS+=("$p"); done
[ ${#ROOTS[@]} -gt 0 ] || { echo "§1-§6 N/A: no knowledge layer (no CLAUDE.md, AGENTS.md, ai/ or .claude/)"; exit 0; }
H=(-g '!**/ai/audits/**' -g '!**/ai/incidents/**' -g '!**/ai/runs/**' -g '!**/ai/migration/**' -g '!**/*_history.md' -g '!**/CHANGELOG*' -g '!**/node_modules/**')

# 1-6. The engine: scope (P-3, P-10, P-21), resolution (P-6), history (DOCER, ReCite), commands (P-23), markers.
python3 -I "$KS/knowledge-ref-scan/scripts/knowledge-refs.py" . > "$RUN/refs.tsv" 2> "$RUN/refs.ledger"
echo "knowledge-refs exit $? (0 clean · 1 rows · 2 blocked)"; cat "$RUN/refs.ledger"; cut -f1-8 "$RUN/refs.tsv"
#    Per-site rows for the fix command, and the info rows (abbreviations, outputs, ambiguous suffixes) for a reviewer:
python3 -I "$KS/knowledge-ref-scan/scripts/knowledge-refs.py" . --expand --all > "$RUN/refs-sites.tsv" 2>/dev/null

# Cross-checks: the engine must not be quieter than a plain search.
# 5. Framework paths written into installed artifacts (the anchor header names Refract's apply-anchors.sh).
rg -n --pcre2 '`(?:scripts/[\w.-]+\.(?:sh|py)|\.claude/_codebase-scan\.md|templates/[\w./-]+)`' -g '*.md' "${ROOTS[@]}" "${H[@]}" > "$RUN/g5.txt"
echo "rg 5 exit $? ($(wc -l < "$RUN/g5.txt" | tr -d ' ') lines; each must be a KN-05 site or a path the project really has)"
# 6. Marker lines per file, fenced examples included: a file whose count is not 2 is read against the engine's §6 rows.
rg -c '^<!-- project-specific:(start|end) -->' -g '*.md' "${ROOTS[@]}" "${H[@]}" > "$RUN/g6.txt"
echo "rg 6 exit $?"; awk -F: '$NF != 2' "$RUN/g6.txt"
# 3. Backticked package-manager commands and slash commands the engine resolves.
rg -n --pcre2 '`(?:pnpm|npm|yarn|bun)\s+(?:run\s+)?[A-Za-z][\w:.-]*' -g '*.md' "${ROOTS[@]}" "${H[@]}" > "$RUN/g3.txt"
echo "rg 3 exit $? ($(wc -l < "$RUN/g3.txt" | tr -d ' ') script lines)"
```

Read the ledger first. It prints the census (`git` or `find`), the corpus by scope (live, pack-body anchor regions, history excluded, sinks handed to `memory-hygiene-scan`), the command universe (project, global, pack catalog; `global NOT READ` when `~/.claude` is absent) and, per lane, how references resolved. A lane that resolved nothing is `N/A` or `blocked`, never clean.

**Measured** (2026-10-19), read-only on a real NestJS + React monorepo (13,620 tracked files, 657 knowledge files; `find -newer` on a start stamp: 0 files written). A naive "every backticked path, `test -e`" prototype returned 15,173 dead-reference candidates. The engine scanned 478 files (124 live, 354 anchor-only; 164 history and 11 sink files excluded) in 7.8 s:
- 13,655 path references: 7,800 exact, 4,161 abbreviations (P-6), 219 relative, 35 ambiguous suffixes (INFO), a handful through aliases and workspace packages; 1,440 unresolved.
- Of those: 169 name the V1 codebase (P-8), 9 are outputs a command will write (P-7), 49 are bare file names never in history — naming examples (P-4) — 297 sites cite oracle files never written (8 KN-19 groups), 690 sites carry framework paths (8 KN-05 groups — `apply-anchors.sh` under Refract's scripts dir and `.claude/_codebase-scan.md` in 341 anchor headers each), 9 sites DELETED in history (6 KN-01 groups, e.g. a deleted `bulk-status-change.test.ts` named by 3 anchors), 6 KN-04 sites (5 `ai/patterns/*.md` listed in the patterns README and never installed), and 211 never-existed sites in 91 groups (Unconfirmed; 123 are anchor "Where this applies" lines naming files that were never committed).
- 734 symbols: 660 present, 72 never in history (P-5, dropped), 2 DELETED (KN-02).
- §3: 217 script references, 1 dead (`bun run scripts/…` first read as a script until the engine learned that a path argument runs a file); 941 slash tokens, 79 route-like and ignored, 1 unknown command (Unconfirmed).
- §6: 2 files — 6 live anchor blocks in one skill (5 holding a literal `...content...` placeholder) and a nested start in another.
- Cross-checks: rg 5 returned 527 lines — 341 anchor headers (the KN-05 group) and 186 lines that are pack-generic bodies outside an anchor (P-10) or paths that resolve (the project's own deploy script; `templates/snippets/*.md`, which resolve by suffix to the installed `.claude/templates/snippets/`). rg 6 listed the same 2 files the engine flagged (a 14-line and an 8-line count, fenced examples included).

On `benchmarks/fixtures/*` (24 trees, none carries a full knowledge layer; `port-pair` has 42 `ai/` files): 0 rows on 23 of them (`convention-drift` first returned 4 Unconfirmed rows — `.store.ts`, `OrderRow.tsx` — naming examples in its conventions doc, now P-4 INFO); `launch-gaps` returned 1 row — `/define-success` cited from 2 `ai/product/success/*.md` files, a product-pack command that is not installed in that tree (a true row for a tree that is not an install). The self-test seeds 15 rows across the six classes (with a case-only rename, a script named with its `--filter` flag, and a dead path in an untracked subtree whose census is the walk) and 16 decoys (abbreviation, alias, history file, sink, HTML comment, placeholder, global command, route, external symbol, pack-generic body, workspace script, fenced marker, output, V1 path, naming example, a gitignored `dist/` directory).

On `stale-knowledge` (the seeded fixture, staged with its 15-commit history; `--global-dir` a scratch dir linking the checkout's `commands`, `scripts` and `templates`): 45 files (23 live, 10 anchor-only, 1 history, 9 sinks handed off); 165 paths, 17 symbols, 18 scripts, 18 slash tokens → 16 grouped rows (22 with `--expand`), all on seed sites: **16 seeds printed** (the fixture totals 58 of its 59 learning seeds across the five detectors) — RENAMED and DELETED paths, a case-only rename (`ApiClient.ts` → `apiClient.ts`, read case-exactly on a case-insensitive disk), a renamed and a deleted symbol, a renamed script, an uninstalled catalog command, a renamed skill (Unconfirmed), an uninstalled pattern, an ADR id with no file, the framework-path header (one group, 5 anchors), a nested and an unclosed marker, plus the never-written idioms oracle as one KN-19 group. Decoys: 0 of 26 rows (`--all` reads `apps/web/dist/` as `ignored` through the `dist/` pattern). On the one-commit copy (no history) both KN-02 seeds vanish and three dead paths drop to `never-existed` (Unconfirmed).

## The 3,000-hit path

A repo with years of `ai/` notes can return thousands of unresolved references. Triage in this order and record every step in the coverage block:

1. **Group by root cause.** Rows already collapse by (class, reference, resolution) with `sites=N`. One anchor header line copied into 341 files is one row; fix the generator (`apply-anchors.sh`, IR-1), not 341 files.
2. **Rank by load.** Files loaded every session (`CLAUDE.md` and its imports, rules without `paths:`, anchor blocks) first, then `ai/*` files commands read by name, then the rest.
3. **Take the classified rows first.** RENAMED rows carry their successor: a mechanical repoint. DELETED rows need one decision per group.
4. **Read the top 30 Unconfirmed groups fully.** A never-existed path is a typo, a planned file (P-7), another codebase (P-8) or an uncommitted local file named by a generator.
5. **Ledger the rest** as `Live, unreviewed (k groups / n sites)` with the command that continues them (`knowledge-refs.py . --expand --classes=1`). Never `checked`.

## Scans for

| § | Class | Default |
|---|---|---|
| 1 | KN-01 dead path reference (link, backtick, fence, `@import`) | M; H in a file loaded every session or an anchor block |
| 2 | KN-02 dead symbol (class, function, constant named in a claim) | M; H in an anchor |
| 3 | KN-03 dead command: package script, make/just target, slash command, skill, agent | H in a loaded file, else M |
| 4 | KN-04 dead knowledge cross-reference: `ai/patterns/x.md`, `ai/runbooks/…`, `ADR-NNNN` with no file | M |
| 5 | KN-05 framework-only path in an installed artifact | M |
| 6 | KN-15 managed-marker corruption: nested start, start without end, duplicate live blocks | M |

### 1. Dead path reference (KN-01)

```
BAD:   CLAUDE.md:2        Billing lives in `apps/api/src/old-name.service.ts`.        (renamed to billing.service.ts)
       .claude/commands/x.md:22 (anchor)  `apps/web/…/bulk-status-change.test.ts`       (deleted in 2b2db317)
GOOD:  `shared/persistence/page-query.ts`  — one tracked file ends with it (P-6)
       `@/shared/api/client` — tsconfig `paths` alias · `ai/align/ledger.md` — an output the command writes (P-7)
```
**Read the code:** Is the reference inside a live region (the engine's scope) — or a history file, a template, a block comment? Did it ever resolve (`RENAMED`/`DELETED` in the resolution column) or never (Unconfirmed)? For RENAMED, open the successor: is it still the same responsibility, or was it split? Is the path generated or gitignored (`--all` shows `ignored`)? Does the line describe another codebase (P-8)? **Finding when** a live claim names a path that resolved once and resolves to nothing now. **Proof:** tier S — the line quoted, the `git log` commit that deleted or renamed it; after the fix, `knowledge-refs.py . --only=<file>:<line>` is quiet (V490).

### 2. Dead symbol (KN-02)

```
BAD:   Call `LegacyBillingService` (renamed BillingService) · `formatLegacyCents` (deleted) · `applyOrdersDelta` (deleted 0f8dfbff)
GOOD:  `ExternalThing` — never in this history: an external or framework symbol (P-5)
```
**Read the code:** Is the symbol the project's (removed in a commit here) or external (never in history: dropped)? Does it survive only in a comment (P-12: still dead)? For RENAMED, does the successor keep the signature the claim describes? `Class.method` with a plain lowercase member is not checked: the receiver carries the claim. **Finding when** the symbol once existed in tracked non-doc source and exists in none now. **Proof:** tier S + V491 — the successor named, or the deletion commit; the engine re-run on the line is quiet.

### 3. Dead command, script, skill or agent (KN-03)

```
BAD:   `pnpm run build:all` (no workspace defines it) · run `/eval` (in the pack catalog, not installed) · dispatch `@style-judge`
GOOD:  `pnpm test:e2e` (defined in apps/api) · `/setup-project` (global, P-23) · serves `/orders` (a route, no command cue)
       `bun run tools/load-check.ts` (runs a file) · `# this just died` in a shell comment (prose, P-33)
```
**Read the code:** Which workspace runs the command (`--filter`, `cd`)? Is the slash name installed globally, by a plugin, or a Claude Code built-in? Is it a renamed skill (a 2026-10-18 rename moved `detect-drift`'s engine to `align-detect`)? Is the `@name` an npm scope or a user mention? **Finding when** a command an agent is told to run resolves nowhere, or resolves only in the Refract catalog (uninstalled). **Proof:** tier S + V492 — the manifest or command set that lacks it; after the fix, the command resolves (the engine is quiet) and the documented invocation runs.

### 4. Dead knowledge cross-reference (KN-04)

```
BAD:   ai/patterns/README.md:17  `project-structure.md` → ai/patterns/project-structure.md was never installed
       CLAUDE.md:10  "follow ADR-0007" — no 0007-*.md in the ADR home (docs/decisions)
GOOD:  ADR-0042 inside a pack-generic body (P-10) · ADR-0001 with a file, even if superseded (decision-record-scan §3 owns that)
```
**Read the code:** Which ADR home did the engine detect (ledger line), and does the index agree? Was the pattern pack-installed and later pruned, or never shipped? **Finding when** a live line names a pattern, runbook or ADR id with no file. **Proof:** tier S + V490 — the home listing without the id; after the fix the id resolves or the line is gone.

### 5. Framework-only path (KN-05)

```
BAD:   > Auto-populated by `<refract>/apply-anchors.sh` from `.claude/codebase-profile.md` + `.claude/_codebase-scan.md`.   (341 anchors)
       `frontend/rules/migration-frontend.md` — a Refract pack path; the installed copy is .claude/rules/migration-frontend.md
GOOD:  `bin/deploy.sh` — the project's own script (it resolves)
```
**Read the code:** Does the project really have that file (then it resolves and never reaches this class)? Does `~/.claude/<path>` exist (the ledger says so — the path belongs to the framework)? Is the line generated (an anchor header)? **Finding when** an installed artifact tells the agent to read or run a path that exists only in the Refract repository. **Proof:** tier S + V490; the fix lands in the generator (`apply-anchors.sh`, IR-1), and a regenerate-twice run is byte-identical (tier U, V493).

### 6. Managed-marker corruption (KN-15)

```
BAD:   <!-- project-specific:start --> … <!-- project-specific:start --> … <!-- project-specific:end -->   (nested)
       six live blocks in one skill, five holding `...content...`
GOOD:  one column-0 start/end pair outside fences · a marker shown inside a ``` example (not live)
```
**Read the code:** Is the extra marker fenced (an example: not live)? Which block is the generator's current one? Does `audit-anchoring.sh has_live_anchor` read the same file the same way? **Finding when** a file has more than one live block, a start with no end, an end with no start, or a nested start. **Proof:** tier U + V493 — after `apply-anchors.sh` re-runs, one live pair remains, and a second run changes no byte.

## Proof

Oracles: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Learning — V490 (re-resolve: the row fires on the seeded reference and is quiet after the fix; decoys quiet), V491 (symbol rename with successor), V492 (command resolves and runs), V493 (marker repair, regenerate twice). The engine's `--only=<file>:<line>` is the before/after probe `/refresh-knowledge --from-audit` records.

## Output

```
knowledge-ref-scan — census git (13,620 files) · corpus 478 scanned (124 live, 354 anchor-only; 164 history, 11 sinks excluded)
Lanes: paths (tsconfig aliases 1, workspace packages 4) · symbols (tokenised 12,215 files) · commands (project 147, global, catalog 161) · ADR home docs/decisions

1. .claude/commands/audit-distributed-tx.md:22 (+2 anchors)               [report-with-fix]   high
   §1 KN-01 — `apps/web/src/features/orders/list/lib/bulk-status-change.test.ts` DELETED in 2b2db317.
   Fix: regenerate the anchors (apply-anchors.sh) so "Where this applies" names a live file. Proof: --only quiet.
2. .claude/agents/*.md:15 (341 sites)                                      [report-with-fix]   medium
   §5 KN-05 — Refract's `apply-anchors.sh` path and `.claude/_codebase-scan.md` in every anchor header: framework paths.
   Fix: apply-anchors.sh stops writing them (IR-1); regenerate twice, byte-identical.
3. ai/references/tool-parity.md:114                                         [report-flagged]    medium
   §3 KN-03 — `/db-migration` resolves in no command set; no catalog entry either. Unproven: a renamed command?

Verification: 31 candidates → 18 findings · 9 unconfirmed · 2 hardening · 0 pre-existing · 2 refuted

Class coverage:
  §1  KN-01 dead path          checked (13,655 refs → 6 groups DELETED; 91 never-existed groups Unconfirmed; 169 P-8, 9 P-7, 49 P-4)
  §2  KN-02 dead symbol        checked (734 → 2 DELETED; 72 never in history, P-5)
  §3  KN-03 dead command       checked (217 scripts, 941 slash tokens → 1 unconfirmed)
  §4  KN-04 knowledge xref     checked (258 ADR ids, 6 pattern refs → 6)
  §5  KN-05 framework path     checked (8 groups, 690 sites)
  §6  KN-15 markers            checked (343 files with markers → 2)
```

`[report-with-fix]`: the reference resolved once and history names the successor or the deletion, and the fix is a repoint, a deleted line, or a regenerated derived file. `[report-flagged]`: one link is open (never in history, an ambiguous suffix, a command that may be renamed), and the row names it. The coverage block lists **all six** classes on every run: `checked (k → m)` only when the lane ran; `N/A (<reason>)` when the repo has no such surface (no knowledge layer, no ADR home); `blocked (<reason>)` when the engine or an `rg` exited 2.

## False positives / precedents

The verifier reads [`precedents/learning.md`](../../../../snippets/precedents/learning.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. The ones this skill meets most: § 1 generated targets, § 3 history, § 4 placeholders and templates, § 5 external symbols, § 6 abbreviations and aliases, § 7 outputs and plans, § 8 another codebase, § 10 pack-generic bodies, § 12 comment-only survivors, § 21 HTML comments, § 23 global commands, § 32 an oracle never written, § 33 commands in shell comments.

## When to run

- On any diff that renames, moves or deletes files, symbols, package scripts, commands, skills, agents, patterns or ADRs, or edits `CLAUDE.md`, `AGENTS.md`, `ai/**`, `.claude/rules/**` or an anchor block: the `/audit-knowledge` dispatch signal.
- On every whole-repo `/audit-knowledge`, reporting all six classes.
- After `/setup-project --refresh` or `apply-anchors.sh`: a regenerated anchor set must not carry a framework path or a doubled block.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10, with [`precedents/learning.md`](../../../../snippets/precedents/learning.md)). Under `/audit-knowledge` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any row without the knowledge `file:line`, the reference as written, and its resolution.
- Never edit a derived file (an anchor block, an index) by hand to close a row: fix the generator and regenerate (tier U).
- Never write into the scanned repository: the engine reads, runs read-only git, and writes only under `$RUN`.
- Never print "references clean" without the coverage block. A lane that did not run (no git, no global dir) is `blocked` or `N/A`, never zero.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `scripts/knowledge-refs.py` (this skill): §1–§6, `--only`, `--corpus`, `--expand`, `--all`, `--global-dir`, `--no-history`, `--self-test`. `scripts/kn_common.py`: the census, corpus, regions, resolver, ADR home and lockfile reader the other four learning engines import. Stdlib only, `python3 -I` safe; nothing is written under the scanned root.
- `knowledge-fact-scan` grades facts and citations that resolve; `memory-hygiene-scan` grades sink entries; `decision-record-scan` grades ADR lifecycle; `context-load-scan` grades what loads. `/audit-knowledge` dispatches all five; `/refresh-knowledge --from-audit` closes the rows with the engine re-run as proof.
- documentation `doc-drift-scan` (when installed) owns human docs and may call this engine with its own corpus. `apply-anchors.sh` (Refract) is where KN-05 and KN-15 are fixed.
