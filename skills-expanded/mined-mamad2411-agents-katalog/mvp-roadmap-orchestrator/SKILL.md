---
name: mvp-roadmap-orchestrator
description: "Use when turning a problem statement into an MVP plan, prioritization stack (Value/Effort, RICE, KANO, MoSCoW), 2-week sprint roadmap, PRD pack, and governed delivery documentation."
cluster: ai-agents-meta
version: 1.0.0
origin: "craft-agent workspace"
---

# MVP Roadmap Orchestrator

Convert a raw idea into an execution-ready MVP plan with explicit prioritization, risk gates, scope control, and versioned product documentation.

## Use When

Activate when the user asks for:
- problem statement → MVP
- roadmap, sprint plan, PRD, or delivery planning
- prioritization with Value/Effort, RICE, KANO, or MoSCoW
- POC before roadmap commitment
- 2-week sprint stories, Gantt/timeline, or scope governance
- documentation/versioning for product delivery

## Out of Scope (Default)

Do **not** treat these as MVP by default unless explicitly requested:
- enterprise/compliance edge cases
- advanced automation and “nice-to-have” integrations
- multi-region scale architecture
- non-critical redesign work

## Input Contract (Ask if Missing)

Before planning, gather:
1. Target user + top pain
2. Business objective + timeline
3. Team capacity (roles, availability)
4. Constraints (budget, legal, platform, dependencies)
5. Success metric baseline (if available)

If key inputs are missing, ask targeted questions first.

## Core Principles

1. Problem-first, feature-second.
2. Evidence over opinion.
3. POC before full commitment on risky items.
4. Scope discipline over roadmap vanity.
5. Versioned docs and explicit decision ownership.

---

## Execution Workflow

### 0) Discovery + Alignment
- Restate the problem and desired outcome in one paragraph.
- Confirm audience split: dev team, exec team, business, ops.
- Define planning horizon (MVP only vs MVP + next 2 horizons).

### 1) Problem Statement → Outcome Definition
- Capture pain, affected segment, current workaround, and impact.
- Define north-star metric + 2–4 leading indicators.
- Define MVP success threshold (launch is “done when …”).

### 2) Opportunity Backlog Creation
- Generate initiatives from user pain, business goals, and constraints.
- Add effort assumptions, dependencies, and risk notes per item.
- Mark each assumption as **validated / unvalidated**.

### 3) Prioritization Framework Stack (in order)

#### A) Value vs Effort
- Plot each opportunity: Quick Wins / Strategic Bets / Fill-ins / Avoid.
- Remove low-value high-effort items from MVP candidate list.

#### B) RICE
- Score formula: `(Reach × Impact × Confidence) / Effort`.
- Show scoring ranges and assumptions for each variable.
- Flag low-confidence high-score items for validation.

#### C) KANO
- Classify as Must-have / Performance / Delighter.
- Keep Delighters out of MVP unless they unlock adoption risk.

#### D) MoSCoW
- Gate final sprint scope into Must/Should/Could/Won’t (this cycle).
- Explicitly list exclusions and rationale.

### 4) POC Gate (Before Roadmap Lock)
- Select top 1–3 risks (technical, desirability, viability, operational).
- Define each POC with:
  - hypothesis
  - success/fail criteria
  - timebox
  - owner
  - decision date
- Require **Go / No-Go / Pivot** decision before roadmap commitment.

### 5) Research + Testing Loop
- Plan lightweight validation: interviews, surveys, prototype tests, concierge.
- Capture insight → decision mapping:
  - keep
  - modify
  - drop
- Update RICE confidence and MoSCoW gates after each evidence round.

### 6) SLC Framing + Data Events
Define MVP through SLC:
- **Simple**: minimum viable user journey
- **Lovable**: moments that create confidence and repeat use
- **Complete**: end-to-end task completion for one core use case

For each SLC element, define data events:
- event name
- trigger point
- properties
- owner
- dashboard metric linkage

### 7) PRD Pack
Create PRD sections:
- problem/opportunity statement
- target users + JTBD
- scope in/out
- assumptions + dependencies
- functional requirements
- non-functional requirements
- acceptance criteria
- data/analytics plan
- risk register + mitigations
- launch readiness gates

