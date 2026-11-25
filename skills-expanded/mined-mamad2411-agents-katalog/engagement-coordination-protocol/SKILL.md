---
name: engagement-coordination-protocol
description: >-
  Standardized protocol for multi-agent engagements. Defines engagement folder
  structure, file formats, handoff templates, and how agents coordinate with
  fresh context to prevent information bloat.
when-to-use: >-
  Use when: orchestrating multi-agent engagements, setting up engagement folders,
  calling other agents from an orchestrator role, responding to org/lead agent
  calls, structuring handoffs for fresh context, maintaining audit trails of
  decisions, setting up retrospective analysis.
categories:
  - coordination
  - multi-agent
  - engagement-management
---

# Engagement Coordination Protocol

Standard protocol for multi-agent engagements. Ensures all agents follow the same folder structure, file formats, and handoff expectations—even across different organizations.

---

## Quick Reference

**Use this skill when**:
- You're orchestrating multiple agents (org/lead role)
- You're being called by an orchestrator agent
- You're setting up an engagement
- You're responding to a coordinated work request
- You need to structure handoffs with fresh context

---

## Engagement Folder Structure

Create this folder structure at engagement start. All agents reference these paths. **Engagement is organized by phases**, with retrospectives at each phase boundary and a final retrospective-of-retrospectives at close.

```
engagement-[name]/
│
├── SCOPE.md
│   What: User request, constraints, success criteria, budget, timeline
│   Owner: Orchestrator agent (initially)
│   Access: All agents read this for context
│
├── ARCHITECTURE-PLAN.md
│   What: Final specification (what we're building, why, constraints met)
│   Owner: Orchestrator agent (synthesized from all division assessments)
│   Created: After all initial assessments complete (Phase 1)
│   Purpose: This is the contract with the user. Everything measured against this.
│
├── AGENT-CALLS.json
│   What: Audit log of every agent call (includes phase field)
│   Format: [See AGENT-CALLS.json Format section below]
│   Owner: Orchestrator agent (maintains throughout engagement)
│   Purpose: Decision trail for retrospective analysis; validation that all calls are to repo agents
│
├── phase-0-discovery/                  ← PHASE 0: DISCOVERY
│   ├── outputs/
│   │   ├── infrastructure-discovery.md (current-state baseline)
│   │   └── [other discovery outputs]
│   └── RETROSPECTIVE-phase-0.md        (phase retrospective)
│
├── phase-1-assessment/                 ← PHASE 1: ASSESSMENT
│   ├── outputs/
│   │   ├── platform-outputs.md
│   │   ├── devops-outputs.md
│   │   ├── azure-specialty-outputs.md
│   │   ├── identity-productivity-outputs.md
│   │   ├── security-review.md
│   │   └── cost-review.md
│   └── RETROSPECTIVE-phase-1.md
│
├── phase-2-planning/                   ← PHASE 2: PLANNING
│   ├── outputs/
│   │   └── [planning outputs, architecture refinements]
│   └── RETROSPECTIVE-phase-2.md
│
├── phase-3-implementation/             ← PHASE 3: IMPLEMENTATION
│   ├── code/
│   │   ├── infrastructure/
│   │   ├── pipelines/
│   │   └── automation/
│   ├── outputs/
│   │   └── [implementation progress notes]
│   └── RETROSPECTIVE-phase-3.md
│
├── phase-4-review-validation/          ← PHASE 4: REVIEW & VALIDATION
│   ├── outputs/
│   │   ├── security-final-review.md
│   │   ├── cost-final-review.md
│   │   └── testing-validation-report.md
│   └── RETROSPECTIVE-phase-4.md
│
├── final-delivery/                     ← DELIVERY: User-provided implementation
│   ├── code/
│   ├── infrastructure/
│   ├── documentation/
│   └── FINAL-DELIVERY-MANIFEST.md
│
└── RETROSPECTIVE-OF-RETROSPECTIVES.md  ← ENGAGEMENT LEVEL: Synthesizes all phase retros
    Contents:
    ├── Phase 0-4 summary findings
    ├── Planned vs Actual across all phases
    ├── Systemic patterns (cross-phase)
    ├── Agent call audit (all calls to repo agents?)
    ├── Missed agents (gaps flagged during phases)
    ├── Action items for next engagement
    └── Organizational learning
```

**Phases:**
- **Phase 0: Discovery** — Current state assessment, baselines
- **Phase 1: Assessment** — Division leads assess from their perspectives
- **Phase 2: Planning** — Synthesize into ARCHITECTURE-PLAN
- **Phase 3: Implementation** — Code authors and specialists build
- **Phase 4: Review & Validation** — Security, cost, testing sign-off
- **Delivery & Retrospective** — User delivers, engage retrospective agent

---

## AGENT-CALLS.json Format

Orchestrator maintains this log throughout engagement. Every agent call is recorded.

