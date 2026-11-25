---
name: triage
description: Classify, size, route, and log an incoming BI request — decide what kind of work it is, what decision it serves, who on the team does it, and whether it should be done at all. Use as the front door for any request that isn't obviously one thing, and for anything arriving from outside the team.
---

# Triage — The Front Door

Real BI teams don't fail because the analysis is bad. They fail because forty
undifferentiated requests arrive, everything is urgent, nothing is written down, and the
same question gets answered three times by three people with three different numbers.

This skill is the front door. It costs two minutes and routinely saves a day.

Use it when a request is vague, large, arriving from outside the team, or one you suspect
has been answered before. Skip it for something you can answer in one query — running
triage on "how many customers signed up yesterday?" is its own kind of waste.

## Procedure

### 1. Find the decision

Ask the one question that matters: **what will you do differently depending on the
answer?**

If there's a clear answer, everything else gets easier — you know when to stop, what
precision is enough, and what to lead with. If there genuinely isn't one, that's the most
valuable thing triage produces: some requests are curiosity (fine, but they queue behind
decisions) and some are a reflex nobody has questioned since a reorg. Say so kindly and
ask whether it's still needed.

Also establish **when the decision gets made**. A perfect answer after the meeting is
worth nothing, and a rough answer with stated uncertainty before it is worth a lot. If
the deadline forces a shortcut, agree the shortcut now rather than discovering it later.

### 2. Check whether it's already answered

Before classifying, look:

- `analyses/README.md` — has this question been investigated?
- `knowledge/metrics-catalog.md` — is the metric already defined? (If the request implies
  a *new* definition for an existing metric, stop and route to `metrics-steward`.)
- `dashboards/README.md` — does a dashboard already show this?
- `knowledge/request-log.md` — has someone asked this recently?

A request that has been asked three times is not a fourth analysis. It's a dashboard or a
mart, and saying so is a better answer than doing the work again.

### 3. Classify

| Type | Looks like | Routes to |
|---|---|---|
| **Question** | "how many", "why did", "which segment" | `bi-analyst` → `/analyze` |
| **Incident** | a number looks impossible, a report is blank, a pipeline failed | `data-quality-engineer` → `knowledge/incident-runbook.md` |
| **Metric dispute** | two sources disagree, "what counts as active?" | `metrics-steward` → `/define-kpis` |
| **Recurring view** | "can I see this every week" | `dashboard-developer` → `/build-dashboard` |
| **New data** | "can we analyse X" where X isn't in the warehouse | `data-engineer` → `/build-pipeline` |
| **Performance** | "this query takes forever", "the dashboard is slow" | `analytics-engineer` |
| **Prediction** | "who will churn", "which accounts will upgrade" | `data-scientist` → `/build-model` |
| **Forecast** | "what will revenue be next quarter", "how much capacity will we need" | `data-scientist` → `/forecast` |
| **Impact / causal** | "did the price change cause the churn", "what was the launch worth" | `data-scientist` → `/causal-analysis` (or `/experiment` if the change has not happened yet) |
| **Privacy / permission** | "are we allowed to use this data", a new source with personal data, an access or deletion request | `governance-officer` → `/privacy-review` |
| **Is the team right?** | "that number was wrong", "can we trust these answers" | orchestrator → `/eval` (a correction becomes `/eval add`) |
| **Deliverable** | "I need this for the board on Thursday" | `insights-communicator` → `/make-deliverable` |

Two classification traps worth naming, because both are common:

- **An incident dressed as a question.** "Why did revenue drop 40% yesterday?" is usually
  a data incident, not an analysis. Check freshness before commissioning a deep dive —
  about half of these are a stale table, and the analysis time is wasted.
- **A dashboard request that's really one question.** "Can I get a dashboard for X" often
  means "I need to know X once." Ask whether they'll look at it again next week. A
  dashboard nobody opens costs refresh, maintenance, and a chance to be wrong forever.

### 4. Size it

Rough and honest beats precise and late:

- **S** — under an hour. One query against known tables.
- **M** — under a day. Multiple sources, some new logic, a written finding.
- **L** — multiple days. New pipeline, new model, a dashboard, or cross-source joins with
  unverified keys.
- **XL** — over a week, or blocked on access, data that doesn't exist, or a decision
  nobody has made.

For anything L or larger, **offer the S version first**. A rough cut today usually
answers the actual decision, and if it doesn't, it tells you exactly what the full version
needs to cover. Say what the cheap version would and wouldn't tell them.

### 5. Prioritise honestly

Rank against what's already in flight, using: the size of the decision, whether the
deadline is real, whether anything is blocked on it, and how much it costs.

Then **say what it displaces.** "Yes, by Thursday" is not a commitment unless you also say
what moves. Everything-is-priority-one is how a BI team becomes a queue nobody trusts —
and the standing cadence (scorecards, health checks) does not get displaced by ad-hoc
work, because it's the thing that catches problems nobody asked about.

### 6. Log it and hand off

Add a row to `knowledge/request-log.md`: date, requester, the request, the decision it
serves, type, size, routed-to, and status. This is the record that lets anyone answer
"what does the BI team actually spend its time on" three months from now — and the
recurring-request pattern in it is the best guide there is to what should become a
dashboard or a mart.

Then hand off with the framing intact: the specialist should receive the *decision*, the
deadline, and what's been ruled out — not just the original words. Restating the request
is the cheapest quality step in the whole workflow.

## Reviewing the log

Every month or so, read `knowledge/request-log.md` as a dataset rather than a list:

- Which questions recur? Those are marts and dashboards waiting to be built.
- Which requesters dominate, and is that the right allocation against the company's
  priorities?
- What did the team promise and miss, and why? A pattern of misses is a sizing problem,
  not an effort problem.
- What was delivered and never used? Worth knowing before building more of it.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
