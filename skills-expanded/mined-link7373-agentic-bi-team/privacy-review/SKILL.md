---
name: privacy-review
description: Review a new data source, model, dashboard, or analysis that touches personal data before it is built — purpose, minimisation, classification, audience, retention, and regime-specific obligations — or handle a data-subject request (access, deletion, correction, opt-out). Use before connecting a source with personal data, before a model scores people, before widening an audience, and whenever someone asks "are we allowed to do this?".
---

# Privacy Review

Owner: `governance-officer`, with the owning agent for the thing under review. Args name the subject, e.g. `/privacy-review churn model using support ticket text`, or `/privacy-review request: delete customer 4417`.

This is a short, structured assessment, not a legal opinion. It exists so the privacy question is asked while changing the design is still cheap — and so the answer is written down. Where a regime pack says a privacy professional must decide, this skill stops and says so.

Read `knowledge/governance-policy.md` first. If `regimes:` lists any, read `standards/privacy/<regime>.md` for each — they add questions to Mode A step 6.

## Mode A — Review a new use (default)

1. **Describe the use in one paragraph.** What is being built, from which tables, for whom, to drive what decision. If you cannot say what decision it drives, that is the first finding.

2. **Screen.** Does it involve data about identifiable people — customers, users, employees, patients, leads? Check the tables against the Column Registry and sweep for unregistered personal columns (`python scripts/check_governance.py`). **If no personal data is involved, record "screened out" in the decision log and stop.** Most BI work ends here, and that is the right outcome.

3. **Purpose.** Was this data collected for this use, or a compatible one? Billing data used for revenue reporting: yes. Support-ticket text used to score employees: a new purpose. A new purpose is the user's decision, not the team's — and under most regimes needs more than a decision.

4. **Minimise — redesign before you approve.** For each personal column, ask what breaks without it:
   - Can the question be answered with a count, a rate, or a bucket?
   - Can the join use a surrogate key in place of an identifier?
   - Can dates become months, ages become bands, postcodes become regions?
   - Is free text needed at all? It contains everything, and nobody has classified it.

   The best outcome of a review is a design that no longer needs one.

5. **Audience and exposure.** Who sees the output, at what grain? Apply `min_group_size`, then check the indirect routes: differencing between two views, filters that intersect down to one person, quasi-identifiers in combination. Does the output leave the approved export destinations?

6. **Regime questions.** For each enabled regime, work through the "review questions" section of its pack. Anything it marks as needing a privacy professional — record it as **open, owner: privacy contact** and do not proceed past design on that item.

7. **If it is a model that scores or decides about people,** add: what happens to someone the model is wrong about? Who can override it? Which groups could it treat differently, and how will that be measured (`analytics.md` Part 1, fairness impossibility)? Is the person told? Record the risk tier:
   - **minimal** — aggregate forecasting, no individual decisions
   - **limited** — ranks or segments people; a human decides
   - **high** — materially affects access to a service, price, credit, employment, or health. Needs explicit user sign-off and, under most regimes, a formal assessment by a privacy professional.

8. **Retention and deletion.** Where do extracts, features, and scored outputs live, and when are they deleted? If a person is deleted from the source, does this artifact still hold them?

9. **Write it down.** `PRIVACY-REVIEW.md` in the artifact's own folder (`models/<name>/`, `dashboards/<name>/`, `pipelines/<name>/`, or the analysis folder):
   - **Verdict:** proceed · proceed with conditions · do not proceed · needs a privacy professional
   - The use, the personal data involved, and its classification
   - What was removed or reduced in step 4
   - Conditions (suppression, audience limits, retention date, human override)
   - Open items and their owners
   - Review date — a review is of a design, and designs change

10. **Update the policy.** New columns into the Column Registry; standing permissions into the Exceptions Log with an expiry; the ruling into `knowledge/decision-log.md`. Run `python scripts/check_governance.py`.

## Mode B — Data-subject request

A person asks what is held about them, or asks for it to be deleted, corrected, or not sold or shared. These have legal deadlines under most regimes; say which applies from the regime pack, and treat the clock as started.

1. **Confirm the request came through the proper channel** and that identity was verified by whoever owns that process. The team does not verify identity and does not act on a request relayed informally.
2. **Locate.** Using the identifier supplied, list every table that holds the person: start from the Column Registry and the cross-source join keys in `knowledge/data-sources.md`, then check derived marts, model feature tables, scored outputs, and local extracts. Queries that read restricted columns need the override marker with the request reference as the reason (`/* AGENTIC_BI_ALLOW_RESTRICTED: DSAR <ref> */`); under `strict` enforcement a person runs them.
3. **Report, do not act.** Produce the location report: system, table, what is held, whether it is a source or a derived copy, and what deletion or correction would cascade to. **The team never deletes or alters personal data itself** — the destructive-SQL hook blocks it, and a human with authority executes the change in the source system.
4. **Check what regenerates.** A deletion that the next pipeline run restores from an upstream copy is not a deletion. Name every upstream source and backup the owner must also handle, and any aggregate small enough that the person remains identifiable in it.
5. **Keep the record minimal.** Log in `knowledge/decision-log.md`: the request reference, date, type, and completion date. Never the person's identity or their data — the log must not become a new copy of what was deleted.

## What this skill does not do
- It does not give legal advice or decide a legal basis.
- It does not replace warehouse access control. A review that concludes "the team should not read this column" is implemented with a grant, and backed up by the query guard.
- It does not approve by default. No answer from the user on a "needs your decision" item means not approved.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
