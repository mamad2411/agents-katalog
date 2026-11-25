---
name: offboarding-checklist
description: "Creates offboarding procedures with access revocation, knowledge transfer, equipment return, and exit interview templates for clean transitions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Offboarding Checklist

## When to Use This Skill

Use this skill when you need to:
- Create a structured offboarding process for departing employees or contractors
- Ensure all system access is revoked and knowledge is transferred
- Build exit interview templates to capture feedback
- Standardize the transition process to protect the business

**DO NOT** use this skill for customer churn processes, vendor contract termination, or legal termination procedures. This is for the operational offboarding workflow.

---

## Core Principle

OFFBOARDING PROTECTS YOUR BUSINESS AND PRESERVES RELATIONSHIPS — A SLOPPY EXIT CREATES SECURITY RISKS AND BURNS BRIDGES WITH PEOPLE WHO COULD BE FUTURE ADVOCATES OR REHIRES.

---

## Phase 1: Departure Context

Gather the details of the departure before building the plan.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Role** | "What role is this person leaving?" | No default |
| **Employment type** | "Employee or contractor?" | Contractor |
| **Departure type** | "Voluntary resignation, contract end, or termination?" | Voluntary |
| **Last day** | "What is their last working day?" | 2 weeks from now |
| **Systems with access** | "What tools, accounts, and systems do they have access to?" | No default |
| **Transition plan** | "Is someone taking over their responsibilities? Who?" | Business owner absorbs |
| **Sensitive data access** | "Do they have access to financial data, customer data, or passwords?" | Yes |

**GATE: Confirm departure details before building the checklist.**

---

## Phase 2: Build Checklist

Create the complete offboarding checklist organized by timeline.

### Immediate (Day of Notice)

```
## Immediate Actions

- [ ] Acknowledge departure and confirm last day in writing
- [ ] Determine transition timeline and priorities
- [ ] Identify all systems and tools the person has access to
- [ ] Begin knowledge transfer planning
- [ ] Notify relevant team members (if appropriate)
```

### Transition Period (Before Last Day)

```
## Knowledge Transfer

- [ ] Document all ongoing projects and their status
- [ ] List all recurring tasks and their deadlines
- [ ] Transfer ownership of files, folders, and documents
- [ ] Record any undocumented processes or tribal knowledge
- [ ] Introduce replacement or backup person to key contacts
- [ ] Complete handoff meetings for each major responsibility

## Project Handoff Template

| Project | Status | Next Steps | New Owner | Key Contacts | Files Location |
|---------|--------|-----------|-----------|-------------|---------------|
| [Name] | [Status] | [Actions] | [Person] | [Names] | [Link] |
```

### Last Day

```
## Access Revocation (Complete on Last Day)

- [ ] Remove from email / Google Workspace / Microsoft 365
- [ ] Remove from Slack / Teams / communication tools
- [ ] Remove from project management tools
- [ ] Remove from CRM and customer-facing systems
- [ ] Remove from financial tools (banking, accounting, payment)
- [ ] Change any shared passwords they knew
- [ ] Remove from code repositories (if applicable)
- [ ] Remove from social media account access
- [ ] Deactivate VPN / remote access
- [ ] Remove from company credit cards or expense accounts

## Administrative

- [ ] Process final payment / invoice
- [ ] Send final pay stub or contractor payment confirmation
- [ ] Collect any company equipment (laptop, phone, keys)
- [ ] Revoke building access / security badges
- [ ] Update team directory and org chart
- [ ] Forward their email to appropriate person (if needed)
- [ ] Conduct exit interview
```

**GATE: Present checklist for review and customization.**

---

## Phase 3: Exit Interview

Design the exit interview process to capture feedback.

### Exit Interview Template

```
## Exit Interview: [Name]

**Date:** [Date]
**Interviewer:** [Name]
**Role:** [Title]
**Tenure:** [Duration]
**Departure reason:** [Voluntary / End of contract / Termination]

### Questions

1. What prompted your decision to leave? (voluntary only)
2. What did you enjoy most about working here?
3. What would you change about the role or the business?
4. Did you have the tools and resources you needed to do your job?
5. How would you describe the communication and feedback you received?
6. Would you recommend this company to a friend? Why or why not?
7. Is there anything we could have done to retain you? (voluntary only)
8. Any final feedback or suggestions?

### Key Themes
- [Summary of main feedback points]

### Action Items
- [Changes to consider based on feedback]
```

### Exit Interview Guidelines

- Conduct the interview in the final week, not the last hour
- Keep it conversational, not confrontational
- For terminations, keep the interview brief and focused on logistics
- Document feedback patterns across multiple exits to identify systemic issues

---

## Phase 4: Post-Departure

Complete follow-up tasks after the person has left.

### Post-Departure Checklist

```
## Post-Departure (Within 1 Week)

- [ ] Verify all access has been successfully revoked
- [ ] Test that shared passwords have been changed
- [ ] Confirm knowledge transfer documents are complete and accessible
- [ ] Send farewell message to team (if appropriate)
- [ ] Archive their files and communications per retention policy
- [ ] Update any client-facing materials that referenced the person
- [ ] Schedule 30-day check to ensure no access gaps were missed
```

### Alumni Relationship (Voluntary Departures)

- Connect on LinkedIn
- Add to alumni network if one exists
- Leave the door open for future collaboration or referrals

---

## Anti-Patterns

- **Delaying access revocation** — revoke access on the last day, not "when we get around to it." Every day of delay is a security risk.
- **No knowledge transfer** — letting someone leave without documenting their work means losing weeks of productivity.
- **Skipping the exit interview** — the person leaving is the most honest source of feedback you will ever get.
- **Burning the bridge** — even in terminations, professionalism matters. Today's departing contractor may be tomorrow's referral source.
- **Forgetting shared credentials** — if the departing person knew any shared passwords, change them immediately.

---

## Recovery

- **Person already left without offboarding:** Do an emergency access audit now. Revoke everything, change shared passwords, and document what knowledge may have been lost.
- **Departing person is uncooperative:** Focus on access revocation and documentation you can build without their help. Pull from email, project tools, and files.
- **No replacement hired yet:** Prioritize documenting processes over transferring to a specific person. The documentation serves whoever comes next.
- **User has never offboarded anyone:** Start with the access revocation checklist — that is the non-negotiable security piece. Add knowledge transfer and exit interviews for future departures.
- **Sensitive termination:** Revoke access before or during the termination conversation, not after. Consult legal counsel if there are concerns about data or IP.
