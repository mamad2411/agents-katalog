---
name: learning-path
description: "Maps learning paths with prerequisite skills, milestone assessments, and recommended resource sequences."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Learning Path

## When to Use This Skill

Use this skill when you need to:
- Map a structured learning path for a skill or knowledge domain
- Sequence prerequisite topics so learners build knowledge in the right order
- Design milestone assessments that confirm readiness before advancing
- Curate resource recommendations for each stage of the path

**DO NOT** use this skill for individual lesson plans (use lesson-plan), course sales pages, or academic degree planning. This is for mapping the full journey from beginner to competent in a specific skill area.

---

## Core Principle

A LEARNING PATH IS A MAP, NOT A MANDATE — IT SHOWS THE MOST EFFICIENT ROUTE FROM "I KNOW NOTHING" TO "I CAN DO THIS CONFIDENTLY" WHILE ALLOWING LEARNERS TO MOVE AT THEIR OWN PACE.

---

## Phase 1: Path Definition

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Skill or domain** | "What skill or topic does this learning path cover?" | No default — must be provided |
| **Target learner** | "Who is this for — complete beginners, career changers, upskilling professionals?" | Complete beginners |
| **End goal** | "What should the learner be able to do at the end of this path?" | No default — must be provided |
| **Estimated duration** | "How long should the full path take?" | 3-6 months at 5-10 hours/week |
| **Resource format** | "Are resources free, paid, your own content, or curated from external sources?" | Mix of free and recommended paid |

**GATE: Confirm the skill, target learner, and end goal before mapping the path.**

---

## Phase 2: Path Architecture

### Stage Design

Organize the path into 3-5 stages:

```
## [Learning Path Title]

### Stage 1: Foundation (Weeks 1-4)
**Goal:** [What the learner can do after completing this stage]
**Prerequisites:** None
**Milestone:** [How they prove they're ready to move on]

### Stage 2: Core Skills (Weeks 5-10)
**Goal:** [What the learner can do after completing this stage]
**Prerequisites:** Stage 1 milestone passed
**Milestone:** [Assessment or project]

### Stage 3: Application (Weeks 11-16)
**Goal:** [What the learner can do after completing this stage]
**Prerequisites:** Stage 2 milestone passed
**Milestone:** [Real-world project or portfolio piece]

### Stage 4: Mastery (Weeks 17-24)
**Goal:** [What the learner can do after completing this stage]
**Prerequisites:** Stage 3 milestone passed
**Milestone:** [Capstone project, certification, or demonstration]
```

### Stage Detail Template

For each stage, provide:

```
## Stage [X]: [Stage Name]

### Learning Objectives
By the end of this stage, you will be able to:
1. [Objective 1 — specific and measurable]
2. [Objective 2]
3. [Objective 3]

### Topics Covered
| Topic | Description | Estimated Hours |
|-------|-------------|----------------|
| [Topic 1] | [Brief description] | [X] hours |
| [Topic 2] | [Brief description] | [X] hours |
| [Topic 3] | [Brief description] | [X] hours |

### Recommended Resources
| Resource | Type | Cost | Notes |
|----------|------|------|-------|
| [Resource 1] | [Book / Course / Video / Article] | [Free / $X] | [Why this resource] |
| [Resource 2] | [Type] | [Cost] | [Notes] |
| [Resource 3] | [Type] | [Cost] | [Notes] |

### Practice Activities
- [Activity 1 — hands-on practice applying the topic]
- [Activity 2]
- [Activity 3]

### Milestone Assessment
**Format:** [Quiz / Project / Skill demonstration]
**Passing criteria:** [What qualifies as "ready to move on"]
**If not passed:** [What to review before retaking]
```

---

## Phase 3: Prerequisite Mapping

### Dependency Chart

Map which topics depend on which:

```
## Prerequisite Map

[Topic A] → No prerequisites (start here)
[Topic B] → Requires Topic A
[Topic C] → Requires Topic A
[Topic D] → Requires Topics B + C
[Topic E] → Requires Topic D
[Capstone] → Requires all topics
```

### Skill Level Indicators

Help learners self-assess where to start:

```
## Where Should You Start?

**Start at Stage 1 if:**
- You have never [done this skill] before
- You cannot define [key term 1] or [key term 2]
- You have no practical experience in this area

**Start at Stage 2 if:**
- You understand the basics but have not applied them
- You can [basic skill] but struggle with [intermediate skill]
- You have completed a beginner course or tutorial

**Start at Stage 3 if:**
- You have been practicing for [X] months
- You can [intermediate skill] independently
- You want to refine your approach and build a portfolio

**Start at Stage 4 if:**
- You have [X] months/years of experience
- You want to master advanced techniques or specialize
- You are preparing for [certification / career transition]
```

---

## Phase 4: Path Delivery

### Progress Tracking

```
## Learning Path Progress Tracker

| Stage | Topic | Status | Milestone | Date Completed |
|-------|-------|--------|-----------|---------------|
| 1 | [Topic 1] | ☐ Not started / ◐ In progress / ☑ Complete | | |
| 1 | [Topic 2] | ☐ / ◐ / ☑ | | |
| 1 | Milestone 1 | ☐ / ◐ / ☑ | [Pass/Fail] | |
| 2 | [Topic 3] | ☐ / ◐ / ☑ | | |
```

### Estimated Time Investment

```
## Time Commitment

| Stage | Duration | Hours/Week | Total Hours |
|-------|----------|-----------|-------------|
| Foundation | 4 weeks | 5-8 hours | 20-32 hours |
| Core Skills | 6 weeks | 8-10 hours | 48-60 hours |
| Application | 6 weeks | 10-12 hours | 60-72 hours |
| Mastery | 8 weeks | 8-10 hours | 64-80 hours |
| **Total** | **24 weeks** | | **192-244 hours** |
```

### Learning Path Checklist

- [ ] Clear end goal defined — what the learner can DO, not just know
- [ ] 3-5 stages with progressive difficulty
- [ ] Every stage has measurable learning objectives
- [ ] Prerequisites and dependencies are mapped
- [ ] Resources recommended for each topic (mix of free and paid)
- [ ] Practice activities included at every stage
- [ ] Milestone assessments gate advancement between stages
- [ ] Self-assessment guide helps learners find their starting point
- [ ] Time estimates are realistic for the target learner

---

## Anti-Patterns

- **No clear end state** — "learn marketing" is not a learning path. "Be able to plan and execute a paid ad campaign that generates leads" is.
- **All theory, no practice** — if every stage is reading and watching, the learner never builds real skill.
- **No milestones** — without checkpoints, learners either stall or skip ahead unprepared.
- **Resource overload** — recommending 20 books and 10 courses per stage paralyzes the learner. Curate ruthlessly.
- **Linear-only structure** — some topics can be learned in parallel. Show which are sequential and which are flexible.
- **No "start here" guidance** — experienced learners should not have to sit through basics they already know.

---

## Recovery

- **Learner stuck at a stage:** Break the milestone into smaller sub-goals. Identify the specific concept causing difficulty and provide targeted resources.
- **Resources become outdated:** Review and update recommended resources quarterly. Replace deprecated or discontinued content.
- **Path is too long:** Offer a "fast track" version that covers only the essentials for learners who need to be productive quickly.
- **Learner skips stages and struggles:** Redirect them to the self-assessment guide. Recommend completing the prerequisite stage before continuing.
- **Multiple valid learning sequences:** Offer a "recommended path" and an "alternative path" for learners with different starting points or priorities.
