---
name: workflow-sequences
description: Step-by-step agent sequences for all six Lumen workflows (W1–W6). Reference when routing a workflow to understand which agents run, in what order, and what gates apply.
triggers:
  [
    "pmf-discovery", "pmf-recovery", "strategy", "feature", "launch", "churn",
    "workflow", "run workflow", "pmf", "churn crisis", "W1", "W2", "W3", "W4", "W5", "W6",
  ]
---

## W1 — PMF Discovery

PostHog required for PMF scoring; runs in PARTIAL mode without it (v2.3). 7 steps.

1. **SetupGuide** — validate MCP connections, seed `business_model_type`, write `setup_state`
2. **EventIQ** — validate event schema, confirm BM type, write `validated_event_schema`, `cohort_definitions`, `compliance_flags`
3. **SignalMonitor** — PMF scoring per segment, write `pmf_score_by_segment`, `evidence_quality`, `churn_cohort_fingerprint` — **SKIPPED if PostHog absent; workflow continues as PARTIAL**
4. **DiscoveryOS** — customer discovery, opportunity solution tree, write `opportunity_solution_tree`, `interview_saturation_flag`
5. **MarketIQ** — competitive context, PMF failure classification, write `competitive_moat_map`, `positioning_statement`
6. **DecideWell** *(oversight 2 — APPROVE/DECLINE/MODIFY)* — recovery path decision [consensus: MarketIQ + DiscoveryOS], write `decision_memo`, `outcome_tracking_id`
7. **RoadMap** — PMF recovery roadmap (0–90 days), write `quarterly_roadmap`
8. **HypothesisLab** — 2–3 experiments with network effect isolation check, write `experiment_brief`
9. **Orchestrator** — aggregate evidence, detect conflicts → generate PMF Discovery Report (marked PARTIAL if SignalMonitor skipped)

---

## W2 — PMF Recovery / Churn Crisis

Triggered when `crisis_severity_score` ≥ 7 or PM invokes directly. 7 steps.

1. **SetupGuide** — MCP check + context seed
2. **SignalMonitor** — confirm signal, calculate `crisis_severity_score`, classify `churn_attribution_type`
3. **[parallel]** EventIQ + SignalMonitor — behavioural forensics, write `churn_cohort_fingerprint`
4. **DiscoveryOS** — emergency exit interviews (5 within 72h), participant bias check, write `opportunity_solution_tree`
5. **DecideWell** *(oversight 2 — APPROVE/DECLINE/MODIFY)* — recovery decision [consensus: DiscoveryOS + GrowthIQ + MarketIQ], write `decision_memo`, `outcome_tracking_id`
6. **HypothesisLab** — fastest-possible intervention experiment (2-week max), write `experiment_brief`
7. **GrowthIQ** — win-back campaign, at-risk accounts by ARR × health score, write `at_risk_user_list`, `win_back_sequence`, `nrr_decomposition`
8. **OpsCommand** — leadership briefing adapted to awareness level, write `executive_update`
9. **Orchestrator** → PMF Recovery Report (Day 14 and Day 30 NRR review scheduled)

---

## W3 — Strategy

No hard MCP dependency. 7 steps.

1. **SetupGuide** — MCP check + context seed
2. **[parallel]** SignalMonitor → `pmf_score_by_segment`, `evidence_quality` · MarketIQ → `competitive_moat_map`, `positioning_statement`
3. **DiscoveryOS** — prior quarter interview synthesis, saturation and bias checks, write `opportunity_solution_tree`
4. **NorthStar** — confirm or revise North Star, OKR cascade with conflict check *(Level 2 if NS changes)*, write `north_star_definition`, `okr_cascade`
5. **DecideWell** *(oversight 1)* — three strategic alternatives [consensus: SignalMonitor + DiscoveryOS + MarketIQ + GrowthIQ], write `decision_memo`
6. **PriceLogic** — pricing assessment aligned to `sales_motion`, write `pricing_model`
7. **RoadMap** — quarterly roadmap with capacity_constraint and contract commitment checks, write `quarterly_roadmap`
8. **[parallel]** NarrativeEngine → `narrative_suite` · OpsCommand → `executive_update`, `operating_rhythm_calendar`
9. **Orchestrator** → Strategy Report

---

## W4 — Feature Validation

DataLayer ethics checkpoint is mandatory for AI/ML features. 7 steps.

