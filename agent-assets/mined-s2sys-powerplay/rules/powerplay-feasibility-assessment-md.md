---
name: feasibility-assessment
description: Feasibility assessment — 3-dimension analysis, risk tiers, estimation principles, Definition of Ready
alwaysApply: false
---

# Feasibility Assessment & Risk Evaluation

Applied when assessing whether a user story or feature should proceed to development. Ensures the team understands what can realistically be built, what could go wrong, and when to spike before building.

---

## 3 Feasibility Dimensions

Every requirement must pass evaluation across all three dimensions. Each dimension has known-good and known-bad indicators.

### 1. Technical Feasibility

**Evaluation Questions:**
- Do we have experience with this technology or can we ramp quickly?
- Are there unknowns or unproven integrations (third-party APIs, new libraries, unfamiliar frameworks)?
- Does this introduce breaking changes to existing systems?
- Is there a migration path if this approach fails?
- What dependencies exist on infrastructure, external services, or other teams?

**Green Indicators** (Low Risk):
- Uses existing tech stack or proven alternatives
- Integration points are well-documented
- API contracts are clear
- No database migration complexity
- Dependencies are internal and manageable

**Red Indicators** (High Risk):
- New framework or language we've never used
- Third-party API has limited documentation
- Unproven integration with production systems
- Requires major database refactoring
- Hard dependency on external team's delivery

---

### 2. Resource Feasibility

**Evaluation Questions:**
- Do we have the right skill set on the team?
- Is there a single person who owns this knowledge (key-person risk)?
- Do we have capacity in the current sprint or team bandwidth?
- Are external resources or contractors required?
- What is the estimated effort (story points, developer-days)?

**Green Indicators** (Low Risk):
- Team has built similar features before
- Knowledge is distributed across 2+ people
- Capacity matches estimate
- No external dependencies
- Estimate converges (all estimates within 2× range)

**Red Indicators** (High Risk):
- Only one person knows the domain
- Team has never attempted this type of work
- Capacity is tight or allocated elsewhere
- Requires vendor or contractor engagement
- Estimate range is > 3× (uncertainty is high)

---

### 3. Timeline Feasibility

**Evaluation Questions:**
- Is there a fixed deadline? How much buffer?
- What is the critical path (longest chain of dependent tasks)?
- Are there external dependencies (design reviews, compliance, other teams)?
- What is the review/approval cycle time?
- Are there holidays, PTO, or planned outages in the window?

**Green Indicators** (Low Risk):
- No hard deadline or deadline is 3+ sprints away
- Work is parallelizable (no hard serial dependencies)
- Review cycles are < 2 days
- Team availability is 100% or near it
- Built-in buffer (estimate is 60% of available time)

**Red Indicators** (High Risk):
- Hard deadline is < 2 sprints away
- Critical path has many sequential steps
- Review cycle is slow (legal, compliance, stakeholder)
- Key people have planned PTO during window
- Estimate is 100% of available time (zero buffer)

---

## Risk Tiers

Assign each requirement a risk tier based on how many dimensions show red indicators and their severity.

| Tier | Criteria | Response | Max Wait Before Spike |
|------|----------|----------|----------------------|
| **Low** | All three dimensions green; familiar pattern; estimate converges | Proceed directly to development. Document assumptions. | N/A (no spike needed) |
| **Medium** | 1 dimension has amber indicator; estimate range is 2-2.5×; some unknown unknowns | Document risks and mitigations. Proceed to development with heightened monitoring. Risk owner assigned. | Can proceed; no spike required |
| **High** | 1 red indicator in any dimension; estimate range > 2.5×; unknowns are significant | **MANDATORY SPIKE** before starting development. Max spike duration: 3 days. Spike must resolve the red indicator or provide a workaround. | Cannot proceed; spike first |
| **Critical** | 2+ red indicators; hard timeline + unknown tech; blocking dependency uncertai; showstopper risk | **IMMEDIATE STOP.** Do not assign to a sprint. Form spike team. Max spike duration: 5 days. Spike MUST produce a prototype, risk register, or decision to pivot. Go/No-Go gate after spike. | Cannot proceed under any circumstance; mandatory extended spike |

