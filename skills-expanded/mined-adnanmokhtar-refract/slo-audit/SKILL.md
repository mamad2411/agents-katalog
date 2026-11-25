---
name: slo-audit
description: "SLO attainment from live data: budget, too lax / too tight, STALE vs NO-DATA; sole writer of ai/runtime/slos.md (--no-write reads only)."
kind: skill
pack: observability
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: slo-audit

## Premise

Find real issues. Every verdict cites the achieved %, the budget remaining, and the window it was measured over. Numbers come from the observability backend's SLO endpoint or dashboard, never estimates. Each SLO is named from `ai/runtime/slos.md`; incidents are named with their ID; a vendor or service is called out by name. "Recommend raise to 99.5%" requires both 90d data backing it AND a named stakeholder for the buy-in.

**This skill runs where the code is, and the measurements are somewhere else.** An agent invoked in a repository usually cannot reach a production TSDB, a vendor SLO API, or a paging history. That is the normal case, not the exception, so it has a first-class output (`NO-DATA`). The failure this skill exists to prevent is filling the table with plausible numbers instead of using it. Every other verdict is a claim about attainment; you may not make one you did not measure (precedents/observability.md § 36).

**This skill is the behavioural, L-tier half of SLO quality.** Everything decidable from files is `slo-rule-scan`'s (this pack): no burn alert (SLO-01), a factor that does not match the objective and period, a single window, generated-rule drift (SLO-02, SLO-03, `burn-check.py`), an impossible objective (SLO-04), a wrong SLI error definition (SLO-06), a latency threshold that is not a bucket edge (SLO-07), a window longer than retention (SLO-10). This skill **consumes those rows and never re-derives them**. It answers what only data can: is the SLO met, how much budget is left, is the target too lax or too tight, did it catch the last incidents.

Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md). The live oracle is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability (*Live series*); the definition oracle it consumes is V207.

## Modes and the writer contract

This skill is the **only writer of `ai/runtime/slos.md`** in the pack (`ownership.json` row `obs-slo`: `slo-rule-scan` detects, `slo-audit` writes the registry). Everyone else reads it or proposes rows to it:

| Artifact | Relation to the registry |
|---|---|
| `slo-audit` (this skill, write mode) | **Creates** it when absent (step 1) and **updates** a target, window or owner when a recommended change is accepted |
| `/alert-design` Phase 1 | **Proposes** rows and dispatches this skill in write mode to write them; it never writes the file itself |
| `/obs-audit` | Dispatches this skill with `--no-write`; the registry is never touched by an audit run |
| `slo-rule-scan`, `alert-audit`, `synthetic-monitoring`, `/add-telemetry`, `ai/patterns/slo.md` | Read only. A missing probe-SLO or SLO row is their finding, routed to `/alert-design` Phase 1 |
| `@sre-engineer` | Writes the budget-policy text and postmortems, never registry rows |

Two modes:
- **Write mode** (default, direct invocation or `/alert-design` Phase 1): writes `ai/audits/slo-audit-<date>.md` and creates or updates `ai/runtime/slos.md` as step 1 and step 5 describe.
- **`--no-write`** (read mode, `/obs-audit` and any read-only caller): writes **nothing**, not the registry and not an audit file. It returns the ledger to the caller. A bootstrap that write mode would perform is returned as `PROPOSED REGISTRY` rows, each with its `origin`, and the caller's report carries them (`/obs-audit` Phase 5 writes only `ai/audits/<date>-observability.md`). Verify the tree after a read-mode run: `git status --porcelain -- ai/runtime/slos.md` prints nothing.

Before any write in write mode, read the current file and edit only the rows you change. A write that changes nothing is not made.

## Inputs

1. **`slo-rule-scan` rows for the same tree, run today:** spec and burn-rule rows with their objective and period sources, `burn-check.py` output, regenerate-and-diff result, retention. Under `/obs-audit` they are already in the run; standalone, run `slo-rule-scan` first. Without them, halt the definition-dependent steps (2, 3's arithmetic gate, 5's target-change gate) and say so; attainment rows may still run, tagged `definition not verified (slo-rule-scan not run)`.
2. **`ai/runtime/slos.md`:** read. May be absent; that routes to step 1's define branch, never to a halt.
3. **90 days of measurement (L):** the TSDB through a URL the user gave (sloth's `slo:sli_error:ratio_rate*` and `slo:objective:ratio` recordings, Pyrra's `<metric>:burnrate<w>`, a hand-written ratio), or a vendor SLO API or export. Retention must cover the window (`slo-rule-scan` §6 reads it).
4. **Incident log**, if available.

