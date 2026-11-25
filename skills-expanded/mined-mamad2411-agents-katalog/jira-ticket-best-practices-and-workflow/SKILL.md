---
name: jira-ticket-best-practices-and-workflow
description: >
  Guides writing well-formed Jira issues (clear title, reproduction steps
  or acceptance criteria, correct issue type/priority/labels/components),
  disciplined status-workflow movement (To Do → In Progress → In Review →
  Done, avoiding stale or prematurely closed tickets), and linking related
  issues/epics — plus the underlying Jira REST API shape
  (`POST /rest/api/3/issue`, transitions, issue links) for doing this
  programmatically. Use when the user asks to "write a Jira ticket",
  "file a bug report", "create a user story", "update ticket status",
  "move a ticket to In Progress/Done", "link this to the epic", or
  "review whether this ticket is ready to work on".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: enterprise-collaboration
  maturity: stable
---

# Jira Ticket Best Practices and Workflow

## Purpose

A Jira ticket is the unit of work that everyone downstream — the engineer
who picks it up, the reviewer, the release manager, and whoever debugs a
regression six months later — has to reconstruct intent from. A vague
title, a missing reproduction case, or acceptance criteria that only exist
in someone's head turns every handoff into a Slack thread or a meeting.
This skill covers how to write a ticket that is actionable on its own,
how to pick the issue type/priority/labels that make triage and reporting
meaningful instead of noise, how to move a ticket through its workflow
states honestly (not just to make a board look green), and how to do all
of this programmatically against the Jira REST API when an agent is
creating or updating issues on a user's behalf. It does not cover how to
comment on or automate updates to an existing ticket (see
[jira-comments-and-tracking-automation](../jira-comments-and-tracking-automation/SKILL.md))
or how to document the resulting work in Confluence (see
[confluence-page-authoring-and-governance](../confluence-page-authoring-and-governance/SKILL.md)).

## When to use

- Drafting a new bug report, user story, task, or epic before filing it.
- Reviewing an existing ticket for readiness ("is this ready to pick up?")
  before it enters a sprint or a "Ready for Dev" column.
- Deciding what issue type, priority, labels, and components a piece of
  work should have.
- Moving a ticket between workflow states (To Do → In Progress → In
  Review → Done) and deciding whether that move is actually justified.
- Linking a ticket to its parent epic, a blocking/blocked-by dependency,
  or a duplicate.
- Creating or updating issues programmatically via the Jira REST API
  (Cloud or Data Center) from a script, CI job, or agent workflow.

## Prerequisites & environment

- A Jira Cloud or Data Center/Server project with a configured workflow
  (issue types, statuses, transitions) — the exact status names and
  transition IDs are project-specific and must be looked up per project,
  not assumed.
- API access: a Jira Cloud API token (Atlassian account → API tokens) or,
  for Data Center, a Personal Access Token (PAT). Store as
  `${JIRA_API_TOKEN}`; never hardcode it.
- Base URL as `${JIRA_BASE_URL}` (e.g. `https://your-domain.atlassian.net`
  for Cloud; an internal hostname for Data Center).
- Jira Cloud REST API is `/rest/api/3/...` and expects issue
  descriptions/comments in **Atlassian Document Format (ADF)**, a JSON
  tree, not plain markdown. Data Center/Server on older versions may
  still be on `/rest/api/2/...` with plain-text/wiki-markup bodies —
  confirm the API version before assuming ADF is accepted.
- Permission to create/transition issues in the target project (Jira
  permission scheme — "Create Issues", "Transition Issues", etc.).
- If no direct REST access is available, the same guidance applies when
  relaying instructions to a human or through an MCP Jira integration —
  the ticket-quality and workflow discipline below is tool-agnostic; only
  the "how it's submitted" mechanics differ.

## Step-by-step guidance

1. **Pick the issue type deliberately.** Bug = something that used to
   work, or should work per a spec, and doesn't. Story = user-facing
   increment of value. Task = internal work with no direct user-facing
   behavior change. Epic = a container for a body of related stories/
   tasks, not a to-do list itself. Filing a regression as a "Task" hides
   it from defect-rate metrics; filing routine maintenance as a "Bug"
   inflates them. When unsure, ask "would this show up in a bug-count
   dashboard a manager reviews?" — if yes, it's a Bug.

2. **Write a title that stands alone in a list of 200 other titles.**
   Format: `[Component/Area] Symptom, not root cause`. Bad: `Fix bug`.
   Good: `[Checkout API] 500 error when cart contains >50 line items`.
   The title should let someone triaging a backlog understand impact and
   area without opening the ticket.

3. **Structure the description by issue type:**
   - **Bug**: Summary → Steps to Reproduce (numbered) → Expected
     Behavior → Actual Behavior → Environment (version, env name, browser/
     OS if relevant) → Logs/screenshots/links → Impact/scope.
   - **Story**: Summary → User story (`As a <role>, I want <capability>,
     so that <benefit>`) → Acceptance Criteria (checklist, testable,
     unambiguous — "Given/When/Then" is fine) → Out of scope (explicit).
   - **Task**: Summary → What needs to happen → Definition of done.
   Acceptance criteria must be objectively checkable by someone other
   than the author — "works well" is not a criterion; "API returns 200
   with the updated resource within 2s at p95" is.

