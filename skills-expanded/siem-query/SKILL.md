---
name: siem-query
description: SIEM query-builder workflow — Splunk SPL, Microsoft Sentinel/Defender KQL, Elastic EQL/KQL, with cross-translation patterns, performance tuning (data models, summary indexes, CCS), and query-by-detection-need. Source layer for detection-engineer, log-triage, and threat-hunt.
---

# SIEM Query Builder

> **Performance discipline**: a correct query that does not return in reasonable time is operationally unusable. A lot of SOC time is lost in queries that scan unnecessarily much data. The second half of this skill is performance discipline, not just syntax.

## When to use

This skill is the tooling substrate underneath `detection-engineer` (rules), `log-triage` (incident investigation), `threat-hunt` (proactive), and `ioc-hunter` (enrichment queries).

Triggers on:

- A question like "write an SPL for X", "translate this KQL into EQL", "why is my query slow", "which index for this data", "set up a summary index".
- Cross-platform migration or a multi-platform organization where the same detection logic must exist in both.
- Performance tuning of existing queries that are too slow for real-time alerting.
- Setting up data models (Splunk CIM, Sentinel ASIM/Watchlist, Elastic ECS) for a consistent schema across sources.

### When NOT (handoff)

- Detection-rule design and lifecycle → `detection-engineer`, `alert-tuning`. This skill provides query building blocks; those skills handle the lifecycle.
- Triage of live alerts/events → `log-triage`. This skill provides the query; that one analyses the result.
- IOC-feed management and threat-intel enrichment → `ioc-hunter`.
- Threat-hunt hypothesis design → `threat-hunt` (command).
- Forensic depth → `forensics-assist`.
- Log-pipeline engineering (collection, parsing, enrichment) → ops team. This skill works with data as the SIEM presents it.

## Approach

Six phases. Phase 3 (cross-translation) and phase 4 (performance) are where SIEM time really sits.

### 1. Tool and context

Three mainstream platforms in most organizations:

- **Splunk Enterprise / Cloud** — SPL (Search Processing Language). Pipe-style, function-rich, powerful on mass data with an indexer/search-head architecture.
- **Microsoft Sentinel + Microsoft Defender XDR** — KQL (Kusto Query Language). Modern, fast, strong join and aggregation syntax. Sentinel = log-source side, Defender XDR = endpoint side; shared query language.
- **Elastic Security** — EQL (Event Query Language) for sequence detection, KQL/Lucene for search filters, ESQL as the newer unified language. Lots of tooling around the Elastic Common Schema (ECS).

Other stacks: IBM QRadar (AQL), Sumo Logic, Chronicle (YARA-L), Devo. Concepts overlap, syntax differs.

For each query task, the first question: which platform is the target? Which retention window? Which data model? Which time zone in the events?

### 2. Query-construction patterns

The canonical shapes per platform:

**Splunk SPL**:

```spl
index=cloudtrail eventName=ConsoleLogin
  | where 'additionalEventData.MFAUsed'="No"
  | stats count by userIdentity.userName, sourceIPAddress
  | where count > 5
```

Pipeline mindset: filter first (`index=`, `sourcetype=`), then transform (`stats`, `eval`, `lookup`), then present (`table`, `chart`).

Powerful features: `tstats` (data-model acceleration), `transaction` (event correlation), `dedup`, `streamstats` (running aggregates), `lookup` (CSV/KV-store enrichment), `metasearch` (metadata only, faster).

**Sentinel/Defender KQL**:

```kql
SigninLogs
| where ResultType == 0 and AppDisplayName == "Office 365"
| where ConditionalAccessStatus == "success"
| summarize SignInCount = count() by UserPrincipalName, IPAddress, bin(TimeGenerated, 1h)
| where SignInCount > 10
```

Pipeline here too (`|`-style). Strengths: `summarize` with `bin()` for time bucketing, `join kind=` for different join types, `let` for variables, materialize for caching.

Multi-table join: `union`, `join`, `lookup`. ASIM (Advanced SIEM Information Model) for cross-source normalization.

**Elastic EQL** (sequence-aware):

```eql
sequence by host.id with maxspan=5m
  [process where event.action == "fork" and process.name == "bash"]
  [network where event.action == "connection_attempted" and destination.port == 4444]
```

EQL is unique in its out-of-the-box support for event sequences. For ad-hoc searching, KQL/Lucene/ESQL is more practical.

Consistent ECS field names: `event.action`, `process.name`, `host.id`, `user.name`. Migration of non-ECS data is a separate task.

### 3. Cross-translation patterns

The three languages are semantically similar but differ in syntax. Pattern per category:

| Concept | SPL | KQL | EQL/KQL-Elastic |
|---|---|---|---|
| Filter exact | `field="value"` | `field == "value"` | `field == "value"` |
| Wildcard | `field=value*` | `field has "value"` | `field : value*` |
| Negation | `NOT field=val` | `field != "val"` | `not field == "val"` |
| Time bucket | `bin _time span=1h` | `bin(TimeGenerated, 1h)` | `histogram(@timestamp, fixed_interval=1h)` |
| Group-by-count | `stats count by field` | `summarize count() by field` | aggregations API |
| Distinct count | `dc(field)` | `dcount(field)` | cardinality |
| Top-N | `top N field` | `top N by count_` | top-hits |
| Join | `join field [...]` | `T1 \| join T2 on field` | enrich pipeline |
| Lookup | `lookup file field` | `lookup table on field` | enrich processor |

