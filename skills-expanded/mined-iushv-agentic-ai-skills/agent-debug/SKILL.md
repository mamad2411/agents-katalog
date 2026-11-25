---
name: agent-debug
description: Diagnose why an agent is failing, looping, choosing the wrong tools, hallucinating, overrunning its budget, or dying silently. Use this whenever the user reports an agent misbehaving, pastes an agent trace or error, or says things like "my agent keeps looping", "it calls the wrong tool", "costs are spiking", or "it returns nothing and no error".
---

# Agent Debug

Systematically diagnose why an agent is failing, looping, producing wrong answers,
or exceeding budgets. Follows the production incident playbook.

## When to Use

- Agent produces wrong or incomplete answers.
- Agent loops without converging on an answer.
- Agent exceeds cost, token, or time budgets.
- Agent fails silently or returns generic errors.
- Tool calls fail or return unexpected results.

## Inputs

Provide as many as available:
- **Error description**: What's going wrong.
- **Agent trace/logs**: Step-by-step execution log.
- **Agent config**: AgentConfig with limits.
- **Tool definitions**: Schemas of registered tools.
- **System prompt**: The agent's system prompt.
- **Example input**: A failing query.

## Diagnostic Flowchart

```
Agent is failing
├── Is it looping? → Check: iteration limits, tool output quality, stop condition
├── Is it exceeding budget? → Check: cost tracking, token counting, timeout
├── Is it calling wrong tools? → Check: tool descriptions, tool count, prompt clarity
├── Is it getting wrong tool results? → Check: tool implementation, input validation
├── Is it hallucinating? → Check: output guardrails, grounding, context window
├── Is it timing out? → Check: tool latency, LLM latency, network issues
├── Is it returning errors? → Check: error handling, circuit breaker, fallback chain
└── Is it silently wrong? → Check: eval dataset, golden trajectories, output validation
```

## Incident Playbook

### 1. Infinite Loop / Excessive Iterations

**Symptoms**: Agent hits max_iterations, repeats same tool calls, cost spikes.

**Root causes and fixes**:

| Cause | Signal | Fix |
|-------|--------|-----|
| Tool returns unhelpful output | Same tool called repeatedly with same args | Improve tool output format and description |
| No stop condition | Agent never produces final_answer | Add explicit "answer the question" instruction after N steps |
| Ambiguous tool descriptions | Agent oscillates between tools | Clarify WHEN to use each tool, add exclusions |
| Context window overflow | Late steps lose early context | Summarize intermediate results, reduce tool output size |
| Missing tool | Agent can't find what it needs | Add the missing tool or clarify which tool handles the case |

### 2. Wrong Tool Selection

**Symptoms**: Agent uses `run_sql` when it should use `search_docs`, or vice versa.

**Root causes and fixes**:

| Cause | Signal | Fix |
|-------|--------|-----|
| Vague tool descriptions | Tool chosen by name alone | Add WHEN/DON'T USE sections to docstring |
| Too many tools | Random selection from 10+ tools | Reduce to 3-7 tools, split into specialized agents |
| Overlapping tools | Two tools seem to do the same thing | Merge or clearly differentiate in descriptions |
| Prompt doesn't guide | System prompt doesn't mention tools | Add tool selection guidance to system prompt |

### 3. Budget Exceeded

**Symptoms**: Cost or token limit reached before answer.

**Root causes and fixes**:

| Cause | Signal | Fix |
|-------|--------|-----|
| Large tool outputs | Token count spikes after tool calls | Truncate outputs (10K char limit), summarize |
| Too many iterations | Steady cost increase per step | Lower max_iterations, improve per-step quality |
| Expensive model | High cost per call | Use cheaper model for simple steps, reserve expensive for final |
| No caching | Same queries repeated | Add exact/semantic cache |

### 4. Hallucination / Wrong Answers

**Symptoms**: Agent returns plausible but incorrect information.

**Root causes and fixes**:

| Cause | Signal | Fix |
|-------|--------|-----|
| No grounding check | Answer contradicts tool results | Add output guardrail comparing answer to tool outputs |
| Stale context | Answer uses outdated information | Refresh retrieval, check cache TTL |
| Prompt injection | External content influences behavior | Wrap external content in untrusted markers |
| Missing tool result | Agent answers from parametric knowledge | Force tool use before answering on factual queries |

### 5. Silent Failures

**Symptoms**: No error, but agent returns generic or empty response.

**Root causes and fixes**:

| Cause | Signal | Fix |
|-------|--------|-----|
| Swallowed exceptions | No error in logs | Add structured error logging, never bare except |
| Missing tracing | Can't see what happened | Add trace events for every LLM and tool call |
| Fallback to empty | Degradation returns nothing useful | Ensure degradation level 5 returns helpful message |
| Circuit breaker stuck | All providers marked failed | Add health check / reset mechanism |

### 6. Provider Failures

**Symptoms**: LLM API errors, timeouts, rate limits.

**Root causes and fixes**:

| Cause | Signal | Fix |
|-------|--------|-----|
| Rate limiting | 429 errors | Add retry with backoff, request quota increase |
| Provider outage | 5xx errors | Verify circuit breaker + fallback chain active |
| Network issues | Connection timeout | Check DNS, proxy settings, firewall rules |
| Auth expired | 401/403 errors | Rotate API keys, check token expiration |

## Debug Checklist

Quick triage — check these first:

1. [ ] Are iteration/cost/timeout limits set? What are current values?
2. [ ] Is tracing enabled? Can you see the execution trace?
3. [ ] What's the last successful step before failure?
4. [ ] Are tool outputs reasonable? (Check size, format, content.)
5. [ ] Is the circuit breaker open for any provider?
6. [ ] Does the eval dataset cover this failure case?
7. [ ] Has this agent been reviewed with `/agentic-design-review`?

## Output Format

```
## Agent Debug Report

**Symptom**: {description}
**Category**: {loop | wrong_tool | budget | hallucination | silent | provider}
**Root Cause**: {identified cause}
**Evidence**: {trace excerpt or log line}

### Fix
{Step-by-step fix with code changes}

### Prevention
{What to add to prevent recurrence: test, alert, guardrail}
```
