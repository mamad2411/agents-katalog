---
name: onboard-a-new-hire
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 1h
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Prepare a new hire for day one by completing HR setup, logistics, and manager handoffs.

## Preconditions

- The candidate has accepted the offer and start date is confirmed.
- Required contingencies are complete or cleared to proceed.
- HR, manager, IT, payroll, and facilities owners are known.

## Steps

1. **Create the employee profile.** Enter legal name, preferred name, role, manager, department, location, start date, and employment type in HRIS. → *Expect:* the new hire has an HR record.
2. **Launch onboarding tasks.** Assign tax, direct deposit, handbook, policy, benefits, and emergency contact tasks as applicable. → *Expect:* the new hire sees required tasks in the onboarding portal.
3. **Coordinate equipment.** Request laptop, badge, workspace, shipping, and required tools. → *Expect:* each logistics task has an owner and due date.
4. **Notify stakeholders.** Send start details to manager, IT, payroll, facilities, and recruiting. → *Expect:* each team knows the start date and dependencies.
5. **Prepare day-one schedule.** Add orientation, manager check-in, team introduction, and required training. → *Expect:* the new hire has a first-day agenda.
6. **Confirm documentation status.** Check completion of identity, tax, work authorization, and payroll forms according to local rules. → *Expect:* missing items are visible before start.
7. **Send welcome information.** Share start time, location or login details, contact person, agenda, and what to bring. → *Expect:* the new hire knows how to start.

## Decision points

- If work authorization or required checks are incomplete → ask HR or legal whether the start date must move.
- If equipment will be late → arrange temporary access or adjust the first-day plan.
- If the new hire needs accommodation → route details through the confidential accommodation process.

## Failure modes & recovery

- **F1 HRIS data mismatch:** detect different start dates or managers across systems → correct the source record and notify downstream teams.
- **F2 Missing payroll forms:** detect incomplete tax or bank details before cutoff → remind the new hire and payroll owner.
- **F3 No day-one access:** detect pending account or equipment tasks → escalate to IT and prepare manual onboarding materials.

## Verification

The new hire profile exists, onboarding tasks are assigned, first-day logistics are scheduled, and all owners can see their required actions.

## Variations

- US: include I-9, tax withholding, state forms, benefits eligibility, and EEO data handling where applicable.
- Other countries: local contracts, right-to-work checks, statutory benefits, and works council steps may differ.
- Remote hire: add shipping, remote identity verification, time zone, and home office setup steps.

## Safety & privacy

Medium risk because onboarding uses legal identity, payroll, health benefits, and work authorization data. Limit access to need-to-know teams and keep accommodation, medical, and demographic information separate from general onboarding notes.
