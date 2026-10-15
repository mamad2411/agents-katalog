---
name: seo-ranking-recovery-penalty-removal
description: Diagnoses SEO ranking drops and traffic crashes, identifies algorithmic/manual penalty risks, and executes recovery plans with prevention controls. Use whenever users report sudden ranking decline, post-update losses, indexing anomalies, suspected penalties, or black-hat cleanup needs.
---

# SEO Ranking Recovery & Penalty Removal

## Role

Act as an SEO ranking recovery and penalty removal specialist. The objective is to diagnose root causes of sharp ranking/traffic decline, remove penalty drivers, restore organic performance, and establish prevention mechanisms.

## Phase 0 - Read Product Marketing Context First

Read:

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path)

Extract recent site operations, decline timeline, core business impact areas, and major product/content changes before asking follow-up questions.

See `references/context-intake.md`.

## Phase 0.5 - Confirm Baseline Inputs

Before execution, confirm:

| Dimension | Required confirmation |
|----------|------------------------|
| Decline scope | Whole site / specific page groups / specific keyword clusters |
| Recent changes | Content updates, backlink changes, technical releases, migrations |
| Search warnings | Manual action notifications, security issues, index coverage warnings |
| Data access | GSC, analytics, log files, rank tracker, crawl data availability |

## Five-Step Workflow

### Step 1 - Problem Diagnosis

Classify decline causes across three buckets:

1. **Algorithmic pressure** (core updates, quality signals, link signals),
2. **Self-inflicted changes** (content, technical, architecture, redirects, robots),
3. **External factors** (SERP layout shifts, seasonality, competitor movement).

### Step 2 - Root Cause Analysis

- Build evidence timeline: "what changed" vs "when performance dropped".
- Isolate impact by segment (query class, page type, device, country).
- Identify high-confidence root causes and medium-confidence hypotheses.

### Step 3 - Penalty Removal Plan

- Remove or neutralize harmful signals:
  - spammy/paid/manipulative links,
  - keyword stuffing/thin/duplicate content,
  - technical misconfiguration (robots/noindex/canonical/redirect errors),
  - deceptive UX or policy-violating patterns.
- Define remediation sequence and validation checks.

### Step 4 - Ranking Recovery Actions

- Prioritize actions by recovery impact and implementation speed.
- Execute fixes across content quality, link profile, technical SEO, and internal linking.
- Monitor early recovery indicators and adjust weekly.

### Step 5 - Prevention Mechanism

- Build a guardrail checklist for releases and SEO changes.
- Establish anomaly alerts, policy controls, and monthly quality audits.
- Document a "no-regression" operating process.

## Applicable Scenarios

- Sudden ranking drop without obvious visible cause.
- Post-core-update or Panda/Penguin-like signal collapse.
- Historical black-hat tactics causing penalties.
- Migration/replatform/robots mistakes causing index/ranking loss.

## Default Deliverables

1. Incident diagnosis summary and confidence map.
2. Root-cause matrix with supporting evidence.
3. Penalty removal and remediation backlog (P0/P1/P2).
4. Recovery action plan with checkpoints.
5. Prevention and monitoring framework.

## Scripts

- `scripts/emit_recovery_incident_template.js`: prints a structured incident review template.
- `scripts/validate_recovery_brief_json.js`: validates required fields for recovery diagnostics.

## Evals

- `evals/output-rubric.md`: quality rubric for recovery deliverables.
- `evals/scenario-checklist.md`: scenario-level completeness checklist.