**CRITICAL tier examples:**
- "Build new payment processor integration" + "never integrated payments before" + "PCI compliance unknown" + "hard deadline in 2 weeks"
- "Migrate 10-year-old monolith to microservices" + "zero team experience with K8s" + "live data migration required" + "cannot afford downtime"
- "Integrate third-party audit service" + "no documented API" + "compliance deadline is firm" + "single contractor who understands it leaving in 3 weeks"

---

## Spike vs. Build Decision

### When to Spike (Mandatory for High/Critical)

**SPIKE if any of these are true:**
- Technical dimension has red indicator (unknown tech, unproven integration, unclear migration path)
- Estimate range exceeds 3× (Low: 5pts, High: 15pts = uncertainty is too high)
- Team has never attempted this work before and risk is Medium or higher
- Architecture decision between 2+ approaches with different tradeoffs
- External dependency is unproven (API not yet tested, vendor not yet approved)

**Spike Charter (max 3-5 days for High; 5-10 days for Critical):**
- Goal: answer ONE blocking question or reduce estimate variance to < 2×
- Deliverable: working prototype, architectural decision document, or risk register
- Definition of Done: spike owner presents findings; team decides Proceed / Pivot / Abandon

### When to Build (No Spike Needed)

**BUILD directly if all these are true:**
- All three dimensions are green or amber
- Estimate range is ≤ 2× (converges around similar story point range)
- Team has 2+ people familiar with the pattern
- No hard blockers or unknown unknowns
- Resource and timeline feasibility are confirmed

---

## Estimation Principles

### Cone of Uncertainty

As you progress through SDLC phases, estimate accuracy improves:

| Phase | Accuracy Range | Method | Owner |
|-------|-----------------|--------|-------|
| **Requirements** | ±50% | T-shirt sizing (XS/S/M/L/XL) | Product manager |
| **Architecture** | ±30% | Story point range (3-8 pts) | Tech lead |
| **Sprint Planning** | ±10% | Hours (4-8 hrs per task) | Scrum team |
| **Daily Standup** | ±5% | Remaining hours | Developer |

**NEVER estimate in hours at requirements phase.** Use T-shirt sizing only.

### T-Shirt Sizing Guide

Convert requirements to T-shirt size before story pointing:

| Size | Story Points | Duration | Definition | When to Split |
|------|--------------|----------|-----------|---------------|
| XS | 1 | < 2 hours | Trivial change; one file; no testing | N/A |
| S | 2-3 | Half day | One feature; light testing; familiar pattern | If it touches 3+ files |
| M | 5 | 1-2 days | Feature with integration; moderate testing; some unknowns | If estimate range > 2× |
| L | 8 | 3-4 days | Feature + dependent features; integration tests; architecture decision | **ALWAYS split into smaller stories** |
| XL | 13+ | > 1 week | Epic-level; spans multiple features; major refactoring | **MANDATORY SPLIT** before development |

**Rule: Any story > 8 points MUST be split into 5-8pt stories.**

### Reference Class Forecasting

When T-shirt sizing, ask: "What similar work have we done before?"

- **"We built password reset last quarter"** (similar scope) → Use that as reference. Add ±20% if context differs.
- **"We've never done X before"** → Upgrade size by 1 tier (S → M, M → L). Spike first if L.
- **"We're using a new framework"** → Upgrade by 1-2 tiers. SPIKE required.

---

## Definition of Ready Checklist

A story or feature is ready for development only when **ALL 13 items** are satisfied:

**Story Format & Clarity:**
- [ ] Story follows "As a [role], I want [feature], so that [benefit]" format
- [ ] Role is specific (not generic "user")
- [ ] Feature is a single coherent action (not bundled)
- [ ] Benefit is measurable and testable