1. **SetupGuide** — MCP check + context seed
2. **[parallel]** EventIQ + SignalMonitor — behavioural evidence check, write `feature_usage_signal`, `validated_event_schema`
3. **DataLayer** *(oversight 3 — Governance Checkpoint 1)* — **runs ONLY if feature includes AI/ML**; write `ethics_clearance`, `compliance_flags`, `sign_off_required_by`
   - If BLOCKED: stop workflow entirely; escalate to `sign_off_required_by`
4. **DiscoveryOS** — 3–5 targeted interviews (SKIP if `evidence_already_exists = Validated`), write `opportunity_solution_tree`
5. **HypothesisLab** — minimum experiment design, baseline metric required, network effect isolation check, write `experiment_brief`, `power_calculation`
6. **UXLayer** *(oversight 1)* — minimum interaction design, platform constraints, accessibility flags, write `interaction_design_spec`
7. **DecideWell** *(oversight 1)* — build/test/buy decision, implementation capacity check, write `decision_memo`, `outcome_tracking_id`
8. **DataLayer** *(oversight 3 — Governance Checkpoint 2)* — experiment bias audit; **only if Checkpoint 1 cleared**
9. **Orchestrator** → Feature Validation Report

---

## W5 — GTM Launch

Requires launch type + target segment in context. 7 steps. Readiness thresholds: Feature 7/10 · Product 8/10 · Pricing 9/10 · Market entry 8/10.

1. **SetupGuide** — MCP check + context seed
2. **LaunchPad** *(oversight 1 — open)* — readiness audit adapted to launch type, write `launch_readiness_score`
3. **NarrativeEngine** — launch messaging for audiences from intake, regulatory claim check, write `narrative_suite`, `audience_messaging_matrix`
4. **UXLayer** *(oversight 1)* — trust calibration validation, platform constraints, accessibility check, write `interaction_design_spec`
5. **PriceLogic** — pricing confirmation, sales motion alignment, existing customer protection check, write `pricing_model`
6. **DataLayer** *(oversight 2 — Governance Checkpoint 3)* — pre-launch stewardship checklist, confirm `sign_off_required_by`
7. **OpsCommand** *(oversight 2)* — launch execution plan, crisis communications path, go/no-go framed around success_metric, write `executive_update`, `launch_execution_plan`
8. **LaunchPad** *(oversight 2 — close)* — post-launch monitoring, staged rollout plan (Day 1/7/30 checkpoints), write `post_launch_monitoring_plan`
9. **Orchestrator** → Launch Report (GrowthIQ PQL monitoring begins; SignalMonitor tracks PMF impact)

---

## W6 — Churn Crisis

Triggered when `crisis_severity_score` > 7 or NRR < 90%. ARR-prioritised intervention plan. 7 steps.

1. **SetupGuide** — MCP check + context seed
2. **SignalMonitor** — confirm crisis, classify `churn_attribution_type`, quantify ARR at risk
3. **[parallel]** EventIQ + SignalMonitor — behavioural forensics, write `churn_cohort_fingerprint`
4. **DiscoveryOS** — emergency exit interviews (3 if cause known; 5 if unknown), participant bias check, write `opportunity_solution_tree`
5. **GrowthIQ** — NRR decomposition, at-risk accounts by ARR × renewal proximity, upsell vs. cross-sell split, write `nrr_decomposition`, `at_risk_user_list`
6. **HypothesisLab** — intervention experiment (2-week max), network effect isolation check, write `experiment_brief`
7. **DecideWell** *(oversight 2 — APPROVE/DECLINE/MODIFY)* — intervention options [consensus: GrowthIQ + DiscoveryOS + PriceLogic]; exclude already-tried options from intake *(Level 2 if pricing option)*, write `decision_memo`, `outcome_tracking_id`
8. **OpsCommand** — leadership briefing, crisis comms path, 30/60/90-day recovery metrics, write `executive_update`
9. **Orchestrator** → Churn Crisis Report (GrowthIQ monitors daily; 30/60/90-day outcome tracking IDs set)

---

## Cross-workflow rules

- SetupGuide always runs first; never skip.
- W1 runs in PARTIAL mode if PostHog is absent — SignalMonitor is skipped; EventIQ and DiscoveryOS continue; report is marked PARTIAL with PMF scoring section empty. No CSV fallback. (v2.3)
- DecideWell requires PM APPROVE/DECLINE/MODIFY before Orchestrator proceeds.
- DataLayer BLOCKED status (W4 Governance Checkpoint 1) stops the workflow entirely until `sign_off_required_by` grants clearance.
- If any two parallel agents write conflicting values to the same downstream slot, Orchestrator sets `conflict_detected=true` and routes to DecideWell before generating the report.
