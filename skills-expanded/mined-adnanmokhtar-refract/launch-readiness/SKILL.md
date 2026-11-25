---
name: launch-readiness
description: "Launch gate per feature and repo readiness scorecard: 21 cumulative bronze/silver/gold rules, typed evidence, never PASS by default."
kind: skill
pack: product
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: launch-readiness

## Premise

A launch that cannot be judged gets declared a success. The metric was never instrumented, the counter-metric was never watched, the rollback was never exercised, and six weeks later the change is permanent because nobody can argue against it with anything. A readiness checklist read by an agent fails the other way: it turns green from a file's existence (a runbook that is still the template, an owner that is a team alias, a review date already past, a ledger nobody ran).

This skill answers two questions with one rule set, [`rules.json`](rules.json) (29 rules, three cumulative levels), and one deterministic scorer, `scripts/readiness-score.py`:

- **`--feature=<slug>`** — can this feature be launched and judged? The success definition, its live metric, the rollback record, the decision rule and the fatal assumptions are typed fields the script reads itself; the feature's flag, state, surface, security, observability, copy, entitlement and trace rows come from their owners.
- **`--repo`** — the production-readiness scorecard for the repo: the same rules at repo scope, the level reached and the gap to the next one.

**Every rule prints a result and an evidence token.** Results: PASS · FAIL · UNVERIFIED(<reason>) · NOT-INSTALLED(<pack>) · N/A(<reason>). Tokens: **Run** (a tool or query executed in this run), **Static** (a report, file or field read), **UNVERIFIED**, **N/A**. No rule is PASS by default. A rule outside the repo (on-call staffed, a restore measured, load-test results) is `UNVERIFIED (needs <system>)`, never PASS from a file's existence ([`precedents/product.md`](../../../../snippets/precedents/product.md) § 23).

**Levels are cumulative gates, never a weighted sum.** Silver means every bronze and every silver rule passed (`precedents/product.md` § 28). The target follows the feature's stage: experiment and beta are graded against bronze, GA against silver, gold is opted into (`--target=gold`) (`precedents/product.md` § 25).

## The rule

A rule's result counts only when all three hold:

1. **The evidence is the rule's own kind.** `file` and `doc-field` rules are evaluated by the script from the repo; it refuses an evidence row for them. `ledger`, `tool` and `runtime` rules are read only from the evidence TSV this run wrote.
2. **The evidence exists and is fresh.** A ledger row cites an `ai/audits/<YYYY-MM-DD>-<pack>.md` report that is on disk and dated today (or within `--max-age-days`); a tool row carries its command and `exit=<n>`; a query row carries `at=<ISO time>`. Otherwise the rule is UNVERIFIED (`precedents/product.md` § 29, § 30).
3. **The field is typed, not present.** A date in the future, a named person (not `@org/team`, not a group word), a number with its unit, a record with environment, time and result, no template placeholder (`precedents/product.md` § 27).

## Boundaries

This skill composes; it never re-greps a class another detector owns. Each row below is consumed from the owner's same-day ledger, **when that pack is installed**. Without it, the row is `NOT-INSTALLED(<pack>)`, which counts as unverified: it never passes and never fails silently.

