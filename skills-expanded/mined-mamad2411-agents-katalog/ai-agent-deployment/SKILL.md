---
name: ai-agent-deployment
version: 1.0.0
min_mindforge_version: 10.1.1
status: stable
triggers: ai agent deployment, agent hosting, agent scaling, agent versioning, agent A/B testing, agent monitoring production, agent rollback, agent health check, agent cost production, agent performance monitoring, agent canary, agent shadow testing
compose: deployment-workflow
---

# Skill — AI Agent Deployment

## When this skill activates
Any task involving deploying AI agents to production, versioning agent configurations,
A/B testing agent variants, monitoring agent quality in production,
or managing the operational lifecycle of AI agents.

## Mandatory actions when this skill is active

### Before writing any code
1. Define the agent version tuple: model + prompt + tools + config (all pinned together).
2. Identify success metrics (quality, latency, cost, user satisfaction).
3. Plan rollback strategy (instant version pointer switch).
4. Design monitoring (token usage, error rate, quality signal).

### During implementation
- Package agent as a versioned, immutable deployment artifact.
- Implement health check endpoint (synthetic task probe).
- Add structured logging for every agent action (input, output, tools used, tokens).
- Build traffic splitting capability for A/B and canary.
- Instrument cost tracking per-task and per-user.
- Implement graceful degradation (fallback to simpler model on failure).

### After implementation
- Verify shadow test shows no regression vs current version.
- Confirm monitoring dashboards capture all key metrics.
- Test rollback procedure end-to-end.
- Validate cost projections against actual usage.
- Run synthetic probes for health verification.

## Versioning Strategy

### Agent Version = Immutable Tuple
```json
{
  "version": "agent-v2.3.1",
  "model": "claude-sonnet-4-20250514",
  "prompt_hash": "sha256:abc123...",
  "tools": ["search_v2", "code_exec_v1", "web_browse_v3"],
  "config": {
    "temperature": 0.3,
    "max_tokens": 4096,
    "timeout_ms": 30000
  }
}
```

### Rules
- Changing ANY component = new version.
- Never mutate a deployed version in place.
- Keep previous N versions warm for instant rollback.
- Version string includes all components for traceability.

## Hosting Patterns

### Containerized (Recommended)
- Docker container with model client, prompt, tool implementations.
- Auto-scale on queue depth (not CPU — agents are I/O bound).
- GPU allocation only if running local inference.
- Isolate per-tenant for data separation.

### Scaling Signals
| Signal | Scale Direction | Reason |
|--------|----------------|--------|
| Queue depth increasing | Scale up | Work is backing up |
| P95 latency rising | Scale up | Capacity insufficient |
| Queue empty for 5min | Scale down | Over-provisioned |
| Error rate > 5% | Pause scaling | Fix errors first |

## A/B Testing

### Setup
1. Define hypothesis (e.g., "new prompt reduces hallucination by 20%").
2. Split traffic (e.g., 90/10 control/experiment).
3. Run for statistical significance (typically 1000+ samples per variant).
4. Measure: quality score, latency, cost, user feedback.

### Metrics to Compare
- Task success rate (did the agent complete the task correctly?).
- Token usage (cost proxy).
- Latency p50/p95/p99.
- Tool failure rate.
- User satisfaction signal (thumbs up/down, follow-up corrections).
- Hallucination rate (if measurable via ground truth).

### Graduation Criteria
- Improvement statistically significant (p < 0.05).
- No regression in any critical metric.
- Cost increase acceptable (<20% for same quality).

## Shadow Testing

### Pattern
```
User Request → Production Agent (responds to user)
            → Shadow Agent (runs silently, output logged)
```

### Purpose
- Test new version against real traffic without user impact.
- Compare outputs offline (human eval or automated scoring).
- Detect regressions before any user sees them.

### Rules
- Shadow agent output never reaches the user.
- Shadow uses same input but may have different model/prompt/tools.
- Compare at scale (1000+ requests) before promoting.
- Track divergence rate and categorize differences.

## Monitoring

### Key Metrics (Real-Time Dashboard)
| Metric | Alert Threshold | Action |
|--------|----------------|--------|
| Token usage/task | >2x baseline | Check for loops/verbose output |
| Latency p95 | >30s | Scale up or investigate bottleneck |
| Tool failure rate | >5% | Check tool availability |
| Hallucination rate | >3% | Rollback, investigate prompt |
| User negative feedback | >10% | Investigate, consider rollback |
| Cost per task | >$0.50 | Check for inefficiency |

### Structured Logging
Every agent invocation must log:
- Request ID, user ID, agent version.
- Input (sanitized of PII).
- Output summary.
- Tools invoked and their results.
- Token counts (input, output, total).
- Latency breakdown (thinking, tool calls, generation).
- Success/failure determination.

## Rollback

### Instant Rollback
- Version pointer in config store (not redeployment).
- Switch pointer → immediate traffic to previous version.
- Keep N previous versions warm (containers running, ready).
- Rollback decision within 5 minutes of detecting regression.

### Rollback Triggers (Automatic)
- Error rate > 10% for 3 consecutive minutes.
- P95 latency > 60s for 5 minutes.
- User negative feedback spike (3x normal rate).

## Health Checks

### Synthetic Probes
- Run a known-good task against the agent every 5 minutes.
- Verify output matches expected structure.
- Check latency within bounds.
- Alert if probe fails 2 consecutive times.

### Probe Design
- Task must be deterministic (or have verifiable structure).
- Must exercise core capabilities (reasoning + at least one tool).
- Must complete within health check timeout (10s recommended).
- Results logged for trend analysis.

## Self-check
- [ ] Agent version tuple defined (model + prompt + tools + config).
- [ ] Health check probes running every 5 minutes.
- [ ] Monitoring covers: tokens, latency, errors, quality, cost.
- [ ] Rollback tested and confirmed instant.
- [ ] Shadow test shows no regression.
- [ ] A/B framework ready for future experiments.
- [ ] Cost per task tracked and within budget.
- [ ] Graceful degradation implemented for failures.
