---
name: agent-orchestrator
description: |
  Decompose complex tasks and orchestrate multiple sub-agents to work in parallel — planning,
  delegation, progress tracking, and result consolidation. Use when: "多agent协作", "任务拆分",
  "委派子任务", "agent orchestration", "parallel execution", "复杂任务分解", "子agent管理",
  "multi-agent workflow", "任务编排", "并行处理". The foundation skill for scaling beyond
  single-agent capacity. Part of the UniqueSkills platform toolkit.
---
# Agent Orchestrator
> Decompose, delegate, track, and consolidate — turn complex requests into coordinated multi-agent work.

## When to Use
Use this skill when:
- A task involves **3+ independent workstreams** that can run in parallel
- The user asks for **comprehensive research** across multiple sources or dimensions
- A **large batch** of similar items each needs end-to-end processing (e.g., 20+ documents, 50+ records)
- The task requires **specialized sub-agents** with different domain expertise
- You need to **delegate and monitor** long-running work while staying responsive to the user

Do NOT use this skill if:
- The task is simple enough for a single agent to finish directly
- The work is strictly serial with no parallelizable units
- The user expects an immediate, interactive answer — delegation adds latency
- You only need to call a single tool or run a short script

Typical triggers:
- 「这个任务比较大，拆分一下」「帮我并行处理」「委派给子agent」
- "orchestrate multiple agents", "delegate this task", "break this down"
- 「全面调研一下」「批量处理这些」「同时做几件事」

## Workflow

### Step 1: 探查 — Scope and Decompose
- Read the full request and all attachments before planning
- Identify independent work units (`U`): objects, dimensions, source families, or pipeline stages
- Count the decision-relevant workload: `O` (options/objects), `D` (dimensions), `C` (channels), `P` (platforms/scenarios), `N` (records), `B` (corpus size)
- Decide: does this meet the delegation threshold? If not, execute directly.

### Step 2: 约束 — Define Acceptance Criteria
- For each work unit, write explicit input, output schema, and completion criteria
- State constraints that must propagate: language, format, brand voice, data sources, deadlines
- Identify dependencies: which units must finish before others can start
- Name the organizer and the shard owners; exactly one organizer per task

### Step 3: 证据 — Establish Shared Facts
- Collect and verify any facts that all sub-agents need (definitions, reference data, API specs)
- Put shared context into the organizer's hint so sub-agents don't re-derive it
- Flag ambiguous items; resolve those that change conclusions before delegating

### Step 4: 执行 — Dispatch and Monitor
- Partition units into the smallest number of balanced shards (normally 2–4)
- Create shard owners in the same round; each owns its units end-to-end: acquire → process → analyze → verify → standardize output
- Track progress via periodic summaries; do not block the user — acknowledge delegation immediately
- Cancel drifting agents; re-dispatch fresh ones with reusable deliverable IDs

### Step 5: 验证 — Reconcile and Cross-Check
- Reconcile definitions and duplicates across shards
- Preserve source provenance; identify coverage gaps
- Spot-check a sample of each shard's output against the acceptance criteria
- Re-run any unit that fails verification

### Step 6: 交付 — Consolidate and Present
- Merge shard outputs into one coherent result
- State what was done, what remains, and any blockers
- Deliver the final artifact through the proper channel; never present intermediate working files

## Output
A consolidated result that includes:
- **Summary**: what was accomplished and the key conclusion
- **Shard breakdown**: which agent handled what, with per-shard status
- **Artifacts**: files, links, or structured data produced
- **Gaps & blockers**: anything incomplete and why
- **Next actions**: recommended follow-up steps

## Guardrails
- **Exactly one organizer** per delegated task; the organizer may create multiple sub-agents, but the main agent never creates non-organizer sub-agents directly
- **Never delegate trivial tasks** — single-tool calls, short scripts, and simple Q&A stay in the main agent
- **Shared state stays with the organizer**; sub-agents get explicit inputs, not implicit context
- **Cancellation cascades recursively**, but already-finished deliverables are kept
- **Do not pretend a failed delegation succeeded** — report the error and either retry with a changed approach or explain the blocker
- **Sizing is a one-pass decision gate**, not an excuse to avoid work; once triggered, stop probing and delegate

## Related Skills
- **skill-discovery** — Find and load the right skills before orchestrating their use
- **tool-router** — Route each sub-task to the correct tool or API
- **cron-scheduler** — Schedule recurring orchestration workflows
- **memory-manager** — Persist task outcomes and user preferences across sessions

## About
Part of the UniqueSkills platform toolkit — capabilities extracted from the Doubao agent runtime.
🌐 https://uniqueclub.ai | 📂 https://github.com/wulaosiji/skills