4. **Set priority from an impact × urgency rubric, not gut feel.** e.g.
   Highest = production outage / data loss, no workaround. High =
   significant functionality broken, workaround exists. Medium = minor
   functionality issue, low user impact. Low = cosmetic/nice-to-have.
   Publish and reuse the same rubric across the project so "Highest"
   still means something after 500 tickets.

5. **Set labels and components for future search, not decoration.** Use
   components for the owning subsystem/team (drives routing and reports);
   use labels for cross-cutting attributes (`customer-reported`,
   `security`, `tech-debt`, `needs-design`). Don't invent a new label
   per ticket — check existing labels in the project first.

6. **Link related work before it goes stale.** Link a story to its epic
   (`fields.parent` on creation, or the "Epic Link"/parent field
   depending on project type — team-managed vs. company-managed projects
   differ here). Use issue links (`Blocks`/`Is blocked by`, `Relates to`,
   `Duplicates`) for cross-ticket dependencies so a blocked ticket isn't
   silently worked on, and a duplicate isn't independently re-solved.

7. **Move status honestly, not decoratively:**
   - **To Do → In Progress**: only when someone is actually actively
     working it *now*, not "queued for this sprint."
   - **In Progress → In Review**: only once a PR/change is open and
     linked, or the deliverable is ready for another human to check.
   - **In Review → Done**: only when acceptance criteria are verifiably
     met — re-check the AC checklist, don't just trust the reviewer
     approved the code. If AC can't be met as written, either fix the
     work or explicitly amend the AC with a note explaining why, before
     closing.
   - Never skip straight to Done to "clean up the board" — that erases
     the signal the workflow exists to produce (cycle time, review
     backlog, WIP).

8. **Create an issue via the REST API:**

   ```http
   POST /rest/api/3/issue
   Host: ${JIRA_BASE_URL}
   Authorization: Basic base64(${JIRA_USER_EMAIL}:${JIRA_API_TOKEN})
   Content-Type: application/json
   ```

   ```json
   {
     "fields": {
       "project": { "key": "CHK" },
       "issuetype": { "name": "Bug" },
       "summary": "[Checkout API] 500 error when cart contains >50 line items",
       "priority": { "name": "High" },
       "labels": ["customer-reported"],
       "components": [{ "name": "checkout-api" }],
       "description": {
         "type": "doc",
         "version": 1,
         "content": [
           {
             "type": "paragraph",
             "content": [
               { "type": "text", "text": "Steps to Reproduce: POST /cart/checkout with 51+ line items on staging." }
             ]
           },
           {
             "type": "paragraph",
             "content": [
               { "type": "text", "text": "Expected: 200 with order confirmation. Actual: 500, no response body." }
             ]
           }
         ]
       }
     }
   }
   ```

   A successful response returns `201 Created` with the new issue's
   `id`, `key`, and `self` URL — capture the `key` (e.g. `CHK-4821`) for
   linking and follow-up updates.

9. **Transition an issue's status.** First discover valid transitions
   (they are workflow- and current-status-specific, never hardcode an ID
   across projects):

   ```http
   GET /rest/api/3/issue/CHK-4821/transitions
   ```

   Then post the chosen transition `id` from that response:

   ```http
   POST /rest/api/3/issue/CHK-4821/transitions
   Content-Type: application/json

   { "transition": { "id": "31" } }
   ```

10. **Link two issues:**

    ```http
    POST /rest/api/3/issueLink
    Content-Type: application/json

    {
      "type": { "name": "Blocks" },
      "inwardIssue": { "key": "CHK-4821" },
      "outwardIssue": { "key": "CHK-4790" }
    }
    ```

    Exact field names (`inwardIssue`/`outwardIssue` semantics, available
    link `type` names) are configurable per Jira instance — confirm with
    `GET /rest/api/3/issueLinkType` rather than assuming defaults.

## Best practices

- Write the acceptance criteria (or reproduction steps) *before* work
  starts, not retroactively when someone asks "how do I know this is
  done?" — if you can't write them, the ticket isn't ready to leave
  backlog.
- Keep one ticket = one deliverable. A ticket with an AC list that reads
  like five unrelated features should be split into an epic with
  sub-tickets, each independently closeable.
- Prefer editing the ticket's fields (status, priority, fix version) for
  state that other people/dashboards depend on; reserve free-text
  comments for narrative context (see the companion comments skill).
- When creating tickets programmatically in bulk, dry-run against a
  single issue first and inspect the `201` response before looping —
  a bad `fields` payload silently applied 200 times is expensive to
  unwind.
- Treat "Definition of Ready" (has AC, has priority, has an owner
  identified) and "Definition of Done" (AC verified, linked
  PR/commit merged, no unresolved blocking links) as project-wide
  checklists, not a memory exercise per ticket.
