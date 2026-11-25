---
name: find-and-align
description: "Align's per-row fix as a proof ladder: route non-align rows, classify EQ/VC/FN, cheap diff gates, re-detect to zero, zero style diff or an approval."
kind: skill
pack: align
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: find-and-align

## Premise

**An align row is closed when the convention it cites now holds at every evidence line, nothing else in the commit changed, and the proof that fits its class says the behaviour is the same, or a named human approved the visible change.** A green build is not that proof. In the Patchwork study (arXiv 2607.08981, 2026-07), 97% of cross-file coherence failures in model-written code passed the type checker and 100% passed the tests. An alignment sweep is a cross-cutting task: one literal swapped to two different tokens in two files, an import reordered in an untouched function, a snapshot re-recorded so the swap "passes". Each hunk looks fine alone.

So this skill is a **ladder of deterministic gates run in cost order, before any reviewer reads the diff**. The first failure stops it. The gates are implemented once, in `scripts/align-sweep-gate.py` (this skill's folder). An LLM judge is advisory only: it can move a PASS to `pending-review`, never a FAIL to PASS (the script prints `judge-override-refused`).

Below, a spaced `§ n` is [`precedents/align.md`](../../../../snippets/precedents/align.md) § n, and V-numbers are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align.

This skill is the fix half of alignment. The detect half is `align-detect`, which dispatches the detectors whose rows arrive here.

## When to use

- Dispatched per row by `/align-phase` (serial) and `/align-fast` (waves), and by `/align --from-audit` for each row of an audit's `## What to do next`.
- Dispatched with `--dry-run` to run DETECT and DECIDE only.

## Inputs

| Input | Source | Required |
|---|---|---|
| The row | `ai/align/ledger.md`, `- id: A<NNN>` form: `al_class`, `oracle` (+ `oracle_tier`), `owner`, `evidence` (base line numbers), `scope`, `closure_verb`, `shared_equivalent` / `idiom_cited`, `proof_class`, `detector_cmd` (or `detector_re`), `detector_scope`, `canary`, `approval`, `tier`, `status` | yes |
| `$RUN` | the run folder (`mktemp -d` under `$TMPDIR`); nothing is written elsewhere except the fix itself and the ledger row | yes |
| Base ref | the commit before the row's first edit | yes |
| The oracle map | `convention-oracle` § 0 (`oracle-map.py --out=$RUN/oracle`) | yes, for L0 |
| `token-map.py` | the ui-ux `design-token-audit` skill's script, when the ui-ux pack is installed | token rows only; without it L8 is `NOT RUN (blocked: token-map.py absent)` and the row stays VC |
| Lint, type, build and test commands | `_extracted-idioms.md`, then `ai/stack.md`, then the manifests | yes for L9 |

## Step 1 — ROUTE: is this row align's to close?

Most of what a scan sees is owned elsewhere. Before any edit, the row goes to its owner's fix command when one of these holds. It moves to `routed (<command>)` with the audit id, and gets no commit here.

| The row is | Closed by |
|---|---|
| a security class (injection, XSS, secret, auth gate, tenant filter, validation) | `/security-fix`. The security pack is always installed, so align never closes it |
| a performance or query class (N+1, missing index, cache, sequential await) | `/perf-fix` or `/db-fix` when that pack is installed. Without it, the carve-out below |
| error handling (silent catch, unhandled I/O), dead code, a diverged copy (AL-13 diverged), SOLID or complexity | `/quality-fix` (code-quality is always installed) |
| new copy (AL-26 with no catalog value), catalog defects (AL-27), an a11y convention on a native element (AL-28) | `/frontend-fix` when the frontend pack is installed |
| an envelope or error shape against a **declared** contract (AL-23) | `/backend-fix`; no contract declared → `/polish` |
| casing or pagination uniformity (AL-24, AL-25), a token or state that does not exist yet | `/polish` |
| a wrapper gap: the raw primitive does something the wrapper does not expose (precedents § 9) | `/unify-surfaces` |
| a layer rework beyond a re-route through a named public surface (AL-20/21) | `/optimize` |
| a rename of a wire, DB, env or generated name (§ 15) | `/refactor` with an ADR |
| an oracle tagged T2g (generated) | `pending-ratification`: one probe per rule ("confirm `ai/conventions.md:<n>`"), never an edit (§ 28) |
| an idiom the fix needs that no oracle names | halt `missing-idiom` → `/setup-project --refine` |

**The carve-out** (eval O-3, proposed). A performance or database row whose fix applies an idiom the oracle already names (a declared batch loader, a declared cache wrapper) stays here only when the owning pack is absent. Its baseline must be **measured** by a failing-first test (a query-count scaling test, [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Query-count scaling), never a number in `notes`.

## Step 2 — DETECT: re-verify the row

1. Re-run the row's `detector_cmd` (or `detector_re`) on the current tree, scoped to its evidence files.
   - Every evidence line still matches → continue.
   - A line moved within the file → update the evidence and continue.
   - **0 hits, and the detector ran and matched files** (V399) → `archived-pre-existing` (aged out), with no commit. A detector that matched 0 files proves nothing: halt `re-detect-vacuous`.
   - A row the verifier refuted is not "aged out": it keeps its refuted bucket. `archived-pre-existing` means someone else fixed it.
2. Run the oracle check (L0 below) now, before any edit. A quote that no longer resolves halts `oracle-gone`: the convention changed under the row.

## Step 3 — DECIDE: classify the proof

Every row gets one `proof_class` (batch-6 eval § 3.2; `align-sweep-gate.py` re-derives it at L8):

| Swap | **EQ** — mechanical | Otherwise |
|---|---|---|
| literal → token | the literal's normalised value equals the token's resolved value **in every shipped theme**, within **one property family**, with **exactly one** semantic candidate: `token-map.py <root> --lookup=<value> --prop=<css prop> --site=<evidence file>` prints `EXACT … eq=yes` (without `--site` the lookup reads every package's tokens) | `NEAREST`, `xfam=` (another family) or several candidates → **AL-06, VC** (precedents § 7, § 27) |
| raw primitive → wrapper | the wrapper's defaults reproduce the raw call's props or options: a prop-diff table read from the wrapper's types, every row equal; the import resolves to the same module | **VC**, or a wrapper gap → `/unify-surfaces` |
| literal → `t('key')` | the literal equals an existing catalog value under the namespace the convention names, and the key resolves in every shipped locale (§ 31) | new copy → `/frontend-fix` |
| `rename` | not exported, or every consumer is in the repo; no wire, DB, env or generated name | contract change → `/refactor` + ADR |
| a functional verb that adds a declared idiom (`add-gate` with the declared `<Can>`) | **FN** — proven by a behaviour test (V401) | — |

Measured 2026-10-18 on `benchmarks/fixtures/web-dashboard`:
- `#d92d20` (`invoicelist.tsx:42`) looks up `EXACT --color-danger eq=yes` → EQ.
- `padding: '13px'` (`:39`) looks up `NEAREST --space-3=12px (1px)` with `xfam=--font-size-sm` → AL-06, VC. The answer key only asks `/align` to report it. Snapping it changes pixels, so it never closes without an approval.

Measured 2026-10-18 on a staged copy of `benchmarks/fixtures/convention-drift`:
- `align-sweep-gate.py --self-test --fix-runs=<fixture>/fix-runs` matches 14 of 14 seeded runs against their `.expect` (FAIL: run-01–04, 06, 08–12; PASS: run-05; PASS-flagged: run-06b with its approval; NOT RUN: run-07, the rule matching 0 files; pending-review: run-13), then the synthetic suite `29/29 OK`.
- The four EQ seeds look up `EXACT … eq=yes` only with `--site`: `#d92d20` at two component files → `--color-danger`, `8px` in both CSS modules → `--space-2`. Without `--site`, admin's `--color-error` and `--gap-sm` hold the same values, each lookup has two candidates, and it prints eq=no. `13px` (one component's font size) stays NEAREST with `xfam=--font-size-sm` → VC; `#1a73e9` NEAREST at 0.15 ΔE → VC.

Then dispatch **`@align-idiom-auditor`** against the plan: no new symbol unnamed in the oracle, every added functional block cites an idiom that resolves, no oracle file in the scope. A `HALT — idiom inventory gap` stops the row before any edit exists.

## Step 4 — FIX: apply the verb, rule first

- **Rule first where expressible** (eval § 3.3 L2). Write or extend an ESLint `no-restricted-imports` / `no-restricted-syntax` rule, or an ast-grep rule with `fix`. Give it BAD and GOOD cases (`RuleTester`; `sg test`, where Noisy and Missing must both be 0). Run it **from `$RUN`** on a 5–10% sample, read every diff, tune it, then sweep. Commit the rule only when the row's closure is "enable the rule". An ast-grep rewrite does not add the import: that is a second rule or the verb's import footprint.
- **Change only the matched expression.** The verb's footprint is the whole allowance:
  - `replace-with-shared`: the hit expression, plus one import added and one removed (a wrapper specifier merged into an import the file already has is that one added import);
  - `rename`: the declaration plus the references the language server reported;
  - `dedupe`: the copy deleted, plus one import.
  
  An explicit preservation instruction cut excess edits by about a third and *raised* the pass rate in "When Models Edit Too Much" (arXiv 2609.04061). The formatter owns formatting (§ 19).
- **The closed verb set.** The 21 verbs of `align-discipline.md` are the only closures. Structural verbs keep net lines ≤ 0 (the first `replace-with-shared` import is exempt). A functional verb's added block calls the idiom it cites. No new symbol that the oracle does not name.
- **Tests are read-only.** An align commit edits no test, snapshot, fixture, lint config for the class, or baseline file (V408). This replaces the old rule that let a security row update its test fixtures in the same commit: security rows are now `/security-fix`'s, with its own failing-first proof. In ImpossibleBench (arXiv 2510.20270), "modify the tests" was over 79% of one model's cheating; read-only tests close that path.
- Touch only files in `scope`. One row, one commit.

## Step 5 — VERIFY: the ladder

Run `align-sweep-gate.py` over the row's commit, then the steps the script does not cover. Stop at the first FAIL. `NOT RUN` never stops the ladder and never counts as PASS.

```bash
G=$(find .claude/skills -path '*/find-and-align/scripts/align-sweep-gate.py' 2>/dev/null | head -1)   # this skill's script
TM=$(find .claude/skills -name token-map.py -path '*design-token-audit*' 2>/dev/null | head -1)
GIT_OPTIONAL_LOCKS=0 TMPDIR="$RUN" python3 -I "$G" ladder --repo=. --base="$BASE" --ledger=ai/align/ledger.md \
  --oracle="$RUN/oracle" ${TM:+--tokens="$TM"} --run-json="$RUN/run.json" --json > "$RUN/ladder-$ID.json"; echo "exit $?"
# exit 0 PASS / PASS-flagged · 1 FAIL · 2 usage · 4 NOT RUN (no FAIL) or pending-review. The head tree is a copy under
# $TMPDIR (git archive), so the gate never writes the repo. `--all` runs every step instead of stopping at the first FAIL.
```

| Step | Check | Run by | FAIL when | V |
|---|---|---|---|---|
| L0 | the row's oracle resolves in base: the quote is found in the file, or the rule id is declared | script `oracle` | quote absent → AL-01, the row is dropped | V389 |
| L1 | the proof class: a VC row has `approval: <name>@<iso>` | script `approval` | VC with no approval → stop at `pending-approval` | V407 |
| L2 | rule first, with BAD/GOOD tests | this skill (Step 4) | `sg test` Noisy or Missing ≠ 0 | — |
| L3 | no whitespace-only, comment-only or token-identical file; no test, snapshot, fixture, lint-config, baseline or oracle file in the diff | script `diffkind`, `lock-paths` | any | V392, V408 |
| L4 | every removed line is an evidence line or verb footprint; every evidence line changed; no file outside `scope` | script `scope` | an out-of-scope hunk (AL-34), or an unchanged hit | V392 |
| L5 | the row's `detector_cmd` on the head copy: 0 at evidence lines, no new hit in touched files | script `redetect` | any | V391 |
| L6 | one way per pattern: hunks grouped by normalised before → after across the run | script `consistency` | a before-key with two afters (AL-33), unless they split by role (text vs border colour, padding vs gap) | V393 |
| L7 | every token, import path and export the diff introduced exists | script `names` | a hallucinated name (`var(--color-dangerous)`) | V398 |
| L8 | each literal → token pair round-trips per theme and family | script `roundtrip` (token-map.py) | an EQ row that does not round-trip → reclassify AL-06 | V397 |
| L9 | the class rule at error, lint, types, build, scoped tests | this skill | red | V402, V404 for rename / move |
| L10a | **EQ: zero computed-style diff per theme**, or zero compiled-CSS diff | this skill | any value change | V394, V396 |
| L10b | **VC: visual diff** per route × theme, approved | this skill | unapproved | V407 |
| L11 | baselines only shrink; no suppression added; no severity loosened | script `ratchet` | growth (AL-30) | V395 |
| L12 | test cases and assertions at head ≥ base; coverage not down (a drop > 5 pp is a hard fail); full suite + `smoke-verify` | script `lock-count` + this skill | red | V408 |
| L13 | each rule's scope matched ≥ 1 file, and the canary is flagged | script `vacuous` | 0 files → the class is `NOT RUN`, not clean | V399 |
| judge | an optional reviewer sees the diff, the oracle quote and the scope | `--judge` | can flip PASS → `pending-review`, never FAIL → PASS | — |

**L9 commands.** `tsc --noEmit --incremental false` (an incremental project would otherwise write `.tsbuildinfo`). ESLint and stylelint run with no `--cache`, Ruff with `--no-cache`. A TypeScript-7-only repo runs `tsc` 7 for types and prints typed lint `NOT RUN (TS 7, no programmatic API)`.

**L10a — EQ: zero computed-style diff per theme** (V394). Playwright `page.evaluate` dumps `getComputedStyle` for the changed elements' properties on every route that renders them, per shipped theme (light, dark, high-contrast), base build vs head build, on the **same host**. Playwright's screenshot names carry browser and OS, and its docs say to compare only where the baseline was made. Wait for `document.fonts.ready`, turn transitions off, and normalise colours through a canvas (`design-token-audit`'s `offToken` helper does this). Every value must be equal; one changed value makes the row VC. **Without a browser:** a zero compiled-CSS diff (V396): build base and head, minify both with one tool, resolve `var()` per theme, `diff`. **Without either harness:** L8 passing gives `[report-with-fix] (static EQ)`, and the runtime check stays Unconfirmed with its probe written out.

**L10b — VC: visual diff with a recorded approval** (V407). `toHaveScreenshot` with `maxDiffPixels: 0`, because Playwright's default `threshold` of 0.2 hides a 1-px snap. The baseline comes from the pre-rewrite commit, and the diff images stay in `$RUN/pw`. The ledger row carries `approval: <name>@<iso>`. **A visual diff is never auto-accepted**: not for a token swap, not with an allowance configured, never under `--safe-only`. An agent never fills `approval:`.

**Proof by verb** (eval § 3.3):

| Verb | Proof |
|---|---|
| `replace-with-shared` (token) | L8 + L10a |
| `replace-with-shared` (wrapper) | the prop-diff table + a render test of the site; L10a when the defaults reproduce the props, else L10b |
| `rename` | a language-server or ts-morph rename (ts-morph needs the TS 6 API through `@typescript/typescript6`, else `NOT RUN`); no serialised-name change (`oasdiff breaking` or a schema snapshot when an API is near); V402 |
| `dedupe` | a differential test of copy vs canonical on the copy's call-site inputs, then delete; knip or `dead-code-scan` shows no orphan; V403 |
| move / re-route | the whole-repo boundary tool is green on every module; V404 |
| `add-gate` (FN) | a render test as the role that must not see the action: it fails first, then passes; V401 |
| ratchet enablement | the class rule at error with a baseline generated **after** the fixes; L11 |

**Second idiom audit.** Dispatch `@align-idiom-auditor` against the diff that landed. A paper citation (an idiom named in `notes` with no matching import or call), a new public symbol, or an oracle file in the commit is a HALT: revert, do not amend.

## Step 6 — RECORD

- **fixed**: `status: fixed`, `fixed_at`, `commit` (one row, one commit, subject `align/<phase-N>/<id>: <description>`), `gaps_closed` = `len(evidence)`, `proof_class`, `proof:` (the V-numbers that passed and the ladder file `$RUN/ladder-<id>.json`), `approval:` for VC. A heavy-tier row pauses at `pending-review` for a named reviewer.
- **routed**: `status: routed`, `routed: <command> <audit id>`, no commit.
- **pending-approval** (VC, no approval) and **pending-ratification** (T2g oracle): no commit; the probe is written into the row.
- **halted**: `halt_reason` and `ai/align/halts/<id>.md` with the failing step, its ladder line and the destination.
- **archived-pre-existing**: aged out only (Step 2), never for a false positive, with no commit.

`routed`, `pending-approval` and `pending-ratification` are side states of the ledger's state machine, with the fields each one requires (`ai/patterns/align-ledger.md` § Record format, "Required fields per state").

## Halt conditions

| Step | Halt | Destination |
|---|---|---|
| ROUTE | an idiom no oracle names | `/setup-project --refine` |
| ROUTE | a wrapper gap | `/unify-surfaces` |
| DETECT | the detector matched 0 files | `re-detect-vacuous`: fix the detector command, not the row |
| DETECT | the oracle quote no longer resolves | `oracle-gone`: re-scan |
| DECIDE | the verb is not in the closed set, an `inline` target has more than one consumer, a `remove` target has importers | re-classify; `/refactor` |
| FIX | a file outside `scope`; a new unnamed symbol; a structural row with net lines > 0; a functional block without its idiom | revert; re-scope or `/setup-project --refine` |
| VERIFY | any ladder FAIL | revert; the ladder line goes into the halt file |
| VERIFY | an EQ row with a computed-style difference | reclassify VC; stop at `pending-approval` |
| RECORD | `gaps_closed ≠ len(evidence)` | `halted`: the row is not done |

Do not mark a row fixed until the ladder file shows every applicable step PASS or PASS-flagged. A step that is `NOT RUN` is listed with its reason, and it makes the row `[report-with-fix] (static EQ)` or Unconfirmed, never verified. A HIGH row's confirmation follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10, through a verifier other than the run that found it.

## Hard rules

- **Deterministic gates before any judge.** The judge cannot rescue a FAIL.
- **EQ is proven by a zero difference, VC by a named approval.** Nothing else closes a visible change.
- **Tests, snapshots, fixtures, the class's lint config and baselines are read-only** in an align commit.
- **One way per pattern.** One before-value maps to one after-value across the whole run, unless the token map is context-keyed by role.
- **No invention.** Tokens, imports, exports and props in the diff exist in the declared set (L7). Idioms come from the oracle.
- **Route, do not absorb.** A security, performance, database, quality, frontend or backend row goes to its owner's fix command.

## Failure modes

- **The swap "needed" a snapshot update.** Then it was not exact: the row is VC (V394, V408), and the snapshot edit is AL-34. Revert, reclassify, request approval.
- **Two files took two tokens for one hex.** L6 fails the run, not the row: pick the one the token map's role column names, and re-run both rows.
- **The nearest token is "close enough".** That is AL-06 by definition (§ 7). It needs an approval or `/polish`, never an EQ commit.
- **The fingerprint aged out.** `archived-pre-existing` with no commit. Marking it `fixed` with no commit is the stale-ledger lie `@align-ledger-auditor` catches later.
- **7 of 8 evidence sites closed.** `halted`. Splitting the eighth into a follow-up loses the link between the evidence and the fix.
- **A flaky test at L9.** One retry, then quarantine that test for this row only and say so. A flaky test does not make the suite green.
- **No reviewer for a heavy row.** `pending-review`. Do not self-approve and do not demote the tier.

## Output

```
find-and-align A047 — AL-05 replace-with-shared · proof_class EQ · oracle ai/conventions.md:31 (T2)
  L0  oracle       PASS   quote found (ai/conventions.md:31)
  L1  approval     PASS   EQ — no approval needed
  L3  diffkind     PASS   1 file, value change
  L3  lock-paths   PASS   no test / snapshot / lint-config / oracle file
  L4  scope        PASS   1 removed line = evidence invoicelist.tsx:42; footprint 0
  L5  redetect     PASS   '#d92d20' 1 → 0 in touched files
  L6  consistency  PASS   '#d92d20' → var(--color-danger) (1 key, 1 after)
  L7  names        PASS   --color-danger declared (src/styles/tokens.css:9)
  L8  roundtrip    PASS   light #d92d20 = #d92d20
  L9  lint/types   PASS   tsc --noEmit --incremental false; scoped tests 14/14
  L10a computed    PASS   /orders × light: color rgb(217, 45, 32) = rgb(217, 45, 32)
  L11 ratchet      PASS   no baseline file changed
  L12 lock-count   PASS   tests 212 → 212, assertions 538 → 538
  L13 vacuous      PASS   detector_scope matched 1 file
verdict PASS — fixed in align/2/A047 (a1b2c3d)
```

## Related

- `align-detect` (this pack): the class ledger and dispatcher that produces the rows. `convention-oracle` (§ 0 oracle map, the L0 quote check), `wrapper-adoption-scan`, `naming-layout-scan` and `convention-ratchet-scan` own the align classes.
- `scripts/align-sweep-gate.py` (this skill): the ladder. Its `--self-test` and `--fix-runs=<dir>` replay seeded fix runs with expected verdicts.
- ui-ux `design-token-audit` and its `token-map.py` (when installed): the token classifier behind L8 and the EQ/VC split.
- `@align-idiom-auditor` (DECIDE and VERIFY), `@align-gate-auditor` (the phase verdict), `@align-ledger-auditor` (ledger ↔ git).
- [`precedents/align.md`](../../../../snippets/precedents/align.md), [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Align (V389–V408), [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10.
- `/security-fix`, `/perf-fix`, `/db-fix`, `/quality-fix`, `/frontend-fix`, `/backend-fix`, `/polish`, `/unify-surfaces`, `/optimize`, `/refactor`: the owners a row is routed to.
