---
name: align-detect
description: "Align's class ledger and dispatcher: runs the four align detectors and every installed owner detector, maps legacy classes to AL ids, reduces, never halts."
kind: skill
pack: align
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: align-detect

## Premise

Align owns one question: **the project declares a convention, and a live site does not follow it.** This skill is the ledger of that question. It holds the 34 align classes AL-01…AL-34 (the batch-6 align eval § 2), says which detector owns each one and which command closes it, and dispatches the detectors. It detects nothing by itself: every candidate row comes from a detector skill's pre-flight output, and every row cites the oracle that declares the convention.

It replaces the old `detect-drift` skill. That skill ran eleven "universal detectors" inline, including SOLID, complexity, N+1, SQL-injection and secret greps that the code-quality, security, performance and database packs now own with bar-grade detectors and failing-first proofs. It also halted when `_extracted-idioms.md` was absent, which halted it on the pack's own `web-dashboard` fixture. The name changed because the learning pack ships a `/detect-drift` command and Claude Code resolves a skill and a command of one name to **the skill** (§ Notes). With both packs installed, the old name hid the learning command.

**The rule of the ledger.** A row exists only when:
- a detector's pre-flight produced it, with the site `<file:line>`;
- it carries `oracle:` (rule id at `error` in the resolved config, or a doc `path:line` with its quote) that survives `convention-oracle` §1 (V389);
- the class is align-owned, or the class's owner said the closure is an align EQ swap.

Everything else is a routed line naming its owner, or a reduction line naming what did not run. A row derived from what "this codebase probably has" is fabrication.

## The class ledger — owner, detector, closer

The verifier, the validator and every align command read this table. "Detector" is what this skill dispatches; "Closer" is the command that fixes a confirmed row.

| AL | Class | Detector (dispatched) | Owner | Closer |
|---|---|---|---|---|
| 01 | Invented convention (no oracle) | `convention-oracle` §1, on every row from every detector | align | drop and count |
| 02 | Split with no declared winner | `convention-oracle` §2 | align | human ratifies → `/setup-project --refine` |
| 03 | Declared but unenforced | `convention-oracle` §3 | align | ratchet enablement (V395) |
| 04 | Doc contradicts current code | `convention-oracle` §4 | align | doc update (human) |
| 05 | Literal = a token's value | ui-ux `design-token-audit` §1, §3, §10 | ui-ux | align EQ `replace-with-shared` |
| 06 | Literal with only a nearest token | ui-ux `design-token-audit` swap trap | ui-ux | VC with approval (V407), or `/polish` |
| 07 | Tailwind arbitrary or default palette | ui-ux `design-token-audit` §2, §8 | ui-ux | align if EQ, else `/polish` |
| 08 | Primitive tier where semantic is mandated | ui-ux `design-token-audit` §8 (partial) | ui-ux | align when one semantic candidate exists |
| 09 | Deprecated token or DS component | ui-ux `design-token-audit` §7 | ui-ux | align if the replacement is EQ; `/upgrade-dep` for a bump |
| 10 | Escape hatch over a DS component | ui-ux `design-token-audit` §3, §5 | ui-ux | report-flagged |
| 11 | Raw primitive where a wrapper exists | `wrapper-adoption-scan` §1 | align | align `replace-with-shared` |
| 12 | Native element where a DS component exists | ui-ux `design-token-audit` §6 | ui-ux | align EQ, or `/unify-surfaces` (wrapper gap) |
| 13 | Copy of a named helper | `wrapper-adoption-scan` §2 | align | `dedupe` after V403; diverged → `/quality-fix` |
| 14 | Deep import past a public entry | `wrapper-adoption-scan` §3 | align | align |
| 15 | Wrapper without a required prop or gate | `wrapper-adoption-scan` §4 | align | align (`add-gate` with the declared gate) |
| 16 | File or directory name | `naming-layout-scan` §1 | align | align `rename` (git mv) |
| 17 | Identifier name | `naming-layout-scan` §2 | align | align `rename` (language server) |
| 18 | Synonym against the glossary | `naming-layout-scan` §3 | align | align `rename` (internal names only) |
| 19 | Placement and module skeleton | `naming-layout-scan` §4 | align | align (move) |
| 20 | Layer direction | code-quality `architectural-diagnosis` §1 | code-quality | align re-route through a named public surface; rework → `/optimize` |
| 21 | Cross-module private import | code-quality `architectural-diagnosis` §1–§2 | code-quality | as AL-20 |
| 22 | Forbidden or non-allowlisted library | `wrapper-adoption-scan` §5 | align | align |
| 23 | Envelope or error shape vs a declared contract | backend `edge-error-scan` §6–§7 | backend | `/backend-fix`; none declared → `/polish` |
| 24 | Field or path casing | backend `api-consistency-audit` §3, §3b | backend | `/polish` |
| 25 | Pagination style | backend `api-consistency-audit` §4 | backend | `/polish` |
| 26 | Hard-coded user-visible string | frontend `i18n-scan` §1 | frontend | align only for an EQ key (precedents § 31); else `/frontend-fix` |
| 27 | Key namespace, missing or unused keys | frontend `i18n-scan` §2 | frontend | `/frontend-fix` |
| 28 | Dropped a11y convention | frontend `a11y-code-scan` | frontend | align in the AL-15 form; else `/frontend-fix` |
| 29 | Suppression dodging a convention rule | `convention-ratchet-scan` §1 | align | align `remove` + fix, or a reasoned exception |
| 30 | Ratchet regression | `convention-ratchet-scan` §2 | align | revert the growth |
| 31 | Per-package config drift | `convention-ratchet-scan` §3 | align | config edit (heavy tier) |
| 32 | Half-finished declared migration | `convention-ratchet-scan` §4 | align | align, ratcheted |
| 33 | One pattern resolved two ways in a sweep | `find-and-align`'s `align-sweep-gate.py consistency` | align | blocks the fix run |
| 34 | Out-of-scope edit in an align commit | `align-sweep-gate.py scope`, `lock-paths` | align | blocks the row |

