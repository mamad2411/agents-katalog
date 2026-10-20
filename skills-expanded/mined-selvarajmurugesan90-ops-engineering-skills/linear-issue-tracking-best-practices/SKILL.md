---
name: linear-issue-tracking-best-practices
description: >
  Guides Linear's cycle-based workflow model — Issues, Projects, and
  time-boxed Cycles instead of Jira's sprint/board configuration,
  Linear's opinionated status workflow (Triage → Backlog → Todo → In
  Progress → In Review → Done/Cancelled), its keyboard-driven/low-
  friction issue creation philosophy, and the Linear API/SDK for
  programmatic issue management. Use when the user asks to "set up
  Linear for our team," "should we use Linear or Jira," "create a Linear
  issue via the API," "design our Linear cycle/project structure," "why
  did our Jira migration to Linear feel different," or "reduce process
  overhead in our issue tracker." Cross-references the Jira-focused
  ticket-workflow skill for teams comparing or migrating between tools.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: incident-tooling-and-itsm
  maturity: stable
---

# Linear Issue Tracking Best Practices

## Purpose

Linear and Jira both track work as issues moving through a workflow, but
they encode meaningfully different opinions about how a team should
operate, and treating Linear as "Jira with a nicer UI" throws away most
of what makes it a good fit for the teams that prefer it. Linear is
built around **Cycles** — short, fixed-length, automatically-recurring
time boxes (typically 1-2 weeks) that every active team commits to, in
contrast to Jira's more configurable, often longer or irregular sprint
model — and **Projects** as a lightweight, cross-cycle container for
initiative-level work, rather than Jira's heavier Epic hierarchy. It is
also deliberately opinionated about workflow states and low-friction
issue creation (keyboard shortcuts, quick-capture, minimal required
fields) where Jira is deliberately configurable and admin-customizable
per project. This skill covers Linear's actual data model (Issues,
Projects, Cycles, Triage), its default status workflow and why deviating
from it usually costs more than it gains, when a team should actually
prefer Linear over Jira (small-to-mid engineering-only teams wanting low
process overhead) versus when Jira's configurability still wins
(complex cross-functional workflows, ITSM-adjacent needs, heavy
customization requirements), and the Linear API/SDK for programmatic
issue management. It assumes the reader is already familiar with
general ticket-writing hygiene (clear titles, acceptance criteria,
priority discipline) covered in
[jira-ticket-best-practices-and-workflow](../../../enterprise-collaboration/skills/jira-ticket-best-practices-and-workflow/SKILL.md)
and focuses specifically on what's different about Linear's model.

## When to use

- Setting up Linear for a team for the first time — Workspace, Teams,
  Cycles, and initial workflow configuration.
- Deciding between Linear and Jira for a new team or product, and
  wanting the tradeoffs made concrete rather than a generic feature
  comparison.
- Designing a Cycle and Project structure so cycle planning reflects
  real team capacity rather than becoming a rubber-stamped ritual.
- Migrating a team from Jira to Linear (or vice versa) and needing to
  understand what doesn't map 1:1 (Jira's flexible board/workflow
  customization vs. Linear's opinionated defaults, Epics vs. Projects).
- Creating, updating, or querying issues programmatically via the
  Linear GraphQL API or an SDK, from a script, CI job, or agent
  workflow.
- Debugging why a team's Cycle consistently under- or over-commits, or
  why Triage is accumulating unprocessed issues.
- Explaining to a stakeholder used to Jira why Linear doesn't expose the
  same level of workflow customization, and why that's often a
  deliberate tradeoff rather than a missing feature.

## Prerequisites & environment

- A Linear workspace with at least one **Team** created — Linear scopes
  Cycles, workflow states, and most configuration per Team, not
  globally across the whole workspace (closer to a Jira "project" in
  scope, though the underlying model differs).
- Familiarity with Linear's core objects: **Issue** (the unit of work,
  roughly Jira's issue), **Project** (a cross-cycle initiative
  container, lighter-weight than a Jira Epic and not required for every
  issue), **Cycle** (a fixed-length, auto-recurring time box a Team
  commits issues to — Linear's closest analog to a Jira sprint, but
  auto-scheduled rather than manually started/closed), and **Triage** (a
  holding state for incoming issues, especially from integrations, that
  haven't yet been accepted into the team's actual workflow).
- API access: a Linear **personal API key** or an **OAuth2** application
  token for broader integrations. Store as `${LINEAR_API_KEY}`; never
  hardcode it. The API is **GraphQL-only** — there is no REST
  equivalent — at `https://api.linear.app/graphql`.
- Official SDKs (`@linear/sdk` for TypeScript/JavaScript, or direct
  GraphQL calls from any language) if building automation — the
  TypeScript SDK is the most actively maintained and closely tracks API
  changes.
- Permission scoping: API keys inherit the creating user's permissions;
  for team-wide automation (a bot creating issues on behalf of an
  integration), use a dedicated service-account-style user rather than
  a personal API key tied to one engineer who might leave.
- If comparing against or migrating from Jira, review
  [jira-ticket-best-practices-and-workflow](../../../enterprise-collaboration/skills/jira-ticket-best-practices-and-workflow/SKILL.md)
  first — the ticket-quality guidance there (clear titles, acceptance
  criteria, honest status movement) applies equally to Linear issues and
  isn't repeated here.

## Step-by-step guidance

1. **Use Linear's default workflow states rather than heavily
   customizing them**, at least initially — Linear ships with an
   opinionated default (`Triage` → `Backlog` → `Todo` → `In Progress` →
   `In Review` → `Done`/`Cancelled`) that reflects how most engineering
   teams actually work, and Linear's tooling (cycle progress views,
   velocity charts) assumes this shape:
   ```
   Triage      — incoming issues (often from an integration/bug report)
                 not yet accepted into the team's actual workflow
   Backlog     — accepted, not yet scheduled into a cycle
   Todo        — scheduled into the current/upcoming cycle, not started
   In Progress — actively being worked
   In Review   — a PR/change is open, awaiting review
   Done        — complete
   Cancelled   — explicitly won't be done (not the same as Done)
   ```
   Resist adding many custom intermediate states early — Linear's
   opinionated default is a large part of why teams find it lower-
   friction than a heavily customized Jira board; each added state is a
   small ongoing cost to the team's shared mental model of "what does
   this status actually mean."

2. **Use Triage deliberately as a real gate**, not a state issues sit in
   indefinitely. Every issue entering from an external integration
   (a bug reporting tool, a support ticket sync, a Slack integration)
   should land in Triage and be actively processed (accepted into
   Backlog with a priority, or declined/merged as a duplicate) on a
   short, regular cadence:
   ```
   Team norm: Triage is reviewed daily; nothing sits longer than 48h
   without either being accepted into Backlog or explicitly declined.
   ```
   An unprocessed, growing Triage queue is Linear's equivalent of Jira's
   "everything ends up Highest priority" anti-pattern — it stops being a
   meaningful signal the moment it's not actively worked.

3. **Plan Cycles around real committed capacity, not a wish list.**
   Linear auto-schedules Cycles on a fixed cadence (commonly 1 or 2
   weeks) once configured at the Team level:
   ```
   Team settings → Cycles: enabled, length = 2 weeks, starts Monday
   ```
   At the start of each cycle, move only issues the team genuinely
   expects to complete from Backlog into the cycle — an over-stuffed
   cycle that routinely carries 40% of its issues into the next one
   defeats the purpose of a fixed time box as a forecasting signal, the
   same failure mode as Jira sprints that never actually close clean.

4. **Use Projects for genuinely cross-cycle, multi-person initiatives**,
   not for every piece of work — Linear's Project is deliberately
   lighter-weight than a Jira Epic, and forcing every issue under a
   Project adds overhead without adding clarity for small, standalone
   tasks:
   ```
   Project: "Checkout API v2 migration"
     — spans multiple cycles, has a target date, has a project lead,
       contains issues from possibly multiple teams
   Standalone issue (no Project): "Fix flaky test in checkout-api CI"
     — small, single-cycle, doesn't need a Project wrapper
   ```

