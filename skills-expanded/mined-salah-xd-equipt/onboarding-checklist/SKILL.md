---
name: onboarding-checklist
description: "Creates employee or contractor onboarding checklists with day-by-day tasks, tool access setup, and training schedules for smooth starts."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Onboarding Checklist

## When to Use This Skill

Use this skill when you need to:
- Create a structured onboarding plan for a new employee or contractor
- Build day-by-day task lists for the first 30 days
- Set up tool access, training schedules, and introduction sequences
- Standardize onboarding so every new hire gets the same experience

**DO NOT** use this skill for customer onboarding, vendor onboarding, or offboarding. This is specifically for bringing new team members into the business.

---

## Core Principle

THE FIRST 30 DAYS DETERMINE WHETHER A NEW HIRE BECOMES PRODUCTIVE OR STARTS LOOKING FOR THE EXIT — A STRUCTURED ONBOARDING ELIMINATES CONFUSION AND ACCELERATES CONTRIBUTION.

---

## Phase 1: Role Context

Gather information about the role and business before building the checklist.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Role title** | "What role is this person filling?" | No default |
| **Employment type** | "Employee or contractor?" | Contractor |
| **Work arrangement** | "Remote, hybrid, or in-person?" | Remote |
| **Start date** | "When do they start?" | Next Monday |
| **Key tools** | "What tools/platforms will they need access to?" | No default |
| **Manager/point of contact** | "Who will be their primary contact?" | Business owner |
| **First project** | "What will their first assignment or project be?" | No default |

**GATE: Confirm role context before building the checklist.**

---

## Phase 2: Build Checklist

Create a phased onboarding plan.

### Pre-Start Checklist (Before Day 1)

```
## Pre-Start Setup

### Administrative
- [ ] Send welcome email with start date, time, and first-day instructions
- [ ] Prepare and send contract/offer letter for signature
- [ ] Collect tax forms (W-9 for contractors, W-4 for employees)
- [ ] Set up payroll / payment method
- [ ] Add to team directory

### Tool Access
- [ ] Create email account / add to workspace
- [ ] Add to project management tool ([tool name])
- [ ] Add to communication channel ([tool name])
- [ ] Share relevant document folders
- [ ] Send login credentials securely (password manager invite)

### Preparation
- [ ] Assign onboarding buddy or point of contact
- [ ] Schedule Day 1 welcome call
- [ ] Prepare first-week task list
- [ ] Notify existing team about new hire
```

### Week 1: Orientation

```
## Week 1: Getting Started

### Day 1
- [ ] Welcome call with manager (30 min)
- [ ] Tour of tools and platforms (walkthrough)
- [ ] Review company overview and mission
- [ ] Review role expectations and success metrics
- [ ] Complete tool setup and verify all access works
- [ ] Introduce to team members

### Day 2-3
- [ ] Review key processes and SOPs
- [ ] Shadow or review examples of completed work
- [ ] Begin first small task or assignment
- [ ] Daily check-in with manager (15 min)

### Day 4-5
- [ ] Complete first deliverable (low-stakes)
- [ ] Receive feedback on first deliverable
- [ ] Ask and document any questions about processes
- [ ] End-of-week check-in with manager (30 min)
```

### Week 2-4: Ramp-Up

```
## Week 2-4: Building Competence

### Week 2
- [ ] Take on regular workload at 50% capacity
- [ ] Learn remaining tools and processes
- [ ] Weekly check-in with manager
- [ ] Document any process gaps or confusion

### Week 3
- [ ] Operate at 75% capacity
- [ ] Handle tasks independently with spot-check review
- [ ] Mid-onboarding feedback session (what is working, what is not)

### Week 4
- [ ] Full workload capacity expected
- [ ] 30-day review meeting with manager
- [ ] Evaluate: Is the role a good fit? Any adjustments needed?
- [ ] Complete onboarding feedback survey
```

**GATE: Present the complete checklist for review.**

---

## Phase 3: Supporting Materials

Create the documents that support the onboarding process.

### Welcome Email Template

```
Subject: Welcome to [Business Name] — Your First Day Details

Hi [Name],

Welcome to the team! Here is everything you need for your first day on [date]:

**Start time:** [Time and timezone]
**First meeting:** [Video link or location]
**Your manager:** [Name and contact]

**Before Day 1, please:**
1. Sign your [contract/offer letter] — [link]
2. Complete your [tax form] — [link]
3. Set up your [tool] account — [invite link]

**What to expect on Day 1:**
- [Agenda item 1]
- [Agenda item 2]
- [Agenda item 3]

If you have any questions before then, reply to this email.

Looking forward to working with you!
[Name]
```

### 30-Day Review Template

```
## 30-Day Review: [Name]

**Date:** [Date]
**Role:** [Title]
**Reviewer:** [Manager name]

### Performance
- Quality of work: [Exceeds / Meets / Below expectations]
- Speed of learning: [Fast / On track / Needs support]
- Communication: [Proactive / Adequate / Needs improvement]

### Feedback
- What is going well:
- What needs improvement:
- Support or resources needed:

### Next 30-Day Goals
1. [Goal]
2. [Goal]
3. [Goal]
```

---

## Phase 4: Optimize

Refine the onboarding process over time.

### Onboarding Feedback Survey

5 questions to send after the first 30 days:
1. Did you feel prepared on Day 1? What was missing?
2. Which tools or processes were hardest to learn?
3. Was the pace too fast, too slow, or about right?
4. What would have made your first week better?
5. On a scale of 1-10, how confident do you feel in your role?

### Continuous Improvement

- Track time-to-productivity for each new hire
- Review feedback surveys quarterly and update the checklist
- Maintain a "lessons learned" log for onboarding issues

---

## Anti-Patterns

- **No checklist at all** — "Just figure it out" is not onboarding. New hires waste days finding basic information.
- **Information overload on Day 1** — spreading orientation across a week prevents the new hire from drowning.
- **No check-ins for the first month** — daily check-ins in Week 1, weekly after that. Do not go silent.
- **Giving the hardest project first** — start with a small win to build confidence before ramping up complexity.
- **No tool access on Day 1** — there is no faster way to make someone feel unwelcome than having them sit idle while IT gets set up.

---

## Recovery

- **New hire is struggling after 2 weeks:** Increase check-in frequency. Identify if the issue is skills, tools, or unclear expectations.
- **User has never onboarded anyone:** Start with the pre-start and Week 1 checklists only. Add Weeks 2-4 after the first hire.
- **Contractor onboarding needs to be faster:** Compress to a 3-day onboarding. Cut orientation, focus on tools, deliverable standards, and first assignment.
- **Previous hires left quickly:** Review exit feedback. Common causes: unclear expectations, no feedback, feeling isolated. Fix the root cause in the checklist.
- **User onboards infrequently:** Keep the checklist as a template. Review and update it before each new hire, not after.
