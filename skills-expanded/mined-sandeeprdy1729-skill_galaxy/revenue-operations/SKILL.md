---
name: revenue-operations
description: "Implement revenue operations (RevOps) workflows including pipeline management, forecasting, sales-marketing alignment, lead scoring, and quota tracking. Covers automation patterns for modern go-to-market teams."
license: Apache 2.0
tags: ["revops", "sales-ops", "pipeline", "forecasting", "lead-scoring", "gtm", "business-operations"]
difficulty: intermediate
time_to_master: "10-16 weeks"
version: "1.0.0"
---

# Revenue Operations

## Overview

Revenue Operations (RevOps) unifies sales, marketing, and customer success operations under a single data and process framework. As AI agents gain access to CRM and analytics tools, RevOps workflows become automatable — from lead scoring to pipeline forecasting to churn prediction. This skill covers the operational patterns, data models, and automation strategies for modern RevOps.

## When to Use This Skill

- Building AI-powered pipeline forecasting and deal scoring
- Automating lead routing and qualification workflows
- Implementing sales-marketing alignment with SLA tracking
- Creating revenue dashboards from CRM, billing, and usage data
- Designing quota management and commission calculation systems

## Core Concepts

### The RevOps Data Flow

```
Marketing              Sales                Customer Success
─────────              ─────                ────────────────
Lead Gen ──► MQL ──► SQL ──► Opportunity ──► Closed Won ──► Onboarding ──► Renewal
  │           │        │         │              │              │              │
  ▼           ▼        ▼         ▼              ▼              ▼              ▼
 CAC      Conversion  Win Rate  ACV          Time-to-      NPS/CSAT      Net Revenue
 Metrics   Rates              Pipeline      Value                       Retention
```

### Key Metrics

| Metric | Formula | Healthy Range |
|--------|---------|---------------|
| MQL-to-SQL Rate | SQLs / MQLs | 15-30% |
| SQL-to-Opportunity | Opps / SQLs | 40-60% |
| Win Rate | Closed Won / Total Opps | 20-35% |
| Sales Cycle Length | Avg days from SQL to Close | Industry-dependent |
| Pipeline Coverage | Pipeline Value / Quota | 3-4x |
| CAC Payback Period | CAC / Monthly Gross Margin | < 18 months |
| Net Revenue Retention | (Revenue + Expansion - Churn) / Starting Revenue | > 110% |
| ARR per Rep | Total ARR / Quota-carrying Reps | $500K-$1.2M |

### Lead Scoring Model

```python
class LeadScorer:
    """Multi-factor lead scoring combining firmographic and behavioral signals."""

    FIRMOGRAPHIC_WEIGHTS = {
        "employee_count": {"1-50": 10, "51-200": 20, "201-1000": 30, "1000+": 25},
        "industry": {"technology": 30, "finance": 25, "healthcare": 20, "other": 10},
        "title_level": {"c-level": 40, "vp": 35, "director": 25, "manager": 15, "individual": 5},
    }

    BEHAVIORAL_WEIGHTS = {
        "pricing_page_visit": 20,
        "demo_request": 40,
        "whitepaper_download": 10,
        "webinar_attendance": 15,
        "email_open": 2,
        "email_click": 5,
        "return_visit": 8,
    }

    def score(self, lead):
        firm_score = sum(
            self.FIRMOGRAPHIC_WEIGHTS.get(attr, {}).get(getattr(lead, attr, "other"), 0)
            for attr in self.FIRMOGRAPHIC_WEIGHTS
        )
        behavior_score = sum(
            self.BEHAVIORAL_WEIGHTS.get(action, 0) * count
            for action, count in lead.activities.items()
        )
        total = min(firm_score + behavior_score, 100)

        if total >= 80: return {"score": total, "grade": "A", "action": "route_to_sales"}
        if total >= 60: return {"score": total, "grade": "B", "action": "nurture_high"}
        if total >= 40: return {"score": total, "grade": "C", "action": "nurture_standard"}
        return {"score": total, "grade": "D", "action": "continue_marketing"}
```

## Implementation Guide

### Pipeline Forecasting

```python
def forecast_pipeline(deals, method="weighted"):
    """Generate revenue forecast from pipeline deals."""
    stage_weights = {
        "discovery": 0.10,
        "qualification": 0.25,
        "proposal": 0.50,
        "negotiation": 0.75,
        "verbal_commit": 0.90,
        "closed_won": 1.00,
        "closed_lost": 0.00,
    }

    if method == "weighted":
        return sum(
            deal.amount * stage_weights.get(deal.stage, 0)
            for deal in deals
        )
    elif method == "category":
        return {
            "best_case": sum(d.amount for d in deals if d.stage in ["verbal_commit", "negotiation", "proposal"]),
            "commit": sum(d.amount for d in deals if d.stage in ["verbal_commit"]),
            "closed": sum(d.amount for d in deals if d.stage == "closed_won"),
        }
```

### Lead Routing Automation

```python
class LeadRouter:
    """Route leads to sales reps based on territory, capacity, and specialization."""

    def route(self, lead):
        # 1. Territory match
        territory_reps = self.get_reps_for_territory(lead.region)

        # 2. Specialization match
        specialized = [r for r in territory_reps
                       if lead.industry in r.specializations]

        # 3. Capacity check (round-robin among available)
        candidates = specialized or territory_reps
        available = [r for r in candidates
                     if r.active_deals < r.capacity_limit]

        if not available:
            return self.escalate_to_manager(lead)

        # Round-robin by least recent assignment
        selected = min(available, key=lambda r: r.last_assigned_at)
        self.assign(lead, selected)
        return selected
```

### Marketing-Sales SLA Tracking

```python
class SLATracker:
    SLAS = {
        "mql_followup": timedelta(hours=4),     # Sales must contact MQL within 4 hours
        "sql_qualification": timedelta(days=2),   # Must qualify/disqualify within 2 days
        "proposal_delivery": timedelta(days=5),   # Proposal within 5 days of request
    }

    def check_violations(self):
        violations = []
        for lead in self.get_open_leads():
            for sla_name, sla_limit in self.SLAS.items():
                if lead.get_stage_duration(sla_name) > sla_limit:
                    violations.append({
                        "lead": lead.id,
                        "sla": sla_name,
                        "overdue_by": lead.get_stage_duration(sla_name) - sla_limit,
                        "owner": lead.owner,
                    })
        return violations
```

## Best Practices

1. **Single source of truth** — CRM is the system of record; sync everything back to it
2. **Score leads on both fit and intent** — firmographic + behavioral signals
3. **Pipeline coverage of 3-4x** — if your quota is $1M, you need $3-4M in pipeline
4. **Inspect deals weekly** — pipeline reviews catch stalled deals early
5. **Automate handoffs** — lead routing, stage progression notifications, and SLA alerts
6. **Track leading indicators** — activity metrics predict revenue better than lagging metrics

## Resources

- [RevOps Framework by Clari](https://www.clari.com/resources/)
- [HubSpot RevOps Playbook](https://www.hubspot.com/revenue-operations)
- [SaaS Metrics 2.0 by David Skok](https://www.forentrepreneurs.com/saas-metrics-2/)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |
