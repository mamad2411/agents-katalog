---
name: roadmap-doc
description: |
  Generate a complete ROADMAP.md (or PHASES.md) file for any project. Use whenever the user asks to create, write, generate, or draft a ROADMAP.md or PHASES.md — a timeline document that shows what gets built when, in what order, with what milestones and dependencies.

  This skill triggers when users need to document: project timeline, phased delivery plan, release schedule, milestone planning, sprint roadmap, feature prioritization over time, or "what are we building and when".

  Do NOT trigger for single-feature implementation plans (use Design.md skill), or high-level strategy without dates (that's more business planning).

---

# ROADMAP.md Author Skill

You are a project planner documenting the timeline and phased delivery of a software project.

## Philosophy

A ROADMAP.md answers the question: **"What are we building, in what order, and when?"**

It shows:
- **Phases/releases** and what goes in each
- **Timeline** (dates or quarters)
- **Milestones** (key deliverables and checkpoints)
- **Dependencies** (what must happen before what)
- **Prioritization rationale** (why this order)

The audience is **everyone on the team** — engineers need to know what's next, stakeholders need to track progress, and product managers need to communicate externally. This document changes over time as reality meets plan.

## Structure

A ROADMAP.md has **8 core sections**:

1. **Overview** - Vision and timeline summary
2. **Current Status** - Where we are right now
3. **Phased Delivery Plan** - What's in each phase/release
4. **Timeline & Milestones** - Key dates and checkpoints
5. **Dependencies & Blockers** - What depends on what
6. **Success Criteria** - How we measure completion
7. **Risks & Contingencies** - What could go wrong
8. **Future Vision** - Beyond current roadmap

---

## Best Practices

### 1. **Be Realistic, Not Optimistic**
   - Add 20-30% buffer for unknowns
   - Account for holidays, sick days, context switching
   - Past velocity is the best predictor

### 2. **Make Dependencies Explicit**
   - Show what blocks what
   - Identify critical path
   - Track external dependencies closely

### 3. **Define "Done" Clearly**
   - Each phase has concrete completion criteria
   - Not just "code complete" but "tested, documented, deployed"
   - Get stakeholder sign-off

### 4. **Track Risks Proactively**
   - Identify risks early
   - Assign owners
   - Check risk indicators weekly

### 5. **Update Regularly**
   - Reality diverges from plan
   - Update every 2 weeks minimum
   - Track version history

---

## Output Instructions

When generating a ROADMAP.md:

1. **Interview for timeline** (duration, deadlines, constraints)
2. **Understand scope** (what needs to be built)
3. **Start with overview** (vision, timeline summary)
4. **Show current status** (where we are now)
5. **Break into phases** (logical chunks of value)
6. **Add milestones** (key checkpoints and dates)
7. **Document dependencies** (what blocks what)
8. **Define success** (completion criteria)
9. **Address risks** (what could go wrong + contingencies)
10. **Save as `ROADMAP.md`** in working directory
