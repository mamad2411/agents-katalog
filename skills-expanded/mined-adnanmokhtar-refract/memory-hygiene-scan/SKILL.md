---
name: memory-hygiene-scan
description: Learning-sink entries — stale evidence, duplicates, contradictions, no provenance, stuck states, unreadable format.
kind: skill
pack: learning
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: memory-hygiene-scan

## Premise

The learning loop writes observations into nine append-only sinks ([`learning-sink.md`](../../../../snippets/learning-sink.md)) and promotes the mature ones into the formal layer. Agents copy retrieved memories on similar tasks, so a wrong entry spreads (Xiong 2025); provenance-less memory can be planted (MINJA, preprint); current memory agents are weak at resolving conflicts (MemoryAgentBench). Entries rot by their **evidence**: the path an entry cites is deleted, the line it cites is past the end of the file, the rule it corrects was removed. And consumers break silently when a project reshapes a sink: on a real NestJS + React monorepo the drift log declares its own format (no `Status:` line; an entry is deleted on fix), so the curator's "entries with status `OPEN`" reads 0 of 76 entries and reports nothing to do.

`scripts/sink-audit.py` (this skill) parses each sink by the format it **declares** in its own `## Format per entry` block first (P-24), the template second, and owns: §1 stale evidence (KN-20), §2 duplicates (KN-21), §3 contradiction pairs for a judge (KN-22), §4 provenance (KN-23), §5 stuck lifecycle (KN-24), §6 n=1 universal lessons (KN-25, advisory), §7 checkable lessons with no enforcement (KN-26), §8 consumer contracts (KN-27), §9 the eval guard count (KN-36).

**Every finding cites the sink `file:line` of the entry + its heading + what failed (the citation and how it no longer resolves, the duplicate's site, the missing field, the state and its age, the consumer's regex and its match ratio) + the fix that keeps history (mark `RESOLVED → <sha>` or `SUPERSEDED` with a reason; never delete an entry).** "Memory clean" is never printed without the class-coverage block.

## The rule

An entry is a finding when all four hold:

1. **It is open.** Its status is not terminal (RESOLVED, REJECTED, SUPERSEDED, PROMOTED, DISCARDED, REVERSED, ARCHIVED, FIXED, CLOSED); a terminal entry citing a deleted path is history (§ 3).
2. **The sink's own contract applies.** The fields, states and heading shape come from the sink's declared format; an undated `### ` heading in a sink that declares dated entries is a section, not an entry, unless it carries a declared field.
3. **The evidence is checkable.** The entry cites a path, a line, a package or a rule. A memory with no code anchor (a decision, a preference) has provenance "user, <date>" and is never stale by code (§ 19).
4. **The fix keeps the record.** Re-verify and mark, merge two entries into one keeping both citations, promote or record why not, or hand a checkable lesson to enforcement. The curator invariant is "archive, don't delete".

## Boundaries

- **A citation in a non-sink knowledge file** → `knowledge-ref-scan` §1 (paths) and `knowledge-fact-scan` §6 (lines). This skill reads only the sinks.
- **A lesson about a convention** that should be enforced → align (AL-03 "declared, not enforced") when the align pack is installed; §7 here covers lessons, feedback and failures. Without align, convention lessons are listed here, tagged `convention (owner pack align not installed)`.
- **Eval quality** — toothless, stale or regressed cases → `/eval --coverage` grades; §9 here is a count.
- **A secret pasted into an entry** (KN-34) → security `secret-scan-method` when the security pack is installed; `context-load-scan` §5 hands it the file list.
- **The host memory directory** (`~/.claude/projects/<p>/memory/`) is outside the repo: read only with `--memory-dir=` (owner decision O-3). MEMORY.md's 200-line / 25 KB load limit is `context-load-scan` §1.

## Adapt to the codebase — the sink lanes

