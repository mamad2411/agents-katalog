---
title: Civil UI Card System
description: Navigate and execute the 13-card civil engineering workflow system across 5 design phases with agent integration, status transitions, and dependency management
version: 1.0
frequency_percent: 80.0
success_rate_percent: 94.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-ui-card-system
gigabrain_tags: civil-engineering, ui-cards, workflow-system, card-navigation, status-management, phase-tracking
openstinger_context: ui-card-workflow, 13-card-system
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/00850_AGENTS-REGISTRY-SUMMARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/workflow_docs/implementation/0000_UI_CARDS_IMPLEMENTATION_SUMMARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/workflow_docs/main/0000_CIVIL_ENGINEERING_DESIGN_WORKFLOW.MD
related_skills:
  - pre-task-assessment-readiness
  - workflow-implementation
  - civil-site-assessment
  - civil-design-development
  - civil-documentation
---

# Civil UI Card System

## Overview

Navigate and execute the 13-card civil engineering design workflow system. Each card represents a work package within the 5-phase design process (Site Assessment → Conceptual Design → Preliminary Design → Detailed Design → Procurement/Construction). Cards have dependencies, status transitions, agent integration, and completion criteria.

**Announce at start:** "I'm using the civil-ui-card-system skill to navigate the 13-card civil engineering workflow."

## When to Use This Skill

**Trigger Conditions:**
- Accessing the civil engineering workflow dashboard via modal
- Navigating between workflow cards
- Updating card status (Not Started → In Progress → Complete)
- Checking card dependencies before proceeding
- Viewing agent status for card processing
- Exporting card data or status reports

**Prerequisites:**
- Civil engineering workflow modal loaded
- Agent state active (for "Document Generator" functionality)
- Project data loaded and available
- User has appropriate permissions for the workflow

## Card Inventory and Phase Structure

### Phase 1: Site Assessment & Requirements (Cards 1-4)

| # | Card Name | Purpose | Primary Agent | Dependencies |
|---|-----------|---------|--------------|-------------|
| 1 | Project Brief | Project initiation, scope, requirements | CE-LIB-001 | None |
| 2 | Site Survey | Topographic data, boundaries, existing infrastructure | CE-SITE-001 | Card 1 |
| 3 | Geotechnical | Soil investigation, bearing capacity, foundation | CE-GEO-001 | Card 1, 2 |
| 4 | Environmental | Constraints, protected areas, compliance | CE-ENV-001 | Card 1, 2 |

### Phase 2: Conceptual Design (Cards 5-6)

| # | Card Name | Purpose | Primary Agent | Dependencies |
|---|-----------|---------|--------------|-------------|
| 5 | Design Options | Multi-criteria option analysis | CE-DESIGN-001 | Cards 1-4 |
| 6 | Preliminary Layout | Conceptual design and layout | CE-DESIGN-001 | Card 5 |

### Phase 3: Detailed Analysis (Cards 7-8)

| # | Card Name | Purpose | Primary Agent | Dependencies |
|---|-----------|---------|--------------|-------------|
| 7 | Calculations | Engineering analysis and modeling | CE-STRUCT-001, CE-HYDRO-001 | Cards 1-6 |
| 8 | Preliminary Drawings | Construction documentation draft | CE-DOCS-001 | Card 7 |

### Phase 4: Construction Documentation (Cards 9-12)

| # | Card Name | Purpose | Primary Agent | Dependencies |
|---|-----------|---------|--------------|-------------|
| 9 | Construction Drawings | Final IFC drawings | CE-DOCS-001 | Card 8 |
| 10 | Specifications | Technical requirements | CE-DOCS-001 | Card 8 |
| 11 | Quantity Schedules | BOQ and cost estimation | CE-QS-001 | Card 9, 10 |
| 12 | ITP | Inspection and test plans | CE-QA-001 | Cards 9, 10 |

### Phase 5: Procurement & Construction (Cards 13-14)

| # | Card Name | Purpose | Primary Agent | Dependencies |
|---|-----------|---------|--------------|-------------|
| 13 | Tender Documents | Procurement package | CE-PROC-001 | Cards 9-12 |
| 14 | Construction Support | RFI, variations, monitoring | CE-COLLAB-001 | Card 13 |

## Step-by-Step Procedure

### Step 1: Workflow Dashboard Navigation

**Access the workflow system:**
1. Navigate to Civil Engineering page
2. Click "Document Generator" button (visible only in Agent state)
3. Workflow modal opens showing 14 cards organized by phase
4. Review card status indicators:
   - 🔘 Not Started (default)
   - 🔵 In Progress
   - ✅ Complete
   - 🔴 Blocked (dependency not met)
   - 🟡 Under Review

### Step 2: Card Selection and Data Entry

**For each card:**
1. Click card to expand details
2. Review required fields and current status
3. Check prerequisite cards are complete
4. Initiate card workflow:
   - Click "Start" to change status to In Progress
   - Upload required documents/data
   - Run agent processing if applicable
   - Review results and edit as needed

**Card completion criteria:**
- All required fields populated
- Required documents uploaded
- Agent processing completed successfully
- Quality gate passed (auto-validation)
- User clicks "Mark Complete"

### Step 3: Dependency Management

**Respect card dependencies:**
- Card cannot start until all dependency cards are Complete
- System automatically blocks cards with incomplete dependencies
- Override only with documented justification and manager approval
- Changing a completed card status resets all dependent cards to "Under Review"

