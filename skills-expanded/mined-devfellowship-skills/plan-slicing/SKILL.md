---
name: plan-slicing
description: "Use when turning a large plan into PRs that several agents or people will build in parallel — decides where code lives, assigns one owner PR per shared artifact, predicts file and behavior conflicts, adds sweep PRs for everywhere-decisions, forbids temporarily unreachable features, and writes the merge and deploy order into the PR table. Skip for a plan that is a single PR."
author: SamuelStefano
tags: [planning, pull-requests, parallel-work, architecture]
---

# Slicing a plan into PRs

**Core principle:** every shared thing has exactly one owner PR, and every PR
leaves the product fully usable.

Output: the PR table (`complex-plan/templates/PR-TABLE.md`) as the `## Tasks`
section of the plan; each row becomes one tracker task with an owner.

*(Parallel PRs from one base built three copies of the same list; 12 planned PRs
became 16; a post-merge audit found about 10 gaps.)*

## 1. Where code lives

Before the first row, name the repo and package that owns each component.
*(Five new repos, then a consolidation ordered by the lead.)*

## 2. Shared artifacts first

List everything 2+ rows touch — components, hooks, stores, tokens, routes,
settings keys, fixtures, CI config. One owner row each; the others depend on it.
The owner is the **earliest** row in merge order that edits it. *(A seed file was
owned by a phase-2 row while a phase-1 row edited it first.)*

## 3. Cross-tree acceptance

A row that changes a component another tree/platform also renders carries that
tree's rules (permissions, recording guards, touch targets) in its acceptance.
*(Reusing a desktop list on mobile dropped its guards — 6 blockers.)*

## 4. Everywhere-decisions get a sweep row

"One style everywhere", "rename X": a row whose acceptance is a grep count
(`0 imports of OldToggle`).

## 5. Never temporarily unreachable

No row removes an entry point before its replacement lands in the same or an
earlier row.

## 6. Conflict map (in the PR table)

Files touched per row; shared handlers (e.g. a hotkey table with a "shared
handler" column); resolution = serialize or name who resolves. Add tests that
shortcuts do not fire mid-recording, in text fields, or in menus.

## 7. Blast radius of shared modules

A shared component gaining a side-effect import (DB client, env, heavy library):
list every test that renders it, or lazy-load. *(Broke unrelated tests 3 times.)*

## 8. Order, owners, access

- Merge and deploy order across repos ("API deploys before the site, or it lists 0 items").
- Schema and app code that deploy by different paths never share a row: schema
  row → confirm it is applied → code row. *(The rule was written in the plan and
  one row still bundled a migration with UI code.)*
- Scope added in review joins the phase it belongs to but stays **off the critical
  path** of what the requester is waiting for, unless that thing depends on it.
  *(An admin panel and its tests were first placed in front of the launch they had
  nothing to do with.)*
- Who reviews and who merges each row (probe branch protection first).
- Lifecycle column filled for each entity (create / update / move / delete / rotate).
- Any row that grants access (DB grant, row policy, token scope, public endpoint)
  carries a threat line — see `plan-acceptance-gates/non-ui-gates.md` §4.
- Any dispatcher (router, plugin list, cron, DI container, pack root) names the
  new member in the same row; a listing test is the acceptance. Listing is not wiring.

## 9. Audit the chained tip before merging

Check out all rows chained together; run the coverage matrix and the full suite
on that tip **before** merging the stack.