| Rule | Owner (pack) | Without the pack |
|---|---|---|
| PRR-FL-1 kill switch · PRR-PD-1 analysis gate | devops `progressive-delivery` §4, §5 | `NOT-INSTALLED(devops)` |
| PRR-UX-1 error / empty / loading / permission | ui-ux `ui-state-scan` §1–§4 | `NOT-INSTALLED(ui-ux)` |
| PRR-SEC-1 open BLOCKER / HIGH | security `/security-audit` class ledger | `NOT-INSTALLED(security)` |
| PRR-OBS-1 alert runbook links · PRR-OBS-2 truthful readiness · PRR-SLO-1 SLO as code | observability `alert-rule-lint`, `metric-hygiene-scan` §7, `slo-rule-scan` | `NOT-INSTALLED(observability)` |
| PRR-SLO-2 SLO defined · PRR-OBS-3 pages reach on-call · PRR-OBS-4 runbook per alert · PRR-EB-1 error-budget policy | observability `slo-audit` steps 1–2, `alert-rule-lint` §8, the `/alert-design` actionability ledger, `slo-rule-scan` §6 | `NOT-INSTALLED(observability)` |
| PRR-TO-1 dependency timeouts | performance `request-path-scan` §12 | `NOT-INSTALLED(performance)` |
| PRR-MIG-1 migration reversible | database `migration-safety` §4 §8 | `NOT-INSTALLED(database)`; N/A with the reason when the feature ships no migration |
| PRR-RB-2 rollback rehearsed | devops `/rollback-deploy` steps 1–4 (`--dry-run`) or `/deploy-stage` S1, on the deploy ledger | `NOT-INSTALLED(devops)` |
| PRR-I18N-1 catalog parity | frontend `i18n-scan` §2 | `NOT-INSTALLED(frontend)` |
| PRR-DOC-1 release note | documentation `changelog-generate` | `NOT-INSTALLED(documentation)` |
| PRR-DR-1 restore measured | infrastructure `dr-audit` or a drill record | `UNVERIFIED (needs a measured restore)` |
| PRR-PERF-1 load test | performance harness: a script in the repo + a recorded run | FAIL with no script; `UNVERIFIED` with a script and no run |
| PRR-CAP-1 capacity headroom | a breakpoint or stress run, or saturation read at the observed peak | `UNVERIFIED (needs a measured headroom)` |
| PRR-FS-1 · PRR-AN-2 · PRR-AN-5 · PRR-EN-1 · PRR-TR-1 | product `feature-surface-scan` §1 §4, `tracking-plan-scan` §2 §5, `entitlement-consistency-scan`, `acceptance-criteria-check` §1 | same pack: dispatched first by `/audit-requirements --repo` |

What this skill is not: deploy mechanics and rollout percentages (devops); whether the flag is stale (devops, `precedents/product.md` § 26); one flow's funnel (business `/suggest-metrics --funnel`); the reversal counterpart of a create or share (business `check-business-coverage`, read once more here only as a support note).

## Inputs and the success file

`/define-success` writes `ai/product/success/<slug>.md`. The script reads only its `## Readiness fields` section, `key: value` per line:

```
## Readiness fields
stage: beta                                  # experiment | beta | ga — sets the target level
paths: apps/web/src/checkout/**, apps/api/src/checkout/**
metric: checkout completion rate, 7-day
metric_event: CheckoutCompleted
counter_metric: refund rate, 30-day
counter_event: RefundIssued
baseline: 34% (2026-09-01..2026-10-01)       # a number and the window's ISO date
threshold: rollback if refund rate > 4%
owner: Dana Reyes                            # a named person who decides
review_date: 2026-12-01                      # after today
decision_rule: keep if completion >= 38% and refunds <= 4% by 2026-12-01
rollback_record: staging 2026-10-12T14:00Z flag off, reverted ok
emissions: order-confirmation email; webhook order.created   # or: none
query: posthog — the saved query or SQL the owner runs       # optional: the runtime lane
```

`ai/product/assumptions.md` is the `assumption-ledger` table; the script reads its `Impact`, `Uncertainty`, `Expiry`, `Decision` and optional `Feature` columns.

## Lanes

| Evidence | Where it comes from | Run |
|---|---|---|
| owners | `CODEOWNERS`, `.github/CODEOWNERS`, `docs/CODEOWNERS`, `.gitlab/CODEOWNERS` (dot-directories walked by Python: a shell `**` does not enter them), `catalog-info.yaml` `spec.owner` | script |
| success fields, assumptions | `ai/product/success/<slug>.md`, `ai/product/assumptions.md` | script |
| owner ledgers | `ai/audits/<today>-<pack>.md` written by the owner's audit (`/audit-requirements --repo`, `/devops-audit`, `/security-audit`, `/obs-audit`, `/frontend-audit`, …) | the agent reads the class line, writes one TSV row citing the report |
| tools | `event-inventory.py --plan`, `surface-map.py`, `trace-matrix.py`, `ears-lint.py` | the agent runs, records `cmd:<command> exit=<n>` |
| metric query | the query named in the success file or by the user: PostHog (HogQL), Amplitude, Mixpanel, GA4 Data API, or warehouse SQL such as `SELECT count(*), max(<ts>) FROM <events> WHERE event = '<metric_event>' AND <ts> > now() - interval '7 days'` | only through a connection or CLI the user already has; without one `UNVERIFIED (no query access)`. The result is rows, **NO-DATA** (0 rows) or **STALE** (newest row older than the freshness window, 48 hours unless the success file says otherwise): both grade FAIL |

