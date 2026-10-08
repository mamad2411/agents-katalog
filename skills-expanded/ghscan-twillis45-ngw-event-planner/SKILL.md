# 00_NGW_EVENT_PLANNER_MASTER_SKILL.md

You are working on NGW Event Planner, a premium planning and execution app for event professionals.

The product is not a generic task manager, CRM, or calendar app.

It is an event operations command system designed to help planners, coordinators, studios, and event professionals understand what needs attention, what is risky, what is missing, and what must happen next.

## Product Architecture

Preserve the 4-layer product architecture:

L1 Studio → L2 Portfolio → L3 Event Command → L4 Specialist Tabs

### L1 · Studio

Answers:

"What needs attention across my business?"

Surfaces:
- Home
- Events
- Clients
- Schedule
- Studio Setup

### L2 · Portfolio

Answers:

"Which event or client do I work on next?"

Surfaces:
- Events index
- Clients list
- Client detail

### L3 · Event Command

Answers:

"What needs attention inside this event?"

Command Center is the event-level operational triage surface.

It routes to specialist tabs. It does not do deep specialist work.

### L4 · Specialist Tabs

Answers:

"Now I am fixing the thing."

Specialist tabs include:
- Vendors
- Decisions
- Timeline
- Checklist
- Communication
- Calendar
- Run of Show
- Budget
- Guests
- Seating
- Manage Event

## Core Product Rule

Each layer hands off to the next layer.

Do not make one layer redo the work of another layer.

Do not create duplicate workspaces.

Do not add another dashboard unless there is a strong reason.

Do not bury deep work inside overlays.

## Product Standard

This app must feel like:

- premium event command system,
- luxury planner operations desk,
- production readiness board,
- serious studio workflow tool.

It must not feel like:

- generic SaaS dashboard,
- Trello clone,
- spreadsheet skin,
- dull admin system,
- CRM template,
- fake AI app.

## Runtime Rule

All meaningful product work must reach runtime UI.

No test-only improvements. No documentation-only changes unless explicitly requested. No types-only changes unless explicitly requested.

## Truthfulness Rule

Do not invent data.

Do not invent:
- fake AI insights,
- fake readiness scores,
- fake vendor risks,
- fake payment amounts,
- fake document contents,
- fake client approvals,
- fake timeline conflicts,
- fake business metrics.

Unknown means unknown.

Use:
- Missing
- Not tracked yet
- No document attached
- No linked timeline items
- No communication history

## User Experience Rule

The app must clearly answer:

- What matters?
- Why does it matter?
- What should I do first?
- Where do I go next?
- What is blocking event readiness?

The user should not have to hunt for the starting point.

## Claude Behavior

When modifying the app:

1. Inspect before editing.
2. Preserve architecture.
3. Make targeted changes.
4. Keep runtime behavior working.
5. Avoid fake data.
6. Preserve responsive quality.
7. Report what changed.
8. Report risks.
9. Provide manual QA steps.
10. Do not freestyle.
