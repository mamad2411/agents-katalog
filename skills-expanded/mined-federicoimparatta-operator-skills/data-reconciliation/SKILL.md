---
name: data-reconciliation
description: Use this skill when the user asks to reconcile two or more sources that report different numbers for what should be the same metric, resolve a disagreement between a dashboard and a database query, or debug why two reports do not tie. Trigger phrases include "why do these numbers disagree", "reconcile these reports", "the dashboard does not match the database", "tie out these totals", "reconciliar los números", "por qué no coinciden", "audit these metrics". Produces a reconciliation report that names the root cause and the fix, not just the variance.
---

# data-reconciliation

> **Anchor:** When two sources disagree, the gap is the product. The numbers are symptoms.

## When to use

Use this skill when the user has two or more sources that should report the same thing but do not. Works for:

- A dashboard number that does not match a database query.
- Two dashboards that report the same metric differently.
- A finance close that does not tie to the product analytics.
- A customer's numbers that do not match the vendor's numbers.
- A monthly metric that used to match and suddenly does not.

Do not use when:

- The user is defining a metric from scratch. Use `analytics-instrumentation` or `dashboard-spec`.
- The user is debugging a pipeline outage. That is an incident, not a reconciliation.
- The user already knows the cause and wants a fix. That is an engineering task.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: schema, join, filter, timezone, cutoff, source of truth, cohort, window, GMV, MRR, churn, baseline, ingestion, pipeline.
- **EN.** Direct US business register.
- Column names, SQL, and metric names stay in the original casing and language of the data model.

## Method

### Step 1. Write the disagreement precisely

A fuzzy disagreement produces a fuzzy reconciliation. Write:

- **Metric name.** What the two sources claim to measure.
- **Source A.** Name, query or view, value reported.
- **Source B.** Name, query or view, value reported.
- **Window.** Exact start and end timestamps.
- **Scope.** What is in and out.
- **Magnitude of the gap.** Absolute and relative.

If the sources cannot be named with a query or view, stop. The user does not know what they are comparing yet.

### Step 2. Check the schema

Before looking at data, confirm both sources are structurally comparable.

- **Columns.** Same semantic fields with the same names or with explicit mapping.
- **Types.** Same types, or explicit casts.
- **Units.** Dollars vs. cents. Minutes vs. seconds. User events vs. session events.
- **Grain.** One row per what. User, account, event, line item, invoice.

Most reconciliation failures are schema mismatches the user did not realize. Find them here before doing math.

### Step 3. Check the time

Time is the source of more reconciliation bugs than any other axis.

- **Timezone.** UTC vs. local. Sources often default differently.
- **Window definition.** Inclusive vs. exclusive endpoints. "This month" has at least four reasonable definitions.
- **Cutoff.** When the window was queried. A late-arriving row can move a total.
- **Freshness.** The time between the event happening and the source seeing it.

Write the exact time predicate used on each side. Two predicates that sound the same often are not.

### Step 4. Check the definition

The most expensive gap in practice is definitional drift.

For each metric, write the plain-language definition each source implements:

- **Event or entity counted.** What qualifies.
- **Filters applied.** Explicit and implicit. Implicit filters are the killers. Examples: the dashboard excludes internal test accounts; the database query does not. The dashboard joins an is-paying flag; the query does not.
- **Deduplication.** What happens with double-fires, retries, reprocessed rows.
- **Aggregation.** Sum, count distinct, first, last, max.

If the two definitions are not the same, reconciliation stops here. Either align the definitions or document the drift as an accepted divergence with a named reason.

### Step 5. Check the filters and joins

- **Implicit filters.** Soft-deletes, is-active flags, tenant isolation, role scoping, default dashboard filters the user forgot about.
- **Join semantics.** Inner vs. left vs. outer. Nullable fields that silently drop rows.
- **Partition or cluster keys.** Queries against different partitions or periods can produce different totals for the same nominal window.

### Step 6. Sample and compare

Once schema, time, and definition look the same, compare specific records.

- Pull a small identifiable set from each source.
- Find overlap, difference, and duplicates.
- For records only in one source, find why.

A sample-based comparison produces concrete failures faster than pushing more aggregate queries.

### Step 7. Name the root cause

Reconciliation without a root cause is noise. The output of this method is a single-sentence statement of why the sources disagree.

Common categories:

- **Definition drift.** Sources implement different definitions of the same name.
- **Time drift.** Same definition, different time boundaries.
- **Filter drift.** Same definition, different implicit filters.
- **Ingestion lag.** One source sees rows the other has not yet received.
- **Deduplication gap.** One source double-counts.
- **Schema mismatch.** Same field name, different meaning.
- **Broken upstream.** The disagreement is a symptom of an actual bug, not a definition issue.

See `references/root-cause-tree.md` for the full set.

### Step 8. Decide the fix

Four fixes, named explicitly:

- **Align the definitions.** Change one side to match the other. Note which.
- **Declare a source of truth.** Name it, and mark the other source as derived or deprecated.
- **Accept a tolerance.** Document the expected gap and the reason. Only appropriate when the gap does not affect decisions.
- **Fix the upstream bug.** Open a ticket, link from the reconciliation report.

"We will investigate further" is not a fix.

### Step 9. Document for next time

Every reconciliation leaves behind a definition diff that makes the next reconciliation faster.

- Metric name.
- Plain-language definition.
- Implementation per source.
- Known gaps and their status.

File this next to the dashboard or the metric catalog, not in a personal doc.

## Templates

- `templates/en/reconciliation-report.md`: full reconciliation report with root cause and fix.
- `templates/en/definition-diff.md`: metric definition comparison for the long-term catalog.
- `templates/es/reconciliation-report.md`: reporte completo de reconciliación con causa raíz y fix.
- `templates/es/definition-diff.md`: diff de definición de métrica para el catálogo.

## Related skills

- `analytics-instrumentation`: use it when defining a metric from scratch, not reconciling two that disagree.
- `dashboard-spec`: use it when the metric needs a view spec, not a variance investigation.
- `post-mortem`: use it when the disagreement turns out to be an incident, not a definition gap.

## Anti-patterns

This skill must never produce:

- A report that lists the gap without naming a root cause.
- A reconciliation that calls a mismatch "minor" without measuring it.
- "Within 1%" as a pass without a named tolerance policy.
- A fix of "we will monitor it".
- A root cause that is actually a symptom.
- A report that ignores the timezone or cutoff.
- A conclusion that requires future investigation without naming who and by when.

## Checklist before delivery

- [ ] The disagreement is written with exact values, sources, window, and scope.
- [ ] Schema comparison is explicit.
- [ ] Time predicates are written out for both sides.
- [ ] Definitions are stated in plain language per source.
- [ ] Filter and join semantics are compared.
- [ ] A sample-based comparison has been done.
- [ ] A root cause is named in one sentence.
- [ ] A fix is decided from the four named options.
- [ ] A definition diff is filed for future reference.
- [ ] No buzzwords from the voice rules appear.
