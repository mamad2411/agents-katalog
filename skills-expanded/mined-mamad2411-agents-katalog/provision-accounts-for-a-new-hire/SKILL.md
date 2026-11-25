---
name: provision-accounts-for-a-new-hire
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Request and confirm the correct system accounts for a new hire before their start date.

## Preconditions

- The new hire has an approved start date and role.
- Manager, department, location, and access template are known.
- You have access to the identity, ticketing, or HR onboarding system.

## Steps

1. **Confirm access template.** Match the new hire's role, department, location, and worker type to the approved access profile. → *Expect:* required systems and permission levels are identified.
2. **Create the provisioning request.** Enter employee name, start date, manager, title, email format, and access template in the ticket or IAM system. → *Expect:* the request has a ticket or workflow ID.
3. **Add special access needs.** Include approved exceptions such as admin tools, finance systems, or regulated data access. → *Expect:* exceptions are documented with approver names.
4. **Set activation timing.** Schedule accounts to activate on or just before the start date according to policy. → *Expect:* activation timing is visible in the request.
5. **Notify approvers.** Route manager, system owner, security, or data owner approvals as required. → *Expect:* approval tasks are assigned.
6. **Confirm completion.** Check that email, SSO, core apps, groups, and device enrollment are provisioned. → *Expect:* account status shows active or scheduled.
7. **Share access instructions.** Send first-login guidance through the approved channel. → *Expect:* the new hire or manager has secure onboarding instructions.

## Decision points

- If the role needs privileged access → require explicit owner approval and least-privilege justification.
- If start date changes → update activation timing before accounts go live.
- If the new hire is a contractor → use contractor-specific access duration and review rules.

## Failure modes & recovery

- **F1 Overprovisioning:** detect access beyond the role template → remove or deny excess permissions and document the correction.
- **F2 Delayed approval:** detect pending access close to start date → escalate to manager and system owner.
- **F3 Wrong identity:** detect name, email, or employee ID mismatch → pause provisioning and correct the source HR record.

## Verification

The provisioning ticket lists approved systems, account activation timing, required approvals, and completed or scheduled account status for the correct new hire.

## Variations

- US: protect SSN, tax, and demographic data from IT tickets unless explicitly required.
- Other countries: follow local employee monitoring, identity, and data transfer rules.
- Regulated systems: add security training, data owner approval, and audit trail requirements.

## Safety & privacy

Medium risk because account access can expose company, employee, or customer data. Apply least privilege, verify identity, avoid putting sensitive PII in tickets, and keep privileged access time-bound and auditable.
