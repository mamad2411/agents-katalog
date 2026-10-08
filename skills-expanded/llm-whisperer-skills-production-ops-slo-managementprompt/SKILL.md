# SLO Management and Error Budgeting for AI Services

## Overview

Service Level Objectives (SLOs) for LLM services define the reliability and quality targets that engineering teams commit to maintaining. Unlike traditional web services where SLOs focus on availability and latency, LLM SLOs must also capture output quality, hallucination rates, and semantic consistency — metrics that are inherently subjective and variable. In 2026, the industry has converged on a multi-dimensional SLO framework that balances technical performance (latency, throughput, uptime) with AI-specific quality metrics (relevance, factual accuracy, safety).

Error budgeting extends SLOs by quantifying how much "unreliability" remains in the current window. When the error budget is exhausted, the team shifts focus from feature development to reliability improvements. For LLM services, error budgets must account for both traditional errors (5xx responses, timeouts) and quality errors (hallucinated outputs, off-topic responses, safety violations) — a request that returns in 200ms but contains fabricated facts is still a failure from the user's perspective.

The key challenge is measurement: traditional SLOs use deterministic signals (HTTP status codes), while LLM quality requires either LLM-as-judge evaluation, human annotation, or proxy metrics (user feedback, downstream task success). Modern SLO systems combine both, using fast proxy metrics for real-time monitoring and slower but more accurate evaluation methods for budget accounting.

## Key Concepts

- **Service Level Indicator (SLI)**: A quantitative measure of service behavior — latency, error rate, quality score
- **Service Level Objective (SLO)**: Target value for an SLI over a time window (e.g., 99.9% of requests complete under 2s)
- **Error Budget**: The allowed "unreliability" — (1 - SLO target) × total requests in the window
- **Quality SLIs**: Metrics specific to LLM output — relevance, factual accuracy, safety compliance, hallucination rate
- **Multi-window burn rate**: How fast the error budget is being consumed relative to the time remaining
- **Alerting thresholds**: Burn rate thresholds that trigger alerts before the error budget is fully consumed
- **SLO-based deployment gating**: Block deployments that would violate SLOs based on canary metrics
- **Error budget policies**: Pre-agreed actions when budget is exhausted (freeze deployments, focus on reliability)

## Implementation Patterns

### SLO Manager with Multi-Dimensional Tracking

```python
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class SLICategory(Enum):
    AVAILABILITY = "availability"
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    QUALITY = "quality"
    SAFETY = "safety"

@dataclass
class SLODefinition:
    name: str
    category: SLICategory
    target: float  # e.g., 0.999 for 99.9%
    window_days: int
    description: str
    measurement_method: str

@dataclass
class ErrorBudget:
    total: float
    consumed: float
    remaining: float
    burn_rate: float  # fraction of budget consumed per day
    days_until_exhaustion: Optional[float]

class SLOManager:
    """Multi-dimensional SLO manager for LLM services."""

    def __init__(self):
        self.slos: dict[str, SLODefinition] = {}
        self.events: list[dict] = []

    def define_slo(self, slo: SLODefinition):
        self.slos[slo.name] = slo

    def record_event(self, slo_name: str, success: bool, value: float = 0, metadata: dict = None):
        self.events.append({
            "slo_name": slo_name, "success": success,
            "value": value, "metadata": metadata or {},
            "timestamp": time.time()
        })

    def compute_error_budget(self, slo_name: str) -> ErrorBudget:
        slo = self.slos[slo_name]
        window_start = time.time() - (slo.window_days * 86400)
        relevant = [e for e in self.events if e["slo_name"] == slo_name and e["timestamp"] > window_start]

        if not relevant:
            return ErrorBudget(total=0, consumed=0, remaining=0, burn_rate=0, days_until_exhaustion=None)

        total = len(relevant)
        failures = sum(1 for e in relevant if not e["success"])
        allowed_failures = total * (1 - slo.target)

        burn_rate = failures / max(allowed_failures, 1)
        days_elapsed = (time.time() - window_start) / 86400
        burn_per_day = failures / max(days_elapsed, 1)
        days_remaining = (allowed_failures - failures) / max(burn_per_day, 1) if burn_per_day > 0 else None

        return ErrorBudget(
            total=allowed_failures, consumed=failures,
            remaining=max(0, allowed_failures - failures),
            burn_rate=burn_rate,
            days_until_exhaustion=days_remaining if days_remaining and days_remaining > 0 else 0
        )

    def check_deployment_gating(self, canary_events: list[dict]) -> dict:
        """Check if a canary deployment should proceed based on SLO compliance."""
        results = {}
        for slo_name, slo in self.slos.items():
            canary_sli = [e for e in canary_events if e["slo_name"] == slo_name]
            if not canary_sli:
                continue
            success_rate = sum(1 for e in canary_sli if e["success"]) / len(canary_sli)
            results[slo_name] = {
                "measured": success_rate,
                "target": slo.target,
                "pass": success_rate >= slo.target
            }
        return {"proceed": all(r["pass"] for r in results.values()), "details": results}
```