## Halt conditions

- **A high or critical row needs a separate refuter.** A RED or a TOO TIGHT that stops feature work is not reported as confirmed until a verifier other than this run has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Run standalone, apply the protocol as a second pass and tag those rows `self-verified`.
- **A verdict with an empty evidence cell is fabricated.** Every row carries the exact query or API call run AND what came back. No evidence → `NO-DATA`, not a guess and not a blank.
- Refuse to verdict an SLO without 90d of measurements captured: record `NO-DATA(<what was unreachable>)` and continue. Do not skip the row; a missing row reads as "no SLO", a different and much worse finding.
- Refuse to call an SLO TOO LAX without achieved >> target consistently; never propose tightening without the stakeholder who must sign off.
- An adjective where a number belongs ("attainment looks healthy") is not a verdict. Produce the percentage or produce `NO-DATA`.
- **Never write a registry target with an empty `origin`.** A number with neither a commitment nor a measurement behind it is `PROPOSED(<what would settle it>)`.
- **Never write in `--no-write` mode**, and never write any file but the two named in § Modes in write mode.
- **Do not grade a definition defect here.** It is `RULE(slo-rule-scan §N <code>)`, credited there. Never judge a burn factor by a literal; cite `THR-OBS-BURN` and the `slo-rule-scan` row (precedents § 12).

## When to run

