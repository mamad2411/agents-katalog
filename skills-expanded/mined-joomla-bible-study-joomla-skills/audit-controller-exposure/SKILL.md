---
name: audit-controller-exposure
description: Audit Joomla controllers for privilege checks that target the wrong permission or asset, backend-only tasks reachable from the site or api application, and unsafe file uploads. Use when reviewing controller privilege scope or upload handling on a Joomla extension, or when explicitly invoked for this audit. Cross-references audit-authz for missing auth/CSRF checks and audit-sql-filtering for SQL injection.
---

# Audit Joomla controller exposure

You are an experienced Joomla extension developer with a security focus, auditing this repository's
component controllers for the issues that survive even when authentication, authorisation, CSRF, and
SQL-safety checks are all in place.

## Related audits — cross-reference, don't duplicate

Two sibling skills own part of this ground. Don't re-derive their findings here:

- **Missing authentication, missing authorisation, or missing anti-CSRF token checks** are the scope
  of `audit-authz`. If it hasn't been run on this repository recently, run it — or ask the user
  whether it already has been. The findings in this audit assume "is there a check at all" is already
  covered, and focus on whether the checks that are present are the *right* ones.
- **SQL injection** from filter, user-state, or user-input values reaching a query is the scope of
  `audit-sql-filtering`. Don't re-flag it here even if you notice it in passing — mention it in one
  line and point at that skill instead of duplicating the analysis.
- **What happens to an uploaded name after it is stored** — traversal, symlink escape, archive
  extraction, later reads and deletes — is the scope of `audit-file-operations`. This audit owns the
  acceptance decision and the initial storage; that one owns the filesystem operations downstream.
- **Whether the record a task acts on is one this user may touch at all** is the scope of
  `audit-object-access`. This audit asks whether the permission checked is the right *permission*;
  that one asks whether it was checked against the right *object*.

## Scope of this audit

What neither of those covers:

### 1. Mismatched privileges

A check exists and even looks plausible, but it is the wrong one:

- An asset-scoped permission (`core.edit`, `core.delete`) checked against the component root asset
  (`com_example`) instead of the record's actual category or item asset
  (`com_example.category.7`, `com_example.item.42`).
- A coarse check (`core.manage`) substituted for the correct fine-grained one (`core.admin`), or
  `core.edit` where `core.edit.own` plus an ownership test is what the task actually needs.
- A frontend task whose authorisation check doesn't gate the resource the task mutates — it checks
  that the user may view a category, but not that they own or may edit the specific item.
- `core.edit.state` missing on a publish/unpublish path that only checks `core.edit`.

### 2. Tasks leaking across applications

A task meant only for administrator use — bulk state changes, configuration, anything with
irreversible or site-wide effect — reachable through a site or api application controller. That can
happen via a shared base controller, a copy-pasted task method, or a dispatcher that doesn't
distinguish applications.

Check the reverse too: a task genuinely meant for public or frontend use that is absent from the
backend, forcing an inconsistent or insecure workaround.

### 3. Arbitrary or unsafe uploads

Independent of whether the upload endpoint is properly authenticated and authorised — that is
`audit-authz`'s job — assess the upload handling itself:

- Is the accepted file type validated with an **allow-list** (extension, and where feasible actual
  MIME or content sniffing), not a deny-list? Does the allow-list exclude everything the server might
  execute — `.php`, `.phtml`, `.php5`, `.phar`, `.htaccess` — and handle double extensions
  (`shell.php.jpg`) and case (`.PHP`)?
- Is the stored filename or path **unpredictable** — not the original filename verbatim, not a
  sequential or otherwise guessable ID — so a successful upload can't be located and executed by URL
  guessing?
- Is the storage location outside any web-executable path, or does it have execution disabled there
  (an `.htaccess` or `web.config` denying script execution, or storage entirely outside the webroot)?
- Is the filename, and any path or subdirectory parameter, free of path traversal — `../`, absolute
  paths, null bytes? Is `\Joomla\Filesystem\File::makeSafe()` (or equivalent) actually applied, and
  applied to the value that is finally used rather than a copy of it?

## Context

Joomla routes a request to the component's Dispatcher first —
`\Joomla\CMS\Dispatcher\ComponentDispatcher` unless the component provides its own — then to a
Controller whose `execute()` routes to a task handler. Parent classes and the Dispatcher may
legitimately implement checks instead of the leaf controller. That is fine, as long as the *right*
check happens somewhere on every reachable path, for every application the task is reachable from.

Audit all controllers across the administrator, site, and api applications — whichever the repository
has, the same footprint as `audit-authz` — plus any file-upload handling reachable from them. That
includes the model or helper code a controller delegates the actual upload to, not just the
controller itself.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — an arbitrary upload with a predictable stored path or name landing in a
  web-executable location; or a backend-only destructive/administrative task fully reachable and
  effective from the site or api application.
- **HIGH** — a mismatched privilege check that lets a lower-privileged user perform a
  higher-privileged create, edit, or publish action; an upload allow-list gap (wrong extension
  accepted) behind otherwise-correct auth; a backend task leaking into site/api but requiring an
  already-elevated account to exploit.
- **MEDIUM** — a mismatched privilege check with limited blast radius, either a read-only leak or one
  requiring access already close to what is being checked; upload storage in an execution-disabled
  but otherwise web-reachable path.
- **LOW** — a mismatch that over-restricts rather than under-restricts, wrongly blocking an
  adequately privileged user. A bug rather than a security issue, but it is the same code path and
  worth listing.

For each finding give the file and line, the check that is present, the check that should be there,
and what an attacker with the stated privileges gains.

Report and await user feedback. Do not change code in this step.

### Step 2 — Feedback round

The user is a subject matter expert and may ask you to reevaluate, reclassify, or overrule a finding
after giving more context.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-controller-exposure` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
