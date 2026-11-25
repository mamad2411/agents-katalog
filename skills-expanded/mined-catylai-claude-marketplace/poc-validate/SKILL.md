---
name: poc-validate
description: "Checks a proof of concept against its own .poc/poc.json contract and recommends GRADUATE, KILL or EXTEND. Use when a POC reaches a time-box checkpoint or feels adrift. Read-only. Not for closing a POC (use poc-graduate); not for starting one (use poc-start)."
when_to_use: "is this POC done, check kill criteria, POC checkpoint, should we keep going, validate a proof of concept"
allowed-tools: Read, Glob, Grep, Bash(pwd), Bash(date -u *), Bash(git log *)
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# Validate a POC Against Its Own Contract

This skill judges a POC by the criteria **it** wrote, not by general good practice. It is
read-only: it reports, it does not fix, scaffold, or migrate.

## Step 1 — Gather context and load the contract

Run `pwd` and `date -u +%Y-%m-%d` (Step 2 compares today against `time_box.ends`), then Read
`.poc/poc.json`.

**Without a checkout (web/Cowork):** ask the user to paste `.poc/poc.json` and today's date, and
wait for both. Skip the drift scan in Step 6 and judge drift only from what they describe.
Do not judge a time box against an assumed date, or a contract you have not read.

If `.poc/poc.json` is absent, stop: this is not a POC. Suggest `poc-start` if one is
intended.

If it is present but `poc_active` is `false`, report that the POC is already closed, show
`outcome`, `closed_at` and `decision_rationale` (written by `poc-graduate`), and stop.

Read and restate the contract before judging anything: the question, the success signal,
each kill criterion, the time box, the out-of-scope list, and the target runtime. If the
user disagrees with the contract, that is a conversation to have before validation, not
during — a contract edited to match the result proves nothing.

## Step 2 — Assess the time box

Compare today against `time_box.ends`. Report one of:

- **Within the box** — days remaining.
- **At the box** — due now.
- **Past the box** — days over. Note that the time-box kill criterion has fired, and say so
  plainly even if the work looks promising. "Nearly there" past a deadline is the single
  most common way a POC turns into an unbudgeted project.

## Step 3 — Judge each kill criterion

For each entry in `kill_criteria`, assign exactly one verdict:

| Verdict | Meaning |
| --- | --- |
| `MET` | The criterion has fired. Evidence shows the condition that ends the POC. |
| `NOT MET` | Evidence shows the condition has not fired. |
| `UNMEASURED` | No evidence bears on this criterion either way. |

`UNMEASURED` is a real and common result, and it must never be reported as `NOT MET`.
Silence is not a pass. A criterion nobody measured is a question nobody answered.

Cite the evidence for every `MET` and `NOT MET`: the entry in `.poc/poc.json` evidence, a
test output, a benchmark file, a log. A verdict with no citation is an opinion — downgrade
it to `UNMEASURED` and say why.

## Step 4 — Judge the success signal

Has the observation named in `success_signal` actually been observed? Same three verdicts,
same evidence requirement. If the signal was a threshold, report the measured value against
the threshold, not a characterization of it.

## Step 5 — Check the evidence trail itself

Count the entries in the contract's `evidence` array.

- **Empty** — the POC has produced no recorded observations. Report this at the top of the
  findings; it dominates everything else. A repository full of code with no evidence answers
  no question.
- **Sparse or undated** — note which criteria have no evidence attached.
- **Reconstructed** — if every entry shares one late date, say so; evidence written up at
  the end is weaker than evidence recorded as it happened.

## Step 6 — Check for drift

Scan for work the contract put out of scope, and for the shape of a project rather than an
experiment:

- Glob each of `.github/**`, `**/.gitlab-ci.yml`, `.circleci/**`, `**/Dockerfile*`, `**/*.tf` and
  `**/Chart.yaml`.
- Run `git log --oneline -20 --stat`.

Compare what you find against `out_of_scope` literally, then against these shapes, which mean
"project, not experiment" unless the contract put them in scope:

| Shape | Why it costs the box | Cheaper path for a POC |
| --- | --- | --- |
| CI/CD pipeline configuration | Delivery machinery, not an answer | Run it locally |
| Deployment or hosting definitions | The target runtime is a graduation concern | Local execution |
| More than one service | Coordination overhead | One process |
| Abstraction over a second implementation that does not exist | Speculative generality | Call the one you have |
| Hardening, failover, multi-region, key management | Production concerns | Note them for graduation |
| Schema migrations, versioned APIs | Compatibility with a future that may not happen | Rewrite freely |
| Configuration layers and plugin systems | Flexibility nobody is using yet | Hardcode, note it as debt |

Report drift as an observation, not a violation, and quantify it from the log: "three of the
last ten commits touched deployment plumbing" lands better than "there is scope creep". Also
check the reverse drift: recent commits that no longer touch the question's subject at all.

## Step 7 — Report

```markdown
## POC VALIDATION: <poc name>

**Question:** <question>
**Time box:** <start> → <end> — <within / at / N days past>

### Success signal

<signal> — **MET / NOT MET / UNMEASURED**
Evidence: <citation, or "none">

### Kill criteria

| Criterion | Verdict | Evidence |
|---|---|---|
| <criterion> | MET / NOT MET / UNMEASURED | <citation or none> |

### Evidence trail

<N entries; gaps noted>

### Drift

<out-of-scope work observed, or "none">

### Recommendation

**GRADUATE / KILL / EXTEND** — <one paragraph, grounded in the verdicts above>
```

Recommendation rules, applied in order:

1. Any kill criterion `MET` → **KILL**. That is what the criterion was for. Say which one.
2. Success signal `MET`, no kill criterion `MET` → **GRADUATE**.
3. Time box spent and the signal is `UNMEASURED` → **KILL**. The bet was time, and it is
   spent. If the user wants to continue, that is a new POC with a new contract and a new
   box — which is a decision someone makes deliberately, not a default.
4. Within the box, signal `UNMEASURED` or `NOT MET`, no criterion met → **EXTEND**, and name
   the specific measurement that would settle it (for `NOT MET`, what would have to change for
   the signal to be met inside the remaining days).

Give the recommendation straight. A POC's whole value is that someone was willing to hear
"no" cheaply; softening the verdict destroys that value.

This skill changes nothing. To act on the recommendation, run `poc-graduate`.

## Calibration examples

<example>
Contract: kill criterion "p95 extraction latency above 2 s on the 200-invoice sample". Evidence:
`{"criterion": "latency", "observation": "p95 3.4 s", "source": "bench/run-2.json"}`.
Verdict: that criterion `MET`, cited to `bench/run-2.json`. Recommendation `KILL`, naming the
criterion, even though the success signal (field accuracy ≥ 95 %) is also `MET`: rule 1 wins.
</example>

<example>
Contract: success signal "95 % field accuracy". Evidence array empty; the repo has a working
pipeline and a README claiming "accuracy looks great". Verdict: success signal `UNMEASURED`
(the README is an opinion, not evidence), every kill criterion `UNMEASURED`, the empty evidence
trail reported first. Within the box → `EXTEND`, naming the measurement: run the 200-invoice
sample and record accuracy with its source.
</example>

<example>
Contract ends 2026-03-01; today is 2026-03-09; accuracy evidence shows 91 % against a 95 %
threshold. Verdict: time box 8 days past, so the time-box kill criterion is `MET`; success signal
`NOT MET` with the measured value shown. Recommendation `KILL`; a user who wants to continue
writes a new contract with a new box.
</example>