**Dependency validation rules:**
| Dependent Card | Requires | Validation Check |
|---------------|----------|-----------------|
| Card 3 (Geotech) | Card 1, 2 | Site boundaries and survey data available |
| Card 5 (Options) | Cards 1-4 | All Phase 1 data collected |
| Card 6 (Layout) | Card 5 | Preferred option selected |
| Card 7 (Calcs) | Cards 1-6 | Design parameters defined |
| Card 8 (Drawings) | Card 7 | All calculations signed |
| Cards 9-12 | Card 8 | Preliminary design approved |
| Card 13 (Tender) | Cards 9-12 | All documentation complete |
| Card 14 (Support) | Card 13 | Contract awarded |

### Step 4: Agent Integration per Card

**Agent-assisted card processing:**
Each card integrates with specialist agents for automated data processing:

**Card 1 (Project Brief):** CE-LIB-001 extracts and structures requirements
**Card 2 (Site Survey):** CE-SITE-001 processes survey DWG data via civil-dwg-processing skill
**Card 3 (Geotech):** CE-GEO-001 analyzes borehole logs and generates recommendations
**Card 4 (Environment):** CE-ENV-001 maps constraints against site boundaries
**Card 5 (Options):** CE-DESIGN-001 runs multi-criteria analysis with weighted scoring
**Card 6 (Layout):** CAD agent generates conceptual layout from selected option
**Card 7 (Calcs):** Structural, hydraulic, and traffic analysis agents run calculations
**Card 8 (Drawings):** Drawing agent generates preliminary drawing set
**Cards 9-12 (Phase 4):** Documentation agents generate specs, BOQ, ITPs
**Card 13 (Tender):** Procurement agent assembles tender package
**Card 14 (Support):** RFI and variation agents process construction queries

### Step 5: Status Transitions and Quality Gates

**Card status transition rules:**
```
Not Started → In Progress    (user clicks Start)
In Progress → Complete        (all criteria met, user confirms)
In Progress → Under Review    (submitted for review)
Under Review → Complete       (review passed)
Under Review → In Progress    (review returned for revision)
Any Status → Blocked          (dependency invalidated)
Blocked → Not Started         (dependency restored)
```

**Phase gate enforcement:**
Cards within each phase must ALL be Complete before any card in the next phase can be started. The CE-ORCH-001 orchestrator automatically enforces phase gates.

### Step 6: Progress Tracking and Reporting

**Dashboard metrics:**
- Overall completion percentage
- Phase completion status
- Individual card status
- Days in current status (age tracking)
- Agent processing status
- Outstanding quality gate issues

**Export options:**
- Workflow status report (PDF)
- Card-by-card completion log (CSV)
- Agent activity log
- Dependency graph visualization

## Success Criteria

- [ ] Workflow dashboard loaded with all 14 cards visible
- [ ] Card dependencies correctly enforced
- [ ] Agent processing initiated for each card
- [ ] All required fields populated for completed cards
- [ ] Phase gates respected (no phase skipped)
- [ ] Status transitions logged with timestamps
- [ ] Progress report exportable at any point

## Common Pitfalls

1. **Ignoring Dependencies** — Attempting to complete Card 5 before Phase 1 cards are done wastes effort. Follow the dependency order.
2. **Forgetting Agent Processing** — Cards that require agent processing (most of them) will show empty results if agents aren't triggered. Always check agent status.
3. **Partial Data Entry** — Incomplete card data causes downstream errors. Fill all required fields before marking Complete.
4. **Skipping Quality Gates** — Phase gates exist for a reason. Bypassing them risks rework when later-phase work is invalidated by earlier-phase changes.
5. **Not Tracking Agent Status** — If an agent is down or slow, card processing will fail. Check agent availability before attempting card automation.

## Cross-References

### Related Skills
- `civil-site-assessment` — Phase 1 cards execute site assessment workflow
- `civil-design-development` — Phase 2-3 cards execute design workflow
- `civil-documentation` — Phase 4 cards execute documentation workflow
- `civil-quality-assurance` — Quality gate enforcement
- `workflow-implementation` — General workflow system patterns

### Related Agents
- `CE-ORCH-001` (OpenClaw) — Workflow orchestrator and dependency manager
- All specialist agents listed per card above

## Example Usage

**Scenario:** Complete Phase 1 cards for a new subdivision project

1. **Dashboard:** All 14 cards showing Phase 1 cards (1-4) as Not Started, Phase 2-5 as Blocked
2. **Card 1 (Project Brief):** Clicked Start, uploaded client brief and project requirements, CE-LIB-001 processed and structured — Marked Complete
3. **Card 2 (Site Survey):** Clicked Start, uploaded RTK survey DWG file, CE-SITE-001 processed via civil-dwg-processing — Marked Complete
4. **Card 3 (Geotech):** Clicked Start, uploaded geotechnical report PDF, CE-GEO-001 extracted and structured recommendations — Marked Complete
5. **Card 4 (Environment):** Clicked Start, GIS layers loaded, CE-ENV-001 identified 3 constraint areas — Marked Complete
6. **Phase Gate:** All Phase 1 Complete → Phase 2 cards unblocked
7. **Export:** Phase 1 completion report generated and shared with team

## Performance Metrics

**Target Performance:**
- Card load time: <1 second for card data
- Agent processing time: <5 seconds per card (non-DWG), <30 seconds (DWG processing)
- Dependency check time: <100ms
- Progress dashboard render: <2 seconds
- Report export: <5 seconds
- User task completion rate: >90% of cards completed without assistance