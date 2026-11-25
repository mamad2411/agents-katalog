---
name: agentic-design-review
description: Review agent code, tool schemas, or system prompts against production rules and report violations with severity and concrete fixes. Use this whenever the user asks to review, audit, or sanity-check an agent, a tool definition, or a prompt; before merging a PR that touches agent behavior; when they ask "is this agent production ready?"; or right after scaffolding a new agent — even when they never say the word "review".
---

# Agentic Design Review

Review agent code, tool definitions, or system prompts against the production rules
defined in AGENTS.md. Flag violations, suggest fixes, and rate overall readiness.

## When to Use

- Before merging a PR that adds or modifies agent behavior.
- After scaffolding a new agent to verify compliance.
- When auditing an existing agent for production readiness.

## Inputs

Provide one or more of:
- Agent loop code (Python file or snippet).
- Tool schema definitions (Pydantic models or JSON Schema).
- System prompt text.
- Configuration (AgentConfig or equivalent).

## Review Checklist

The review checks every item below. Each is pass/warn/fail:

### Architecture Level
- [ ] Architecture level (0-5) is identified and justified.
- [ ] No premature escalation to higher levels.

### Tool Design
- [ ] Tool names follow verb_noun format.
- [ ] Every tool has a rich description with WHEN/WHAT/edge cases.
- [ ] Parameters are constrained (enums, min/max, patterns).
- [ ] Agent has 3-7 tools, not more.
- [ ] Tools are idempotent where applicable.
- [ ] Tools return structured data, not free-form text.

### Safety
- [ ] Input passes through schema validation layer.
- [ ] Injection detection is present (prompt injection, SQL injection).
- [ ] SQL tools are read-only (SELECT only).
- [ ] External content is wrapped with untrusted markers.
- [ ] Code execution is sandboxed (network=none, non-root, resource limits).
- [ ] Output guardrails include PII scrubbing and schema validation.

### Reliability
- [ ] Retry policy with exponential backoff and jitter.
- [ ] Circuit breaker on LLM provider calls.
- [ ] Model fallback chain configured.
- [ ] Graceful degradation levels defined.

### Budget Enforcement
- [ ] `max_iterations` is set and bounded (hard cap 50).
- [ ] `max_tokens` is set.
- [ ] `max_cost_usd` is set.
- [ ] `timeout_seconds` is set (hard cap 600).
- [ ] Budget checks happen before every LLM call.

### Observability
- [ ] Every LLM call and tool call emits a trace event.
- [ ] Errors include structured context (run_id, step, error_type).
- [ ] Alert rules are configured for error rate, cost, latency.

### Testing
- [ ] Unit tests exist for every tool and guardrail.
- [ ] Integration tests mock LLM and test the loop.
- [ ] Eval dataset with golden trajectories exists.
- [ ] CI/CD gates on eval results.

## Output Format

```
## Design Review: {component_name}

**Architecture Level**: L{n} — {justification}
**Overall Score**: {PASS | WARN | FAIL}

### Findings

| # | Category | Severity | Finding | Fix |
|---|----------|----------|---------|-----|
| 1 | Safety   | FAIL     | ...     | ... |

### Summary
- Passes: {n}/{total}
- Warnings: {n}
- Failures: {n}
- Top priority fix: {description}
```

## Anti-Pattern Detection

Flag these specific anti-patterns with severity FAIL:

| Anti-Pattern | Detection Signal |
|---|---|
| Premature multi-agent | Level 4-5 without justification for split permissions |
| God Agent | More than 7 tools registered |
| No iteration limits | Missing max_iterations or max_tokens in config |
| LLM for everything | LLM call for regex-parseable or deterministic tasks |
| Raw API exposure | Tool wraps raw HTTP endpoint without focused interface |
| Fire-and-forget | No tracing or logging in agent loop |
| Trust the output | No output validation or grounding check |
| No fallbacks | Single model, no circuit breaker |
| Skipping eval | No eval dataset or CI gate |