- Quarterly review of all SLOs.
- After a significant incident (did the SLO catch it? was it too lax?).
- Before raising or lowering a target (step 5's gate).
- When defining a service's first SLOs (`/alert-design` Phase 1, write mode).
- On every whole-repo `/obs-audit`, after `slo-rule-scan` (*SLO attainment* row, `--no-write`).

## Procedure

### 1. Inventory SLOs, or define them when the registry is empty

Read `ai/runtime/slos.md`. Per SLO capture **statement**, **SLI**, **target**, **window** (rolling 30 days standard), **owner**, **origin** (vendor SLA, customer promise, engineering aspiration). Join each row to its `slo-rule-scan` spec or burn-rule row by name or SLI; a registry SLO with no spec and no burn rule is that skill's SLO-01, credited there.

**If the file is missing or holds no entries, write mode creates it.** That is the bootstrap, not an error path. Three artifacts route registry creation here (`/alert-design` Phase 1, `synthetic-monitoring` §4, `/add-telemetry`) and none of them will invent a target, so a run that stops at "this project has no SLOs" strands all three. In `--no-write` mode the same entries are returned as `PROPOSED REGISTRY` rows.

A first target has exactly two defensible sources:

| Where the target comes from | When it applies | What you write |
|---|---|---|
| **An existing commitment** — a customer contract, a published SLA, a vendor SLA you resell | The number is already promised outside the team | The promised figure verbatim, `origin:` naming the document |
| **Measured recent behaviour** — attainment over the last 90d on that SLI, rounded *down* to a level the service already clears | No commitment exists, the common case | The achieved figure minus headroom, `origin:` carrying the query |

If neither resolves, still write the entry with SLI, window and owner, and `target: PROPOSED(<what would settle it>)`, plus a `NO-DATA` row in step 3. **A burn rule already in the repo implies an objective** (`slo-rule-scan`'s row reads `budget = 1 − objective`): record it as `PROPOSED(implied by <file:line> budget <b>; owner to confirm)`, never as an agreed target. **A round number chosen because it looks like an SLO is the fabrication this step exists to prevent**: `99.9%` is a claim that the service may be down 43 minutes a month, and nobody in this run agreed to that.

Every entry carries `sli`, `target`, `window`, `owner`, `origin`. Missing `owner` or `origin` and it is not done.

### 2. Gate the definition before reading attainment

An attainment number is only as good as the SLI and budget behind it. Per SLO, read its `slo-rule-scan` rows:
- **SLO-07** (`le` names no bucket edge) or **SLO-06** (wrong error definition): the SLI itself is wrong, so a measured "achieved %" is a number about something else. Verdict `RULE(slo-rule-scan §5 SLO-07)` or `§4 SLO-06`; no attainment verdict until it is fixed.
- **SLO-10** (period longer than retention): 90d attainment cannot be computed from this TSDB. `NO-DATA(history shorter than window)` unless a long-term store answers.
- **SLO-03** (budget ≠ 1 − objective) or **drift**: the burn alerts page at the wrong burn; attainment can still be measured, and the row carries the credit `RULE(slo-rule-scan §2 SLO-03)` beside its verdict.
- **SLO-04** (100 %, or a page that cannot fire): no budget exists to measure. `RULE(slo-rule-scan §3 SLO-04)`.

### 3. Pull 90 days of measurement

Use whichever the stack provides: Prometheus or another TSDB through the URL given (the sloth or Pyrra recordings named in the `slo-rule-scan` row, never a hand-typed metric name — a query naming a series in no inventory is Refuted, precedents § 37); a vendor SLO product (Datadog, New Relic, Grafana Cloud, Honeycomb, cloud-vendor service monitoring) through its API or a pasted export.

For each SLO compute: achieved % over 30d and 90d (trend), error budget remaining, burn trend (linear / accelerating / plateau). Print the query and what it returned.

### 4. Verdict per SLO

Pick exactly one, no synonyms. Six are claims about attainment and each requires the measurement in the evidence cell; `NO-DATA` is what you use when you could not measure, and `RULE(…)` credits a definition defect to `slo-rule-scan`.

| Verdict | Criteria | Recommendation |
|---|---|---|
| **GREEN** | Achieved > target consistently for 90d, budget > 50% remaining | Hold, or consider tightening |
| **YELLOW** | Achieved ≈ target; burn occasionally spikes | Monitor; investigate the spikes |
| **RED** | Achieved < target, or budget exhausted | Stop feature work per the budget policy; fix root causes |
| **TOO LAX** | Achieved >> target consistently for 90d, no incidents | Raise target (step 5's gate) |
| **TOO TIGHT** | Achieved << target despite effort; target was aspirational | Lower with stakeholder agreement, or invest in reliability |
| **STALE** | The SLO **is** measurable from here and the series has no fresh samples (> 7 days) — a property of the instrumentation | Fix instrumentation or remove the SLO |
| **NO-DATA(reason)** | *You* could not reach the measurement — backend unreachable, no credentials, no SLO endpoint, history shorter than the window. A property of the audit, not of the SLO | Name what was unreachable and the one command that would close it |
| **RULE(slo-rule-scan §N code)** | The definition is wrong in a way that makes attainment meaningless (step 2) | Fix the spec first; `/obs-fix` closes it |

**`STALE` and `NO-DATA` are not interchangeable.** STALE says *the service stopped emitting*, a finding about the system. NO-DATA says *I could not look*, a finding about this run that obliges nobody to change code. Reporting NO-DATA as STALE invents a production defect; reporting STALE as NO-DATA hides one. **A NO-DATA row is UNVERIFIED, not a pass**, and it makes the audit `INCOMPLETE`.

### 5. Recommend changes, and gate every target change through `burn-check.py`

A recommended objective or period change (TOO LAX, TOO TIGHT, a new window) also changes every burn rule built on it. Before recommending, re-run the arithmetic with the proposed values and put its output in the row:

```bash
python3 .claude/skills/slo-rule-scan/scripts/burn-check.py <the SLO's burn-rule files> --slo='<alert regex>=<proposed objective>/<period>' --retention=<the server's> --format=text; echo "burn-check exit $?"
```

Measured (2026-10-10): a Workbook rule written for 99.9 % (`14.4 * (1 - 0.999)`) passes at `--slo=…=99.9/30d` (exit 0) and, re-run at a proposed 99.95, prints `§2 SLO-03 [H] threshold budget 0.001 is not 1 − objective (0.0005) … fires at 2× the intended burn` (exit 1). So the recommendation is never "raise the target" alone: it is "raise the target **and** regenerate the burn rules from the spec" (precedents § 42: a generated rule is fixed at its spec), with the owner's sign-off. In write mode, the registry row changes only when the owner has accepted it; the rules change through `/obs-fix`, never here.

### 6. Cross-correlate with incidents

For each incident in the last 90 days: did an SLO catch it, with what lead time? Did it consume budget, how much? Was the SLI and window right? If several SLOs cover the service, did they all signal, or is one redundant? Whether the burn *alerts* fired is `alert-audit`'s §5 (this pack); cite it.

## Output

The inventory table is a **ledger**: one row per SLO, and the `Evidence` column carries the query or API call actually run and what it returned. The numbers below are placeholders; a run that reproduces them without querying anything is the fabrication this skill exists to stop.

```
## SLO audit — <service> — <date> — mode: write | --no-write
slo-rule-scan rows: 5 SLOs, run <date> · backend: <URL given | UNREACHABLE (no URL)> · retention: 30d (k8s/prometheus.yaml:8)

| SLO | Target | Window | Achieved 30d | Budget left | Definition (slo-rule-scan) | Evidence (query run → observed) | Verdict |
|---|---|---|---|---|---|---|---|
| api.availability | 99.9% | 30d | 99.93% | 70% | ok (workbook-4, burn-check 0) | `slo:sli_error:ratio_rate30d{sloth_slo="availability"}` → 0.0007 | GREEN |
| orders.success | 99.5% | 30d | 99.2% | 0 | ok | vendor SLO API `orders.success` → 99.2%, budget 0 on d14 | **RED** |
| email.delivery | 99% | 30d | 99.95% | 95% | ok | `slo:sli_error:ratio_rate30d{sloth_slo="email"}` → 0.0005 | TOO LAX |
| api.latency | 99% < 300ms | 30d | — | — | §5 SLO-07: le="0.25", buckets [0.1, 0.3, …] | not queried: the SLI numerator is empty by construction | RULE(slo-rule-scan §5 SLO-07) |
| jobs.completion | 99% | 7d | — | — | ok | no TSDB URL given | **NO-DATA(backend unreachable)** |

Audit status: INCOMPLETE — unmeasured: jobs.completion (re-run with the Prometheus URL or paste a 90d export); api.latency blocked on slo-rule-scan §5.

### Recommended changes
| # | Change | Reason | Gate | Owner sign-off |
|---|---|---|---|---|
| 1 | email.delivery 99% → 99.5% and regenerate its rules | TOO LAX 90d | burn-check at 99.5: 2 rows SLO-03 → regenerate from slo/sloth/email.yml | <named stakeholder> |
| 2 | orders.success: pause feature work per policy | budget exhausted d14 | — | <policy owner> |

### PROPOSED REGISTRY (--no-write only)
| slo | sli | target | window | owner | origin |
| checkout.success | non-5xx ratio of POST /checkout | PROPOSED(implied by rules/slo.yml:12 budget 0.001; owner to confirm) | 30d | payments | rules/slo.yml:12 |
```

### Closure gate

Compute the status from the ledger, never by hand:
- **`COMPLETE`**: every row carries a measurement and one of the six attainment verdicts.
- **`INCOMPLETE — unmeasured: <list>`**: any `NO-DATA` or `RULE(…)` row. Name each SLO, what was missing, and the one command that would close it.

Under `/obs-audit` this skill is the *SLO attainment* row. At `NO-DATA` that row alone does not force GO-UNVERIFIED (the verdict line prints `behaviour lane NO-DATA(<source>)`); a `RULE(…)` row is carried by `slo-rule-scan`'s own finding. The gate is **[self-policed]**, wired to a checkable artifact: `@observability-reviewer` and `@sre-engineer` BLOCK a COMPLETE whose rows carry verdicts with empty evidence.

## False positives / precedents

- **Audited only 7 days** → missed slow burn. **GREEN treated as no work** → missed TOO LAX.
- **Achieved % filled from the target column** because the backend was unreachable: the fabrication `NO-DATA` exists to make unnecessary.
- **STALE reported where the truth was NO-DATA**, or a row dropped instead of marked `NO-DATA`.
- **A Pyrra 14 / 7 / 2 / 1 set or a fourth 3× 24h/2h ticket tier read as wrong** (precedents § 12): the arithmetic in `THR-OBS-BURN` decides, and it is `slo-rule-scan`'s row.
- **A target raised without regenerating the burn rules**: the alerts then page at the old budget (step 5).
- **A 100 % SLO** is always a definition finding (precedents § 14), credited to `slo-rule-scan` §3.

## Related

- `slo-rule-scan` (this pack) — the definition rows and `burn-check.py` this skill consumes; `alert-audit` (this pack) — whether the burn alerts fired.
- `/alert-design` (this pack) — proposes registry rows and dispatches this skill in write mode; `/obs-audit` — dispatches it with `--no-write`; `/obs-fix` — closes definition rows.
- `synthetic-monitoring` §4, `/add-telemetry` — route a missing SLO here through `/alert-design` Phase 1.
- `@sre-engineer` — budget policy and the stakeholder conversation; `@incident-responder` — uses SLO context during incidents; `@observability-reviewer` — judges these rows.
- `ai/patterns/slo.md` (method), `ai/runtime/slos.md` (data, written here).
