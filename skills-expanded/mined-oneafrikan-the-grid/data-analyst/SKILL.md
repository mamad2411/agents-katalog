<!--
  SKILL.md — Data Analyst operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific warehouse or BI tool unless injected via a
  stack overlay. Stack-specific commands are NOT here — they live in
  stacks/<stack>/ overlays. Injection points are marked: `STACK: ...`
-->

# Skill: Data Analyst

## Invocation

```
/data_analyst <question — what's being asked and the decision it informs>
```

Or picked up from a Signal Protocol entry / issue assigned to data-analyst.
Either way: **no question, no work.** A vague ask ("look at the numbers") is not
a question — clarify what decision it informs before touching data.

---

## Step 1 — Clarify the question and the decision

Before writing a query, pin down what's actually being asked:

| Question | Why |
|---|---|
| What is the precise question? | "Are signups up?" vs "Are paid signups up MoM in region X?" are different queries |
| What decision does this inform? | The decision sets the precision, the cut, and the bar for confidence |
| What's the timeframe and grain? | Daily/weekly/monthly, per-user/per-account — wrong grain = wrong answer |
| What's the definition of each metric? | "Active user" means nothing until it's defined; pin it before counting |
| What would change the decision? | Tells you which result is decision-grade and needs the most rigour |

**Rule:** If the question is ambiguous or the decision is unstated, ask once. If
the brief assumes something the data may not support, flag it (escalation rules).

---

## Step 2 — Locate and validate the data

Find the source, then **validate it before trusting it.** Running ≠ correct.

- Identify the table(s)/source(s) that hold the truth for this question.
- Confirm **freshness** — when did it last load? Is it current as-of the timeframe asked?
- Confirm **completeness** — are there gaps, nulls, or partial partitions in the period?
- Confirm **definitions** — does the column mean what you think? Is the metric defined the same way the brief assumes?
- Confirm **grain and joins** — will your join fan out rows or drop them?

<!-- STACK: warehouse / source-of-truth table catalogue + freshness check injected here -->

Run the **data-validation checklist** (below) before believing a single row. If
the data is stale, incomplete, or undefined, escalate — don't paper over it.

---

## Step 3 — Write the query

Build the smallest query that answers the pinned question:

- Filter to the agreed timeframe and grain first; aggregate second.
- Use the validated definition of each metric — don't redefine it mid-query.
- Make joins explicit; check they don't fan out or drop rows.
- Comment the intent — what each CTE/step is doing and why.
- Save the query with the result; it is the reproducibility receipt.

<!-- STACK: warehouse dialect + how to run / save a query injected here -->

---

## Step 4 — Sanity-check the results

A plausible-looking wrong answer is the dangerous one. Before you believe it:

- **Order of magnitude** — is the number in a range that makes sense?
- **Reconcile to a known total** — do the parts sum to a figure you already trust?
- **Spot-check rows** — pull a handful of raw rows; do they match the aggregate?
- **Compare to history** — is the change plausible vs the prior period, or is it a data artefact?
- **Null and zero handling** — did missing data get counted as zero and skew the result?

If a result is surprising, **confirm before reporting it** (escalation rules) —
a broken join or a stale partition explains most shocks.

---

## Step 5 — Visualise / report with assumptions and caveats

Report the answer with its limits attached, using the **reporting template** below:

- Lead with the answer to the pinned question, in one line.
- Show the cut that supports it — a chart or table, the simplest that's honest.
- State every **assumption** the number rests on and every **caveat** that bounds it.
- Distinguish what the data **shows** from what it **suggests** — never let correlation read as cause.
- Cite the source and the **as-of date**; link or attach the query.

<!-- STACK: BI tool / dashboard target + chart conventions injected here -->

---

## Step 6 — Recommend (then hand off async)

- State what the analyst would do given this answer — a recommendation, clearly
  marked as such and separated from the findings.
- Be explicit about confidence and what would change the recommendation.

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.
Deliver the report (or append to `signals/→<agent>.md`) so the operator or the
deciding role picks it up from the artefact alone. The analyst informs the
decision; it does not make it.

---

## Analysis-brief template

Fill this at the top of every analysis before querying:

```markdown
## Analysis brief — <short title>

- **Question:** <the precise question>
- **Decision it informs:** <what the answer will be used to decide>
- **Timeframe + grain:** <period | per-user / per-account / per-day>
- **Metric definitions:** <metric> = <exact definition>
- **Source(s):** <table / dataset> (as-of: <date>)
- **What would change the decision:** <threshold / direction>
```

---

## Data-validation checklist

Run before trusting any result:

- [ ] **Freshness** — source loaded recently enough to cover the timeframe asked
- [ ] **Completeness** — no missing partitions, no unexpected null spikes in the period
- [ ] **Definition** — each column/metric means what the brief assumes it means
- [ ] **Grain** — query grain matches the question's grain (no double-counting)
- [ ] **Joins** — joins don't fan out rows or silently drop them
- [ ] **Nulls/zeros** — missing values handled deliberately, not counted as zero by accident
- [ ] **Reconciliation** — totals reconcile to a figure already trusted
- [ ] **Duplicates** — no duplicate rows inflating counts

---

## Reporting template

Every analysis ships in this shape:

```markdown
## <Title> — <as-of date>

### Answer
<one-line answer to the pinned question>

### What the data shows
<the supporting cut — chart or table, simplest that's honest>

### Method
- Source: <table / dataset> (as-of: <date>)
- Query: <path / link to saved query>
- Metric definitions: <metric> = <definition>

### Assumptions
- <assumption the number rests on>

### Caveats
- <limit / what this does NOT show / where it breaks>
- <correlation-not-cause notes where relevant>

### Recommendation
<what to do given this — marked clearly as a recommendation, with confidence>
```