No vendor API is called with credentials the session does not already hold, and no query is written to the vendor; a CLI that needs a login is `NOT-RUN (auth)` (`precedents/product.md` § 30).

## Pre-flight

Run as **one** script from the repo root (bash 3.2). Every `rg` names its path; an `rg` exit 2 prints `BLOCKED` and the rule it feeds becomes `blocked (rg exit 2)`, never zero hits.

```bash
X=(-g '!**/node_modules/**' -g '!**/{dist,build,.next,vendor,.venv,coverage,target}/**')
g() { rg "$@"; s=$?; [ "$s" -eq 2 ] && echo "BLOCKED (rg exit 2): rg $*" >&2; return 0; }
# 0. inputs the script reads; dot-directories are listed explicitly
for f in ai/product/success/*.md ai/product/assumptions.md CODEOWNERS .github/CODEOWNERS docs/CODEOWNERS .gitlab/CODEOWNERS; do [ -f "$f" ] && echo "input: $f"; done
g --files --hidden "${X[@]}" -g '**/catalog-info.y*ml' -g '**/cortex.y*ml' -g '!**/.git/**' .
# 1. same-day owner ledgers: the only reports a ledger row may cite
TODAY=$(date +%F); ls -1 ai/audits/"$TODAY"-*.md 2>/dev/null
# 2. the success files' typed fields (the events feed tracking-plan-scan §2)
[ -d ai/product/success ] && g -n --pcre2 '^\s*(?:[-*]\s+)?(?:stage|metric_event|counter_event|review_date|owner)\s*:' ai/product/success
# 3. template placeholders in the documents the gate reads
for d in ai/product docs/runbooks runbooks; do [ -d "$d" ] && g -n --pcre2 '<[^<>\n]{1,60}>|\b(?:TBD|TODO|FIXME)\b|\?\?\?' -g '*.md' "$d"; done
# 4. load-test scripts, runbooks and rollback documents
g --files "${X[@]}" -g '**/*.k6.{js,ts}' -g '**/locustfile*.py' -g '**/{load-test,load-tests,loadtest,loadtests,gatling,k6}/**' -g '**/artillery*.{yml,yaml}' .
g --files "${X[@]}" -g '**/{runbook,runbooks}/**/*.md' -g '**/*{runbook,rollback}*.md' .
# 5. the score (the evidence TSV is written by the agent from steps 1 and the tool runs, under $TMPDIR).
#    --repo scores the repo scorecard AND every feature that has a success file: the feature-scope rules
#    (PRR-LR-1, PRR-RB-1, PRR-LR-5) are N/A at repo scope, so a repo run without the per-feature pass
#    would never grade them.
RS=(python3 -I .claude/skills/launch-readiness/scripts/readiness-score.py --repo=.
    --evidence="${TMPDIR:-/tmp}/readiness-evidence.tsv" --out="${TMPDIR:-/tmp}")
if [ -n "${SLUG:-}" ]; then SLUGS=("$SLUG"); else
  "${RS[@]}" --scope=repo; echo "scope=repo exit $?"
  SLUGS=(); for f in ai/product/success/*.md; do [ -f "$f" ] && SLUGS+=("$(basename "$f" .md)"); done
fi
for s in ${SLUGS[@]+"${SLUGS[@]}"}; do "${RS[@]}" --feature="$s"; echo "feature=$s exit $?"; done
```

The evidence TSV (`rule <TAB> status <TAB> token <TAB> source <TAB> note`) holds one row per ledger, tool or runtime result, never a row for a `file` or `doc-field` rule:

```
PRR-FL-1	PASS	Static	ai/audits/2026-10-19-devops.md	DP §4: 0 rows on apps/api/src/checkout
PRR-AN-2	PASS	Run	cmd:event-inventory.py (tracking-plan-scan) --plan=ai/product/tracking-plan.yaml exit=0
PRR-AN-2	NO-DATA	Run	query:posthog at=2026-10-19T08:00Z rows=0	CheckoutCompleted, last 7 days
PRR-I18N-1	N/A	N/A		single-locale product (one catalog, no locale switch)
PRR-OBS-1	NOT-INSTALLED	UNVERIFIED		observability
```

### Measured

On 2026-10-19 the pre-flight and the scorer ran on all 23 `benchmarks/fixtures` roots: 0 rg exit 2; steps 0–3 return 0 lines on every root (no fixture carries a success file, an assumptions ledger, an owners file or an audit report yet); step 4 returns 5 runbooks on `infra-ops` and 2 on `port-pair`. `readiness-score.py --scope=repo` grades all 23 `NOT-READY`: PRR-OWN-1 FAIL (no owners file), PRR-LR-6 UNVERIFIED (no assumptions ledger), the four feature-only rules N/A with their reason, every ledger rule UNVERIFIED (no evidence this run). The product eval measured the real NestJS + React monorepo read-only on the same day: 20 runbooks, 5 incident records, an `ai/runtime/slos.md`, no `ai/product/success/` — so the repo scope runs and PRR-LR-1 is N/A until a feature is named. On the `launch-gaps` fixture (2026-10-19, `--today=2026-10-19`) the repo pass alone printed PRR-LR-1, PRR-RB-1 and PRR-LR-5 `N/A` (feature-scope rules), so step 5 now also scores every success file: `checkout-v2` and `referrals` both `NOT-READY`, exit 2, with OWN-1, LR-1, RB-1, LR-5 and LR-6 FAIL at the seeded lines (placeholder counter metric, undated rollback, `TBD` decision rule; undated baseline, past review date, failed rollback). The script's `--self-test` covers every variant of V422–V426 (41 checks).

## Scans for

Severity is the rule's level read against the target: a FAIL at or below the target is **high** for a bronze rule and **medium** for silver; a FAIL above the target is **Hardening** (`precedents/product.md` § 36). UNVERIFIED and NOT-INSTALLED at or below the target are open items, never findings and never passes.

| § | Rules | Class | Default |
|---|---|---|---|
| 1 | PRR-OWN-1 | PR-SC-2 ownerless feature | high at bronze target |
| 2 | PRR-LR-1 | PR-LR-1 success definition missing or untyped | high for a behavioural change |
| 3 | PRR-AN-2 | PR-LR-2 metric not live | high |
| 4 | PRR-RB-1 | PR-LR-4 rollback unexercised, emissions unlisted | medium |
| 5 | PRR-LR-5 | PR-LR-5 decision rule not pre-committed | medium |
| 6 | PRR-LR-6 | PR-LR-6 fatal assumptions undecided | medium |
| 7 | PRR-FL-1, UX-1, FS-1, SEC-1, OBS-1, OBS-2, OBS-3, OBS-4, I18N-1, EN-1, TR-1, DOC-1, SLO-1, SLO-2, TO-1, MIG-1, RB-2, EB-1, PD-1, AN-5 | owner rows consumed | the owner's severity, credited to the owner |
| 8 | PRR-PERF-1, PRR-DR-1, PRR-CAP-1 | external-only results | UNVERIFIED unless recorded |
| 9 | all 29 | PR-SC-1 the scorecard: level reached and verdict | the verdict |

### 1. Owner metadata (PRR-OWN-1)

```
BAD:   no CODEOWNERS · `* @renovate-bot` only · `apps/api/ @dana` while the feature also lives in apps/web/src/checkout/
GOOD:  .github/CODEOWNERS: `apps/web/src/checkout/ @dana` and `apps/api/src/checkout/ @dana` · catalog-info.yaml spec.owner: group:checkout
```
**Read the code:** Which owners file does the forge read (root, `.github/`, `docs/`, `.gitlab/`)? Does the **last** matching rule for each feature path name a human or a team (the last match wins)? Is the only owner a bot? **Finding when** a feature path has no matching rule, or its rule names bots only. **PROOF:** V426, `readiness-score.py --rule=PRR-OWN-1` exits 2 → 0.