### Quality SLO Evaluator

```python
class QualitySLOEvaluator:
    """Evaluates LLM output quality against SLO targets."""

    def __init__(self, judge_client, slo_manager: SLOManager):
        self.judge = judge_client
        self.slo_manager = slo_manager

    async def evaluate_request(self, request_id: str, prompt: str, response: str, context: str = ""):
        """Evaluate a single request against quality SLOs."""
        relevance = await self.judge.evaluate(
            prompt=prompt, response=response,
            criteria="Is the response relevant and on-topic?"
        )
        self.slo_manager.record_event("quality_relevance", relevance["score"] >= 0.7, relevance["score"])

        factual = await self.judge.evaluate(
            prompt=prompt, response=response, context=context,
            criteria="Is the response factually accurate based on the provided context?"
        )
        self.slo_manager.record_event("quality_factual", factual["score"] >= 0.8, factual["score"])

        safety = await self.judge.evaluate(
            prompt=prompt, response=response,
            criteria="Is the response safe, non-harmful, and appropriate?"
        )
        self.slo_manager.record_event("quality_safety", safety["score"] >= 0.95, safety["score"])
```

### SLO Alert Configuration

```yaml
slos:
  - name: availability
    target: 0.999
    window: 30d
    alert_thresholds:
      - burn_rate: 14.4  # 2% budget in 1 hour
        severity: page
      - burn_rate: 6.0   # 5% budget in 6 hours
        severity: ticket
      - burn_rate: 1.0   # normal burn rate
        severity: info

  - name: latency_p99
    target: 0.995  # 99.5% of requests under 2s
    window: 7d
    alert_thresholds:
      - burn_rate: 10.0
        severity: page

  - name: quality_relevance
    target: 0.95
    window: 7d
    alert_thresholds:
      - burn_rate: 6.0
        severity: page

  - name: quality_safety
    target: 0.999
    window: 30d
    alert_thresholds:
      - burn_rate: 1.0
        severity: page  # Any safety violation pages oncall
```

## Best Practices

1. Define SLOs collaboratively with product, engineering, and stakeholders — SLOs represent a business commitment, not just a technical target
2. Use multi-window burn rate alerting (1h, 6h, 30d) to distinguish between acute incidents and gradual degradation
3. Implement quality SLOs alongside traditional latency/availability SLOs — a fast response that hallucinates is still a failure
4. Make error budget policies explicit and pre-agreed: when budget is exhausted, freeze feature deployments and prioritize reliability
5. Use LLM-as-judge for quality SLO measurement with human annotation sampling to calibrate the judge
6. Track SLO compliance per model version, per user segment, and per request type to identify specific regression areas
7. Set stricter SLOs for safety metrics (99.9%+) than for quality metrics (95%+) — safety violations have outsized impact
8. Implement SLO-based deployment gating: canary deployments must maintain SLO compliance before proceeding
9. Review and adjust SLO targets quarterly based on actual performance data and business requirements
10. Make SLO dashboards visible to the entire organization — SLOs only drive behavior if everyone can see them

## Common Pitfalls

- **Too many SLOs**: Tracking 20+ SLOs dilutes focus — pick 3-5 that matter most to users
- **Unrealistic targets**: Setting 99.99% quality SLOs when the underlying model can't deliver leads to constant budget exhaustion
- **Ignoring measurement cost**: LLM-as-judge evaluation is expensive — balance measurement frequency against cost
- **SLO theater**: Having SLOs that nobody acts on is worse than having none — they erode trust in the reliability process
- **Conflating SLOs with SLAs**: SLOs are internal targets; SLAs are external contracts with financial penalties — keep them separate
- **Static targets**: SLOs that never change become either trivially easy or impossibly hard as the system evolves

## References

- Google SRE Book, "Service Level Objectives": https://sre.google/sre-book/service-level-objectives/
- Google SRE Workbook, "Implementing SLOs": https://sre.google/workbook/implementing-slos/
- Sloth SLO Tool: https://sloth.dev/
- Pyrra SLO Tool: https://pyrra.dev/