`sigma-cli` with the right backend (see `detection-engineer`) automates much of this. The reviewer role remains: check edge cases (field-name mapping, semantic difference between `wildcard` and `contains`).

### 4. Performance tuning

A correct-but-slow query is operationally not usable. Top categories:

- **Index/scope filtering first**. SPL: `index=` directly. KQL: table-specific (`SigninLogs`, not `union *`). Elastic: tighten the index pattern.
- **Time-range discipline**. Default last 24h, not "all time". Every extension deliberate.
- **Avoid eager field extraction**: SPL `extract` on mass data is expensive — use regex-extracted fields at index time where possible.
- **Subsearches to a minimum**. SPL subsearches run a separate search and have a default 10k-result limit. KQL `let` with materialize is often more performant.
- **Use data models** (Splunk CIM, Sentinel ASIM, ECS). A `tstats` against an accelerated CIM data model is orders of magnitude faster than equivalent search-time extraction.
- **Summary indexes / scheduled saved searches** for recurring aggregations. Do not recompute the same hourly count from scratch — roll up once per hour.
- **Cross-cluster search (CCS)** in Splunk and Elastic: deliberate about whether you want to span clusters. Latency cost.
- **JOIN cost**: in KQL `join`, order matters; smaller table on the left. Elastic's enrich pipeline at index time is often better than a query-time join.
- **Result cardinality**: a query that returns 10M rows in order to show 100 has a forgotten filter.

Profiling help:

- Splunk: the `Search Job Inspector` shows per-stage time. `tstats` vs raw-search comparison.
- Sentinel/Defender: query-takes-long warnings + `set notruncation=true` debug, `evaluate execute_query_stats(...)`.
- Elastic: profile API for the query-execution plan.

### 5. Library management

Well-built queries are reusable. Discipline to keep them that way:

- **Detection-as-code repo** with Sigma rules + transpiled queries + saved searches in version control. Not just in the SIEM UI.
- **Macros / functions / saved searches**: SPL macros, KQL functions (`function` keyword), Elastic painless scripts. Reuse per common sub-pattern (define "what is a suspicious LSASS access" once, use it in N rules).
- **Naming convention**: prefix pattern for saved searches (`sec_`, `hunt_`, `dashboard_`) so the purpose is immediately clear.
- **Documentation per query**: purpose, owner, last-tested date, FP notes. In the commit message or comment block.

### 6. Verification-loop

Layer 1: scope (query covers all relevant fields + time window, no unintended scope creep through wildcard table selection?), assumptions (data model up to date, schema fields exist?), gaps (FP path checked, not just the TP path?). Layer 2: function names against current platform docs (KQL and SPL add and deprecate functions), no invented table names or field syntax, time-bucket syntax correct, performance claims supported by profiling output.

## Output

```
Query package — <goal>
Platform target: <Splunk SPL | Sentinel KQL | Defender KQL | Elastic EQL/KQL | multi>
Data source(s):  <indexes / tables / index patterns>
Time window:     <default + customizable>

Query (primary):
  <full query text>

Translations (multi-platform):
  Splunk SPL: <...>
  KQL:        <...>
  EQL:        <...>

Performance profile:
  Test run:        <events scanned, runtime>
  Bottleneck:      <field extraction / subsearch / join / etc>
  Optimization applied: <data model / summary / index filter>

Edge cases / FPs:
  - <known FP pattern, how to filter>
  - <field-name issues when translating between platforms>

Library integration:
  Saved as:                <macro/function/saved-search name>
  Detection-as-code path:  <repo path>

Handoffs:
  detection-engineer:  <if query becomes the basis for a rule>
  log-triage:          <if query is for incident investigation>
  threat-hunt:         <hunt context>

Verification-loop: ...
```

## References

- **Splunk Search Reference** — [https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/). Full SPL reference.
- **Splunk Common Information Model (CIM)** — [https://docs.splunk.com/Documentation/CIM/latest/User/Overview](https://docs.splunk.com/Documentation/CIM/latest/User/Overview). Cross-source data model.
- **Microsoft KQL quick reference** — [https://learn.microsoft.com/en-us/azure/data-explorer/kql-quick-reference](https://learn.microsoft.com/en-us/azure/data-explorer/kql-quick-reference).
- **Microsoft Sentinel ASIM** — [https://learn.microsoft.com/en-us/azure/sentinel/normalization](https://learn.microsoft.com/en-us/azure/sentinel/normalization). Cross-source normalization for Sentinel.
- **Microsoft Defender XDR Hunting** — [https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-overview](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-overview).
- **Elastic Security Reference** — [https://www.elastic.co/guide/en/security/current/](https://www.elastic.co/guide/en/security/current/).
- **Elastic Common Schema (ECS)** — [https://www.elastic.co/guide/en/ecs/current/index.html](https://www.elastic.co/guide/en/ecs/current/index.html). Field-naming standard.
- **Elastic ESQL** — [https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html). Newer unified query language.
- **Sigma project** — [https://github.com/SigmaHQ/sigma](https://github.com/SigmaHQ/sigma). Source of truth for cross-platform rules.
- **uncoder.io** — [https://uncoder.io/](https://uncoder.io/). Browser tool for cross-platform query translation; always verify the output.

## Categories

- blue