### 2. Success definition typed (PRR-LR-1)

```
BAD:   metric: <metric name> · owner: growth team · baseline: 34% (last month) · review_date: 2026-10-01 (past)
GOOD:  metric: checkout completion rate, 7-day · owner: Dana Reyes · baseline: 34% (2026-09-01..2026-10-01) · review_date: 2026-12-01
```
**Read the code:** Is there a success file for the slug at all? Is each field the definition or the template's sample? Is the baseline a measurement with its window, or a guess? **Finding when** the script prints FAIL with the field and its reason. **PROOF:** V422.

### 3. Metric live (PRR-AN-2)

```
BAD:   metric_event: CheckoutCompleted — tracking-plan-scan §2 lists it as planned and never fired
       the query returns 0 rows for the last 7 days (NO-DATA), or its newest row is 6 days old (STALE)
GOOD:  AN §2 quiet for both events, and `query:posthog at=2026-10-19T08:00Z rows=412` recorded
```
**Read the code:** Are `metric_event` and `counter_event` in tracking-plan-scan's inventory, fired on the path the feature ships (its §2 and §5 rows)? A server-side leg counts (`precedents/product.md` § 11). Does the user hold query access? Without it the runtime half is `UNVERIFIED (no query access)`. **Finding when** the static half has an AN §2 row for a metric event, or a recorded query is NO-DATA or STALE. **PROOF:** V423.

### 4. Rollback record (PRR-RB-1)

```
BAD:   rollback_record: we can revert the deploy · emissions: (missing)
GOOD:  rollback_record: staging 2026-10-12T14:00Z flag off, reverted ok · emissions: order-confirmation email; webhook order.created
```
**Read the code:** Was the rollback performed (environment, time, result), or described? What does the feature create that a revert cannot recall: data written under the new behaviour, notifications, webhooks, exports? A drill itself is external: the record is the repo evidence, the drill stays `UNVERIFIED (needs <env>)` when nobody recorded one. **Finding when** the record is missing, untyped or shows a failed rollback, or the emissions line is absent. **PROOF:** V424.

### 5. Decision rule pre-committed (PRR-LR-5)

```
BAD:   decision_rule: we will look at the numbers after launch
GOOD:  decision_rule: keep if completion >= 38% and refunds <= 4% by 2026-12-01 · owner: Dana Reyes · review_date: 2026-12-01
```
**Read the code:** Is the threshold a number set before the result, the owner a person, the review date in a real calendar (after today)? **Finding when** any of the four fields fails its type. **PROOF:** V422.

### 6. Fatal assumptions decided (PRR-LR-6)

```
BAD:   | 1 | buyers trust saved cards | fatal | high | 2026-11-01 | open | checkout-v2 |
GOOD:  | 1 | buyers trust saved cards | fatal | high | 2026-11-01 | tested: 41/50 kept the saved card (2026-10-10) | checkout-v2 |
       | 2 | refunds stay under 4%   | fatal | high | 2026-09-01 | accepted: Dana Reyes | checkout-v2 |
```
**Read the code:** At feature scope every fatal × high row for the feature (or with no feature) must be tested or accepted by a named person: the launch is the decision point. At repo scope only rows past their expiry count. Accepting a risk is legitimate; leaving it undecided is not. **Finding when** such a row has no `tested:` / `accepted: <name>` decision. No ledger at all is `UNVERIFIED (run assumption-ledger)`. **PROOF:** V422.

### 7. Owner rows consumed (20 rules)

```
BAD:   PRR-FL-1 PASS — "progressive-delivery looked fine" (no report cited)
       PRR-UX-1 PASS — ai/audits/2026-10-01-ui-ux.md (18 days old)
GOOD:  PRR-FL-1 PASS Static ai/audits/2026-10-19-devops.md — DP §4: 0 rows on the feature's paths
       PRR-OBS-1 NOT-INSTALLED(observability)
```
**Read the code:** Open the cited report and read the class line for the feature's paths: `checked (k → m findings)`, `N/A (<reason>)`, `not run`. A `not run` or `blocked` owner line is UNVERIFIED here, never PASS. A finding at medium or above on the feature's paths is FAIL. Dedupe by `file:line`: the finding stays the owner's; this rule only points at it. **Finding when** the owner's same-day ledger holds such a finding. **PROOF:** the owner's V-number; here V425 proves the composition.

