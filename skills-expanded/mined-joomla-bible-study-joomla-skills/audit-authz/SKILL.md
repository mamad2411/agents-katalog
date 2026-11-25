---
name: audit-authz
description: Audit Joomla component controllers for missing anti-CSRF token checks, missing authentication, and missing authorisation. Use when reviewing controller access control on a Joomla extension, or when explicitly invoked for an authorisation security audit. For checks that exist but target the wrong permission, backend-only tasks reachable from the frontend, or unsafe uploads, use audit-controller-exposure instead.
---

# Audit Joomla controller authorisation

You are an experienced Joomla extension developer with a security focus, auditing this repository's
components for the basic access controls every acting task needs.

## Context

Joomla routes a request to the component's Dispatcher first — `\Joomla\CMS\Dispatcher\ComponentDispatcher`
unless the component provides its own. A custom dispatcher may perform authentication and
authorisation as a master gate for everything behind it.

The request then reaches the Controller for the view, whose `execute()` routes to a task handler.
Somewhere on that path, three things must happen:

- **Anti-CSRF token check** for any task that acts — anything beyond list/read.
  `$this->checkToken()` in a controller, or `Session::checkToken()` directly.
- **Authentication** — non-public views gated to logged-in users.
- **Authorisation** — permission checks (`$user->authorise('core.edit', 'com_example.article.' . $id)`)
  for private views and every create/modify task.

A parent class may already handle some of this, and the Dispatcher may handle it before or instead of
the Controller. Both are acceptable — blanket gating at the dispatcher level is good practice. What
matters is that the check happens somewhere on **every reachable path**, for **every application**
(administrator, site, api) the task is reachable from.

Two Joomla specifics worth holding in mind while reading:

- `FormController` and `AdminController` call `checkToken()` for you in their standard tasks. A
  controller extending `BaseController` gets no such help — every acting task there needs its own
  check.
- `getUserStateFromRequest()` writes request data into the session. A task reached without a token
  check can poison state that a later, properly gated request then trusts.

## Scope of this audit

This audit covers **whether a check exists at all**.

It does not cover whether an existing check targets the right permission or the right asset, whether
a backend-only task is reachable from a frontend or api controller, or upload handling beyond "is it
gated at all" — that is `audit-controller-exposure`. Run it alongside this one for full coverage of
controller-level issues.

SQL injection is `audit-sql-filtering`. If you notice an unsafe query while reading, mention it in
one line and point at that skill rather than analysing it here.

Audit all controllers across the administrator, site, and api applications — whichever the repository
has.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — unauthenticated file upload, especially with a predictable filename or extension.
- **HIGH** — unauthenticated or under-privileged create, edit, or publish.
- **MEDIUM** — unauthenticated or under-privileged delete or unpublish. Anything not covered above is
  HIGH or MEDIUM by impact.
- **LOW** — an adequately privileged user is blocked from an action. That is a bug, not a security
  issue, but it lives on the same code path and is worth listing.

For each finding give the file and line, the task and application it is reachable from, which of the
three checks is missing, and what an attacker with the stated privileges can do with it. Where a
parent class or dispatcher supplies the check, say so explicitly rather than reporting a false
positive — trace the path before you flag it.

Report and await user feedback. Do not change code in this step.

### Step 2 — Feedback round

The user is a subject matter expert and may ask you to reevaluate, reclassify, or overrule a finding
after giving more context. Take that context seriously; a check you could not see may exist in a
place you did not read.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-authz` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
