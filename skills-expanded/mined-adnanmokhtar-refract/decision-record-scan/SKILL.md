---
name: decision-record-scan
description: ADR home, status, supersede links, superseded ADRs cited as current, chosen option absent from manifests.
kind: skill
pack: learning
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: decision-record-scan

## Premise

Agents treat an Accepted ADR as binding and "fix" code back to it. So an ADR whose decision was reversed in code, a superseded ADR still cited as current, or a supersede link that runs only one way sends an agent back to a decision the team already left. Nygard's rule (2011) and MADR 4 say an ADR is never deleted, only superseded, with the status pointing at its successor; Zimmermann's review checklist asks for the same reciprocity.

There is a defect before any of that: **where the ADRs live**. On a real NestJS + React monorepo the 40 ADRs sit in `docs/decisions/`, and the project's own decision index says not to start a competing `ai/decisions/` ledger. 49 installed agents, commands, skills and rules still read or write `ai/decisions/`, which holds only a README and a template — so a health check counts 0 ADRs and `/promote-decision` would start a second ledger (KN-29).

`scripts/adr-index.py` (this skill) owns: §0 the ADR home and the consumers that read another one (KN-29), §1 status not machine-readable (KN-28), §2 one-way supersede links (KN-28), §3 a superseded or retired ADR cited as current (KN-28), §4 an Accepted ADR whose chosen package is in no manifest (KN-28, Unconfirmed).

**Every finding cites the ADR or the citing `file:line` + the ADR id and its parsed status + the other end (the successor that does not link back, the manifest that lacks the chosen package, the consumers that read the wrong home) + the edit.** "Decisions consistent" is never printed without the class-coverage block.

## The rule

A row is a finding when all four hold:

1. **The ADR home is known.** An index file declares it, or it is the directory with the most `NNNN-*.md` files among `docs/decisions`, `docs/adr`, `doc/adr`, `adr`, `architecture/decisions`, `ai/decisions` and any `decisions/` or `adr/` directory. Without one, every class is `N/A (no ADR directory)`.
2. **The status is read in the shape the project writes it.** `Status: Accepted`, `- **Status:** Superseded by [0014](…)`, `**Status:** accepted · **Date:** …`, `Date: … · Status: accepted`, a `## Status` heading, a frontmatter `status:`, a table row.
3. **The other end is checked, not assumed.** A successor's text for the back link; the corpus outside the ADR home and the index for current citations; the manifests and lockfile for the chosen package.
4. **The fix never deletes a decision.** Add the reciprocal link, re-point the citation, mark `Superseded by` or `Amended by`; a decision reversed in code needs a new ADR, which is the user's to write.

## Boundaries

- **ADR authoring format and the `/add-adr` template** → documentation, when the documentation pack is installed. This skill owns lifecycle and the home.
- **A missing ADR for an architectural dependency** (KN-30) → `/setup-project-health` check 2, which must use the home this skill detects (IR-3). Without it, the row is `N/A (owner: /setup-project-health)`.
- **Decision index rows vs ADR files** → `knowledge-fact-scan` §5 (KN-13); this skill prints the counts in its ledger only.
- **An `ADR-NNNN` id with no file** → `knowledge-ref-scan` §4 (KN-04).
- **A decision the code contradicts at large** (a convention) → align `convention-oracle` AL-04 when the align pack is installed.

## Adapt to the codebase — the ADR lanes

| Lane | Where ADRs live | Status shape | Chosen-option truth | Trap |
|---|---|---|---|---|
| **MADR 3/4** | `docs/decisions/` | `status:` frontmatter or `## Status`; "Decision Outcome: Chosen option: …" | manifests and lockfile | a `Considered options` list names rejected packages on purpose (P-2) |
| **Nygard / adr-tools** | `doc/adr/` or `docs/adr/` | `## Status` heading, next line `Accepted` / `Superseded by [n]` | manifests | adr-tools writes "Superseded by" in the old ADR and "Supersedes" in the new: both ends exist when tooling was used |
| **Refract installs** | detected home; `ai/decisions/` holds the template | as the project writes it | manifests | installed commands may hard-code `ai/decisions/` (§0) |
| **Monorepo** | one home per repo, or per app (`apps/api/docs/adr`) | — | the manifest of the app the ADR governs | several homes: the most populated wins; the ledger lists all candidates |
| **Python / Go / Ruby / PHP / JVM** | same locations | same | `pyproject.toml`, `go.mod`, `Gemfile`, `composer.json` | framework words map to packages (Django → `django`, Rails → `rails`, Laravel → `laravel/framework`) |