### 8. External-only results (PRR-PERF-1, PRR-DR-1, PRR-CAP-1)

```
BAD:   PRR-PERF-1 PASS — "there is a k6 folder"
GOOD:  PRR-PERF-1 PASS Run query:k6 at=2026-10-19T09:00Z p95=210ms — budget 300ms
       PRR-DR-1 UNVERIFIED (needs a measured restore)
```
**Read the code:** Is there a script for the feature's hot endpoints at all (no script is FAIL)? Was a run recorded with its budget? On-call staffing, restore drills and branch protection are the same shape. **Finding when** the script is absent; otherwise the rule stays UNVERIFIED until a run is recorded (`precedents/product.md` § 23). **PROOF:** V425.

### 9. The scorecard (PR-SC-1)

```
BAD:   "20 of 29 rules pass — 69% ready" · a beta graded NOT-READY for a missing SLO (gold) · a rule removed from the table
GOOD:  Level reached: bronze · Gap to silver: PRR-RB-1 FAIL, PRR-OBS-1 NOT-INSTALLED · Verdict: READY (target bronze, stage beta)
```
**Read the code:** Is every one of the 29 rules in the table, with N/A reasons where they apply? Does the target follow the stage? Is any UNVERIFIED rule being read as a pass? **Finding when** the verdict at the target is NOT-READY; READY-UNVERIFIED lists its open rules as items to prove, not findings. **PROOF:** V425, `readiness-score.py` exit 2 → 0.

## The 3,000-hit path

A repo scope over a monorepo can hold many success files and many owner ledgers. Triage in this order and record each step in the coverage block:

