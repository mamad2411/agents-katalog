---
name: cloud-access-request-and-iam-lifecycle-management
description: >
  Handles the everyday operational request to grant, time-box, and later
  revoke a scoped IAM permission for a contractor, new hire, or a
  temporary need (e.g. "give the new contractor read-only S3 access for
  30 days," "grant break-fix access to prod for this incident," "revoke
  Priya's access, she left the team," "why does this access request keep
  getting rejected") — including expiry enforcement and the audit trail
  a security review will ask for. Use for a single access grant/revoke
  transaction, not for designing the underlying IAM policy/role structure
  (see cloud-iam-hardening for that).
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Cloud Access Request and IAM Lifecycle Management

## Purpose

Most IAM risk doesn't come from a badly designed policy — it comes from
the hundreds of small, one-off access grants made under time pressure
that never get revoked: a contractor's temporary S3 access still active a
year after the contract ended, a new hire given broad access "just to get
them started" while the ticket to scope it down never gets filed, an
on-call engineer's incident break-fix grant that quietly becomes
permanent. This skill covers that everyday operational transaction —
receiving a request, granting the narrowest permission that satisfies it,
attaching a hard expiry, and leaving an audit trail that a review can
reconstruct without asking "who approved this and why" — as a repeatable
process, not a design exercise. It assumes the underlying policy/role
structure already exists (or is designed per
[cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)); this skill is
about the individual grant/revoke lifecycle transaction on top of that
structure.

## When to use

- A contractor, new hire, vendor, or auditor needs a specific, scoped
  permission for a defined period (e.g. "read-only access to the
  `analytics` S3 bucket for 30 days").
- An incident responder needs temporary elevated (break-fix) access to a
  production resource beyond their standing role, for the duration of the
  incident only.
- Someone changed teams, finished a contract, or left the company, and
  their previously granted access needs to be revoked.
- A recurring or one-off access request needs to be logged with who
  requested it, who approved it, what was granted, and when it expires —
  because a security review or auditor will ask for exactly that trail.
- An access grant that was supposed to be temporary is still active past
  its intended expiry and needs to be found and cleaned up.
- Someone asks "why do I still have access to X" or "why was my access
  request denied/delayed."

## Prerequisites & environment

- An existing IAM structure to grant *into* — predefined least-privilege
  roles/policies/groups per
  [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md), not
  freehand `AdministratorAccess`/`Owner`/`roles/editor` grants improvised
  per request.
- A ticketing system (Jira, ServiceNow, or equivalent) or a version-
  controlled access-request record as the system of truth for the
  request — an access grant made only via console click-ops with no
  linked ticket has no audit trail.
- Time-bound access mechanics available on the platform: AWS IAM
  Identity Center permission set assignments or IAM Conditions with a
  `aws:CurrentTime`/`aws:TokenIssueTime` expiry, Azure AD **Privileged
  Identity Management (PIM)** eligible/time-bound role assignments, GCP
  IAM Conditions with a `request.time` expression, or Okta/Entra
  access-package expiration policies if access is federated through an
  IdP rather than granted natively per cloud.
- An approver identified and reachable *before* the grant — someone other
  than the requester, per separation-of-duties; for production/sensitive
  scopes this should not be the same person doing the granting.
- A scheduled or automated sweep capability (a cron job, a scheduled
  Lambda/Function, or a recurring script run) to catch expired-but-not-
  yet-removed grants — manual memory is not a control.

## Step-by-step guidance

1. **Capture the request before touching any IAM console/CLI.** Minimum
   fields, logged in the ticket/record: requester, resource/scope needed,
   business justification, requested duration, and approver. Reject or
   bounce back any request missing a concrete scope ("prod access") or a
   duration ("indefinitely," "just in case") — both are the seeds of a
   permanent, over-broad grant.

2. **Map the request to the narrowest existing role/policy, or a new
   narrowly scoped one — never a broad standing role "to save time."**
   AWS example — granting a contractor scoped, time-boxed read access to
   one S3 prefix via a permission set assigned only to their user, with
   an inline session-duration limit and an IAM Condition belt-and-braces
   expiry:
   ```bash
   # 1. Attach a narrowly scoped inline policy (not an existing broad managed policy)
   aws iam put-user-policy \
     --user-name contractor-jsmith \
     --policy-name analytics-readonly-temp \
     --policy-document '{
       "Version": "2012-10-17",
       "Statement": [{
         "Effect": "Allow",
         "Action": ["s3:GetObject", "s3:ListBucket"],
         "Resource": [
           "arn:aws:s3:::analytics-reports-<AWS_ACCOUNT_ID>",
           "arn:aws:s3:::analytics-reports-<AWS_ACCOUNT_ID>/*"
         ],
         "Condition": {
           "DateLessThan": { "aws:CurrentTime": "2026-08-27T00:00:00Z" }
         }
       }]
     }'
   ```
   Azure example — a **PIM eligible** (not standing) role assignment
   scoped to a resource group, time-boxed at activation:
   ```bash
   az role assignment create \
     --assignee "jsmith@example.com" \
     --role "Storage Blob Data Reader" \
     --scope "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/analytics-rg"
   # then configure as a PIM-eligible (not permanent) assignment in Entra ID PIM,
   # with a maximum activation duration (e.g. 8 hours) and required justification
   ```
   GCP equivalent — an IAM Condition-bound binding on the specific
   bucket, not a project-level role:
   ```bash
   gcloud storage buckets add-iam-policy-binding gs://analytics-reports-<PROJECT_ID> \
     --member="user:jsmith@example.com" \
     --role="roles/storage.objectViewer" \
     --condition='expression=request.time < timestamp("2026-08-27T00:00:00Z"),title=contractor-temp-access,description=Expires 2026-08-27'
   ```

3. **Record the grant in the audit trail immediately**, linking: the
   ticket ID, the exact policy/role/condition applied, the expiry
   timestamp, and the approver — in the ticket itself and, ideally, as a
   tag/label on the IAM resource (`access-ticket=JIRA-1234`,
   `expires=2026-08-27`) so the grant is traceable from the cloud console
   alone, not only from the ticketing system.

4. **For incident break-fix access, grant via the platform's
   time-bound elevation mechanism, not a manually attached policy someone
   has to remember to remove.** AWS IAM Identity Center or Azure PIM
   "activate" flows both auto-expire the session; if neither is available,
   attach the same `DateLessThan`/`request.time` condition pattern from
   step 2 to any manually created break-fix policy, and open a follow-up
   ticket to remove it even though it will also stop working once expired
   — a policy that silently no-ops past its expiry is still a stale
   artifact.

5. **Revoke deliberately, not by deleting broadly.** When revoking:
   remove only the specific policy/binding/role assignment tied to the
   ticket, not the user's other unrelated access. Confirm scope before
   removing:
   ```bash
   # Verify exactly what's attached before removing anything
   aws iam list-user-policies --user-name contractor-jsmith
   aws iam get-user-policy --user-name contractor-jsmith --policy-name analytics-readonly-temp
   # Only then remove the specific policy
   aws iam delete-user-policy --user-name contractor-jsmith --policy-name analytics-readonly-temp
   ```
   > **Warning:** Revoking access for someone changing teams or roles is
   > not the same as offboarding them entirely. Confirm with the
   > requester/manager exactly which grants are being revoked before
   > running a broad `detach-user-policy`/`role assignment delete
   > --all`/`remove-iam-policy-binding` sweep — removing more than the
   > ticket asked for can break access the person still legitimately
   > needs, and removing less leaves a stale grant behind. When in doubt,
   > scope the revoke to exactly what was granted (matched by the ticket
   > ID tag from step 3).

6. **Run a scheduled sweep for expired-but-still-present grants** as a
   backstop to time-bound conditions (which stop working, but often
   don't self-delete the IAM object): a weekly script/scheduled function
   that lists policies/bindings with an `expires=` tag/condition in the
   past and either auto-removes them or opens a ticket for a human to
   confirm removal — never silently auto-delete a *standing* (non-
   time-boxed) grant this way, only ones explicitly tagged as temporary.

7. **Review pending and denied requests for pattern, not just
   throughput.** If the same kind of request is repeatedly needed (e.g.
   every new hire on a team needs the same three permissions), that's a
   signal to fold it into the team's standing least-privilege role design
   — escalate to [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)
   rather than repeating the same one-off grant indefinitely.

## Best practices

- **Every grant needs a ticket, an expiry, and an approver who isn't the
  requester** — treat any of the three missing as a reason to pause the
  grant, not a formality to backfill later.
- **Default duration should be the shortest that satisfies the stated
  need** (days, not months) — extending a grant on request is cheap;
  walking back an over-long standing grant nobody remembers approving is
  not.
- **Prefer the platform's native time-bound mechanism** (IAM Identity
  Center session duration, Azure PIM activation window, GCP IAM
  Conditions) over a calendar reminder to "remember to revoke this" —
  humans forget, expiring conditions don't.
- **Tag every temporary grant with its ticket ID and expiry** on the IAM
  object itself, not only in the ticketing system, so an access review
  or `cloud-iam-hardening` audit can reconcile cloud-side reality against
  the ticket trail without cross-referencing two systems by hand.
- **Revoke access the same day someone's role or employment changes** —
  a scoped one-off grant left dangling after an offboarding is exactly
  the kind of stale, unowned access that
  [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)'s quarterly
  review exists to catch, but catching it quarterly is a backstop, not
  the primary control.
- **Log break-glass/incident access grants with an automatic
  notification on use**, mirroring the break-glass guidance in
  [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md), so an
  emergency grant always gets a post-incident review even under time
  pressure.
- **Fold recurring identical requests into a standing role**, don't keep
  re-granting the same permission set one ticket at a time — repeated
  one-off requests for the same access are a signal, not a workflow.

## Common pitfalls

- **Symptom:** A contractor's access review, months after their contract
  ended, finds their S3/Blob/GCS read access is still active.
  **Fix:** The original grant had no enforced expiry — only a note in the
  ticket to "remove after 30 days" that nobody actioned. Re-grant using a
  platform-native time-bound condition (IAM Condition `DateLessThan`,
  PIM eligible assignment, GCP IAM Condition `request.time`) so expiry is
  enforced by the platform, and add the scheduled sweep from step 6 as a
  backstop for any grant that predates this practice.

- **Symptom:** An access request for "read-only access to the reports
  bucket" gets fulfilled by attaching `AmazonS3ReadOnlyAccess` (every
  bucket in the account), not scoped to the one bucket requested.
  **Fix:** The path of least resistance during a busy on-call/help-desk
  shift was to use an existing broad managed policy instead of writing a
  three-line scoped inline policy. Always scope the `Resource` (or
  Azure `scope`/GCP `condition`) to exactly the resource named in the
  ticket — a scoped policy costs one extra minute to write and prevents
  an unrelated data-exposure finding later.

- **Symptom:** Revoking access for someone who changed teams
  accidentally removes their access to a *different* system they still
  legitimately need, breaking their work.
  **Fix:** The revoke was done as a broad "remove all of this user's
  non-default policies" cleanup instead of removing only the specific
  grant tied to the original ticket. Match revocations to the ticket-ID
  tag applied at grant time (step 3) so a revoke action is as scoped as
  the original grant — never a blanket sweep of everything attached to a
  user unless that user is being fully offboarded and that is explicitly
  confirmed.

- **Symptom:** An incident break-fix access grant to production is still
  active weeks after the incident closed, and nobody can say why.
  **Fix:** Break-fix access was granted as a standing policy attachment
  instead of through a time-bound elevation mechanism (IAM Identity
  Center, Azure PIM activation). Always grant incident access with a
  hard expiry tied to the expected incident window (extend explicitly if
  the incident runs long, don't grant open-ended "for now" access), and
  require a post-incident ticket confirming the grant either already
  expired or was manually removed.

- **Symptom:** An access-request queue has a growing backlog of pending
  tickets, and engineers start bypassing the process by asking a
  teammate with existing access to do the work directly ("shadow
  access").
  **Fix:** This is a process-design failure, not just a queue-depth
  problem — it produces access equivalent to an ungoverned grant with
  zero audit trail. Set an SLA for routine, pre-approved-pattern requests
  (e.g. same-team standard onboarding access) to auto-approve or
  fast-track, reserving manual approval friction for genuinely unusual or
  high-privilege requests.

## Worked example

**Scenario:** A 6-week contractor, `jsmith`, joins to help the analytics
team build a report. They need read-only access to one S3 bucket
(`analytics-reports`) and nothing else, for the duration of the contract.

1. The analytics team lead files a ticket: requester = team lead,
   resource = `analytics-reports-<AWS_ACCOUNT_ID>` (read-only), duration
   = 42 days, approver = analytics team lead's manager (a different
   person from the requester).
2. On approval, an admin creates an IAM user (or, if federated,
   associates the contractor's existing SSO identity) and attaches a
   scoped inline policy granting `s3:GetObject`/`s3:ListBucket` on only
   that bucket and prefix, with a `DateLessThan` condition set to the
   contract end date plus one day of buffer.
3. The IAM policy is named `analytics-readonly-temp` and tagged (via the
   user's tags, since inline policies can't carry tags directly)
   `access-ticket=JIRA-4821`, `expires=2026-09-08`, `granted-by=<manager>`.
4. The ticket is updated with the exact policy JSON applied and the
   expiry date, then closed as fulfilled — the ticket itself is now the
   audit record a review can pull up months later.
5. A weekly scheduled script queries all IAM users/roles for an
   `expires=` tag in the past; when `jsmith`'s tag matches after
   2026-09-08, it opens a low-priority ticket confirming the grant either
   already stopped working (condition expired) or flagging it for manual
   removal if the IAM object is still present.
6. When the contract ends early (week 5), the team lead files a revoke
   ticket referencing `JIRA-4821`; an admin runs
   `aws iam delete-user-policy --user-name contractor-jsmith --policy-name analytics-readonly-temp`
   and deletes the now-unused IAM user, closing the loop before the
   original expiry date is even reached.

## Cross-references

- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md) — designs the
  underlying least-privilege role/policy structure and break-glass
  process that this skill grants *into*; use it when a recurring one-off
  request pattern should become a standing role, or when doing the
  periodic access review this skill's grants feed into.
- [aws-landing-zone-setup](../aws-landing-zone-setup/SKILL.md) — IAM
  Identity Center permission sets and OU-level guardrails that scope what
  any individual grant made under this skill can reach.
- [cloud-cost-anomaly-investigation](../cloud-cost-anomaly-investigation/SKILL.md) —
  a spike caused by a resource an over-broad or stale temporary grant let
  someone provision is one of the things that investigation traces back
  to a specific identity/grant.