## Pre-flight

Run as **one** bash script from the repo root. Step **N** feeds detector **§N**. Every `rg` names its path; any `rg` exit 2 is `blocked`.

```bash
[ -n "${BASH_VERSION:-}" ] || { echo "pre-flight: run it with bash (arrays and PIPESTATUS are bash-only)"; exit 2; }
KS="${KS:-.claude/skills}"        # installed engines; in the Refract repo itself: templates/packs/learning/skills
RUN="${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/knowledge.XXXXXX")}"; mkdir -p "$RUN"; echo "RUN=$RUN"
export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true

# 0-4. The engine: home detection, status parse in every shape above, reciprocity, current citations, chosen option.
python3 -I "$KS/decision-record-scan/scripts/adr-index.py" . > "$RUN/adr.tsv" 2> "$RUN/adr.ledger"
echo "adr-index exit $? (0 clean · 1 rows · 2 blocked)"; cat "$RUN/adr.ledger"; cut -f1-7 "$RUN/adr.tsv"
python3 -I "$KS/decision-record-scan/scripts/adr-index.py" . --list > "$RUN/adr-list.tsv"      # id, file, status, superseded-by, supersedes
HOME_DIR=$(awk -F'\t' 'NR==2{print $2}' "$RUN/adr-list.tsv" | sed 's#/[^/]*$##'); echo "ADR home: ${HOME_DIR:-none}"

# Cross-checks.
if [ -n "$HOME_DIR" ]; then
  # 1. Status lines in every shape: the count must equal the engine's parsed statuses.
  rg -c -i --pcre2 '^\s*(?:[-*]\s*)?\**Status\**\s*:|^#{1,4}\s*Status\s*$|[·|]\s*\**Status\**\s*:' -g '[0-9]*.md' "$HOME_DIR" | wc -l; echo "rg 1 exit ${PIPESTATUS[0]}"
  # 2. Supersede wording: every hit is an end of a pair the engine checks both ways.
  rg -n -i 'supersed' -g '[0-9]*.md' "$HOME_DIR" > "$RUN/g2.txt"; echo "rg 2 exit $? ($(wc -l < "$RUN/g2.txt" | tr -d ' ') lines)"
fi
# 0. Installed artifacts that name ai/decisions/ (the engine groups them into one root-cause row).
[ -d .claude ] && { rg -l '(^|[^/\w])ai/decisions/' -g '*.md' .claude > "$RUN/g0.txt"; echo "rg 0 exit $? ($(wc -l < "$RUN/g0.txt" | tr -d ' ') files)"; }
```

Read the ledger first: the home and how it was chosen (declared by an index, or most `NNNN-*.md`), every candidate directory with its count, the status histogram, and the index's row count against the file count.

**Measured** (2026-10-19), read-only on a real NestJS + React monorepo (0.75 s; 0 files written): home `docs/decisions` (declared in `ai/_decision-index.md`), 40 ADRs — 37 accepted, 2 superseded, 1 retired, every status parsed (rg 1: 40 status lines). Rows:
- §0: **1 root-cause row, 49 sites** — installed agents, commands, skills and rules that read or write `ai/decisions/` (rg 0: 50 files under `.claude/`; the engine also reads `CLAUDE.md` and `AGENTS.md` and drops lines that name the home too), and the second directory itself (README + template, 0 ADRs).
- §2: ADR-0028 "Supersedes: the chrome clause of [0016]" while 0016 stays Accepted — a partial supersede, Unconfirmed, fix `Amended by` (P-29). 0001 → 0014 links both ways: quiet (the decoy).
- §3: 0. A first cut flagged a runbook citing `ai/audits/2026-10-13-order-variant-matching.md` as ADR-0013 (retired): a dated file name, not an ADR citation (P-30).
- §4: 0 — every chosen package of an Accepted ADR is in a manifest.
- Index: 33 ids cited against 40 files (graded by `knowledge-fact-scan` §5).
- On `benchmarks/fixtures/*`: one tree has an ADR directory (`infra-ops`, `iac/docs/adr/`, 1 ADR whose status is written mid-line, `Date: … · Status: accepted`): 0 rows after the parser learned that shape (the first run printed "status missing"). The other 23 print `N/A (no ADR directory)`. The self-test seeds 7 rows (a second ADR directory, a command hard-coding it, a status-less ADR, a superseding ADR with no back link, an ADR another one supersedes still Accepted, a superseded ADR cited as current, an Accepted ADR choosing `axios` with only `fastify` in the manifest) and 5 decoys (history-marked citations, a dated file name, a reciprocal pair, a rejected option, a partial supersede reported as Unconfirmed).
- On `stale-knowledge` (the seeded fixture; home `docs/decisions` declared by its index, 8 ADRs — 6 accepted, 2 superseded): 5 rows, **5 of 5 seeds** — a superseding ADR that never names its predecessor, an Accepted Express ADR on a Fastify API (Unconfirmed), a superseded ADR cited as current in `CLAUDE.md`, the installed curator and `/promote-decision` writing to `ai/decisions/` (one row, 2 sites), and that second directory. Decoys: 0 of 26 (a reciprocal pair, a rejected option). The ledger counts both index id forms (`6 ids cited vs 8 files` for an index of `ADR-NNNN` rows).

