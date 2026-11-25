---
name: provider-router
description: "Intelligent LLM provider selection based on task characteristics, cost-latency-quality optimization. Use when choosing the best AI provider for a task."
version: 1.0.0
platforms: [linux, macos]
---

# Provider Router

## What It Does
Intelligently routes tasks to the optimal LLM provider based on task characteristics, cost constraints, latency requirements, and quality needs. Maintains a provider capability matrix, implements fallback chains for resilience, manages token budgets across providers, and monitors provider health. The routing decision is explainable — every choice comes with a "why this provider" justification.

## Iron Laws (NEVER violate)
1. **Task before provider** — Analyze the task first, then pick the provider. Never default to a favorite provider.
2. **Budget is a contract** — Never exceed the token budget allocated for a task. Budget overruns are failures to route correctly.
3. **Fallback is automatic** — If primary provider fails (timeout, rate limit, error), automatically fall back to the next best. No user-visible failure for transient issues.
4. **Explain every route** — Every routing decision must include a 1-line justification. "Routed to Claude because: architectural reasoning task, 128K context needed."

## Red Flags (STOP immediately)
- **Single point of failure** — All tasks routing to one provider → provider outage = total failure
- **Cost anomaly** — Task cost 3x estimate → routing decision was wrong; analyze and update capability matrix
- **Quality degradation** — Provider consistently underperforming on its designated task type → re-evaluate capability mapping
- **Latency SLA breach** — Provider response time exceeds task latency budget → demote in capability matrix

## Common Rationalizations (self-deception)
- "Provider X is the best, just use it for everything" → No single provider is best at everything. Routing exists because strengths vary.
- "The cheapest provider is good enough" → Cost optimization without quality gates leads to bad outputs that cost more to fix.
- "We'll handle fallback manually" → Manual fallback means user sees errors. Automatic fallback means user never knows there was a problem.

## When To Use
- Multi-provider environment where task routing decisions are frequent
- User asks "which model should I use for this?"
- Setting up provider fallback chains for production reliability
- Managing token budgets across multiple providers
- Monitoring provider health and performance

## Human Partner Signals (escalate to human)
- **All providers down** — Fallback chain exhausted → critical infrastructure issue
- **Budget threshold** — Monthly token spend approaching limit → budget decision needed
- **New provider evaluation** — Considering adding a new provider → capability matrix update
- **Quality dispute** — User disagrees with routing decision repeatedly → capability matrix needs adjustment

## Pipeline
1. Analyze: examine task characteristics — reasoning depth, context length, domain, output format, latency needs
2. Score: compute provider suitability scores using capability matrix (quality × latency × cost × availability)
3. Route: select highest-scoring provider, record justification
4. Monitor: track response time, token usage, quality signal (user corrections, task success)
5. Fallback: on failure, route to next-best provider with same justification pattern
6. Learn: update capability matrix based on actual performance vs predicted scores

## Verification Checklist
- [ ] Every routing decision has a recorded justification
- [ ] Fallback chains defined for all critical task types (min 2 alternatives)
- [ ] Token budget enforced per-task and per-session
- [ ] Provider health monitored with <5 minute detection latency
- [ ] Capability matrix updated based on actual performance data (not assumptions)
- [ ] Cost optimization active: similar-quality tasks route to cheaper providers

## Related Skills
- `cross-model-reviewer` — Provider router selects which models participate in cross-model review
- `multi-agent-debate` — Debate participants selected by provider routing logic
- `serving-llms-vllm` — Self-hosted models as additional routing targets
- `llama-cpp` — Local inference as a routing option for low-latency/sensitive tasks
