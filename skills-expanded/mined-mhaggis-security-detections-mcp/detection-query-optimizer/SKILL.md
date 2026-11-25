---
name: Detection Query Optimizer
description: Optimize detection queries for performance across Splunk (SPL), Microsoft Sentinel (KQL), and Elastic Security (EQL/ES|QL). Covers search pipeline internals, common anti-patterns, and optimization techniques for detection rules on each platform.
---

# Detection Query Optimizer Skill

## Overview

Every SIEM processes queries differently. Understanding the execution model is essential for writing detections that run fast enough for scheduled execution without excessive resource consumption. This skill covers optimization for the three major query languages.

**Set `$SIEM_PLATFORM`** to focus guidance: `splunk`, `sentinel`, `elastic`

## Quick Reference: Which Section?

| Platform | Query Language | Section |
|----------|---------------|---------|
| Splunk Enterprise / Cloud | SPL | [SPL Optimization](#spl-optimization-splunk) |
| Microsoft Sentinel / Defender | KQL | [KQL Optimization](#kql-optimization-microsoft-sentinel) |
| Elastic Security | EQL / ES\|QL | [EQL/ES\|QL Optimization](#eqlesql-optimization-elastic-security) |
| Sigma | N/A | Optimization happens at the backend/compiler level. Write clean Sigma; let pySigma optimize for the target. |

---

## SPL Optimization (Splunk)

### The Splunk Search Pipeline

Every SPL search flows through these phases:

```
[Input] → [Parsing] → [Search (Map/Reduce)] → [Reporting] → [Output]
```

### Phase 1: Input (Index Selection)

The search head determines which indexes and buckets to read.

**Optimizations:**
- Specify `index=` explicitly (never rely on default index)
- Specify `sourcetype=` to narrow bucket scanning
- Use `earliest=` and `latest=` to limit time range
- Use `host=` or `source=` if applicable

```spl
// BAD — scans all default indexes
sourcetype=WinEventLog EventCode=4688

// GOOD — targets specific index
index=wineventlog sourcetype=WinEventLog:Security EventCode=4688
```

### Phase 2: Search (Map Phase)

Indexers scan buckets and return raw events matching search terms.

**Key concept: Bloom filters and tsidx.**
Splunk uses bloom filters for fast negative lookups and tsidx files for field indexing. Raw text terms in the search string hit bloom filters; field=value pairs hit tsidx if the field is indexed.

**Optimizations:**
- Put the **most restrictive terms first** — they filter out more events earlier
- Use indexed fields (`index`, `sourcetype`, `source`, `host`) before extracted fields
- Add raw text terms that must appear in matching events

```spl
// BAD — extracted field first, no index specification
| search process_name="powershell.exe" index=endpoint

// GOOD — indexed fields first, raw term for bloom filter
index=endpoint sourcetype=sysmon EventCode=1 powershell.exe
| where process_name="powershell.exe"
```

### Phase 3: Reporting (Reduce Phase)

Transforming commands (`stats`, `timechart`, `chart`, `top`, etc.) aggregate results.

**Optimizations:**
- Push `stats` as early as possible to reduce event volume
- Use `by` clauses to let indexers do partial aggregation
- Prefer `stats` over `transaction` (10x+ faster for most use cases)

### SPL Optimization Techniques

#### 1. Use tstats for Data Model Searches

`tstats` queries accelerated data models and is dramatically faster than raw search.

```spl
// SLOW — raw search with field extraction
index=endpoint sourcetype=sysmon EventCode=1
| stats count by Image, ParentImage

// FAST — tstats against accelerated data model
| tstats count from datamodel=Endpoint.Processes
  where Processes.process_name="powershell.exe"
  by Processes.process_name, Processes.parent_process_name
```

#### 2. Avoid Leading Wildcards

Leading wildcards (`*something`) defeat bloom filter optimization.

```spl
// SLOW — leading wildcard, full scan required
index=endpoint process_name=*powershell*

// FAST — trailing wildcard, bloom filter can help
index=endpoint process_name=powershell*
```

#### 3. Replace Transaction with Stats

`transaction` is expensive because it must group events by time ordering.

```spl
// SLOW — transaction groups events by session
index=web sourcetype=access_combined
| transaction clientip maxspan=30m

// FAST — stats can achieve similar results
index=web sourcetype=access_combined
| stats earliest(_time) as start, latest(_time) as end,
        values(uri_path) as pages, count
  by clientip
| eval duration=end-start
```

#### 4. Filter Early, Aggregate Late

Every command in the pipeline processes all events passed to it. Reduce event count as early as possible.

```spl
// SLOW — extracts fields then filters
index=endpoint sourcetype=sysmon
| rex field=_raw "CommandLine=(?<cmdline>[^\r\n]+)"
| search cmdline="*-encoded*"

// FAST — filter with raw text first, then extract
index=endpoint sourcetype=sysmon EventCode=1 "-encoded"
| rex field=_raw "CommandLine=(?<cmdline>[^\r\n]+)"
| search cmdline="*-encoded*"
```

#### 5. Use Lookup Efficiently

```spl
// SLOW — lookup on every event
index=endpoint sourcetype=sysmon EventCode=1
| lookup malware_hashes hash AS SHA256 OUTPUT is_malicious
| where is_malicious="true"

// FASTER — drop unneeded fields first, then lookup
index=endpoint sourcetype=sysmon EventCode=1 
| fields + SHA256, Image, CommandLine, _time
| lookup malware_hashes hash AS SHA256 OUTPUT is_malicious
| where is_malicious="true"
```

#### 6. Subsearch Optimization

Subsearches have a result limit (default 10K) and timeout (default 60s). Use `| lookup` alternatives when possible.

```spl
// RISKY — subsearch may hit limits
index=endpoint [search index=threat_intel | fields hash]

// BEST — use lookup command (streaming, no limits)
index=endpoint sourcetype=sysmon EventCode=1
| lookup threat_intel_hashes.csv hash AS SHA256 OUTPUT is_threat
| where is_threat="true"
```

### ESCU Detection Pattern (Standard)

```spl
| tstats `security_content_summariesonly`
  count min(_time) as firstTime max(_time) as lastTime
  from datamodel=Endpoint.Processes
  where Processes.process_name IN ("powershell.exe","pwsh.exe")
        Processes.process IN ("*-EncodedCommand*","*-enc *")
  by Processes.dest Processes.user Processes.parent_process_name
     Processes.process_name Processes.process Processes.process_id
| `drop_dm_object_name(Processes)`
| `security_content_ctime(firstTime)`
| `security_content_ctime(lastTime)`
```

**Why this pattern is fast:**
1. `tstats` hits accelerated data model (pre-indexed)
2. Filters in `where` clause reduce events before aggregation
3. Only needed fields are projected via `by` clause
4. CIM field names ensure portability

### SPL Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| No `index=` specification | Scans all default indexes | Always specify `index=` |
| `| search` as first command | Bypasses index-time optimization | Put terms before first pipe |
| Leading wildcards `*term` | Defeats bloom filters | Use trailing wildcards or raw text |
| `transaction` for simple grouping | Extremely expensive | Use `stats` with `by` clause |
| Unnecessary `| table` in saved search | Adds formatting overhead | Only use in dashboards |
| `| eval` before `| where` | Processes all events | Filter first, compute later |
| Subsearch hitting 10K limit | Silent result truncation | Use lookups instead |
| `NOT` without positive filter | Scans everything then excludes | Add a positive match first |

### SPL Command Cost Reference

| Cost | Commands | Notes |
|------|----------|-------|
| Free | `search` (inline terms) | Hits bloom filter / tsidx |
| Cheap | `where`, `fields`, `rename`, `eval` | Streaming, per-event |
| Medium | `stats`, `chart`, `timechart` | Aggregation, but parallelizable |
| Expensive | `transaction`, `join`, `append` | Memory-intensive, serialized |
| Very Expensive | `| map`, nested subsearches | Sequential execution |

### SPL Performance Measurement

After running a search, use **Job Inspector** (`Job` menu → `Inspect Job`) to see:
- `scanCount` — Total events scanned
- `resultCount` — Events returned
- `execution_time` — Wall clock time
- Component breakdown (input, search, reporting phases)

---

## KQL Optimization (Microsoft Sentinel)

### KQL Execution Model

KQL queries in Sentinel/Defender are executed by the Kusto engine (Azure Data Explorer). The engine:
1. **Parses** the query into a logical plan
2. **Optimizes** the plan (predicate pushdown, column pruning)
3. **Distributes** execution across cluster nodes
4. **Streams** results back

Unlike Splunk, Kusto has a built-in query optimizer, but you can still help it significantly.

### KQL Optimization Techniques

#### 1. Filter Early with `where` Clauses

Put the most selective `where` clauses first. The optimizer pushes predicates down, but explicit early filtering helps.

```kql
// SLOW — processes all events, then filters
DeviceProcessEvents
| extend CommandLower = tolower(ProcessCommandLine)
| where CommandLower has "encodedcommand"
| where Timestamp > ago(1h)

// FAST — time and table filters first, compute later
DeviceProcessEvents
| where Timestamp > ago(1h)
| where ProcessCommandLine has "encodedcommand"
```

#### 2. Use `has` Instead of `contains`

`has` uses the term index (inverted index) and is orders of magnitude faster than `contains`, which does a substring scan.

```kql
// SLOW — substring scan on every row
DeviceProcessEvents
| where ProcessCommandLine contains "mimikatz"

// FAST — term index lookup
DeviceProcessEvents
| where ProcessCommandLine has "mimikatz"

// ALSO FAST — for exact prefix/suffix matching
DeviceProcessEvents
| where FileName =~ "powershell.exe"
```

**When to use which:**
| Operator | Index-Backed | Use When |
|----------|-------------|----------|
| `has` | Yes | Searching for whole terms |
| `has_any` | Yes | Searching for any of several terms |
| `has_all` | Yes | All terms must be present |
| `contains` | No | Substring match needed (e.g., partial path) |
| `startswith` | Partial | Prefix matching |
| `matches regex` | No | Complex pattern matching (slowest) |

#### 3. Minimize `let` Statement Overhead

`let` statements are materialized when referenced. Avoid creating large intermediate tables.

```kql
// SLOW — materializes full table then filters
let AllProcesses = DeviceProcessEvents | where Timestamp > ago(1d);
AllProcesses
| where FileName == "powershell.exe"

// FAST — filter inline
DeviceProcessEvents
| where Timestamp > ago(1d)
| where FileName == "powershell.exe"
```

Use `let` when you need to reference the same dataset multiple times (e.g., join both sides).

#### 4. Prefer `in` Over Multiple `or` Conditions

```kql
// VERBOSE
DeviceProcessEvents
| where FileName == "powershell.exe" or FileName == "pwsh.exe" or FileName == "cmd.exe"

// CLEAN AND FAST
DeviceProcessEvents
| where FileName in ("powershell.exe", "pwsh.exe", "cmd.exe")

// CASE-INSENSITIVE
DeviceProcessEvents
| where FileName in~ ("powershell.exe", "pwsh.exe", "cmd.exe")
```

#### 5. Use `project` to Drop Unneeded Columns

Reducing column count reduces data transferred between nodes.

```kql
// SLOW — carries all columns through the pipeline
DeviceProcessEvents
| where FileName == "powershell.exe"
| join kind=inner (DeviceNetworkEvents) on DeviceId

// FAST — project early to reduce join payload
DeviceProcessEvents
| where FileName == "powershell.exe"
| project DeviceId, Timestamp, ProcessCommandLine, AccountName
| join kind=inner (
    DeviceNetworkEvents
    | project DeviceId, RemoteIP, RemotePort, Timestamp
  ) on DeviceId
```

#### 6. Join Optimization

Joins are expensive. Always put the smaller table on the left.

```kql
// FAST — small result set on left
DeviceProcessEvents
| where FileName == "powershell.exe"
| where ProcessCommandLine has "-enc"
| join kind=inner (
    DeviceNetworkEvents
    | where RemotePort == 443
  ) on DeviceId, $left.Timestamp == $right.Timestamp

// ALTERNATIVE — use lookup for reference data
let MaliciousIPs = externaldata(IP: string) [@"https://..."] with (format="txt");
DeviceNetworkEvents
| where RemoteIP in (MaliciousIPs)
```

#### 7. Use `summarize` Efficiently

```kql
// SLOW — high cardinality summarize
DeviceProcessEvents
| summarize count() by ProcessCommandLine, DeviceName, AccountName

// FAST — reduce cardinality first
DeviceProcessEvents
| where ProcessCommandLine has_any ("encoded", "hidden", "bypass")
| summarize count() by FileName, DeviceName, AccountName
```

### KQL Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| `contains` for whole words | Full substring scan | Use `has` (term-indexed) |
| `matches regex` for simple patterns | No index acceleration | Use `has`, `startswith`, `endswith` |
| No time filter | Scans entire retention | Always add `where Timestamp > ago(Xh)` |
| `*` in project (all columns) | Excess data transfer | `project` only needed columns |
| Large table on left of join | Excessive shuffle | Put smaller table on left |
| Nested `toscalar()` calls | Sequential execution | Materialize with `let` |
| `mv-expand` on large arrays | Row explosion | Filter before expanding |

### KQL Performance Measurement

Use the **Query performance** pane in Log Analytics:
- **CPU time** — Total processing time across nodes
- **Data scanned** — Bytes read from storage
- **Result set size** — Output volume
- Click **Query stats** for detailed breakdown

In Advanced Hunting (Defender):
- Execution time is shown after each query run
- Queries are capped at 10 minutes and 10K results by default

### KQL Detection Pattern (Sentinel Analytics Rule)

```kql
// Suspicious Encoded PowerShell Execution
// MITRE: T1059.001
let timeframe = 1h;
DeviceProcessEvents
| where Timestamp > ago(timeframe)
| where FileName in~ ("powershell.exe", "pwsh.exe")
| where ProcessCommandLine has_any ("-EncodedCommand", "-enc ", "-e ")
| project Timestamp, DeviceName, AccountName, FileName, ProcessCommandLine,
          InitiatingProcessFileName, InitiatingProcessCommandLine
| extend AccountName = tolower(AccountName)
```

---

## EQL/ES|QL Optimization (Elastic Security)

### Elastic Query Types

Elastic Security supports multiple query languages:

| Language | Use Case | Best For |
|----------|----------|----------|
| **EQL** (Event Query Language) | Ordered event correlation | Sequences, parent-child, multi-step attacks |
| **ES\|QL** (Elasticsearch Query Language) | Aggregation and exploration | Hunting, aggregations, complex transforms |
| **KQL** (Kibana Query Language) | Simple filtering | Dashboard filters, quick searches |
| **Lucene** | Full-text search | Free-text, complex boolean queries |

### EQL Optimization Techniques

#### 1. Use Specific Event Categories

EQL queries are fastest when scoped to a specific event category.

```eql
// SLOW — searches all event types
any where process.name == "powershell.exe"

// FAST — scoped to process events only
process where process.name == "powershell.exe"
```

**Event categories:** `process`, `file`, `network`, `registry`, `dns`, `library`

#### 2. Put Most Selective Conditions First

```eql
// SLOW — broad condition first
process where process.parent.name == "explorer.exe"
  and process.args : "*-EncodedCommand*"

// FAST — rare condition first
process where process.args : "*-EncodedCommand*"
  and process.parent.name == "explorer.exe"
```

#### 3. Optimize Sequence Queries

Sequence queries correlate events across time. They are powerful but expensive.

```eql
// SLOW — wide time window, no filtering
sequence by host.id with maxspan=30m
  [process where process.name == "cmd.exe"]
  [network where true]

// FAST — narrow window, filtered events
sequence by host.id with maxspan=2m
  [process where process.name == "cmd.exe"
    and process.args : "*download*"]
  [network where destination.port != 443
    and destination.port != 80]
```

**Sequence optimization tips:**
- Use the narrowest `maxspan` possible
- Add filters to each event in the sequence (never use `where true`)
- Put the rarest event first in the sequence
- Limit `by` clause to low-cardinality fields
- Use `until` to define sequence-breaking events

#### 4. Prefer `:` (Wildcard) Over `regex`

```eql
// SLOW — regex is expensive
process where process.command_line regex ".*(?i)encodedcommand.*"

// FAST — wildcard match (case-insensitive by default)
process where process.command_line : "*encodedcommand*"
```

#### 5. Use `?` for Optional Fields

```eql
// ERROR if field is missing in some events
process where process.parent.name == "winlogon.exe"

// SAFE — handles missing fields gracefully
process where ?process.parent.name == "winlogon.exe"
```

### ES|QL Optimization Techniques

#### 1. Filter with WHERE Before Processing

```esql
// SLOW — processes all events then filters
FROM logs-endpoint.events.process-*
| EVAL lower_name = TO_LOWER(process.name)
| WHERE lower_name == "powershell.exe"

// FAST — filter first, compute later
FROM logs-endpoint.events.process-*
| WHERE process.name == "powershell.exe"
| WHERE @timestamp > NOW() - 1 hour
```

#### 2. Use KEEP to Limit Columns

```esql
// SLOW — carries all columns
FROM logs-endpoint.events.process-*
| WHERE process.name == "powershell.exe"
| STATS count = COUNT() BY host.name

// FAST — drop unneeded columns early
FROM logs-endpoint.events.process-*
| WHERE process.name == "powershell.exe"
| KEEP process.name, process.command_line, host.name, @timestamp
| STATS count = COUNT() BY host.name
```

#### 3. Minimize EVAL Computations

```esql
// SLOW — computes on all rows
FROM logs-endpoint.events.process-*
| EVAL cmd_lower = TO_LOWER(process.command_line)
| WHERE cmd_lower LIKE "*encoded*"

// FAST — filter with WHERE first, compute on fewer rows
FROM logs-endpoint.events.process-*
| WHERE process.command_line LIKE "*encoded*"
```

### EQL Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| `any where` instead of typed event | Searches all event types | Use `process where`, `file where`, etc. |
| `regex` for simple matching | Expensive pattern evaluation | Use `:` wildcard operator |
| Wide `maxspan` in sequences | Large state to maintain | Use narrowest window possible |
| `where true` in sequence events | Matches everything | Add meaningful filters |
| No time range in rule settings | Scans full retention | Set look-back to detection interval |
| High-cardinality `by` in sequences | Memory explosion | Use host.id or user.name, not process.pid |

### EQL Detection Pattern (Elastic Security Rule)

```eql
// Suspicious Encoded PowerShell Execution
// MITRE: T1059.001
process where host.os.type == "windows"
  and process.name : ("powershell.exe", "pwsh.exe")
  and process.args : ("-EncodedCommand", "-enc", "-e")
  and not process.parent.executable : (
    "C:\\Windows\\System32\\svchost.exe",
    "C:\\Program Files\\*"
  )
```

### Elastic Performance Measurement

- **Kibana Dev Tools:** Use the `_search` API with `profile: true` to see shard-level timing
- **Rule monitoring:** Elastic Security → Detection Rules → Rule detail → Execution log shows timing and gaps
- **ES|QL:** Execution stats are shown in the Discover response metadata

---

## Cross-Platform Optimization Principles

These principles apply regardless of which SIEM you use:

1. **Filter early** — Reduce event volume before expensive operations (joins, aggregations, regex)
2. **Use indexed fields first** — Every platform has fields that are indexed vs. extracted at search time
3. **Avoid unnecessary regex** — Use string functions, wildcards, or term matching when possible
4. **Limit time range** — Always scope queries to the minimum needed window
5. **Project/select only needed fields** — Drop columns before joins and aggregations
6. **Put the rare condition first** — Let the engine skip events that don't match the most selective filter
7. **Test with realistic data volumes** — A query that runs in 2 seconds on 1 day of data may timeout on 30 days

## Sigma Note

Sigma rules are platform-agnostic and are compiled by pySigma backends into the target query language. Optimization happens at two levels:
1. **Rule authoring** — Write clean, minimal conditions with specific logsource definitions
2. **Backend compilation** — The pySigma backend generates optimized output for the target SIEM

To get the best compiled output, avoid overly complex Sigma conditions (deeply nested AND/OR/NOT) that backends may translate inefficiently. Prefer flat condition structures when possible.