## The 3,000-hit path

ADR sets are small; the volume is in §0 and §3 citations across installed artifacts.

1. **Group §0 by root cause**: the consumers are one finding — the home is hard-coded — fixed once in the pack sources (IR-3), not per file.
2. **Rank §3 by load**: citations in files loaded every session first.
3. **Read every §2 pair**: both files, whole header.
4. **Ledger the rest** as `Live, unreviewed (k sites)` with `adr-index.py . --classes=3`.

## Scans for

| § | Class | Default |
|---|---|---|
| 0 | KN-29 wrong ADR home: a second ADR directory, consumers reading it | M; H when a file loaded every session names it |
| 1 | KN-28 status missing or not a lifecycle word | L |
| 2 | KN-28 supersede link one-way; Superseded with no successor; partial supersede unmarked | M; L (Unconfirmed) when partial |
| 3 | KN-28 superseded or retired ADR cited as current | M; H in a file loaded every session |
| 4 | KN-28 Accepted ADR whose chosen package is in no manifest | M, Unconfirmed |

### 0. Wrong ADR home (KN-29)

```
BAD:   docs/decisions/ holds 0001–0040; ai/decisions/ holds README + _template; /promote-decision writes `ai/decisions/<NNNN>-<slug>.md`
GOOD:  one home; ai/decisions/README.md points at it; tooling reads the home this script detects
```
**Read the code:** Does an index or README declare the home? Do the installed consumers read the directory literally or resolve it? **Finding when** ADRs live in one directory and installed tooling reads or writes another, or a second directory starts beside the home. **Proof:** tier S + V505 — the listing of both directories and the consumer lines; after the fix the consumers resolve the detected home and `/setup-project-health` check 2 counts the real ADRs.

### 1. Status not machine-readable (KN-28)

```
BAD:   # 6. No status — "We decided things."
GOOD:  Status: Accepted · - **Status:** Superseded by [0014](0014-….md) · Date: 2026-09-28 · Status: accepted · ## Status / Accepted
```
**Read the code:** Is the status written in prose the parser missed (then extend the parser with the shape, and record it)? **Finding when** no status line exists, or its word is not a lifecycle word. **Proof:** tier S — `adr-index.py . --list` shows the status after the fix.

### 2. One-way supersede link (KN-28)

```
BAD:   0001: "Superseded by 0003"; 0003 never mentions 0001 · 0008 "supersedes ADR-0007"; 0007 still Accepted
GOOD:  0001 ↔ 0014 both ways · "Supersedes: the chrome clause of [0016]" → 0016 marked Amended by 0028 (P-29)
```
**Read the code:** Is the supersede total or partial? Did tooling write one end only? **Finding when** one ADR names another as successor or predecessor and the other does not answer. **Proof:** tier S + V504 — both headers quoted; after the fix each names the other.

### 3. Superseded ADR cited as current (KN-28)

```
BAD:   CLAUDE.md: "HTTP follows ADR-0001."        (0001 superseded by 0014)
GOOD:  "Old HTTP was ADR-0001, replaced by ADR-0003" (P-14) · "ADR-0004 → ADR-0005" · `2026-10-13-x.md` (a date, P-30)
```
**Read the code:** Does the citing line also name the successor or mark history? Is the citing file loaded every session? **Finding when** a live line outside the ADR home and the index cites a superseded, deprecated or retired ADR as if it holds. **Proof:** tier S + V505 — the citation re-pointed to the successor; the engine is quiet on that line.