AL-33 and AL-34 exist only on a fix run, so a detect run prints them `N/A (detect run — checked by align-sweep-gate.py on the fix)`.

**Owner rows.** A pack that owns a class grades it; align never grades it in the owner's place. When the owner pack is installed, its detector's coverage line is folded in as-is, and its Findings enter the ledger as `routed (<closer>)` rows. Align takes the closure only where the Closer column says align **and** the owner marked the row EQ with a T1/T2 oracle. Without the owner pack, the class prints `N/A (owner pack <x> not installed)`. Code-quality and security are always installed (`_registry.md`); ui-ux, frontend, backend, performance and database are not.

## The legacy class map

Ledgers, `/align-scan` reports and `validate-align-artifacts.sh` written before the AL ids carry the old class names. Read them as follows; a new row carries both `al_class:` and the legacy `class:` until the validator reads AL ids (eval item 22).

| Legacy `class` / `subclass` | Now |
|---|---|
| `reinvented-wrapper`, `raw-library-component` | AL-11; a native element → AL-12 (ui-ux) |
| `drift` | the AL id of the rule it cites: AL-14, AL-16–19 or AL-22 (`align-sweep-gate.py` reads an unmapped `drift` row as AL-16) |
| `stack-specific` / `design-token-drift` | AL-05; AL-06 when the swap is not EQ |
| `i18n-key-drift` | AL-26; catalog defects AL-27 |
| `permission-gate-drop`, `default-true-prop` | AL-15 |
| `a11y-violation` | AL-28 (frontend) |
| `missing-ui-state`, `motion-drift`, `responsive-drift`, `lifecycle-hook-wrong` | not align classes: ui-ux `ui-state-scan` and `motion-audit`, frontend. A site that bypasses a **declared** state or fetch wrapper is AL-11 |
| `duplicated-logic` | AL-13 when the canonical copy is a named helper; otherwise code-quality `duplication-scan` |
| `silent-catch`, `unhandled-io` | code-quality `error-handling-scan` §1–§4 → `/quality-fix` |
| `dead-code`, `over-abstraction`, `solid-violation`, `clean-code` | code-quality (`dead-code-scan`, `architectural-diagnosis`) → `/quality-fix`, `/refactor`, `/optimize`. A naming sub-row whose pattern the oracle declares is AL-17 |
| `performance` | performance / database packs → `/perf-fix`, `/db-fix` |
| `security` | security pack → `/security-fix` |
| `duplicated-surface-styles` | **not a class**: no enum ever held it and no detector emits it. A row carrying it is re-read as AL-11 or AL-12, or routed to `/unify-surfaces` |