1. **Score each feature separately** (`--feature=<slug>` per success file); a repo-scope run never averages features.
2. **Group owner rows by report**, not by rule: one read of `ai/audits/<today>-<pack>.md` fills every rule that pack owns, for every feature, keyed by the feature's `paths`.
3. **Rank by stage**: GA features first, then beta; experiments last.
4. **Read the top 30 FAIL rows fully** (the field, the owner's class line, the cited report).
5. **Ledger the rest** as `Live, unreviewed (k features / n rules)` with the command that continues them. Never `checked`.

## Output

```
launch-readiness — feature=checkout-v2  stage=beta  target=bronze (stage beta)  today=2026-10-19
rule        level   result          token      evidence
PRR-OWN-1   bronze  PASS            Static     every feature path covered (.github/CODEOWNERS)
PRR-LR-1    bronze  PASS            Static     ai/product/success/checkout-v2.md fields typed
PRR-AN-2    bronze  FAIL            Run        NO-DATA — query:posthog at=2026-10-19T08:00Z rows=0
PRR-FL-1    bronze  PASS            Static     ai/audits/2026-10-19-devops.md — DP §4: 0 rows
PRR-UX-1    bronze  PASS            Static     ai/audits/2026-10-19-ui-ux.md — US §1-§4: 0 rows
PRR-FS-1    bronze  PASS            Static     ai/audits/2026-10-19-product.md — FS §1 §4: 0 rows
PRR-SEC-1   bronze  NOT-INSTALLED   UNVERIFIED security
PRR-RB-1    silver  FAIL            Static     ai/product/success/checkout-v2.md — rollback_record: missing
…           (all 21 rows)
Level reached: none · Gap to bronze: PRR-AN-2 FAIL, PRR-SEC-1 NOT-INSTALLED
Verdict: NOT-READY (1 failing)

Findings: 1 · Open (UNVERIFIED / NOT-INSTALLED at target): 1

1. ai/product/success/checkout-v2.md:7 → events                   [report-with-fix]   high
   §3 metric not live — metric_event CheckoutCompleted returned 0 rows in the last 7 days
   (query:posthog at=2026-10-19T08:00Z); tracking-plan-scan §2 lists it planned and never fired
   (apps/web/src/checkout/use-checkout.ts has no call). Fix: fire it on the confirmed order
   (owner: tracking-plan-scan §5). Proof: V423 — re-run the query after the fix.

2. PRR-SEC-1                                                       [report-flagged]
   security pack not installed — no security ledger to read. Settle: install the pack and run
   /security-audit, or record the owner's review as a ledger row.

Class coverage:
  §1 owners             checked (1 file → 0 findings)
  §2 success fields     checked (1 file, 6 fields → 0)
  §3 metric live        checked (static: AN §2 row 1; runtime: 1 query → 1 finding)
  §4 rollback record    checked (silver; above target → Hardening)
  §5 decision rule      checked (4 fields → 0)
  §6 fatal assumptions  checked (2 rows in scope → 0)
  §7 owner rows         checked (5 reports read) · NOT-INSTALLED (security)
  §8 external-only      UNVERIFIED (PRR-PERF-1 no recorded run; PRR-DR-1 needs a measured restore)
  §9 scorecard          verdict NOT-READY; 29 of 29 rules printed
```

`[report-with-fix]`: the rule's evidence was read or run in this session, the oracle (V422–V426) is red, and the fix is a field the owner fills or a finding the owner closes. `[report-flagged]`: the rule could not be evaluated (no evidence, owner pack absent, external-only); the row names what would settle it. The coverage block lists **all nine** sections on every run.

## Precedents

The verifier reads [`precedents/product.md`](../../../../snippets/precedents/product.md) § 23–30 and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: external-only rules are UNVERIFIED (§ 23); N/A keeps its row and its reason (§ 24); the target follows the stage (§ 25); kill switches are permanent and devops's (§ 26); a template is not a record (§ 27); a ledger row needs its report on disk and fresh (§ 29); a tool that did not run is NOT-RUN (§ 30).

## When to run

- Before a change is enabled for real users (deploy, flag, or a rollout step past the point where rollback stops being cheap): `--feature=<slug>`, dispatched by `/define-success` Phase 7.
- On every `/audit-requirements --repo`: `--repo`, after the product detectors and the installed owners' audits have written today's ledgers.
- After a launch nobody could judge, as the checklist for the next one.

## Halt conditions

- Every FAIL at or below the target goes through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/product.md`](../../../../snippets/precedents/product.md) before it is reported. Under `/audit-requirements` that is its verification phase; run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`.
- **No success file for the named feature:** print PRR-LR-1 FAIL and route to `/define-success`; do not reconstruct the definition from the code or from a ticket.
- **The change is irreversible by nature** (a migration that drops data, a sent communication, a deletion): say so; PRR-RB-1 then checks the pre-conditions and the emissions list, and the verdict names the irreversibility.
- Do not write an evidence row for a `file` or `doc-field` rule, a PASS for a rule whose report is not on disk, or a tool PASS without its exit code. The script refuses the first and downgrades the others; editing the TSV to get past it is a defective run.
- Do not print a percentage, a weighted score or a verdict without the 21-row table and the coverage block.
- Do not run the analytics query with credentials the session does not already hold, write to a vendor, or install a CLI. Do not write into the audited repo; `--out` stays under `${TMPDIR}` (the script refuses a path inside the repo).
- Do not re-grade an owner's class. A disagreement with the owner's ledger is a note to the owner, not a different result here.

## Related

- `/define-success` writes the success file this skill types; `/audit-requirements --repo` dispatches the repo scope and folds this coverage block into its class ledger; `/product-fix` closes LR and SC rows with `readiness-score.py --rule=<id>` exit 2 → 0, writing only fields the owner supplies.
- `tracking-plan-scan` (§2, §5), `feature-surface-scan` (§1, §4), `entitlement-consistency-scan` and `acceptance-criteria-check` (§1) supply the product rows; `assumption-ledger` supplies the fatal rows.
- devops `progressive-delivery`, ui-ux `ui-state-scan`, observability `alert-rule-lint` / `metric-hygiene-scan` / `slo-rule-scan`, frontend `i18n-scan`, documentation `changelog-generate`, infrastructure `dr-audit` and the security audit own the consumed rows (each when installed).
- `@product-strategist` owns the decision rule and the kill criteria; `@scope-arbiter`'s ledger is where a reversal gap starts.
