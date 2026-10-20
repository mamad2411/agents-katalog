---
name: lyra-context-optimization
description: "Token-efficiency tactics for LLM agents and pipelines: prompt-cache-stable prefixes, observation masking, disciplined compaction, just-in-time retrieval, sub-agent partitioning, and explicit context budgets. Use when token costs or context limits constrain a task, when cache hit rates are poor, or when an agent drowns in its own tool outputs."
compatibility: "No tools required. Applies to any LLM runtime with a context window; cache rules assume a provider with prefix/prompt caching. Composes with lyra-council (partitioning), lyra-docs (reference layout). Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-context-optimization

## What it does

Extends the effective capacity of a context window without a bigger model: keep the prefix byte-stable so the prompt cache pays for itself, mask tool outputs once they've served their purpose, compact before quality degrades instead of after, retrieve just-in-time instead of loading up-front, and partition to sub-agents only when the math favors it. The governing principle: context quality beats context quantity — every tactic here removes noise while preserving signal, and none is applied without measuring what dominates the window first.

The rules address two actors — apply what your seat controls. The **pipeline builder** owns the prefix, the budgets, and the metrics (rules 2, 7, 8). The **agent working inside a window** owns retrieval, masking-by-summarizing, compaction requests, and partitioning (rules 3–6). An agent can't reorder its own system prompt; a builder can't decide mid-task which file slice to read — a rule applied from the wrong seat is a no-op that looks like diligence.

## The rules

### 1. Measure composition before optimizing

Know what dominates the window — tool outputs, retrieved documents, message history, or system scaffolding — before choosing a tactic. Builders measure exactly (token counts per category from the API). An agent that can't read token counts estimates by proxy: how many tool results and how large, files read whole vs sliced, turns since the last compaction, and whether recent outputs repeat earlier ones — rough proportions are enough to pick a row. Then pick by dominance:

| What dominates                  | First action                          | Second action                     |
| ------------------------------- | ------------------------------------- | --------------------------------- |
| Tool outputs (> 50%)            | Observation masking                   | Compact remaining history         |
| Retrieved documents             | Just-in-time retrieval + summarize    | Partition if docs are independent |
| Message history                 | Compaction with selective preservation | Partition new subtasks            |
| Everything a bit                | Cache-stable prefix first             | Layer masking + compaction        |
| Near-limit while debugging      | Mask resolved outputs only — never active error detail | —        |

### 2. Keep the prefix byte-stable — the cache is the cheapest optimization you'll ever ship

Prompt caching bills cached tokens at a fraction of fresh ones, but only for a byte-identical prefix. Order content stable → dynamic: system prompt, tool definitions, templates and few-shot examples, then history, then the current query. Never interpolate timestamps, session IDs, or counters into the prefix — `Current date: {today}` guarantees a daily full miss, and a single whitespace change invalidates everything after it. Caches also expire (typically ~5 minutes on providers' default tier; extended-TTL tiers — up to an hour — exist and are worth buying for agents with long natural pauses): a long-running agent that sleeps past the TTL pays a full re-read, so batch work inside cache windows and treat any planned pause longer than the TTL as a deliberate, amortized cost.

### 3. Mask observations once they've served their purpose

Tool outputs dominate agent trajectories, and this tactic has a different shape per seat. **Builder-side (true masking):** the harness rewrites history — once an output's conclusion has been extracted, replace the body with a compact, retrievable reference: `[Obs:{id} elided — key: {one-line summary}; full content retrievable]`. **Agent-side (an agent cannot edit its own prior turns):** the equivalent is *never needing the body again* — extract the conclusion into your working notes (or a file, rule 5) at the moment you read the output, then don't re-read or re-fetch it; request harness compaction where the runtime offers it. Either seat: never mask the most recent turn, anything in an active reasoning chain, or error output during live debugging (error in the last ~3 turns suspends masking for everything error-related); always mask duplicates and boilerplate immediately.

### 4. Compact at ~70% utilization — never later, never the system prompt

A model summarizing while itself under context pressure drops goals and constraints; compact at 70–80%, not at 95% when it's an emergency. Builders read utilization off the API; an agent detects "approaching 70%" through rule 1's proxies — many large unmasked tool results, whole files read, a long stretch since the last compaction — plus any harness-provided signal, and errs early rather than precisely. Preserve by type: decisions, commitments, and user constraints from conversation; findings, metrics, and error codes from tool outputs; task-relevant claims from documents. Target 50–70% reduction — beyond that, audit for information loss. After compacting, re-validate the summary against the current task goal: a summary silently carries stale state forward, and it reads as authoritative precisely because it's a summary.

### 5. Retrieve just-in-time; search before you read, read the slice not the file

Loading "everything that might be relevant" up-front is how windows die. Grep for the symbol before opening the file; read the 80 relevant lines, not the 2,000-line file; fetch the reference document when the task reaches it, not at session start. The same applies to capabilities: defer tool schemas and skill bodies until needed — a lean instruction surface with on-demand references (progressive disclosure) beats a comprehensive one that's 90% dead weight in every request.

The retrieval store includes the one the agent writes itself: **the filesystem is working memory**. Persist plans, findings, and intermediate results to files as they're produced, keep a one-line pointer in context, and re-read the slice when needed — state on disk survives compaction, costs nothing while unread, and turns "hold everything in the window" tasks into "hold an index in the window" tasks. This is the highest-leverage tactic for long-running agent work.

### 6. Partition to sub-agents when isolation beats interleaving

Split work across isolated contexts when the estimated task exceeds ~60% of the window, or when a subtask's exploration noise (search transcripts, file dumps) would pollute the coordinator. Sub-agents return **structured conclusions, not transcripts** — the whole point is that the mess stays in their window. Coordination costs real tokens (system prompt + tools per agent, plus aggregation); below ~3 independent subtasks the overhead usually exceeds the savings, so don't partition small work.

### 7. Budget by category, trigger by threshold

Allocate before the session: e.g. tool outputs 35%, history 30%, retrieved documents 20%, reserved buffer 15%. Optimize on triggers, not on a timer: category over budget → apply that category's tactic; total > 70% → compact; degradation signals (repetition, missed instructions, ignored constraints) → diagnose composition before optimizing, because degraded output can mean poisoned context, not just a full one.

### 8. Prove every optimization pays — the machinery isn't free

Masking, compaction, and partitioning all consume tokens and add latency themselves. Track what's directly measurable: cache hit rate (target 70%+ on stable workloads), token reduction from masking (60–80% of masked observations) and compaction (50–70%), and net savings after coordinator overhead for partitioning. "Quality impact" is only a metric where an eval suite exists to measure it — run the task eval before and after enabling a tactic, and hold regressions near zero; without an eval harness, treat quality targets as design intent and watch the honest proxy instead (re-fetch/re-read rate of masked content, and task failures traceable to a compacted detail). An optimization that doesn't move a *measured* metric gets removed. Roll prompt changes out knowingly: any prefix edit causes a cold-cache cost spike until the new prefix warms.

---

_Part of the [skill collection](../README.md)._