## Inputs

| Input | Source | Missing → |
|---|---|---|
| Codebase root(s) | caller | — |
| The oracle map | `convention-oracle` § 0: `oracle-map.py <root> --out=$RUN/oracle` | `blocked (oracle-map.py failed)` for every align class; the run still dispatches owners |
| The wrapper and helper inventory, `PROJECT_KIND` | **fallback order:** `.claude/_extracted-idioms.md` → `.claude/codebase-profile.md` → `ai/conventions.md` (+ `ai/architecture.md`, `ai/modules.md`). The first that exists is read; `oracle-map.py` tags codebase-profile and `_extracted-*` lines T2g | none of the three and no T1 rule → every align class `N/A (no declared convention)`; never a halt |
| Scope | caller: whole repo, `--changed <base>` (diff run), or a path | whole repo |
| `--with-owners` | caller | the legacy non-AL classes print owner lines only (§ Dispatch) |
| `--max-findings-per-class` | caller | unlimited; rows past the cap return as `deferred` for the caller to write to `ai/align/_deferred.md` |

`PROJECT_KIND` comes from `_extracted-codebase.md § Gold standards`, then the `PROJECT_KIND:` line of `codebase-profile.md`. Otherwise it is inferred from the manifests and printed `PROJECT_KIND inferred (<evidence>)`. An unknown kind narrows the owner set, never the align set.

## Dispatch

**Whole-repo run.**
1. Build the oracle map once (`convention-oracle` § 0) and pass `$RUN/oracle` to every detector.
2. Dispatch the four align detectors, `convention-oracle` (§1–§4), `wrapper-adoption-scan`, `naming-layout-scan` and `convention-ratchet-scan`, in parallel, up to `--max-subagents` (default 5).
3. Dispatch every installed owner detector for an AL class: `design-token-audit` (ui-ux), `architectural-diagnosis` §1–§2 (code-quality), `duplication-scan` §1 for AL-13 divergence (code-quality), `i18n-scan` §1–§2 and `a11y-code-scan` (frontend), `edge-error-scan` §6–§7 and `api-consistency-audit` §1–§4 (backend).
4. Run `convention-oracle` §1 (`oracle-map.py quotes`) over every candidate from every detector. A row whose quote does not resolve is dropped and counted (`AL-01: k candidate rows dropped`).

**The legacy non-AL classes** (silent-catch, unhandled-io, dead code, duplicated logic, SOLID, clean code, performance, security) are never grepped here. Each prints one owner line naming the owner's audit, which runs those detectors under its own verification:
- `owner: code-quality → /quality-audit (error-handling-scan, dead-code-scan, duplication-scan, architectural-diagnosis)`;
- `owner: security → /security-audit`;
- `owner: performance → /perf-audit` and `owner: database → /db-audit`, each followed by `(owner pack <x> not installed)` when absent.

With `--with-owners`, this skill dispatches those owner skills too and folds their Findings in as `routed (<fix command>)` rows. The closure stays with the owner's fix command. The one carve-out (eval O-3, proposed) applies when the performance or database pack is absent: an idiom the oracle already names (a declared batch loader, a declared cache wrapper) may be applied by align. Only with a baseline **measured** by a test, never an annotation in `notes`.

**Diff run** (`--changed <base>`): dispatch by signal, and print every detector not dispatched as `N/A (no signal in the diff)`.

