---
name: quality-assurance-checklist
description: "Creates QA checklists for products, services, or content with pass/fail criteria, review workflows, and quality standards documentation."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Quality Assurance Checklist

## When to Use This Skill

Use this skill when you need to:
- Create a QA checklist for products, services, or content before delivery
- Define pass/fail criteria and quality standards for repeatable processes
- Build review workflows with approval gates and sign-off procedures
- Standardize quality checks across team members or contractors

**DO NOT** use this skill for software testing frameworks, manufacturing inspection protocols, or regulatory compliance audits. This is for solopreneur and small business quality control.

---

## Core Principle

QUALITY IS NOT INSPECTED IN AT THE END — IT IS BUILT IN AT EVERY STAGE. A QA CHECKLIST IS THE LAST SAFETY NET, NOT THE FIRST LINE OF DEFENSE.

---

## Phase 1: Scope

Define what is being quality-checked and the standards it must meet.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Deliverable type** | "What are you QA-checking? (product, service delivery, content, digital product, client work)" | Content |
| **Quality standards** | "What does 'good enough to ship' look like? Any specific standards?" | Professional quality, error-free |
| **Common defects** | "What goes wrong most often? What complaints have you received?" | No default — critical input |
| **Who reviews** | "Who performs the QA check? (you, team member, contractor)" | Self-review |
| **Frequency** | "How often do you ship this deliverable?" | Weekly |

**GATE: Confirm scope and standards before building the checklist.**

---

## Phase 2: Build Checklist

Create a comprehensive QA checklist with pass/fail criteria.

### Checklist Structure

Every QA checklist has three layers:

```
## QA Checklist: [Deliverable Name]

**Version:** 1.0
**Last updated:** [Date]
**Reviewer:** [Name/Role]

### Critical Items (Must pass — blocks delivery)
- [ ] [Check item] — **Pass criteria:** [Specific, measurable standard]
- [ ] [Check item] — **Pass criteria:** [Specific, measurable standard]

### Important Items (Should pass — flag if failed)
- [ ] [Check item] — **Pass criteria:** [Standard]
- [ ] [Check item] — **Pass criteria:** [Standard]

### Nice-to-Have Items (Improve if time permits)
- [ ] [Check item] — **Pass criteria:** [Standard]

### Sign-Off
- [ ] All critical items pass
- [ ] Important items reviewed (failures documented)
- **Approved by:** _______________
- **Date:** _______________
```

### Category-Specific Checklists

**Content QA:**
- Spelling and grammar (zero errors)
- Brand voice consistency
- All links functional
- Images properly sized and alt-tagged
- CTA present and working
- Mobile formatting checked

**Service Delivery QA:**
- Deliverable matches scope/SOW
- All promised components included
- Client-specific customizations applied
- Delivery format matches client preference
- Follow-up communication drafted

**Product QA:**
- Product matches listing description
- Packaging intact and branded
- All components included
- Functionality tested
- Shipping label accurate

**GATE: Present the checklist for approval before adding workflow elements.**

---

## Phase 3: Workflow

Design the review process around the checklist.

### Review Workflow

```
## QA Review Workflow

**Step 1: Self-Review**
Creator runs the full checklist before submitting for review.
Time allocation: [X minutes]

**Step 2: Peer/Second-Eye Review** (if applicable)
Second reviewer checks critical items only.
Time allocation: [X minutes]

**Step 3: Fix Cycle**
Any failed items are corrected and re-checked.
Maximum fix cycles: 2 (if still failing after 2 rounds, escalate)

**Step 4: Final Approval**
Sign-off by [role] before delivery/publishing.

**Step 5: Post-Delivery Spot Check**
Random 10% of deliverables get a post-delivery audit monthly.
```

### Defect Tracking

```
## Defect Log

| Date | Deliverable | Defect Found | Severity | Root Cause | Fix Applied | Preventive Action |
|------|------------|-------------|----------|-----------|-------------|------------------|
| | | | Critical/Important/Minor | | | |
```

---

## Phase 4: Improve

Build continuous improvement into the QA process.

### Monthly QA Review

- Review the defect log for patterns (same defect appearing 3+ times means the process is broken, not the person)
- Update the checklist to add checks for new defect types
- Remove checks that have not caught a defect in 3+ months (reduce checklist bloat)
- Recalibrate pass criteria if standards have shifted

### Checklist Versioning

Track changes to the checklist with version notes:
```
**v1.0** — Initial checklist
**v1.1** — Added mobile formatting check after 3 client complaints
**v1.2** — Removed [item] — redundant with new tool auto-check
```

---

## Anti-Patterns

- **Checklist too long** — more than 20 items and reviewers start rubber-stamping. Keep it under 15, prioritize critical items.
- **Vague pass criteria** — "Looks good" is not a criterion. "Zero spelling errors" is a criterion.
- **Skipping the checklist when rushed** — the checklist exists BECAUSE you are rushed. That is when mistakes happen.
- **Same person creates and reviews** — self-review catches 60% of issues. A second set of eyes catches 90%.
- **Never updating the checklist** — a static checklist becomes irrelevant. Update quarterly at minimum.

---

## Recovery

- **User ships something with a defect:** Add the defect type to the checklist immediately. Conduct a brief root cause analysis — was it a missed check or a missing check?
- **QA is taking too long:** Split into "ship-blocking" and "nice-to-have" tiers. Only the ship-blocking tier is mandatory.
- **Team members skip the checklist:** Make the signed checklist a required attachment before delivery. No checklist, no ship.
- **Checklist does not catch real issues:** The checklist is testing the wrong things. Review actual customer complaints and reverse-engineer checks from those.
- **User works alone and cannot do peer review:** Use a time-delay approach — complete the QA check, wait 30 minutes, then review with fresh eyes.