### 4. Chosen option absent (KN-28)

```
BAD:   0002 (Accepted): "We use `axios` for HTTP" — no manifest declares axios
GOOD:  a rejected option in "Considered options" (P-2) · a superseded ADR's choice (not checked)
```
**Read the code:** Was the decision reversed in code (a new ADR is due), not built yet (it is Proposed), or does the package live in another app's manifest? **Finding when** an Accepted ADR's chosen package is in no manifest or lockfile of the repo. Unconfirmed always: a process decision may name no package. **Proof:** V506 — the package present, or the ADR's status corrected by its owner.

## Proof

Oracles: [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Learning — V504 (reciprocal link both ways), V505 (home detected and the citation re-pointed), V506 (chosen option present). `adr-index.py . --only=<file>:<line>` fires before the edit and is quiet after it; `--list` is the before/after status table.

## Output

```
decision-record-scan — home docs/decisions (declared in ai/_decision-index.md) · 40 ADRs: accepted 37, superseded 2, retired 1

1. .claude/agents/api-architect.md:56 (+48 installed artifacts)                    [report-with-fix]   high
   §0 KN-29 — read or write ai/decisions/ while the ADRs live in docs/decisions; ai/decisions/ holds README + _template.
   Fix: the pack sources resolve the home (IR-3), ai/decisions/README.md points at docs/decisions/. One root cause, 49 sites.
2. docs/decisions/0016-one-tab-strip.md:3                                          [report-flagged]    low
   §2 KN-28 — ADR-0028 supersedes "the chrome clause" of 0016; 0016 has no back link. Fix: `Amended by ADR-0028`.

Verification: 3 candidates → 2 findings · 1 unconfirmed · 0 hardening · 0 pre-existing · 0 refuted

Class coverage:
  §0  KN-29 ADR home             checked (1 home, 1 second directory, 49 consumer sites → 2 rows)
  §1  KN-28 status               checked (40 parsed → 0)
  §2  KN-28 supersede links      checked (3 supersede pairs → 1 unconfirmed)
  §3  KN-28 cited as current     checked (3 dead ADRs → 0)
  §4  KN-28 chosen option        checked (37 accepted → 0)
```

`[report-with-fix]`: both ends quoted and the edit adds a link, re-points a citation or moves tooling to the home. `[report-flagged]`: partial supersede, or a chosen option that may be unbuilt. The coverage block lists **all five** classes on every run: `checked`, `N/A (no ADR directory)`, or `blocked (<reason>)`.

## False positives / precedents

The verifier reads [`precedents/learning.md`](../../../../snippets/precedents/learning.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. The ones this skill meets most: § 2 considered options, § 3 ADR Context sections, § 7 Proposed decisions, § 14 history-marked citations, § 29 partial supersede, § 30 dated file names.

## When to run

- On any diff that adds, edits or renames an ADR, edits the decision index, or edits a file that cites an ADR: the `/audit-knowledge` dispatch signal.
- Before `/promote-decision` writes an ADR: the home comes from this script, never a hard-coded directory.
- On every whole-repo `/audit-knowledge`, reporting all five classes.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 10, with [`precedents/learning.md`](../../../../snippets/precedents/learning.md)). Under `/audit-knowledge` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Never delete or rewrite an ADR's decision to close a row; never write a superseding ADR on the user's behalf.
- Never report §4 as a Finding: a chosen package that is absent is a question for the ADR's owner.
- Never write into the scanned repository; never print "decisions consistent" without the coverage block.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `scripts/adr-index.py` (this skill): §0–§4, `--home`, `--list`, `--only`, `--classes`, `--self-test`; imports `kn_common.py` from the knowledge-ref-scan skill (its scripts directory) (`adr_home`, `adr_ids`, manifests). Stdlib only, `python3 -I` safe; nothing is written under the scanned root.
- `knowledge-fact-scan` §5 (index rows), `knowledge-ref-scan` §4 (ids with no file), `/setup-project-health` check 2 (missing ADRs). `/audit-knowledge` dispatches this skill; `/refresh-knowledge --from-audit` closes rows; `/promote-decision` reads the home from it.
- documentation `/add-adr` (when installed) owns the ADR template.