| The diff touches | Dispatch |
|---|---|
| an import, `require`, a package `exports` map | `wrapper-adoption-scan` §1, §3, §5; `convention-ratchet-scan` §1 |
| a JSX/template element of a declared wrapper, a helper definition | `wrapper-adoption-scan` §2, §4 |
| a new, renamed or moved file or directory; a new identifier | `naming-layout-scan` §1–§4 |
| a lint config, a baseline file, a suppression comment | `convention-ratchet-scan` §1–§3; `convention-oracle` §3 |
| `ai/conventions.md`, an ADR, the glossary, `ai/modules.md` | `convention-oracle` §2–§4 |
| a style, token or class string | `design-token-audit` (ui-ux, when installed) |
| user-visible copy or a catalog | `i18n-scan` §1–§2 (frontend, when installed) |
| an API handler, filter or DTO | `edge-error-scan` §6–§7, `api-consistency-audit` (backend, when installed) |

## Pre-flight

One script per run, from the audited repo's root. It writes only under `$RUN` (`mktemp -d` under `$TMPDIR`) and runs git reads with `GIT_OPTIONAL_LOCKS=0`. It resolves the inputs and prints which detectors and owners exist; the detectors' own pre-flights do the grepping.

```bash
RUN=${RUN:-$(mktemp -d "${TMPDIR:-/tmp}/align-detect.XXXXXX")}; export GIT_OPTIONAL_LOCKS=0 DO_NOT_TRACK=1 CI=true
P=${PACKS:-.claude/skills}                                     # installed skills; a pack checkout passes its templates/packs/*/skills
INV=none; for f in .claude/_extracted-idioms.md .claude/codebase-profile.md ai/conventions.md; do [ -s "$f" ] && { INV=$f; break; }; done; echo "inventory: $INV"
K=$(grep -h '^PROJECT_KIND:' .claude/_extracted-codebase.md .claude/codebase-profile.md 2>/dev/null | head -1); echo "${K:-PROJECT_KIND: inferred}"
OM=$(find "$P" -path '*/convention-oracle/scripts/oracle-map.py' 2>/dev/null | head -1)
[ -n "$OM" ] && python3 -I "$OM" . --out="$RUN/oracle" --age-buckets || echo "blocked (oracle-map.py not found under $P)"
for s in convention-oracle wrapper-adoption-scan naming-layout-scan convention-ratchet-scan design-token-audit architectural-diagnosis \
         duplication-scan i18n-scan a11y-code-scan edge-error-scan api-consistency-audit; do
  [ -n "$(find "$P" -path "*/$s/SKILL.md" 2>/dev/null | head -1)" ] && echo "detector: $s" || echo "absent: $s"; done
```

**Measured** 2026-10-18, `oracle-map.py` on the four fixtures this batch names:
- `web-dashboard`: no lint config, so T1 is 0. T2 14 rows from `ai/conventions.md`, T2g 4 rows from `.claude/codebase-profile.md`. No `_extracted-idioms.md`, so the inventory falls back to `.claude/codebase-profile.md`. The old skill halted here.
- `quality-mix`: T1 7 · T1-warn 1 · T1-noci 2 · T2 9, from ESLint, `tsc`, Ruff and depcruise. The depcruise rules are T1-noci because no CI job runs depcruise. 5 ban rows, and 4 `static!=resolved` gates for unexpanded ESLint presets. No inventory file at all (`inventory: none`), so the T1 rows and `ai/architecture.md` are the whole oracle.
- `a11y-states`: T1 2 (`tsc`), no docs, so every doc-oracle align class is `N/A (no declared convention)`.
- `frontend-correctness`: T1 2, T2g 1.

Dispatched on them, `wrapper-adoption-scan` produced 1 AL-11 and 2 AL-15 candidates on `web-dashboard` (WEB-IMPORT-01, WEB-PERM-01 and its icon-button twin). On `quality-mix` it produced 1 AL-22 candidate routed to code-quality as a layer contract (QM-AR-03), and 2 AL-13 copies routed as diverged (QM-DU-01, QM-DU-02). Nothing on the other two. The other `web-dashboard` seeds are owner rows: tokens (ui-ux), i18n and a11y (frontend), the layer import (code-quality), and the silent catch and unhandled I/O (code-quality via `/quality-audit`).

## The 3,000-hit path