5. **Create an issue programmatically via the GraphQL API:**
   ```http
   POST https://api.linear.app/graphql
   Authorization: ${LINEAR_API_KEY}
   Content-Type: application/json
   ```
   ```graphql
   mutation IssueCreate {
     issueCreate(
       input: {
         teamId: "TEAM_UUID"
         title: "Checkout fails when cart has >50 line items"
         description: "Steps to reproduce:\n1. POST /cart/checkout with 51+ items on staging.\n\nExpected: 200 with order confirmation.\nActual: 500, no response body."
         priority: 2
         labelIds: ["LABEL_UUID_CUSTOMER_REPORTED"]
       }
     ) {
       success
       issue { id identifier url }
     }
   }
   ```
   A successful response returns the issue's `identifier` (e.g.
   `CHK-482`) and `url` — capture both for linking and follow-up, the
   same pattern as capturing a Jira issue `key`.

6. **Update an issue's state via GraphQL mutation**, resolving the
   target workflow state's ID first (states are per-Team, not global):
   ```graphql
   query WorkflowStates {
     team(id: "TEAM_UUID") {
       states { nodes { id name type } }
     }
   }
   ```
   ```graphql
   mutation IssueUpdate {
     issueUpdate(
       id: "ISSUE_UUID",
       input: { stateId: "IN_PROGRESS_STATE_UUID" }
     ) { success }
   }
   ```

7. **Use the TypeScript SDK for anything beyond a one-off script**, since
   it handles pagination, retries, and type safety the raw GraphQL calls
   don't:
   ```typescript
   import { LinearClient } from "@linear/sdk";

   const linear = new LinearClient({ apiKey: process.env.LINEAR_API_KEY });

   const issue = await linear.createIssue({
     teamId: "TEAM_UUID",
     title: "Checkout fails when cart has >50 line items",
     priorityLabel: "Urgent",
   });
   ```

8. **Sync Linear with an external system (Slack, GitHub, an incident
   tool) via Linear's native integrations before building a custom
   webhook sync** — Linear ships first-party integrations for the most
   common cases (GitHub PR status linking issue state automatically,
   Slack for notifications), which cover most needs with far less
   maintenance than a bespoke sync layer.

## Best practices

- Keep workflow states close to Linear's default set — the tool's own
  cycle/velocity tooling and the low-friction experience teams choose
  Linear for both assume this shape; heavy customization erodes both.
- Treat Triage as an actively-managed daily gate, not a parking lot —
  an unprocessed Triage queue defeats its purpose as a signal the same
  way an unbounded Jira backlog does.
- Commit to Cycles based on real, historically-demonstrated capacity,
  and review completion rate over several cycles rather than reacting
  to any single cycle's carry-over as a one-off.
- Reserve Projects for genuinely cross-cycle, multi-person initiatives;
  don't wrap every small issue in a Project just because the feature
  exists.
- Prefer Linear's native integrations (GitHub, Slack, Sentry, etc.)
  over building custom sync automation — they cover the overwhelming
  majority of real needs with far less ongoing maintenance.
- When comparing to Jira for a new team, be concrete about the actual
  tradeoff: Linear trades configurability for speed and a strong
  opinionated default; a team with complex cross-functional approval
  workflows, heavy custom fields, or ITSM-adjacent needs (see
  [jira-ticket-best-practices-and-workflow](../../../enterprise-collaboration/skills/jira-ticket-best-practices-and-workflow/SKILL.md)
  and, for full ITSM, [servicenow-itsm-integration](../servicenow-itsm-integration/SKILL.md))
  is usually still better served by Jira's or ServiceNow's
  configurability, not Linear's speed.
- Use a dedicated service-account-style user for team-wide API
  automation rather than a personal API key tied to one individual, so
  automation doesn't break when that person changes roles or leaves.

## Common pitfalls

- **Symptom:** A team migrates from Jira to Linear and immediately
  recreates Jira's full custom workflow (eight statuses, several custom
  fields, a complex board configuration) inside Linear.
  **Fix:** This defeats most of the reason Linear tends to feel faster
  — its opinionated default workflow and minimal-friction issue creation
  are core to the tool's design, not a starting point meant to be
  heavily customized back toward Jira's flexibility. Start with the
  default states (step 1) and only add complexity where a team has
  proven, not assumed, a genuine need.

- **Symptom:** Linear's Triage queue has grown to dozens of unreviewed
  issues over several weeks, and nobody's sure which ones are actually
  worth doing.
  **Fix:** Triage needs an active, short-cadence review habit (step 2)
  — assign a rotating owner to clear it daily/every-other-day, the same
  discipline a healthy Jira backlog-grooming process requires, just
  under a different name.