| Sink | Declared format read | Status vocabulary | Promotion threshold (learning-sink.md) | Consumer contracts checked (§8) |
|---|---|---|---|---|
| `ai/dynamic/learnings.md` | its `## Format per entry` fence | RAW · PROMOTE_CANDIDATE · PROMOTED · DISCARDED (as declared) | 3 sightings + ≥ 2 cited examples → `ai/conventions.md` | `/recall` dated headings |
| `ai/dynamic/learned-patterns.md` | same | WATCHING · READY · PROMOTED · REJECTED | READY (≥ 3 files, ≥ 2 weeks) → `ai/patterns/` | `session-start.sh` `^Status: READY` |
| `ai/dynamic/feedback-learned.md` | same | WATCHING · RULE_CANDIDATE · PROMOTED · REJECTED | `Repeated >= 2` → `.claude/rules/` | — |
| `ai/dynamic/decisions-pending.md` | same | WATCHING · VALIDATED · PROMOTED → ADR · REVERSED | VALIDATED → an ADR in the detected home | — |
| `ai/dynamic/drift-log.md` | same (projects often redefine it) | as declared; the template's OPEN/RESOLVED | mark RESOLVED | `session-start.sh` `^Severity: high`; curator duty 4 `status OPEN` |
| `ai/failures/_index.md` | same | as declared | stays (don't-retry catalog) | — |
| `ai/dynamic/vocabulary.md` | same | RAW · PROMOTE_CANDIDATE · PROMOTED · DISCARDED | 2 sightings + 1 citation → glossary | — |
| host memory dir (opt-in) | topic-file frontmatter | — | — | MEMORY.md index lines (P-18) |

The stuck-state threshold defaults to 14 days (the learned-patterns "≥ 2 weeks" rule); `--stuck-days=` changes it, and the coverage block prints the value used.

## Pre-flight

Run as **one** bash script from the repo root. Step **N** feeds detector **§N**. Every `rg` names its paths; any `rg` exit 2 is `blocked`.

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (arrays and PIPESTATUS are bash-only)"; exit 2; }
KS="${KS:-.claude/skills}"        # installed engines; in the Refract repo itself: templates/packs/learning/skills
RUN="${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/knowledge.XXXXXX")}"; mkdir -p "$RUN"; echo "RUN=$RUN"
export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true
SINK_PATHS=(); for p in ai/dynamic ai/failures/_index.md; do [ -e "$p" ] && SINK_PATHS+=("$p"); done
[ ${#SINK_PATHS[@]} -gt 0 ] || { echo "§1-§9 N/A: no learning sinks (ai/dynamic/, ai/failures/_index.md)"; exit 0; }

# 1-9. The engine: declared formats, entries, citations re-resolved, duplicates, polarity pairs, provenance,
#      lifecycle ages, enforcement lookup (lint configs, hooks, CI, tests), consumer contracts, eval count.
python3 -I "$KS/memory-hygiene-scan/scripts/sink-audit.py" . > "$RUN/sinks.tsv" 2> "$RUN/sinks.ledger"
echo "sink-audit exit $? (0 clean · 1 rows · 2 blocked)"; cat "$RUN/sinks.ledger"; cut -f1-7 "$RUN/sinks.tsv"
#    Opt-in, never by default (O-3): add --memory-dir="$HOME/.claude/projects/<encoded>/memory" to the line above.

# Cross-checks.
# 0. Entry headings per sink: the engine's `entries` must be explained against this (sections are not entries).
rg -c '^### ' -g '*.md' "${SINK_PATHS[@]}"; echo "rg 0 exit $?"
# 5. State lines as written (column 0): states the engine counts as stuck or non-standard.
rg -o --no-filename '^Status: [A-Z_]+' -g '*.md' "${SINK_PATHS[@]}" | sort | uniq -c; echo "rg 5 exit ${PIPESTATUS[0]}"
# 8. Consumer greps in installed hooks: every one the engine checks, and any it does not know yet.
[ -d .claude/hooks ] && { rg -n --pcre2 'grep[^\n]*"\^[A-Z][a-z]+:[^"]*"[^\n]*ai/(?:dynamic|failures)/' .claude/hooks; echo "rg 8 exit $?"; }
```

Read the ledger first: per sink, the entry count, whether the format is declared (and its fields) or the template is assumed, and citations ok / gone / past-EOF; per consumer contract, how many entries it matches. A sink the engine could not parse is `blocked`, never empty.

**Measured** (2026-10-19), read-only on a real NestJS + React monorepo (8 of 9 sinks present, every one declaring its own format; 0.9 s; 0 files written):
- §1: drift log 76 entries, citations 178 resolving / 6 gone / 33 past the end of the file → 29 stale entries; learnings 3 entries cite a deleted `tailwind.config.ts` or a moved wire file; 1 READY pattern cites a line past EOF. The first cut also read `this.tx.run` and `engine.io` as files: a citation now needs a known file extension.
- §5: both READY patterns stuck 79 days, both PROMOTE_CANDIDATE learnings stuck 43–44 days (the research's own count), and 1 of 3 patterns with no state.
- §7: 1 lesson with a checkable subject (`@utility`) and no lint, hook or test naming it — Unconfirmed, because it describes a Tailwind ordering rule, not a banned import.
- §8: the curator's `status OPEN` contract reads **0 of 76** drift entries: the sink declares a format with no Status field (P-24). The session hook's `^Severity: high` reads the 1 entry that carries the line.
- §9: 0 eval cases; 0 of 11 promoted project units guarded.
- §2, §3, §4: 0 rows after the fixes. A first cut paired 12 "contradictions" that were drift entries quoting both sides of a divergence and lines whose only shared subject was a path (`apps/web`); §3 now pairs lessons, patterns, feedback, pending decisions and failures against `CLAUDE.md` and rules, on code subjects, with imperative polarity only (§ 31). §4 first flagged 7 failure entries dated `2026-08` (month precision is a date) and 2 vocabulary section headings (not entries).
- On `benchmarks/fixtures/*` (24 trees): 0 rows beyond the §9 count line — no fixture carries learning sinks. The self-test seeds 12 rows (gone path, past EOF, n=1 universal lesson, a lesson contradicting `CLAUDE.md`, an unenforced import ban, an undated unsourced entry, a duplicate heading, a stuck PROMOTE_CANDIDATE and a stuck READY, the curator's population contract, a `Severity` written as a list item the hook cannot read, a `- **Status:** READY` entry stuck) and 8 decoys (a resolving entry, a RESOLVED entry citing a deleted path, an enforced ban, a safety lesson from one incident, a "user, <date>" provenance, a declared format without Status, dotted identifiers, `Severity: low` at column 0 under a `^Severity: high` hook).
- On `stale-knowledge` (the seeded fixture; 5 sinks, each declaring its format; `--today=2026-10-12`): 28 entries, citations 24 ok / 2 gone / 1 past EOF → 17 rows plus the §9 count, all on seed sites — **17 seeds printed**: three stale entries, two duplicates, two judge pairs, an undated and an unsourced entry, READY for 30 days and `Repeated: 3` for 41, two one-incident universal lessons (advisory), an unenforced import ban and an unchecked `lock_timeout` lesson, and the session hook's two template greps (0 of 5 and 0 of 2 entries read). `--eval-coverage`: 4 of 5 units guarded. The toothless case is `/eval`'s to grade. Decoys: 0 of 26. A subset contract counts an entry as unreadable only when its field is outside the consumer's shape (`Severity: low` at column 0 is read), and `- **Status:** READY` (colon inside the bold) reads as READY.

## The 3,000-hit path

A sink with hundreds of entries (a long-lived drift log) can return hundreds of rows.

1. **Group by cause.** Stale entries that cite files deleted in one commit are one re-verification; a contract that reads 0 of N is one row, not N.
2. **Close what moved, then what is old.** Entries whose evidence is gone first (they mislead now), then stuck states by age, then provenance.
3. **Judge pairs in batches.** §2 near-duplicates and §3 polarity pairs carry both quotes; one judge pass reads them all, and only pairs a second reader confirms become findings.
4. **Ledger the rest** as `Live, unreviewed (k entries)` with `sink-audit.py . --classes=<n>`.

## Scans for

| § | Class | Default |
|---|---|---|
| 1 | KN-20 stale entry: cited path gone, line past EOF | M (L in the failures catalog: a lesson can outlive its code) |
| 2 | KN-21 duplicate entries within or across sinks | L |
| 3 | KN-22 contradicting entries, or an entry vs `CLAUDE.md` / a rule | judge pair; H when the other side loads every session |
| 4 | KN-23 entry without date or source | M without a source, L without a date |
| 5 | KN-24 stuck lifecycle, stateless entries, undeclared states | L; M past 4× the threshold |
| 6 | KN-25 universal lesson from one case | L, advisory (Unconfirmed only) |
| 7 | KN-26 checkable lesson with no hook, lint rule or test | M |
| 8 | KN-27 consumer cannot read the sink's format | M |
| 9 | KN-36 knowledge with no guarding eval case | a count (`/eval --coverage` grades) |

### 1. Stale entry (KN-20)

```
BAD:   ### 2026-09-01 — api: orders helper moved      - Where: `src/legacy-orders.ts:10`   (deleted)
       ### 2026-09-02 — api: list past end            - Where: `src/orders.ts:205`         (file has 120 lines)
GOOD:  ### 2026-09-04 — RESOLVED api: old thing       (terminal: history) · a preference entry with no code anchor (P-19)
```
**Read the code:** Did the code move (repoint), was the drift fixed (mark `RESOLVED → <sha>`), or did the failure lesson outlive its code (mark `SUPERSEDED` with a reason, keep the lesson)? Does the line quote another codebase (P-8)? **Finding when** an open entry's citation no longer resolves or points past the end of the file. **Proof:** tier S + V499 — the citation and the `git log` that moved it; after the fix the entry re-resolves or carries RESOLVED/SUPERSEDED with a reason (`sink-audit.py . --only=<sink>:<line>` quiet).

### 2. Duplicate entries (KN-21)

```
BAD:   learnings.md:23 and :32 — "axios must not be imported" twice, two citations
GOOD:  MEMORY.md index line + its topic file (P-18) · two entries on one topic with different subjects
```
**Read the code:** Same correction, or two sightings that should increment one entry's count? **Finding when** two open entries have the same normalised heading (Candidate) or ≥ 0.8 token overlap (a judge pair). **Proof:** V500 — one entry remains with both citations and its sighting count updated.

### 3. Contradiction pair (KN-22)

```
BAD:   learnings.md:13 "Never wrap `transactions` around reads"  vs  CLAUDE.md:2 "Always use `transactions` around a money write"
GOOD:  a pair marked SUPERSEDED (P-14) · scopes that do not overlap (reads vs money writes is a judge question, not a regex one)
```
**Read the code:** Do both lines govern the same subject in the same scope? Is one newer and explicit (the newer user statement wins)? **Finding when** a judge reading both quotes agrees they cannot both hold; the engine only pairs them (`judge` rows). **Proof:** V500 — one side marked SUPERSEDED with a reason, or both rewritten with their scopes.

### 4. Provenance (KN-23)

```
BAD:   ### Undated thing with no source        (no date, no Source/Where, no citation)
GOOD:  "Source: user, 2026-08-05" (P-19) · a heading dated 2026-08 (month precision)
```
**Read the code:** Which fields does the sink declare? Is there evidence elsewhere in the entry (a PR, a commit, a URL)? **Finding when** an entry has no date, or no source and no citation. **Proof:** V501 — the entry carries a date and a source.

### 5. Stuck lifecycle (KN-24)

```
BAD:   learned-patterns.md:85  Status: READY for 79 days, never promoted
       learnings.md:80        Status: PROMOTE_CANDIDATE for 44 days
GOOD:  a state the sink declares that is not a promotion state · a sink that deletes entries on fix and declares no Status (P-24)
```
**Read the code:** Was it promoted under another name (an `ai/patterns/` file, a rule, an ADR)? Did the owner decide not to promote? **Finding when** an entry sits in a promotion state past the threshold, an entry has no state in a sink whose format declares one, or a state is not in the sink's declared vocabulary. **Proof:** V501 — promoted (`/promote-pattern`, `/promote-decision`) or a recorded reason.

### 6. Universal lesson from one case (KN-25)

```
BAD:   "never use transactions in read paths" — one citation
GOOD:  "never force-push to main" — one incident is enough for an irreversible action (P-20)
```
**Read the code:** Is the scope really universal? Is it a safety or irreversible action? Advisory only: it never becomes a Finding without a second case or a judge. **Proof:** V501 — the lesson scoped, or a second cited case.

### 7. Checkable lesson with no enforcement (KN-26)

```
BAD:   "Never import `axios` directly; use the http client" — no lint rule, hook, CI step or test names `axios`
GOOD:  "Never import `moment`" — `no-restricted-imports` names it in eslint.config.mjs
```
**Read the code:** Is the subject matchable (an import, an API call, a path)? Is it a convention (align's)? **Finding when** an open lesson bans or requires a matchable subject and no lint config, hook, CI workflow, Semgrep rule or test file names it. **Proof:** V502 — a real failing lint rule or test on a violating snippet, then green on the fixed one; the prose keeps one pointer line.

### 8. Consumer cannot read the format (KN-27)

```
BAD:   curator duty 4 reads drift entries "with status `OPEN`" — the sink declares no Status field: 0 of 76 match
       session-start greps `^Severity: high` — two entries write `- Severity: high` in a list
GOOD:  a sink that declares its own format and a consumer that reads that format (P-24)
```
**Read the code:** Which side moved — the sink's declared format or the consumer's template assumption? Is the consumer a filter (a subset by design: compare entries carrying the field in any shape with those it reads) or a population reader (ratio < 0.5)? **Finding when** a consumer's pattern matches under half of a sink's entries that it is meant to read, or misses entries that carry its field in another shape. **Proof:** V503 — after the format or consumer fix, the ratio is ≥ 0.5 (population) or every carrier matches (subset).

### 9. Eval guard count (KN-36)

A count only: `N case(s); k of m promoted unit(s) guarded`, where units are project patterns and project rules without a `pack:` frontmatter. `/eval --coverage` grades UNGUARDED, TOOTHLESS and STALE; `sink-audit.py . --eval-coverage` prints the JSON it reads.

## Proof

Oracles: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Learning — V499 (entry re-resolves or carries a terminal state with a reason), V500 (duplicate merged / contradiction resolved, both quotes on record), V501 (provenance and lifecycle), V502 (lesson → a failing-first lint rule or test), V503 (consumer ratio). `sink-audit.py . --only=<sink>:<line>` fires before the edit and is quiet after it; `--entry=<sink>:<line>` is the reconcile-on-write check `/learn-from-task` runs before appending.

## Output

```
memory-hygiene-scan — 8 of 9 sinks · formats declared 8 · stuck threshold 14 d · memory dir NOT READ (O-3)

1. .claude/agents/knowledge-curator.md:115                                  [report-with-fix]   medium
   §8 KN-27 — "drift entries with status `OPEN`" reads 0 of 76 ai/dynamic/drift-log.md entries: the sink declares
   Where/Drift/Suggested fix and deletes an entry on fix (P-24). Fix: the curator reads the declared format.
2. ai/dynamic/drift-log.md:102 (+28 entries)                                [report-with-fix]   medium
   §1 KN-20 — `apps/api/src/bootstrap.ts:336` past EOF (224 lines). Fix: re-verify; RESOLVED → <sha> or re-point.
3. ai/dynamic/learned-patterns.md:85                                        [report-flagged]    medium
   §5 KN-24 — READY for 79 days, never promoted. Unproven: promoted under another name? Settling: rg the pattern name in ai/patterns/.

Verification: 41 candidates → 33 findings · 6 unconfirmed · 0 hardening · 0 pre-existing · 2 refuted

Class coverage:
  §1  KN-20 stale evidence     checked (263 citations → 33 entries)
  §2  KN-21 duplicates         checked (109 entries → 0)
  §3  KN-22 contradictions     checked (0 pairs)
  §4  KN-23 provenance         checked (0)
  §5  KN-24 lifecycle          checked (threshold 14 d → 5)
  §6  KN-25 n=1 universal      checked (advisory → 0)
  §7  KN-26 lesson → check     checked (1 unconfirmed)
  §8  KN-27 consumer contract  checked (3 contracts → 1)
  §9  KN-36 eval guards        0 cases; 0 of 11 units guarded (count only)
```

`[report-with-fix]`: the entry's evidence or contract is shown at both ends and the fix keeps history. `[report-flagged]`: one link is open (promoted under another name, a judge pair, a convention lesson). The coverage block lists **all nine** classes on every run: `checked`, `N/A (<reason>)` (no sinks, no consumer installed, no eval dir), or `blocked (<reason>)`.

## False positives / precedents

The verifier reads [`precedents/learning.md`](../../../../snippets/precedents/learning.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. The ones this skill meets most: § 3 history (terminal entries), § 8 another codebase, § 14 history-marked pairs, § 18 index plus topic, § 19 preference memories, § 20 safety lessons, § 24 declared formats, § 25 gitignored session files, § 31 drift entries are not rules.

## When to run

- On any diff that touches `ai/dynamic/**`, `ai/failures/_index.md`, `ai/evals/**`, a consumer of the sinks (`.claude/hooks/session-start.sh`, the curator, `/recall`), or deletes or moves files the sinks cite: the `/audit-knowledge` dispatch signal.
- Before `/learn-from-task` appends an entry: `--entry=<sink>:<line>` (duplicate, contradiction, provenance).
- On every whole-repo `/audit-knowledge`, reporting all nine classes.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10, with [`precedents/learning.md`](../../../../snippets/precedents/learning.md)). Under `/audit-knowledge` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Never delete an entry to close a row: mark RESOLVED, SUPERSEDED or DISCARDED with a reason (the curator invariant).
- Never promote a judge pair (§2 near-duplicate, §3 contradiction) or an §6 advisory row to a Finding without both quotes and a second reader.
- Never read the host memory directory without `--memory-dir` (O-3), and never write into the scanned repository.
- Never print "memory clean" without the coverage block; a sink that did not parse is `blocked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `scripts/sink-audit.py` (this skill): §1–§9, `--only`, `--entry`, `--memory-dir`, `--stuck-days`, `--today`, `--eval-coverage`, `--self-test`; imports `kn_common.py` from the knowledge-ref-scan skill (its scripts directory). Stdlib only, `python3 -I` safe; nothing is written under the scanned root.
- [`learning-sink.md`](../../../../snippets/learning-sink.md) — the nine sinks and their thresholds. `knowledge-curator` promotes; `/learn-from-task` writes; `/recall` reads; `/eval` grades. `/audit-knowledge` dispatches this skill; `/refresh-knowledge --from-audit` closes rows with the engine re-run as proof.
- align (when installed) owns convention lessons as AL-03; security (when installed) owns secrets pasted into entries.
