---
name: class-schedule-planner
description: "Plans class/session schedules with instructor assignments, room allocation, and enrollment capacity management."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Class Schedule Planner

## When to Use This Skill

Use this skill when you need to:
- Plan a weekly class or session schedule for a studio, gym, or learning center
- Assign instructors to time slots while managing availability and specialties
- Allocate rooms or spaces based on class size and equipment needs
- Manage enrollment capacity and waitlists

**DO NOT** use this skill for individual appointment scheduling, event planning, or school academic scheduling. This is for recurring group class schedules at fitness studios, yoga studios, learning centers, or similar facilities.

---

## Core Principle

A WELL-DESIGNED SCHEDULE MAXIMIZES SPACE UTILIZATION AND INSTRUCTOR TALENT WHILE MATCHING THE TIMES AND CLASSES YOUR CLIENTS ACTUALLY WANT — BUILD AROUND DEMAND, NOT CONVENIENCE.

---

## Phase 1: Schedule Parameters

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Facility type** | "What type of facility — fitness studio, yoga studio, learning center, other?" | Fitness studio |
| **Rooms/spaces** | "How many rooms or spaces are available, and what capacity?" | 1 main studio, capacity 20 |
| **Operating hours** | "What are your hours of operation?" | 6 AM - 9 PM weekdays, 8 AM - 2 PM weekends |
| **Class types offered** | "What classes do you offer?" | No default — must be provided |
| **Instructors** | "How many instructors, their availability, and specialties?" | No default — must be provided |
| **Peak demand times** | "When do most clients want to attend?" | Early morning (6-8 AM) and evening (5-7 PM) weekdays |

**GATE: Confirm spaces, instructors, and class types before building the schedule.**

---

## Phase 2: Schedule Design

### Schedule Grid Template

```
## Weekly Class Schedule — [Facility Name]

### Studio A (Capacity: 20)

| Time | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
|------|--------|---------|-----------|----------|--------|----------|--------|
| 6:00 AM | [Class] | — | [Class] | — | [Class] | — | — |
| 7:00 AM | [Class] | [Class] | [Class] | [Class] | [Class] | [Class] | — |
| 9:00 AM | [Class] | [Class] | [Class] | [Class] | [Class] | [Class] | [Class] |
| 12:00 PM | [Class] | — | [Class] | — | [Class] | — | — |
| 5:30 PM | [Class] | [Class] | [Class] | [Class] | [Class] | — | — |
| 6:30 PM | [Class] | [Class] | [Class] | [Class] | — | — | — |
```

### Scheduling Rules

1. **Peak times get your most popular classes** — do not schedule niche classes at 5:30 PM
2. **Buffer time between classes** — 15-30 minutes for cleanup, setup, and late arrivals
3. **Instructor limits** — no instructor teaches more than 3 back-to-back classes
4. **Class variety across the day** — avoid scheduling similar classes in adjacent time slots
5. **Weekend schedules reflect demand** — fewer classes, mid-morning focus

### Class Mix Strategy

| Time Slot | Best Class Types | Audience |
|-----------|-----------------|----------|
| Early morning (6-7 AM) | High energy — HIIT, cycling, boot camp | Before-work crowd |
| Mid-morning (9-10 AM) | Moderate — yoga, pilates, barre | Stay-at-home parents, retirees, remote workers |
| Lunchtime (12-1 PM) | Quick — 45-min express classes | Office workers |
| After work (5-7 PM) | Popular variety — strength, cardio, yoga | Post-work crowd |
| Evening (7-8 PM) | Recovery — yoga, stretch, meditation | Wind-down seekers |
| Weekend morning | Community — longer classes, workshops | Flexible schedules |

---

## Phase 3: Instructor & Room Management

### Instructor Assignment Matrix

```
## Instructor Assignments

| Instructor | Specialties | Availability | Weekly Classes | Max Classes |
|-----------|-------------|-------------|----------------|-------------|
| [Name 1] | Yoga, Pilates | M/W/F mornings, T/Th evenings | 6 | 8 |
| [Name 2] | HIIT, Strength | M-F mornings and evenings | 8 | 10 |
| [Name 3] | Cycling, Cardio | T/Th/Sat | 4 | 6 |
```

### Sub/Cover Policy

```
## Instructor Substitution Policy

1. Instructor notifies management [48] hours in advance of absence
2. Instructor is responsible for finding a qualified sub from the approved list
3. If no sub is found, management will attempt to cover or cancel with notice
4. Cancellation notice sent to enrolled clients at least [4] hours before class
5. Sub instructors are paid [same rate / flat sub rate of $X]
```

### Room Allocation (Multi-Space Facilities)

| Room | Capacity | Equipment | Best For |
|------|----------|-----------|----------|
| Studio A | 25 | Mirrors, sound system, mats | Group fitness, dance, yoga |
| Studio B | 12 | Spin bikes, screens | Cycling, small group training |
| Outdoor space | 15 | None (portable) | Boot camp, seasonal classes |

---

## Phase 4: Enrollment & Capacity

### Capacity Management

```
## Enrollment Settings

| Class | Capacity | Min to Run | Waitlist Limit |
|-------|----------|-----------|---------------|
| Yoga Flow | 20 | 3 | 5 |
| HIIT | 15 | 4 | 5 |
| Cycling | 12 | 3 | 3 |
| Boot Camp | 20 | 5 | 5 |
```

### Waitlist Rules

- Waitlisted clients are notified automatically when a spot opens
- Clients have [2] hours to confirm or lose their spot
- No-shows are tracked — 3 no-shows in 30 days result in booking restrictions

### Schedule Review Cadence

| Frequency | Review |
|-----------|--------|
| Weekly | Check attendance per class, address low-enrollment classes |
| Monthly | Review overall schedule performance, instructor feedback |
| Quarterly | Adjust class times, add/remove classes based on demand trends |
| Seasonally | Account for seasonal shifts (summer drop-off, January surge) |

### Key Metrics

| Metric | Target |
|--------|--------|
| Average class fill rate | 70%+ of capacity |
| Classes cancelled (low enrollment) | Under 5% |
| Waitlist conversion rate | 60%+ |
| No-show rate | Under 15% |
| Instructor utilization | 70-85% of available hours |

---

## Anti-Patterns

- **Scheduling based on instructor preference, not demand** — the schedule should serve clients first.
- **No buffer between classes** — back-to-back classes without transition time create chaos.
- **Too many class types** — spreading thin across 15 class types dilutes quality. Focus on 5-8 core offerings.
- **Ignoring attendance data** — a class that averages 2 attendees should be moved, changed, or cut.
- **Static schedule year-round** — demand shifts seasonally. Adjust accordingly.

---

## Recovery

- **Consistently low attendance for a class:** Move it to a different time slot, try a different instructor, or replace it with a more popular format.
- **Instructor burnout:** Reduce their weekly class count, ensure rest days, and cross-train other instructors in their specialties.
- **Scheduling conflicts between instructors:** Use a shared calendar and confirm availability before publishing the schedule.
- **Seasonal enrollment drop:** Offer limited-time promotions, add seasonal class themes, and reduce the schedule temporarily rather than running empty classes.
- **New class type not gaining traction:** Give it 6-8 weeks with active promotion before cutting. Offer introductory pricing to build a base.