```json
{
  "engagement": "enterprise-migration",
  "calls": [
    {
      "sequence": 1,
      "timestamp": "2024-03-15T10:30:00Z",
      "agent": "Platform Engineering Lead",
      "phase": "assessment",
      "prompt_summary": "Assess landing zone readiness, governance gaps",
      "input_files": ["SCOPE.md"],
      "output_path": "outputs/platform-outputs.md",
      "agent_response_summary": "ALZ pattern, 3-tier mgmt groups, RBAC strategy",
      "what_made_into_plan": [
        "3-tier management group hierarchy",
        "service principal RBAC model"
      ],
      "what_was_rejected": [
        "Multi-subscription vending (deferred to Phase 2)"
      ],
      "blockers": [],
      "status": "incorporated"
    },
    {
      "sequence": 2,
      "timestamp": "2024-03-15T11:00:00Z",
      "agent": "Security & Compliance Analyst",
      "phase": "assessment",
      "prompt_summary": "Identify compliance requirements, security controls",
      "input_files": ["SCOPE.md"],
      "output_path": "outputs/security-review.md",
      "agent_response_summary": "HIPAA required. Encryption, audit, CA baseline.",
      "what_made_into_plan": [
        "HIPAA compliance requirements",
        "encryption at rest/transit",
        "Conditional Access baseline"
      ],
      "what_was_rejected": [],
      "blockers": [],
      "status": "incorporated"
    }
  ]
}
```

**Log fields**:
- `sequence` — Call number (1, 2, 3, etc.)
- `timestamp` — When call was made
- `agent` — Which agent was called (MUST be a repo agent; see Agent Validation below)
- `phase` — discovery | assessment | planning | implementation | review | retrospective
- `prompt_summary` — What was asked (1 line)
- `input_files` — What files agent read
- `output_path` — Where agent wrote output
- `agent_response_summary` — What agent returned (2-3 lines)
- `what_made_into_plan` — Which parts were incorporated into ARCHITECTURE-PLAN.md
- `what_was_rejected` — Which parts were not used and why
- `blockers` — Any blockers agent reported
- `status` — incorporated | rejected | pending | blocked
- `agent_validated` — true (agent exists in repo) or false with miss explanation

---

## Agent Validation

**CRITICAL**: All agent calls must be to agents defined in the repository (`agents/*.agent.md`).

**During the engagement:**
1. **Before calling** — Verify agent exists: check `agents/` folder or valid agent name
2. **If agent doesn't exist** — This is an agent gap. Options:
   - **Non-critical gap** — Note in AGENT-CALLS.json with `agent_validated: false`. Proceed with workaround or delay. Document in phase retrospective.
   - **Showstopping gap** — Agent must exist to proceed. Log the miss with `blocker: "SHOWSTOP: Missing agent [name]"`. HALT work. Escalate to human for new agent creation.

**Examples of gaps:**
- Need a "Database Migration Specialist" but don't have one → note as miss, flag for new agent creation
- Need "Infrastructure Cost Auditor" but can delegate to Cost Optimization Specialist → proceed with note
- Need "Kubernetes Security Hardening" but don't have it → assess if showstopper or deferrable

**In phase retrospectives:**
- Tally all `agent_validated: false` entries
- List each missing agent with: name, why it was needed, impact (deferred work? workaround?)
- Mark as showstop if it blocked delivery

**In engagement retrospective:**
- "Missed agents" section — all gaps from all phases
- Priority for next engagement: Create missing agents in priority order
- Trigger for new agent creation if gap appears in multiple engagements

---

## Handoff Template: Division/Lead Assessment

**Use this when**: Orchestrator calls a division lead for initial assessment

```markdown
# ENGAGEMENT ASSESSMENT REQUEST

**Engagement**: [name]
**Phase**: Assessment
**Requested from**: @[Lead-Name]
**Due**: [Date]

---

## Your Task

Assess this engagement from your division's perspective.

**Read**: `engagement-[name]/SCOPE.md`

**Write to**: `engagement-[name]/outputs/[division]-outputs.md`

---

## What We Need

1. **Readiness assessment** — What's in place, what's missing, what's risky
2. **Recommended approach** — Your solution to this problem
3. **Constraints & assumptions** — What you're assuming, what could break
4. **Dependencies** — What needs to happen first for your division
5. **Blockers** — Anything preventing your division from moving forward

---

## Expected Output Format

Write to: `engagement-[name]/outputs/[division]-outputs.md`

Include sections:
- Executive summary (2 lines max)
- Assessment findings (specific, not generic)
- Recommended approach and rationale
- Known constraints
- Dependencies on other divisions (if any)
- Next recommended step

---

## Return to Orchestrator

Path: `engagement-[name]/outputs/[division]-outputs.md`  
Summary: 2-3 bullets of key findings  
Blockers: Any blockers identified  

---

## Context

[User request, success criteria, why this matters]
```

---

## Handoff Template: Specialist Implementation Task

**Use this when**: Orchestrator calls a specialist to build/implement something