Each detector triages its own hits (its § The 3,000-hit path). Across detectors this skill does three things:
1. **Dedupe by `file:line`.** An align row and an owner row on one site become one row: the owner's class, with the align detector listed as corroboration.
2. **Collapse T2g.** Every row under an unratified generated rule becomes one ratification line per rule, never N rows (precedents § 28).
3. **Group by the V393 key** (rule, normalised before-value), so `/align-plan` phases a group as one decision.

What remains unread is reported per class as `Live, unreviewed (k groups / n hits)`, or `Live, ratcheted` where a shrink-only baseline holds it. It is never `checked`.

## Output

One row per site, in the ledger's `- id:` form (the caller assigns `A<NNN>`):

```yaml
- id: A___
  al_class: AL-11
  class: reinvented-wrapper                 # legacy name, kept until the validator reads AL ids
  oracle: 'ai/conventions.md:19 "`src/lib/api-client.ts` is the only module permitted to construct an HTTP request."'
  oracle_tier: T2
  owner: align                              # or code-quality | ui-ux | frontend | backend | security | performance | database
  evidence: [src/components/billing/InvoiceDrawer.tsx:16]
  scope: [src/components/billing/InvoiceDrawer.tsx]
  closure_verb: replace-with-shared
  shared_equivalent: src/lib/api-client.ts
  proof_class: EQ                           # EQ | VC | FN — find-and-align L1 re-derives it
  detector: wrapper-adoption-scan §1
  detector_cmd: "<the exact grep line, narrowed to this rule>"
  routed: ""                                # or the closer command for an owner row
  tier: standard
  status: detected
```

The run ends with the class coverage ledger — all 34 classes, every run — and two denominators:

```
Class coverage (AL ledger):
  AL-01 invented            checked (14 candidates → 1 dropped)
  AL-02 split               checked (3 concerns → 1 proposed canonical, 2 undetermined; 0 rows)
  AL-05 token = value       routed (ui-ux design-token-audit: 1 EQ → align closer)
  AL-06 nearest token       routed (ui-ux: 1 report-flagged — 13px, cross-family match --font-size-sm)
  AL-11 raw primitive       checked (4 hits → 1 candidate)
  AL-13 helper copy         N/A (no named helper in the inventory)
  AL-15 prop / gate         checked (2 hits → 2 candidates)
  AL-20 layer direction     routed (code-quality architectural-diagnosis §1: 1)
  AL-23 envelope            N/A (owner pack backend not installed)
  AL-26 hard-coded copy     routed (frontend i18n-scan §1: 1 EQ key → align closer)
  AL-30 ratchet regression  N/A (no baseline file)
  AL-33 / AL-34 sweep       N/A (detect run — checked by align-sweep-gate.py on the fix)
  … every other AL row, each with checked / N/A / blocked / Live, unreviewed / Live, ratcheted
Owners (legacy non-AL classes): code-quality → /quality-audit · security → /security-audit · performance, database: not installed
Detector: reinvented-wrapper — AL-11 checked, AL-12 routed (ui-ux)
Detector: security — owner: security (/security-audit); not run by align
RAN 4 of 4 align detectors · OWNERS — RAN 3 of 5 installed owner detectors (backend, database not installed)
```

The `Detector: <legacy name>` lines (one per legacy class) serve the validator's scan-evidence check until it reads AL ids. A run whose align or owner denominator falls short lists each reason on the next lines.

**The split special case.** "Half our modules do X and half do Y" is AL-02, never drift. `convention-oracle` §2 prints the BIMODAL block with `proposed canonical: <shape> (k/n, newest 20 files m/20) — ratify?` at or above the floor (≥ 30 sites and ≥ 0.75 share), or `undetermined — ask` below it. It writes **0 ledger rows**. Routes: ratify through `/setup-project --refine`, after which the sites become rows on the next run; or `/polish` if neither shape is right. A category under `## Unsettled conventions` or `[CONTESTED: …]` lands here even when a generated line names a side (precedents § 29).

## Reductions — never halts

A detector that did not run and a detector that found nothing both produce zero rows, and only one of them is good news. So every missing input is a **reduction** with a printed line, and the run continues:

| Condition | Effect | Line |
|---|---|---|
| No `_extracted-idioms.md` | inventory from the next source in the fallback order | `inventory: .claude/codebase-profile.md (T2g)` |
| No inventory, no doc, no T1 rule | align classes have no oracle | `AL-<n> N/A (no declared convention)` per class |
| An owner pack not installed | its classes do not run | `AL-<n> N/A (owner pack <x> not installed)` |
| A tool absent (eslint, ruff, depcruise, ast-grep, ls-lint) | that lane falls back to its grep | `blocked (<tool> not installed) — grep fallback` on the lane |
| An `rg` exit 2, a PCRE2 compile error | that grep is not evidence | `AL-<n> blocked (rg exit 2: <grep id>)` |
| A rule matched 0 files (V399) | that rule proves nothing | `AL-<n> NOT RUN (rule matched 0 files: <rule>)` |
| TypeScript 7 with no `@typescript/typescript6` alias | typed lanes off | `AL-17 typed lane NOT RUN (TS 7, no programmatic API)` |
| `--changed` or a path narrowed the run | fewer detectors | `SCOPED — <n> of 34 classes, scope <path>` |
| No git history, or a single commit | age buckets off | `history-blind (<reason>)` on AL-02, AL-04, AL-30, AL-32 |

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under `/align-scan` that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on a row without `oracle:` that resolves: it is dropped and counted as AL-01, never emitted.
- Halt on a row whose evidence does not resolve at HEAD: drop it and log it as a detector error.
- Halt on a hand-wave token in any row (`etc.`, `~N`, `several`): the detector is mis-configured.
- Halt on any write outside `$RUN`. This skill never touches source, the ledger or an oracle file.
- Never grep a class another pack owns (security, performance, database, error handling, SOLID, complexity). Dispatch its owner or print its owner line.

## Hard rules

- **A row is a site a detector found, with an oracle that resolves.** One site, one row. Never `~8 raw imports`.
- **Class before verb.** The class comes from the detector and the ledger table; the verb comes from the class. A verb chosen to make a row closable is how a security row acquired a structural verb in the old skill.
- **Never invent an oracle or an idiom.** `shared_equivalent` names a wrapper an oracle row declares. A needed primitive that no oracle names is a missing-idiom halt for that row (`/setup-project --refine`). A capability the wrapper lacks is a gap for `/unify-surfaces`.
- **Report every denominator.** All 34 AL rows, the align denominator, the owner denominator.

## Notes

- **The rename** (owner decision O-1, settled 2026-10-18). The Claude Code skills docs (`code.claude.com/docs/en/skills`, fetched 2026-10-18) say that `.claude/commands/<name>.md` and `.claude/skills/<name>/SKILL.md` both create `/<name>`. Their "resolve skills that share a name" table rules: a skill and a file in `.claude/commands/`, **the skill** wins.
  - The learning pack is always installed and ships `/detect-drift` (a read-only conventions-vs-code report).
  - Align is opt-in and shipped a skill of the same name. With align installed, the user's `/detect-drift` ran align's dispatcher instead.
  - `scripts/lint-description-budget.sh` already lists one entry per name for the same reason. The security pack's `threat-model` skill hid its `/threat-model` command the same way and was renamed `threat-model-method` (2026-10-18).
- Idempotent: two runs on one tree give the same rows. Each detector reads ≤ 5K tokens of shared context; its source reads are scoped to the file it is inspecting.

## Related

- `convention-oracle`, `wrapper-adoption-scan`, `naming-layout-scan`, `convention-ratchet-scan` (this pack): the four align detectors.
- `find-and-align` (this pack): closes a row through the proof ladder and `align-sweep-gate.py` (AL-33, AL-34).
- `/align-scan` (the audit), `/align-phase`, `/align-fast`, `/align-final --re-scan`: the callers.
- [`precedents/align.md`](../../../../snippets/precedents/align.md) and [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align (V389–V408).
- Learning `/detect-drift` (`convention-drift-detector`): the read-only conventions report. Integrator request IR-4 has it dispatch `convention-oracle` when align is installed.