- For cross-team dependencies, link issues explicitly (`Blocks`/`Is
  blocked by`) instead of relying on a mention in the description that
  nobody re-checks once written.

## Common pitfalls

- **Symptom:** A ticket is marked Done, but weeks later someone
  discovers the acceptance criteria were never actually met — only the
  PR was merged, not verified against the AC.
  **Fix:** Before transitioning to Done, re-read the AC checklist against
  the actual behavior (or ask the reporter to verify), not just confirm
  code review happened. If AC genuinely changed mid-flight, edit the
  ticket to reflect the new AC and note why, rather than closing against
  stale criteria.

- **Symptom:** Tickets sit in "In Progress" for weeks with no comments,
  no linked PR, and no one notices until a sprint retro — "stale WIP"
  that quietly breaks cycle-time metrics and hides real status from
  planning.
  **Fix:** Only move to In Progress when work is actually starting
  (not "assigned for later"), and run a periodic stale-ticket query
  (e.g. JQL `status = "In Progress" AND updated <= -7d`) to surface and
  triage them instead of letting the board silently lie.

- **Symptom:** Every ticket in a project ends up `Priority: Highest`
  within a few months, because there's no shared definition of what
  priority means, so it stops being useful for triage.
  **Fix:** Publish and enforce an impact × urgency rubric (see step 4)
  and periodically audit priority distribution — a healthy backlog is
  rarely more than 5-10% Highest.

- **Symptom:** A bug is filed with just a title ("Checkout broken") and
  no reproduction steps; the assignee spends a day just trying to
  reproduce it, then bounces it back with "can't reproduce, need more
  info," losing a full cycle.
  **Fix:** Enforce reproduction steps + environment as a hard
  requirement before a bug leaves "To Do" — reject/return tickets missing
  them rather than letting them enter a sprint.

- **Symptom:** A ticket is filed as a "Task" for what is actually a
  regression, so it never shows up in defect/quality dashboards, and
  the team under-reports its real bug rate.
  **Fix:** Use the issue-type test in step 1 consistently, and correct
  misclassified tickets when spotted rather than leaving them for
  "historical consistency."

## Worked example

**Before — a ticket that generates more questions than it answers:**

> **Title:** login broken
> **Description:** Users can't log in sometimes. Please fix ASAP.
> **Type:** Task · **Priority:** Highest · **Labels:** (none)

This tells the assignee nothing: which login flow (password, SSO,
mobile app)? What does "sometimes" mean — every user, a subset, a
specific browser? Is there an error message? What's actually broken vs.
"Task" (no user-facing regression) implies?

**After — actionable on its own:**

> **Title:** `[Auth Service] SSO login fails with "invalid_grant" for users in EU region`
> **Type:** Bug · **Priority:** High · **Labels:** `customer-reported`
> **Components:** `auth-service`
>
> **Steps to Reproduce:**
> 1. Log in via SSO (Okta) from an account provisioned in the `eu-west-1`
>    tenant.
> 2. Complete the identity-provider redirect.
>
> **Expected:** Redirect back to the app, authenticated session created.
> **Actual:** Auth service returns `400 invalid_grant`; user is bounced
> back to the IdP login screen in a loop.
>
> **Environment:** Production, `auth-service` v2.14.0, EU tenant only —
> US tenant unaffected.
> **Impact:** ~120 EU users unable to log in since 2026-07-27 09:00 UTC.
> **Logs:** link to `auth-service` error trace `req-id=a91f...`.

Creating this ticket via the REST API:

```http
POST /rest/api/3/issue
Content-Type: application/json
Authorization: Basic base64(${JIRA_USER_EMAIL}:${JIRA_API_TOKEN})
```

```json
{
  "fields": {
    "project": { "key": "AUTH" },
    "issuetype": { "name": "Bug" },
    "summary": "[Auth Service] SSO login fails with \"invalid_grant\" for users in EU region",
    "priority": { "name": "High" },
    "labels": ["customer-reported"],
    "components": [{ "name": "auth-service" }]
  }
}
```

Response (`201 Created`):

```json
{
  "id": "148213",
  "key": "AUTH-2231",
  "self": "${JIRA_BASE_URL}/rest/api/3/issue/148213"
}
```

Once a fix PR opens, transition `AUTH-2231` from `To Do` to `In
Progress` (after discovering the transition id via `GET
/rest/api/3/issue/AUTH-2231/transitions`), and link it to the release
epic:

```json
{
  "type": { "name": "Relates" },
  "inwardIssue": { "key": "AUTH-2231" },
  "outwardIssue": { "key": "AUTH-100" }
}
```

## Cross-references

- [jira-comments-and-tracking-automation](../jira-comments-and-tracking-automation/SKILL.md) —
  once the ticket exists, how to comment on it usefully and automate
  status/comment updates from CI/CD without creating noise.
- [confluence-page-authoring-and-governance](../confluence-page-authoring-and-governance/SKILL.md) —
  when a ticket's resolution needs a durable runbook, design doc, or
  postmortem rather than living only in a Jira description.
