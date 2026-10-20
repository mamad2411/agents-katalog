---
name: link-a-task-to-a-ticket
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 5min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Link a project task to a support ticket so support and delivery teams can track the same customer-impacting work.

## Preconditions

- You can view the support ticket and project task.
- The ticket and task refer to the same problem, request, or customer impact.
- Cross-tool linking or URL fields are available.

## Steps

1. **Open both records.** Open the support ticket and the tracker task in separate tabs. → *Expect:* both record URLs and titles are visible.
2. **Confirm they match.** Compare customer, issue, symptom, requested work, and scope. → *Expect:* the link will connect related records, not unrelated work.
3. **Copy the task link.** Copy the task URL or issue key from the tracker. → *Expect:* the task reference is ready to paste.
4. **Add the task to the ticket.** [BRANCH: Zendesk | generic] paste the link in a Zendesk internal note, linked issue field, or side conversation; in a generic helpdesk, use the related task field or internal note. → *Expect:* the ticket references the task.
5. **Copy the ticket link.** Copy the ticket URL or case ID from the helpdesk. → *Expect:* the ticket reference is ready to paste.
6. **Add the ticket to the task.** [BRANCH: Jira | Asana | Linear | generic] add the ticket link to the issue description, linked issue field, comment, or customer-impact field. → *Expect:* the task references the ticket.
7. **Add ownership notes.** State who owns customer updates and who owns task completion. → *Expect:* support and project ownership are distinct.

## Decision points

- If multiple tickets report the same issue → link the task to the parent problem or representative ticket.
- If the ticket contains sensitive data → link to the ticket instead of copying its contents.
- If the task is not created yet → create it first, then link both ways.

## Failure modes & recovery

- **F1 One-way link only:** detect the task links to the ticket but the ticket lacks the task link → recover by adding the missing reciprocal link.
- **F2 Wrong record linked:** detect mismatched customer or issue → recover by removing the link and adding the correct one.
- **F3 Access blocked:** detect one team cannot open the linked record → recover by adjusting permissions or adding a sanitized summary.

## Verification

The support ticket links to the task, the task links to the ticket, and ownership for customer communication and task delivery is documented.

## Variations

- [BRANCH: Zendesk | generic] Zendesk may integrate directly with Jira or use side conversations; generic helpdesks may rely on URL fields and internal notes.
- [BRANCH: Jira | Asana | Linear | generic] Jira and Linear often support issue links; Asana and generic tools may use custom URL fields or comments.

## Safety & privacy

Low risk. Prefer links over copying customer data into broader project spaces.
