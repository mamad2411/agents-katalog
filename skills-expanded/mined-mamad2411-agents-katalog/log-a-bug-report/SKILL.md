---
name: log-a-bug-report
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Log a bug report that gives the owning team enough evidence to reproduce, prioritize, and fix the issue.

## Preconditions

- You can create issues in the tracker.
- You know the affected product area and observed behavior.
- Screenshots, logs, account IDs, or reproduction details are available if applicable.

## Steps

1. **Open issue creation.** [BRANCH: Jira | Asana | Linear | generic] choose Create issue in Jira, Add task in Asana, New issue in Linear, or New bug in a generic tracker. → *Expect:* a blank work item form is visible.
2. **Write a clear title.** Summarize the broken behavior and affected area. → *Expect:* the title distinguishes this bug from similar issues.
3. **Describe expected and actual behavior.** State what should happen and what happened instead. → *Expect:* the failure is understandable without extra context.
4. **Add reproduction steps.** Number the exact actions, inputs, environment, and account type used. → *Expect:* another person can try to reproduce it.
5. **Attach evidence.** Add screenshots, logs, links, browser or app version, and timestamps after removing secrets. → *Expect:* supporting evidence is available from the issue.
6. **Set metadata.** Choose product area, priority, severity, customer impact, and labels. → *Expect:* the bug can be routed and reported.
7. **Submit the report.** Save the bug and copy its link if needed. → *Expect:* the bug has an issue ID or URL.

## Decision points

- If the bug affects active customers broadly → escalate through incident or support escalation before routine backlog entry.
- If reproduction is unknown → mark it intermittent and include frequency, environment, and evidence.
- If the report includes sensitive data → redact before attaching files.

## Failure modes & recovery

- **F1 Cannot reproduce:** detect the owner cannot trigger the issue → recover by adding environment, account state, video, or logs.
- **F2 Wrong component:** detect reassignment away from the chosen area → recover by updating product area and labels.
- **F3 Sensitive evidence attached:** detect tokens, passwords, or personal data in attachments → recover by removing the attachment and uploading a redacted version.

## Verification

The bug report has an ID, title, expected and actual behavior, reproduction details, evidence, severity or priority, and owning team or component.

## Variations

- [BRANCH: Jira | Asana | Linear | generic] Jira may use issue type Bug and components; Asana may use a task template; Linear may use labels and teams; generic tools may use custom fields.

## Safety & privacy

Bug reports often include logs or customer examples. Redact credentials, tokens, and personal data before sharing.
