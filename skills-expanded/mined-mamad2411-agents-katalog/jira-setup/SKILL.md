---
name: jira-setup
description: Bring a Jira Cloud project under governance with exact, idempotent REST v3 and Agile API calls — issue type scheme, a workflow whose statuses map cleanly to status categories, the field set including story points and sprint resolved by name, board and sprint configuration, saved JQL filters, and automation that does not fight the team. Reports what Jira permissions block before attempting anything. Use when starting a Jira project, when a board's states cannot be mapped, or when reports disagree with the board. Not for GitHub governance, not for deciding process, not for writing requirements.
argument-hint: "[--project KEY] [--types] [--workflow] [--fields] [--board] [--filters] [--all] [--dry-run]"
user-invocable: true
agent: foundry-pmo:tracker-operator
model: sonnet
effort: medium
metadata:
  foundry.vertical: management
  foundry.io: "plan.v1 -> Jira project configuration + handoff.v1"
license: Apache-2.0
---

# Jira setup

Exact calls, idempotent by construction. Re-running a completed setup produces **zero changes**;
if it does not, that is a defect here rather than a quirk of Jira.

Default posture is `--dry-run`: print the calls, apply after approval. Credentials come from
`JIRA_BASE_URL`, `JIRA_EMAIL` and `JIRA_API_TOKEN` in the environment, and are never printed.

## Step 1 — Preflight, and read the permissions honestly

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/myself"
```

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/mypermissions?projectKey=$JIRA_PROJECT_KEY&permissions=ADMINISTER_PROJECTS,CREATE_ISSUES,EDIT_ISSUES,MANAGE_SPRINTS_PERMISSION"
```

Jira's permission model is the main thing that decides what this skill can do, and it differs
between **company-managed** and **team-managed** projects. Detect which:

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/project/$JIRA_PROJECT_KEY" 
```

| Project style | Consequence |
|---|---|
| team-managed (`"style": "next-gen"`) | schemes are project-local; most global scheme APIs do not apply, and much of the configuration is UI-only |
| company-managed (`"style": "classic"`) | schemes are shared objects; changing one can affect other projects — always check what else uses it before editing |

**The single most consequential trap:** a shared scheme in a company-managed project is not
yours. Editing a workflow or field configuration that six other projects use is a change with a
blast radius nobody asked for. Read what references the scheme first; if it is shared, create a
copy scoped to this project rather than editing in place, and say so.

## Step 2 — `--types`

Keep the set small. Every extra issue type is a decision every reporter has to make forever.

| Type | Use |
|---|---|
| Epic | a body of work spanning cycles |
| Story | user-visible change with acceptance criteria |
| Task | necessary work with no user-visible outcome |
| Bug | defect against expected behaviour |
| Spike | timeboxed investigation with a written outcome |

Sub-tasks are optional and usually a symptom: an item needing sub-tasks to be understood is
usually an item that should have been split. Route splitting to `foundry-pmo:groom-backlog`.

## Step 3 — `--workflow`

Design statuses so they map cleanly onto `tracker-item.v1` and, above all, onto **status
categories** — because that is what every report reads.

| Status | Category | `tracker-item.v1.state` |
|---|---|---|
| To Do | `new` | `triage` |
| Selected for Development | `new` | `ready` |
| In Progress | `indeterminate` | `in-progress` |
| In Review | `indeterminate` | `in-review` |
| Blocked | `indeterminate` | `blocked` |
| Done | `done` | `done` |
| Won't Do | `done` | `cancelled` |

Two rules:

- **A status in the wrong category poisons every report.** A "Blocked" status placed in the
  `done` category makes blocked work count as delivered. Verify the category of each status after
  creating it; do not trust the name.
- **Won't Do must be a distinct resolution**, never the same as Done, or throughput and every
  forecast built on it are inflated.

Keep the workflow to roughly six statuses. Each additional one adds a transition matrix nobody
maintains and a queue nobody watches.

## Step 4 — `--fields`

Resolve every custom field **by name**, at runtime:

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/field"
```

Find `Story Points` (or `Story point estimate` in team-managed projects) and `Sprint` in the
response and use the returned id. Hardcoding `customfield_10016` works on one instance and
silently reads the wrong field on the next — silently, because the API returns a value either way.

Add fields only when something consumes them. An empty custom field on every issue is a question
the team answers with blanks, and blanks train people to skip fields that do matter.

## Step 5 — `--board`

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/agile/1.0/board?projectKeyOrId=$JIRA_PROJECT_KEY"
```

```bash
curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/agile/1.0/board/$BOARD_ID/sprint?state=active,future"
```

Jira is the only one of the four supported trackers where a sprint is a first-class object with
authoritative state and dates. That is worth using: `sprint.state` from here is trustworthy in a
way a GitHub milestone due date is not.

Board columns must map onto statuses one-to-one. A column aggregating three statuses makes cycle
time per state uncomputable, which is exactly the breakdown `--diagnose` needs in
`forecast-delivery`.

Set column WIP limits when the team runs Kanban. A limit nobody set is a limit at infinity.

## Step 6 — `--filters`

Saved JQL that the team actually opens:

```
project = KEY AND statusCategory != Done AND assignee IS EMPTY AND status = "Selected for Development"
project = KEY AND status = Blocked AND updated <= -3d
project = KEY AND statusCategory = "In Progress" AND updated <= -5d
project = KEY AND issuetype = Story AND description IS EMPTY
project = KEY AND resolution = "Won't Do" AND resolved >= -30d
```

The third is ageing work in progress and is the most useful query on any board. The last one
exists so cancelled work stays visible instead of disappearing into the Done category.

## Step 7 — Verify

Re-read after every write and report `created` / `updated` / `unchanged`. Then run the check that
matters: pull ten issues through `sync-tracker` and confirm the states normalise as intended and
the unmapped count is zero. Configuration that looks right in the UI and normalises wrong is the
failure this step exists to catch.

## Degradation

| Condition | Behaviour |
|---|---|
| no credentials | emit every call as copy-pasteable; `status: blocked` |
| not a project admin | apply what is permitted; list the rest with the permission required |
| team-managed project | say plainly which steps are UI-only on this style rather than failing quietly |
| shared scheme detected | do not edit; propose a project-scoped copy and name what else uses it |
| rate limited | honour `Retry-After`, resume, report the pause |

## Refusals

- Editing a shared scheme without naming everything that references it.
- Hardcoding a custom field id.
- Bulk-transitioning issues to "fix" a report — that rewrites history and destroys cycle time.
- Deleting a status, field or sprint. Deprecate and hide; deletion in Jira is rarely recoverable.

## Progressive disclosure

- `references/jira-api.md` — auth, pagination, the v3/Agile split, error shapes.
- `references/workflow-design.md` — statuses, categories, transition rules, verification.
- `references/jql-recipes.md` — the saved filters, and what each one is for.