### 8) Sprint Plan (2-Week Cadence)
- Build 2-week sprints with capacity-aware allocation.
- Write user stories using INVEST quality bar.
- Include acceptance tests for each story.
- Sequence work by dependency chain (product/design/dev/ops/legal if needed).

### 9) Timeline + Gantt View
- Convert sprint plan to timeline with milestones and decision gates.
- Mark critical path, parallel tracks, and buffer windows.
- Include rollback/contingency milestones for risky deliveries.

### 10) Scope Governance + Execution
- Use change requests for any new item after sprint lock.
- Re-score new work with RICE + MoSCoW before acceptance.
- Enforce WIP limits and prevent stealth scope creep.

### 11) Iterate + Version Documentation
- Run sprint review + retro with user and stakeholder feedback.
- Update roadmap as a time-based vision expansion.
- Version PRD, roadmap, events taxonomy, decisions, and release notes.

---

## Hardened Controls (20 Improvements)

1. Explicit input contract before planning.
2. Mandatory clarification when critical fields are missing.
3. Scope boundary section (Out of Scope) to prevent bloat.
4. Assumption tagging as validated/unvalidated.
5. Standard RICE formula and transparent scoring.
6. Confidence-risk flags for low-confidence high-score items.
7. Ordered framework stack to avoid random prioritization.
8. Explicit exclusion list with rationale.
9. POC Go/No-Go/Pivot gate before roadmap lock.
10. Timeboxed POC with owner and decision date.
11. Evidence update loop that re-scores priorities.
12. SLC model tied to measurable data events.
13. Event schema fields (name/trigger/properties/owner/metric).
14. PRD minimum required sections defined.
15. INVEST quality bar for stories.
16. Acceptance tests required per story.
17. Capacity-aware 2-week sprint planning.
18. Critical path + contingency in timeline/Gantt.
19. Change request + re-prioritization for scope creep.
20. Documentation versioning + decision log ownership.

---

## Output Artifacts (Default)

1. Problem-to-MVP summary (with success criteria)
2. Prioritized opportunity backlog (with Value/Effort + RICE + KANO + MoSCoW)
3. POC plan with decision gates
4. PRD draft or structured PRD outline
5. 2-week sprint plan + user stories + acceptance tests
6. Gantt-style timeline with milestones and critical path
7. Scope governance policy (change control + prioritization rules)
8. Documentation/versioning checklist + decision log template

## Reusable Templates (Use by Default)

- `PRDTemplate.md`
- `DecisionLogTemplate.md`
- `BacklogScoringTemplate.md`

When generating deliverables, instantiate these templates first, then fill with project-specific details.

## NotebookLM Asset Automation (Python Module)

Use wired scripts to generate source-backed research artifacts and prefill planning docs:

- Wrapper (recommended): `run_mvp_pipeline.py`
- Generator: `generate_assets_notebooklm.py`
- Prefill: `prefill_templates_from_assets.py`
- Guide: `NotebookLMIntegration.md`

Default flow:
1. Ensure auth (`notebooklm login`).
2. Run generator with sources (URLs/files) and selected assets.
3. Run prefill script to produce PRD/backlog/decision drafts.
4. Review and finalize with team-specific constraints.

Default command pattern:

```bash
./run_mvp_pipeline.py \
  --project-dir /path/to/project \
  --owner "<Owner>" \
  --asset report --asset mind-map --asset data-table
```

Manual two-step fallback:

```bash
./generate_assets_notebooklm.py \
  --title "MVP Research - <project>" \
  --source "https://example.com" \
  --source ./problem-statement.md \
  --asset report --asset mind-map --asset data-table \
  --output-dir ./outputs/<project>

./prefill_templates_from_assets.py \
  --assets-dir ./outputs/<project> \
  --templates-dir . \
  --output-dir ./outputs/<project>/prefilled \
  --project "<Project Name>" \
  --owner "<Owner>"
```

## Quality Gates (Definition of Done)

A plan is complete only when:
- success metrics are measurable,
- assumptions are explicit and risk-ranked,
- POC gates are defined for top risks,
- priorities include transparent scoring and exclusions,
- stories are testable and capacity-bounded,
- data events map to outcomes,
- and document ownership/versioning is clear.

## Failure Modes to Avoid

- jumping into roadmap before defining MVP success
- scoring without confidence assumptions
- mixing Must-have and Delighter work in same sprint without rationale
- accepting scope changes without re-scoring
- claiming completion without testable acceptance criteria
