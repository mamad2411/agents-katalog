---
name: continuing-education
description: "Plans continuing education offerings with credit requirements, course catalogs, and completion tracking systems."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Continuing Education

## When to Use This Skill

Use this skill when you need to:
- Plan a continuing education program with structured credit requirements
- Build a course catalog with categories, prerequisites, and credit values
- Design completion tracking systems for professional development
- Create a CE offering to sell to professionals who need ongoing credentials

**DO NOT** use this skill for one-off courses, degree programs, or informal learning. This is for structured continuing education with credit tracking and compliance elements.

---

## Core Principle

CONTINUING EDUCATION MUST BALANCE COMPLIANCE REQUIREMENTS WITH GENUINE SKILL DEVELOPMENT — THE BEST CE PROGRAMS MAKE PROFESSIONALS BETTER AT THEIR JOBS, NOT JUST CHECK A BOX.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Industry or profession** | "What profession or industry needs these CE credits?" | No default — must be provided |
| **Credit requirements** | "How many credits are required per cycle, and what is the cycle length?" | 20 credits per year |
| **Accreditation body** | "Is there a governing body that must approve the courses?" | Self-certified (no external body) |
| **Delivery format** | "Online, in-person, or hybrid?" | Online self-paced |
| **Revenue model** | "Subscription, per-course, or included in membership?" | Per-course purchase |

**GATE: Confirm the brief before proceeding.**

---

## Phase 2: Program Architecture

### Credit Structure

```
## Credit System
**Total required:** [X] credits per [cycle length]
**Credit categories:**
- Core/mandatory: [X credits minimum]
- Elective: [X credits]
- Ethics/compliance: [X credits if applicable]

**Credit calculation:**
- 1 credit = 1 hour of instructional content
- Live events: [multiplier if applicable]
- Self-paced: [completion requirements]
```

### Course Catalog Structure

```
## Catalog Categories
1. [Category 1] — [X courses, Y total credits]
2. [Category 2] — [X courses, Y total credits]
3. [Category 3] — [X courses, Y total credits]

## Course Listing Format
| Course Title | Category | Credits | Format | Prerequisites | Price |
|-------------|----------|---------|--------|--------------|-------|
```

### Completion Requirements

Define what "completing" a course means:
- Assessment pass rate (e.g., 80% on post-test)
- Minimum time spent (no fast-forwarding through video)
- Attendance requirements for live sessions
- Certificate generation upon completion

**GATE: Present the program architecture for approval.**

---

## Phase 3: Build

### Course Catalog

Create 15-25 course listings across all categories:

```
## [Course Title]
**Category:** [Category name]
**Credits:** [Number]
**Duration:** [Time]
**Format:** [Self-paced / Live / Hybrid]
**Description:** [2-3 sentences]
**Learning objectives:** [3-5 bullet points]
**Prerequisites:** [None or specific courses]
**Assessment:** [Quiz, project, or attendance-based]
```

### Tracking System

```
## Learner Dashboard Requirements
- Credit balance (earned vs. required)
- Completion history with dates and certificates
- Upcoming deadlines (cycle expiration)
- Course recommendations based on remaining requirements
- Transcript export (PDF)
```

### Compliance Documentation

- Certificate of completion template (include name, course, credits, date, ID number)
- Transcript format for reporting to accreditation bodies
- Record retention policy (how long records are kept)
- Audit trail for credit verification

---

## Phase 4: Polish

### 1. Launch Plan

```
## CE Program Launch Checklist
- [ ] Course catalog finalized with at least 1.5x the required credits available
- [ ] Tracking system configured and tested
- [ ] Certificate template created
- [ ] Pricing and payment system ready
- [ ] Marketing materials for target professionals
- [ ] FAQ document addressing common compliance questions
- [ ] Support process for credit disputes or technical issues
```

### 2. Growth Plan

- Add 5-10 new courses per quarter
- Retire outdated courses annually
- Survey completers for topic requests
- Track most-popular and least-popular courses to guide creation

### 3. Quality Metrics

```
## Track Quarterly
- Course completion rates (target: 80%+)
- Assessment pass rates (target: 85%+)
- Learner satisfaction scores (target: 4.2+/5)
- Credit compliance rate (% of learners meeting requirements on time)
- Revenue per learner
```

---

## Example 1: Marketing Professional CE Program

```
Categories: Digital Marketing (8 credits), Analytics (4 credits), Strategy (4 credits), Ethics (4 credits)
Sample courses: "AI in Marketing Ethics" (2 credits), "Advanced Google Analytics" (3 credits)
Cycle: 20 credits per calendar year
```

## Example 2: Financial Advisor CE Program

```
Categories: Regulatory (10 credits), Product Knowledge (5 credits), Ethics (5 credits), Elective (10 credits)
Cycle: 30 credits per 2-year period
Requirement: At least 5 credits from live instruction
```

---

## Anti-Patterns

- **Box-checking culture** — designing courses that are easy to pass but teach nothing destroys the program's reputation.
- **Not enough course variety** — if learners must take the same courses every cycle, they disengage. Offer 2x the required credits in options.
- **No deadline reminders** — professionals procrastinate. Send reminders at 75%, 50%, and 25% of the cycle remaining.
- **Manual tracking** — spreadsheet-based tracking breaks at scale. Build or use a proper LMS with credit tracking.
- **Ignoring mobile** — many professionals complete CE on their phone during downtime. Ensure mobile compatibility.

---

## Recovery

- **No accreditation body exists:** Create an internal certification with clear standards. Market the credential's value based on course quality and industry recognition.
- **User unsure how many credits to require:** Research comparable programs in the industry. Default to 20 credits per year as a reasonable starting point.
- **Not enough content for a full catalog:** Launch with 10 courses covering mandatory categories. Add electives quarterly.
- **Learners not completing on time:** Implement a grace period with late completion options. Add automated reminders starting 90 days before deadline.
