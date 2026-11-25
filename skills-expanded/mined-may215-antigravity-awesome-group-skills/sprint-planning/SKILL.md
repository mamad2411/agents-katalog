---
name: sprint-planning
description: "Group skill: Sprint planning and architecture review — requirements, architecture, API design, database design, estimation, task breakdown, security, TDD, and documentation."
risk: medium
source: self
---

# 📊 Sprint Planning / Architecture Review

> **Group Skill** — Orchestrates sub-skills for sprint kickoff and architecture decisions.
> Activate by saying: "Plan the sprint" or "architecture review"

## When to Use

- Kicking off a new sprint or iteration
- Reviewing architecture decisions
- Breaking down features into tasks

## Step-by-Step Workflow

### Step 1: Requirements
**Skill**: `writing-plans`
- Break down into implementation steps
- Define acceptance criteria
- Identify dependencies

### Step 2: Quick Plan
**Skill**: `concise-planning`
- Atomic checklist from spec
- Order by dependency
- Identify parallelizable work

### Step 3: Architecture
**Skill**: `senior-architect`
- Review system design
- Check scalability concerns
- Document ADRs

### Step 4: API Design
**Skill**: `api-patterns` + `api-design-principles`
- Choose REST vs GraphQL vs tRPC
- Define contracts and schemas
- Plan versioning strategy

### Step 5: Database Design
**Skill**: `database-design` + `domain-driven-design`
- Design schema and relationships
- Plan migrations
- Model domain boundaries

### Step 6: Task Breakdown
**Skill**: `executing-plans`
- Create plan with checkpoints
- Assign effort estimates
- Set review gates

### Step 7: Security Review
**Skill**: `threat-modeling-expert`
- Run STRIDE threat model
- Identify attack surfaces
- Plan security controls

### Step 8: TDD Setup
**Skill**: `tdd-workflow`
- Establish RED-GREEN-REFACTOR
- Define test strategy
- Set coverage goals

### Step 9: Documentation
**Skill**: `wiki-architect`
- Create ADRs
- Document API contracts
- Update project docs

## Completion

Sprint plan complete with architecture vetted and tasks broken down. 📊

## Sub-Skills Referenced

1. `writing-plans`
2. `concise-planning`
3. `senior-architect`
4. `api-patterns`
5. `database-design`
6. `executing-plans`
7. `threat-modeling-expert`
8. `tdd-workflow`
9. `wiki-architect`