**Acceptance Criteria & Testability:**
- [ ] Acceptance criteria follow Given/When/Then (Gherkin) format
- [ ] Minimum 1 happy path, 2 alternative paths, 1 error scenario
- [ ] Each criterion is a single scenario (no compound "or" actions)
- [ ] All side effects are explicitly stated (emails, logs, database changes, flags)

**INVEST Principles:**
- [ ] Independent: Does not require another story to be completed first? (Or dependency is explicitly noted: "Depends on Story-###")
- [ ] Negotiable: Can implementation details be negotiated until sprint start?
- [ ] Valuable: Does this deliver clear value to the named role?
- [ ] Estimable: Can the team size this in story points? (If not, it's too vague)
- [ ] Small: Can it be completed in one sprint (≤ 5 business days)? (Or is it split into smaller stories?)
- [ ] Testable: Can acceptance criteria be verified by a test?

**Feasibility & Risk:**
- [ ] Feasibility assessed: All three dimensions (technical/resource/timeline) evaluated. Tier assigned (Low/Medium/High/Critical).
- [ ] Risk tier ≤ Medium OR spike is complete: If High/Critical, spike has been done and findings documented.
- [ ] Technical approach agreed: Architecture decision made. Existing patterns identified (see security-guard, api-versioning, performance-budget rules). No ambiguity about how it will be built.

**Dependencies & Context:**
- [ ] External dependencies identified: Required from other teams, vendors, or systems.
- [ ] Non-functional requirements defined: Performance thresholds (P95 latency, uptime SLA), security requirements (encryption, RBAC), scalability (concurrent users), availability (graceful degradation).

**Design & Data Model:**
- [ ] UI mockups or acceptance (if UI work): Designer has reviewed. Accessibility (WCAG) considered.
- [ ] Data model or schema change defined (if applicable): Normalization verified. Indexes planned. No data loss on migration.

**Security & Compliance:**
- [ ] Security review completed: Data classification (PII/payment/internal). Authorization rules. Encryption in transit and at rest. Input validation scope.
- [ ] Compliance scope identified (if applicable): GDPR, PCI-DSS, SOC 2, HIPAA, etc. Legal review gate identified.

**Estimation & Sizing:**
- [ ] Story sized in story points: T-shirt size converted to story points. Estimate is ≤ 8 points (split if larger).
- [ ] Team has consensus on size: Min 2 estimates within 3-5 points. Outliers discussed and converged.

**NEVER proceed to development if any item is incomplete.** Return to Product Owner for clarity.

---

## Risk Register Template

When assigning High or Critical tier, create a Risk Register:

| Risk ID | Description | Category | Likelihood (L/M/H) | Impact (L/M/H) | Score (L×I) | Owner | Mitigation |
|---------|-------------|----------|-------------------|-----------------|-------------|-------|-----------|
| RISK-001 | Unknown payment API integration | Technical | H | H | 9 | Tech Lead | Spike: test integration with sandbox API (3 days) |
| RISK-002 | Key developer PTO during delivery window | Resource | M | H | 6 | PM | Pair programming setup; documentation focus |
| RISK-003 | Database migration on live data not tested | Technical | M | H | 6 | DBA | Spike: test migration script on production replica (2 days) |

**Risk Score = Likelihood × Impact** (L=1, M=2, H=3. Max score = 9)

Sort by Score (descending). Focus mitigation on Score ≥ 6.

---

## Go/No-Go Decision After Spike

After a spike is complete, the tech lead presents findings to the team:

### GO Criteria
- [ ] No Critical risks remain unmitigated
- [ ] All High risks have documented mitigations
- [ ] Estimate converges (range ≤ 2×)
- [ ] Technical approach is proven (prototype works, API contract confirmed, migration path validated)
- [ ] Definition of Ready checklist is 100% complete

### NO-GO Criteria (Do Not Proceed)
- [ ] Technical approach is infeasible or unproven
- [ ] One or more Critical risks cannot be mitigated
- [ ] External blocker is unresolved (vendor approval pending, legal review uncompleted, dependency team unavailable)
- [ ] Scope should be pivoted or descoped
- [ ] Resource plan is unrealistic

**If NO-GO**: Document decision, spike findings, and recommended path forward (pivot, defer, abandon, descope).

---

## Good Example: Spike Definition

**Story**: As an admin, I want to integrate with the new compliance audit service, so that we can generate SOC 2 reports automatically.

**Initial Assessment**: High risk (unknown service, PCI compliance deadline firm, single contractor knowledge, hard deadline 6 weeks)

**Spike Charter**:
- **Goal**: Confirm audit service API is production-ready and can meet our data residency requirements
- **Tasks**:
  - Test sandbox API with sample data (day 1)
  - Confirm data residency policy (day 1)
  - Prototype authentication flow (day 2)
  - Validate audit report output format (day 2)
  - Assess compliance with PCI-DSS scope (day 3)
- **Definition of Done**: Working prototype, API integration guide, risk register, Go/No-Go recommendation
- **Owner**: Senior backend engineer

---

## Bad Example: Proceeding Without Feasibility

❌ **BAD** — Story assigned to sprint without assessment:
```
"As a user, I want to use AI to automatically categorize my transactions."
Estimate: "Probably 3 points? Maybe 8? I dunno, we'll see."
Timeline: "2 weeks, hard deadline for customer demo"
Risk: "Should be fine, we can figure it out as we go"
```

**Problems:**
- No feasibility assessment (all three dimensions unknown)
- No identification of High risk (ML integration, new domain)
- No spike planned despite unknown tech
- Estimate variance is huge (3-8 points)
- Definition of Ready is not complete

✅ **GOOD** — Same story with proper assessment:
```
"As a user, I want to categorize my transactions using a classifier (rule: tag 80%+ of transactions correctly)."

Feasibility Assessment:
- Technical: RED (ML expertise missing, no existing infrastructure, unknown API)
- Resource: RED (no data scientist on team, current capacity 20hrs available)
- Timeline: RED (hard deadline 2 weeks, ML training/validation takes 1+ week minimum)
Tier: CRITICAL

Spike Required:
- Goal: Evaluate feasibility of rule-based vs. ML approach within timeline/budget
- Duration: 3 days
- Deliverable: Prototype + Go/No-Go recommendation

Risk Register:
| RISK-001 | ML training data availability | Technical | H | H | 9 | Lead | Spike task: assess data volume |
| RISK-002 | Team has zero ML experience | Resource | H | H | 9 | PM | Spike task: evaluate contractor cost/timeline |
| RISK-003 | Model accuracy SLA (80%+) | Technical | M | H | 6 | Lead | Spike task: baseline with rule engine |

Next Step: Spike execution before sprint assignment
```

---

## Summary Checklist

Before hand-off to development:

- [ ] Feasibility assessed across all three dimensions (Technical/Resource/Timeline)
- [ ] Risk tier assigned (Low/Medium/High/Critical)
- [ ] If High/Critical: spike is complete with findings documented
- [ ] Definition of Ready: all 13 items verified
- [ ] Story follows INVEST principles
- [ ] Acceptance criteria are in Given/When/Then format with test cases
- [ ] Estimate converges (range ≤ 2×, ≤ 8 story points)
- [ ] Technical approach is agreed (no unknowns about HOW)
- [ ] External dependencies are resolved or explicitly managed
- [ ] Risk register (if High/Critical) shows all mitigations assigned
- [ ] Team consensus: all stakeholders agree this is ready to build
- [ ] Go/No-Go decision: explicitly signed off by tech lead and product manager

---

**Last Updated**: 2026-04-09 | **SDLC Phase**: 1 of 6 (Requirements)
