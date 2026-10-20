---
name: practice-management
description: >
  Contains verified six-phase engagement lifecycle with quality gates (onboard through
  archive), capacity planning formula with extension-first surge strategy, and staff
  assignment criteria (competency, continuity, independence, workload balance). Engagement
  throughput, deadline calendar layering (external/internal/reminder triggers), seasonal
  workload distribution, WIP aging, cross-functional handoffs (BK to TX to FP), AICPA SQMS
  No. 1 engagement performance. Consult when planning work allocation across tax seasons,
  building or evaluating a master deadline calendar, balancing staff workloads or assigning
  engagement teams, designing engagement phase workflows or status tracking, coordinating
  cross-service-line handoffs, or assessing whether to extend vs. file on time.
---

# Practice Management

Operational framework for orchestrating firm workflow, resource allocation, and engagement
throughput. All procedures below are synthesized from the firm's practice management
knowledge base and reflect the lifecycle, cadences, and decision rules that govern daily
operations.

## Engagement Lifecycle

Six sequential phases. Each phase has a quality gate that must clear before advancing.

### Phase 1 -- Onboarding

Triggered by signed engagement letter. Deliverable: engagement record in practice
management system, team assigned, internal deadlines set.

- Client acceptance evaluation complete
- Engagement letter signed and filed
- Client record created with entity type, tax year, service codes
- Prior-year returns and financial data obtained and reviewed
- Access credentials secured (accounting system login, bank portal, prior preparer auth)
- Engagement team assigned: preparer, reviewer, engagement partner
- Electronic folder structure created per firm template
- Internal deadlines calculated backward from filing due date

### Phase 2 -- Setup

- Chart of accounts verified or created in accounting software
- Engagement checklist/template loaded for the return type
- Prior-year data imported (trial balance, carryforward amounts)
- Information gaps identified; initial PBC list issued to client
- Client kick-off communication scheduled for new or complex engagements

### Phase 3 -- Execution

- Source documents collected and organized as received
- PBC list completion tracked; follow-up at 2-week, 4-week, 6-week intervals
- Workpapers, lead schedules, and supporting computations prepared
- Draft return or financial statements produced
- Assumptions, judgments, and positions documented
- Items flagged for reviewer attention (uncertain positions, unusual transactions)

### Phase 4 -- Review

Two-tier review structure:

1. **First-level** (senior/manager) -- Technical accuracy, completeness, tie-out to source data
2. **Second-level** (partner/EQ) -- Overall reasonableness, risk positions, presentation

Review notes documented and resolved by preparer. No advancement to delivery until all
open items are resolved and tax e-file diagnostics are clear.

### Phase 5 -- Delivery

- Final return/deliverable generated in client-ready format
- Cover letter prepared: key items, tax due, action items
- Client approval and e-file authorization obtained (Form 8879)
- Return e-filed or paper-filed
- Client copy delivered via secure portal or encrypted transmission
- Invoice issued per engagement letter terms

### Phase 6 -- Archive

- Workpaper file finalized and locked
- Signed engagement letter, e-file authorization, and filed return stored
- Practice management system updated: engagement marked complete, actual time and fees recorded
- Post-engagement assessment documented (lessons learned, client-specific issues)
- Reminder set for next-year engagement start date

## Quality Gates

Each lifecycle transition has a checkpoint. Use this table to validate readiness before
advancing any engagement.

- **Onboarding to Setup** -- Engagement letter signed? Prior data obtained? Team assigned?
- **Setup to Execution** -- PBC list issued? System setup verified? Carryforwards imported?
- **Execution to Review** -- All workpapers complete? PBC items resolved? Diagnostics clear?
- **Review to Delivery** -- Review notes resolved? Partner sign-off? E-file auth obtained?
- **Delivery to Archive** -- Return filed? Invoice sent? File locked?

If any gate fails, the engagement stays in the current phase. Do not skip gates.

## Deadline Tracking

### Calendar Layering

Maintain a master deadline calendar covering all clients and all jurisdictions. Three
layers of dates per engagement:

1. **External deadlines** -- Original due date, extended due date, estimated payment dates, state-specific dates
2. **Internal deadlines** -- Set 7-14 days before external deadlines
3. **Reminder triggers** -- Automated alerts at 30, 14, 7, and 3 days before internal deadline

### Missed-Deadline Protocol

Immediate escalation to engagement partner. Assess filing options (extension, late filing
penalties). Document the miss, root cause, and corrective action.

For tax-specific deadline integration, invoke `tax-prep:tax-compliance` for the
authoritative calendar of federal and state filing dates, extension deadlines, and
estimated payment schedules.

## Staff Assignment

Five criteria, evaluated in order:

1. **Competency match** -- Staff experience must align with engagement type (e.g., corporate tax experience for Form 1120 engagements)
2. **Development opportunity** -- Pair less experienced staff with mentors on moderate-complexity work
3. **Continuity** -- Same team on recurring engagements year-over-year for efficiency and institutional knowledge
4. **Independence** -- Verify no conflicts of interest between staff and client
5. **Workload balance** -- No single person should be the bottleneck for more than a defined percentage of active engagements

## Capacity Planning

### Calculation Framework

1. **Inventory** -- Count total engagements by type and complexity tier (simple, moderate, complex)
2. **Budget hours** -- Assign expected hours per engagement tier

   - Simple (e.g., basic 1120): ~8 hours
   - Moderate: ~20 hours
   - Complex (multi-state, consolidated): ~40 hours

