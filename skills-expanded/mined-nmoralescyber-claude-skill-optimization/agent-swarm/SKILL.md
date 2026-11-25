---
name: agent-swarm
description: Decomposes complex multi-domain tasks into parallelizable subagent dispatches — proposes the swarm structure (which subagents, what each does, what they return) and waits for user confirmation before launching. Make sure to use this skill whenever a task has 2+ of these signals: 3+ independent subtasks, spans multiple domains (frontend+backend, research+implementation, multi-document analysis), estimated >30 min of sequential work, user language implies parallel work ("analyze all these files", "research each of these competitors", "implement each of these features"), or user explicitly types /swarm. Plans the decomposition and gates dispatch on explicit user approval. Do NOT use for: simple single-domain tasks (just do them), tasks where sequential dependency between steps prevents parallelism, or tasks under 30 min where coordination overhead exceeds savings. Defining characteristic: "the task naturally splits into 3+ parallel work streams that can each be done by a separate subagent."
---

# Agent Swarm (Parallel Subagent Dispatch)

Decomposes complex tasks into parallelizable subagent work and gates dispatch on user approval.

## When to use vs. just doing it

| Use this skill when... | Just do it directly when... |
|---|---|
| Task has 3+ independent subtasks | Task is single-domain |
| Domains differ (frontend + backend, research + implementation) | Steps are sequentially dependent |
| Sequential work would exceed 30 minutes | Whole task fits in <30 min sequentially |
| User language implies parallelism | User wants you to do one specific thing |
| User explicitly types `/swarm` | Coordinating subagents would cost more than the parallelism saves |

## The swarm decision: when does parallelism actually help?

Parallel subagent dispatch has real costs:
- Coordination overhead (decomposition, dispatching, integration)
- Context fragmentation (each subagent has narrower scope than you would)
- Risk of inconsistency (subagent A and B make incompatible assumptions)
- Token cost (each subagent has its own system prompt + context window)

It pays off when:
- Subtasks are genuinely independent (rare; most tasks have hidden dependencies)
- Each subtask is substantial enough that coordination cost is amortized (5+ minutes of work per subagent)
- The output of each subagent is well-specified upfront (no clarification mid-flight)
- Integration is mechanical (concatenation, table-merge) rather than synthesis

If integration requires reconciling subagent disagreements, parallelism is the wrong tool.

## The swarm proposal flow

This skill ALWAYS proposes before dispatching. Never silently fans out.

### Step 1 — Decompose

Identify the natural cuts:

```
Original task: [User's stated goal]

Decomposition:
  Subtask A: [Self-contained piece]
    - Inputs: [what A needs]
    - Outputs: [what A returns]
    - Tools: [what A will use]
  
  Subtask B: [Self-contained piece]
    - Inputs: [what B needs]
    - Outputs: [what B returns]
    - Tools: [what B will use]
  
  Subtask C: [...]
  
Integration:
  [How A, B, C combine into the final answer]
  
Estimated savings:
  Sequential: ~N minutes
  Parallel:   ~M minutes (with overhead)
  Net win:    N - M
```

### Step 2 — Show the proposal to the user

Surface the decomposition with explicit confirm/edit/cancel options. The user can:

- Approve as-is → dispatch all subagents
- Edit (add/remove/rescope a subtask) → re-propose
- Cancel → fall back to sequential execution
- Override (do it differently) → user-driven

### Step 3 — Dispatch (only after approval)

For each approved subtask, launch a subagent with:
- Self-contained prompt (subagent doesn't see the original conversation context)
- Explicit input data
- Explicit output specification
- Bounded scope (don't let subagents expand)

### Step 4 — Integrate

Once all subagents return:
- Surface each result with attribution ("Subagent A produced...")
- Reconcile conflicts (if any) — flag to user, don't auto-resolve silently
- Synthesize into the final answer

## Common swarm patterns

### Pattern 1: Multi-document analysis
"Summarize these 8 contracts for comparison."
- Subagent per contract → returns structured summary
- Integration: side-by-side comparison table

### Pattern 2: Multi-competitor research
"Research these 5 competitors for a battlecard."
- Subagent per competitor → returns competitor profile
- Integration: comparison matrix + per-competitor card

### Pattern 3: Codebase audit across modules
"Audit security in our auth, payments, and admin modules."
- Subagent per module → returns findings with severity
- Integration: prioritized findings list across all modules

### Pattern 4: Multi-customer outreach drafting
"Draft personalized outreach to these 12 prospects."
- Subagent per prospect (or batches of 3) → returns research + draft
- Integration: review queue with all 12 drafts

### Pattern 5: Multi-region compliance check
"Check this feature for compliance across EU, US, UK, Singapore."
- Subagent per jurisdiction → returns applicable regulations + findings
- Integration: cross-jurisdiction matrix

### Pattern 6: Parallel research sweep
"Research the latest on [topic] across news, academic papers, and industry blogs."
- Subagent per source type → returns findings
- Integration: synthesis across sources

## Cybersecurity-specific swarm uses

For security work, common parallel-friendly tasks:

- **Vendor security review** — one subagent each on: SOC 2 report, pen test report, public security posture, customer references
- **Cross-framework gap analysis** — one subagent per framework (SOC 2, ISO, HIPAA) to map a control set
- **Multi-account threat scan** — one subagent per cloud account to audit posture
- **Incident postmortem evidence collection** — parallel subagents on: timeline reconstruction, log analysis, comm review, customer-impact assessment
- **Multi-vendor risk register** — one subagent per critical vendor for risk scoring

## Anti-patterns

- **Auto-dispatching without approval** — the gate exists for a reason; subagents are expensive
- **Splitting truly sequential work** — A's output is B's input; no parallelism possible
- **Subagents with vague output specs** — "research this" returns unmergeable results
- **Too many subagents** — 5-7 is usually max useful; beyond that, coordination dominates
- **Single subagent ≠ swarm** — if one subagent does it all, you don't need this skill, just dispatch directly
- **Subagents on subjective tasks** — "what's the best position for X" returns 5 inconsistent answers

## Output

Before dispatch:
1. The decomposition proposal in the format above
2. Estimated time savings
3. Confirm/edit/cancel prompt to user

After dispatch and integration:
1. Each subagent's deliverable, attributed
2. Synthesized final answer
3. Conflicts surfaced (if any)
4. Suggested next steps
