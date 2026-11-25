---
name: auto-orchestrator
description: "Automatically decomposes a complex request into independent subtasks and fans them out to parallel Claude agents simultaneously, then synthesizes the results. Trigger when: do this in parallel, run agents simultaneously, split the work across agents, 平行執行, 同時做, 多agent一起, fan out, 幫我同時處理, orchestrate this, use multiple agents for this. Do NOT trigger for simple single-step tasks, tasks that are inherently sequential and cannot be parallelized, or when the user explicitly wants to do it step by step."
metadata:
  category: dev
  version: "1.0"
---

## Purpose

Decompose a complex request into 2–6 independent subtasks, spawn a dedicated Claude agent for each in a single parallel batch, and synthesize all results into one coherent output.

## Trigger

Apply when:
- User says "do this in parallel", "run simultaneously", "多 agent 一起", "同時做", "fan out"
- A request clearly contains multiple independent parts (e.g. "review security AND performance AND architecture")
- A large corpus needs to be processed (multiple files, repos, URLs) faster than serial execution allows

Do NOT trigger for:
- Tasks where Step B depends on Step A's output — use `pipeline-orchestrator` instead
- Simple one-part requests that cannot be meaningfully split
- Tasks where the user explicitly wants to review each step before proceeding

## Prerequisites

- `Task` tool must be available (verify: attempt a dry Task call; if denied, inform user and stop)
- For background agents: `bypassPermissions` mode or auto-approved tools required
- The request must contain ≥ 2 independently executable subtasks

## Steps

1. **Analyse the request** — read the full request and identify all independently executable components; a component is independent if it does not need output from another component to start; list them explicitly before proceeding

2. **Classify each component** — for each component, select the best agent type:
   - `Explore` — read-only search, code analysis, file review (fast, cheap)
   - `Plan` — architecture, design, strategy (read-only, structured output)
   - `Bash` — git ops, system commands, script execution
   - `general-purpose` — anything requiring writes, edits, multi-step actions

3. **Write the synthesis plan** — before spawning any agent, state in one sentence what you will combine from each agent's output into the final result; this prevents redundant work

4. **Spawn all agents simultaneously** — issue ALL Task() calls in a single response (do not wait between calls); each call must include a complete, self-contained prompt that requires no follow-up:

   ```javascript
   // Issue ALL of these in ONE response turn — they run in parallel
   Task({
     subagent_type: "<type>",
     description: "<one-line description>",
     prompt: "<complete self-contained instructions; include all context the agent needs; end with: return your findings as a structured markdown report>"
   })

   Task({
     subagent_type: "<type>",
     description: "<one-line description>",
     prompt: "<complete self-contained instructions; end with: return your findings as a structured markdown report>"
   })

   // ... repeat for each independent component (max 6)
   ```

5. **Collect all results** — wait for all Task() calls to return; do not proceed until every agent has responded

6. **Synthesize** — combine all agent outputs into a single unified response following the synthesis plan from Step 3; resolve any contradictions between agents; do not simply concatenate — produce a coherent whole

## Output Format

File path: none (synthesized report printed to user)

```
## Auto-Orchestrator Results

### Agents Dispatched
| Agent | Type | Task | Status |
|-------|------|------|--------|
| 1 | Explore | Reviewed security patterns in auth/ | ✓ done |
| 2 | Explore | Reviewed performance bottlenecks in api/ | ✓ done |
| 3 | Plan | Designed refactor plan | ✓ done |

### Synthesized Findings

<unified output — not a list of agent dumps, but a coherent integrated result>
```

## Rules

### Must
- Issue all Task() calls in a single response turn — staggering calls defeats the purpose and serializes what should be parallel
- Write a complete self-contained prompt for each agent — agents have no access to the main conversation context
- State the synthesis plan before spawning so the output structure is decided upfront, not improvised
- Resolve contradictions between agents explicitly — if two agents disagree, state which is correct and why
- Cap at 6 parallel agents — beyond 6, costs exceed benefit; split into batches or use `orchestrating-swarms` with a swarm pattern instead
- If `Task` tool is denied, immediately inform the user: "Multi-agent execution requires Task tool access. Running serially instead." then proceed sequentially

### Never
- Never spawn agents sequentially when they can run in parallel — if you find yourself writing `Task()`, waiting, then `Task()` again for independent work, you are doing it wrong
- Never give an agent an incomplete prompt that says "see previous context" — agents are isolated and have no previous context
- Never spawn more than 6 agents in one batch without user confirmation
- Never synthesize by pasting each agent's output verbatim one after another — that is concatenation, not synthesis

## Examples

### Good Example

User: "Review my codebase for security issues, performance bottlenecks, and test coverage gaps."

Step 1 — Three independent components identified:
- Security review of `src/`
- Performance analysis of `src/`
- Test coverage analysis of `tests/` vs `src/`

Step 2 — All `Explore` type (read-only analysis)

Step 3 — Synthesis plan: produce a prioritized action list combining findings from all three angles

Step 4 — One response, three simultaneous Task() calls:
```javascript
Task({ subagent_type: "Explore", description: "Security review",
  prompt: "Analyze all files in src/ for security vulnerabilities: hardcoded secrets, injection risks, insecure dependencies, missing auth checks. Return findings as markdown with severity levels." })

Task({ subagent_type: "Explore", description: "Performance analysis",
  prompt: "Analyze all files in src/ for performance issues: N+1 queries, blocking I/O, missing caches, large payloads. Return findings as markdown with estimated impact." })

Task({ subagent_type: "Explore", description: "Test coverage gaps",
  prompt: "Compare test files in tests/ against source files in src/. Identify untested functions, missing edge cases, and files with no tests at all. Return findings as markdown." })
```

Step 6 — Synthesized output: a single prioritized action list that cross-references all three agents' findings.

### Bad Example

User: "Review for security, performance, and test coverage."

```javascript
// BAD: sequential calls — runs in series, not parallel
Task({ subagent_type: "Explore", prompt: "Review security..." })
// wait for result...
Task({ subagent_type: "Explore", prompt: "Review performance..." })
// wait for result...
Task({ subagent_type: "Explore", prompt: "Review tests..." })
```

Then output:

```
Security findings: [paste agent 1 output]
Performance findings: [paste agent 2 output]
Test findings: [paste agent 3 output]
```

> Why this is bad: Three sequential calls take 3× the time of parallel calls. Pasting three agent outputs without synthesis forces the user to do the integration themselves — the entire value of the orchestrator is the unified, cross-referenced result.