3. **Available capacity** -- Total professional hours per period minus admin, CPE, and PTO
4. **Load balancing** -- Distribute engagements across team to equalize utilization
5. **Surge planning** -- Identify peak demand windows and plan overtime, seasonal staff, or proactive extensions

### Extension-First Strategy

When total budgeted hours exceed available capacity, extend returns proactively rather
than rushing. An extension-first approach (extend all, then file in complexity order)
produces higher quality than compressing timelines. This is a deliberate quality decision,
not a failure mode.

## Seasonal Workload Distribution

- **January -- March** -- Data collection, W-2/1099 processing, entity return preparation (Form 1120 due April 15 for calendar-year corps)
- **April 1--15** -- Final push for original filings; file extensions for returns not ready
- **May -- September** -- Extended return preparation, tax planning, bookkeeping catch-up, CPE
- **October 1--15** -- Final push for extended returns
- **November -- December** -- Year-end planning, engagement letter renewals, system updates, internal training

## Workflow Design Rules

### Status Tracking

All engagement status tracked in one system. Firm-wide status categories:

- Not Started
- In Progress
- In Review
- Ready to Deliver
- Complete

Avoid parallel tracking in email, spreadsheets, or project boards. Context-switching
cost across fragmented tools exceeds the cost of a single purpose-built system.

### Status Transition Triggers

"In Review" means all workpapers complete and no open PBC items. Every transition
includes a brief handoff note to the next role covering key items and risk areas.
The receiver acknowledges receipt and sets their own completion target.

### WIP Aging

Focus on completing engagements rather than starting many in parallel. A return that
is 90% done but waiting on one document is less valuable than one that is 100% done
and filed. Set WIP aging targets and escalate engagements that exceed expected duration.

### Standardized Templates

Every engagement type has a standard checklist and workpaper template. Templates enforce
completeness -- the preparer cannot skip steps. Update templates annually for law changes,
form revisions, and lessons learned.

## Client Communication Cadence

- **Engagement start** -- Kick-off email with timeline, PBC list, and key deadlines
- **Document collection** -- Follow-up at 2 weeks, 4 weeks, 6 weeks if items outstanding
- **Status update** -- Notify client when return enters review (sets delivery timeline expectation)
- **Delivery** -- Cover letter with action items and payment instructions
- **Post-filing** -- E-file acknowledgment shared with client
- **Off-season** -- Annual check-in for continuance, planning opportunities, fee discussion

## Cross-Functional Handoffs

Service-line coordination follows the engagement lifecycle. Common handoff patterns:

- **BK to TX** -- Bookkeeping produces closed books (trial balance, reconciled bank statements). Tax prep consumes the trial balance as the starting point for return preparation. Handoff trigger: all periods reconciled and closing date password set in the accounting system. For platform-specific closing date procedures, invoke `qbo-integration:qbo-bookkeeping`.
- **TX to FP** -- Completed tax return feeds into financial planning for tax projection models and estimated payment schedules.
- **Engagement start to all lines** -- Engagement management provides the signed letter and client profile that every service line consumes.

## Decision Framework

- **Single vs. multiple workflow tools** -- Consolidate to one practice management system. Fragmentation across tools costs more in context-switching than a purpose-built tool costs in licensing.
- **Extension-first vs. on-time-first** -- See capacity planning section above. Default to extension-first when capacity is constrained.
- **Fixed team vs. rotating assignments** -- Fixed teams build institutional knowledge; rotating assignments build bench strength. Balance based on firm size and key-person risk tolerance.
- **Client portal adoption** -- Require secure portal for document exchange. Email-based collection is both a security risk and an efficiency drag.

## Accounting System Integration

The accounting system serves as both the platform and a workflow artifact -- engagement
execution produces journal entries, reconciliations, and reports within it.

- Document accounting system subscription ownership in the engagement letter (client-owned vs. firm-owned)
- Closing date and password controls enforce the review-to-archive handoff
- Export trial balance and financial statements from the accounting system as part of the archive phase
- For multi-year reconstruction projects, period-locking sequence must follow pipeline stage order
- For platform-specific execution (multi-client management, closing date procedures, period locking), invoke `qbo-integration:qbo-bookkeeping`

## Supporting References

- `references/practice-management.md` -- Complete practice management knowledge base. Sections: engagement lifecycle phases with detailed step lists (lines 9-57), workflow design principles including single-source-of-truth and WIP minimization (lines 58-79), capacity planning formula and surge strategy (lines 80-88), staff assignment criteria (lines 89-96), quality checkpoints per phase transition (lines 98-106), client communication cadence with follow-up intervals (lines 107-115), deadline tracking with reminder schedule (lines 117-123), seasonal workload calendar (lines 124-131), technology stack considerations (lines 132-141), accounting system integration notes (lines 142-150), strategic decision points (lines 152-157), authoritative references including AICPA SQMS No. 1, IRS Circular 230, and Florida FAC 61H1 (lines 159-164). Read for the full procedural detail behind any section above.

## Cross-Plugin References

- Invoke `tax-prep:tax-compliance` for federal/state tax deadline calendars and filing requirement rules that feed the master deadline calendar
- Invoke `firm-operations:engagement-management` for engagement letter procedures, client onboarding checklists, and billing models that initiate the lifecycle
- Invoke `firm-operations:workflow-automation` for automation opportunities in repetitive workflow steps (PBC tracking, status reminders, deadline alerts)

## Cross-Plugin Consumers

- `firm-operations:quality-compliance` -- Consumes review scheduling and quality gate procedures
- `tax-prep:form-1120-prep` -- Consumes engagement timeline and internal deadline targets
- `bookkeeping` skills -- Consume workflow status and handoff triggers for BK-to-TX coordination