```markdown
# IMPLEMENTATION TASK

**Engagement**: [name]
**Phase**: Implementation - [Component]
**Requested from**: @[Specialist-Name]
**Task**: [Specific deliverable]
**Due**: [Date]

---

## Your Task

Implement [specific component] according to ARCHITECTURE-PLAN.md.

---

## What We Need

**Deliverable**: [Specific code/config/script]
- Location: `engagement-[name]/code/[path]/`
- Format: [Terraform / Bicep / PowerShell / Workflow YAML / etc]
- Includes: [tests / validation / documentation]

---

## Read These Files

1. `engagement-[name]/ARCHITECTURE-PLAN.md` — overall spec (skim for your section)
2. `engagement-[name]/outputs/[relevant-output].md` — your specific requirements
3. `engagement-[name]/AGENT-CALLS.json` — decisions made, why they were made

---

## Implementation Constraints

- Security requirements: [from security-review.md]
- Cost constraints: [from cost-review.md]
- Compliance: [from SCOPE.md]
- Dependencies: [what must exist first]

---

## Definition of Done

Your work is done when:
- [ ] All required resources/code defined
- [ ] Tests or validation included
- [ ] Documentation explains setup and operations
- [ ] Naming conventions follow [style-guide skill]
- [ ] No hardcoded secrets or credentials
- [ ] All requirements from ARCHITECTURE-PLAN met

---

## Return to Orchestrator

Path: `engagement-[name]/code/[path]/`  
Summary: What was built, any assumptions made  
Blockers: Anything requiring different approach  
```

---

## Handoff Template: Review & Approval

**Use this when**: Orchestrator calls reviewer (security, cost, etc.)

```markdown
# REVIEW & APPROVAL REQUEST

**Engagement**: [name]
**Phase**: Review - [Component]
**Requested from**: @[Reviewer-Name]
**Scope**: [What to evaluate]
**Due**: [Date]

---

## Your Task

Review deliverables against the specification. Provide findings and approval decision.

---

## What We're Reviewing

[Code / Architecture / Compliance posture / Cost estimate]

---

## Read These Files

1. `engagement-[name]/ARCHITECTURE-PLAN.md` — the specification
2. `engagement-[name]/outputs/[component].md` — what was implemented
3. `engagement-[name]/code/[path]/` or equivalent — actual deliverable
4. `engagement-[name]/AGENT-CALLS.json` — context on decisions

---

## Review Criteria

1. **Does it match specification?** If not, what's different and why?
2. **Requirements met?** Are SCOPE.md requirements satisfied?
3. **Gaps or risks?** Any missing pieces or concerning patterns?
4. **Approval?** Yes / Conditional / No

---

## Return to Orchestrator

Path: `engagement-[name]/outputs/[review-type]-review.md`

Include sections:
- Compliance with specification (yes/no/partial + details)
- Findings (what works, what doesn't, what's risky)
- Recommendation (approve / conditional / reject)
- Conditions/blockers (if applicable)

Return: [path] + summary (approve/conditional/reject + reason)
```

---

## How Agents Respond to Handoffs

When you receive a handoff from an orchestrator:

1. **Read the input files specified in the prompt** (usually SCOPE.md and prior outputs)
2. **Write your output to the exact path specified** (e.g., `engagement-name/outputs/platform-outputs.md`)
3. **Use the section format specified** in the handoff
4. **Return the path + summary** (2-3 bullets)
5. **Report any blockers** that prevent your division from proceeding
6. **Don't ask for clarification on other divisions' work** — that's the orchestrator's job

---

## For Orchestrators: Key Practices

### Before Calling an Agent

- ✅ Create engagement folder and SCOPE.md
- ✅ Have the output path ready
- ✅ Know what files the agent should read
- ✅ Be specific about expected sections/format

### When Agent Responds

- ✅ Log the call to AGENT-CALLS.json
- ✅ Parse the response and note what made it into the plan
- ✅ Note what was rejected and why
- ✅ Store the output file path
- ✅ Call the next agent with fresh context (not prior agent's output)

### At Engagement End

- ✅ Finalize ARCHITECTURE-PLAN.md (this is the spec/contract)
- ✅ Complete AGENT-CALLS.json (full decision trail)
- ✅ When user delivers implementation, call Retrospective Agent with:
  - SCOPE.md (what was requested)
  - ARCHITECTURE-PLAN.md (what was promised)
  - AGENT-CALLS.json (why decisions were made)
  - final-delivery/ (what was actually built)

---

## Key Principles

1. **Fresh context per call** — Each agent gets a focused prompt, not history
2. **Files are the handoff medium** — Not conversation history
3. **One response per agent** — They respond once, move to next
4. **Specification is the contract** — ARCHITECTURE-PLAN.md is measured against
5. **Audit trail for learning** — AGENT-CALLS.json enables retrospective analysis
6. **Engagement structure is consistent** — Same across all engagements