- **Symptom:** A team's Cycles routinely carry over 30-40% of committed
  issues into the next cycle, and cycle planning has become a rubber
  stamp rather than a real forecasting exercise.
  **Fix:** The team is committing to a wish list, not real capacity —
  review actual historical completion rate over several cycles and
  commit to that number going forward (step 3), rather than treating
  each cycle's overcommitment as a one-off that "just happened" to be
  busy.

- **Symptom:** Every single issue, including a one-line typo fix, is
  wrapped in its own Project, and the Projects list has become as
  cluttered and hard to navigate as an over-Epic'd Jira backlog.
  **Fix:** Reserve Projects for genuinely cross-cycle, multi-person
  initiatives with a real target date and lead (step 4); a standalone,
  single-cycle issue doesn't need a Project wrapper, and treating every
  issue as needing one just recreates Jira's heavy-Epic problem under a
  different name.

- **Symptom:** A custom webhook-based sync between Linear and an
  external tool (built because "we needed something specific") breaks
  silently after a Linear API schema change, and issues stop updating.
  **Fix:** Check whether Linear's native integration for that tool
  (GitHub, Slack, Sentry, and others) already covers the actual need
  before building custom sync automation (step 8) — a first-party
  integration is maintained against Linear's own API changes; a custom
  sync is not, and is an ongoing maintenance liability for a need that
  often didn't require a bespoke solution in the first place.

## Worked example

**Scenario:** A 6-person product engineering team moving off Jira picks
Linear specifically to reduce process overhead, and sets up Cycles,
Triage handling, and a GitHub-driven issue-creation automation for
incoming bug reports.

Team configuration:
```
Team: "Checkout Platform"
Cycles: enabled, 2-week length, starting Monday
Workflow states: Linear defaults, unmodified
  (Triage, Backlog, Todo, In Progress, In Review, Done, Cancelled)
```

Triage norm agreed by the team: reviewed every morning standup,
nothing sits longer than 48 hours without being accepted (moved to
Backlog with a priority) or declined (moved to Cancelled with a
comment explaining why).

Automated issue creation from a customer-support bug report tool,
landing directly in Triage via the GraphQL API:
```graphql
mutation IssueCreate {
  issueCreate(
    input: {
      teamId: "TEAM_UUID"
      title: "[Support] Checkout 500 error, customer report #48213"
      description: "Customer reports 500 on checkout with a large cart. See support ticket #48213 for full detail and repro steps."
      priority: 3
    }
  ) {
    success
    issue { identifier url }
  }
}
```
Response confirms `identifier: "CHK-511"`, landing in Triage by
default (Linear's incoming-issue behavior for API-created issues without
an explicit `stateId`) for the team to review at the next standup.

First cycle planning: the team reviews the last three cycles' actual
completion rate (averaging 14 of 18 committed issues, ~78%) and commits
to 14 issues for the upcoming cycle rather than the 20 that were
originally on the wish list — the cycle closes with 13 of 14 complete,
a healthy, forecastable result rather than a rubber-stamped overcommit.

GitHub integration (native, not custom) automatically transitions
`CHK-511` from `In Progress` to `In Review` when a linked PR opens, and
to `Done` when it merges — no custom webhook sync required.

## Cross-references

- [jira-ticket-best-practices-and-workflow](../../../enterprise-collaboration/skills/jira-ticket-best-practices-and-workflow/SKILL.md) —
  the general ticket-quality guidance (clear titles, acceptance
  criteria, honest status movement) that applies equally to Linear
  issues; read this for the parts of good issue hygiene this skill
  doesn't repeat, and for the Jira-specific workflow/API mechanics to
  compare against when deciding between the two tools.
- [servicenow-itsm-integration](../servicenow-itsm-integration/SKILL.md) —
  the ITSM-grade, compliance-auditable alternative for organizations
  whose needs (CAB approval, CMDB-linked routing) exceed what either
  Linear's or Jira's lighter-weight issue-tracking model is designed
  for.
- [chatops-runbook-automation](../chatops-runbook-automation/SKILL.md) —
  a comparable "keep the automation layer thin, delegate to the
  platform's native capability before building custom" principle,
  applied to incident-channel bots rather than issue-tracker
  integrations.
