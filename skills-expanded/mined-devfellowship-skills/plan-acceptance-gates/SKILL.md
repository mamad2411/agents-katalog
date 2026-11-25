---
name: plan-acceptance-gates
description: "Use when writing the acceptance criteria, rollout and risk sections of a large plan, and as the checklist a reviewer attacks a finished draft with. Turns every prose promise into a gate that can fail on its own — checks on the running build, a viewport × input × content matrix, a default-path and flag-exit rule, shared-state isolation, the human who must see each output, measured limits, test hygiene and real-device proof. Pipelines, webhooks and integrations use non-ui-gates.md. Skip only for a pure refactor with no user-visible output, no flag, no limit and no shared state."
author: SamuelStefano
tags: [planning, acceptance-criteria, testing, rollout, mobile, responsive]
---

# Acceptance gates that fire

**Core principle:** in the source cases, code rules with a test survived; prose
rules, human ceremonies and isolation claims did not. If a criterion cannot fail
on its own, it is a wish. Give each one a place where it fails: a test, a CI job,
a screenshot a named person approves, or a PR row.

Non-UI plans (jobs, webhooks, notifications, data, integrations): also `non-ui-gates.md`.

## 1. Done = observed running

Each phase's acceptance includes:
- UI: the **production build** opened in a real browser, **zero console errors**,
  a screenshot per band, on the tree real users get by default.
- Pipeline: a row or log line with a correlation id, on the **production route**,
  triggered once by the named human, and read at the real destination — never a
  log that says "success".

*(Unit tests and build were green while the live canvas was blank: the layout
library crashed only in the production bundle.)*

Every acceptance names the **account and the access path** used to observe it. An
access nobody has confirmed is a human gate with a name and a date, not a line of
the criterion. *(A criterion required a login that was "not in the vault"; the
accounts and their secrets had existed for two months.)*

## 2. Default path and flags

State **what a fresh user with empty storage sees, now and after each phase.**
Every flag, opt-in, `?param`, second tree or internal fallback ("if X missing,
render legacy") needs: owner · date · metric · exit criterion · **flip PR row**.
- Never build the next version on an unshipped flag.
- Every "temporary" or "test" choice (channel, board, project, config) gets an
  owner, a date and a promotion PR row; it blocks scaling to more users or repos.

*(30 PRs of a new mobile UI sat behind an opt-in flag whose removal was one
sentence; phones kept the old UI.)*

## 3. Viewport × input × content — `complex-plan/templates/MATRIX.md`

A missing row is a blocker. Also:
- Map the app's **mode-selection logic** onto the bands (a desktop window at
  390 px got the desktop grid and broke).
- **Content stress**: e.g. the header fits at 360 px with a 60-character title;
  0 items; 200 items. Say which control drops first.
- Clamp every fixed design dimension for the smallest band (a 1040×760 modal
  overflowed a 768 px laptop).
- Every default a design mock shows is checked against the persisted default in
  the data model; a mismatch is a question (a mock's 8 % safe area leaked into
  landscape exports).
- Every prose UI rule becomes an assertion per screen: touch ≥ 44 px, no overlap,
  nothing clipped, focus visible.

## 4. Shared state isolation

"Only mobile changes" lists **shared state**: DB rows and settings, stores,
service worker, manifest, CSP, global CSS/tokens, caches, flags.
- A UI surface never writes persisted settings on open or on defaults. Test:
  "open + cancel = no DB change" (a mobile sheet enabled a watermark project-wide).
- Cross-cutting invariants get one test in the **shared** layer ("an unsaved take
  is never dropped").
- A service worker is whole-origin: plan update flow, stale tabs, desktop.

## 5. The human who must see it

For every output a person consumes: **"P sees Y in place Z without being told
where"** — with the view, default filter, sort, channel and project P actually
uses, asked of P. Verify as P, or get P's confirmation. Details: `non-ui-gates.md` §1.

**New state is an output.** For every entity or state the plan introduces (a
version, a lock, a pin, a draft), name the screen where a person who operates the
product sees it **without an agent, an MCP tool or SQL** — or write "no human
surface" as a question for the decider. *(A plan versioned content across three
repos and left the versions visible only through an agent tool. The decider's
first review question was where the admin panel was.)*

## 6. Unknowns → Phase-0 measurements

Every "limit unknown / API shape unknown / duration unknown" is a spike of at
most 1 h with a yes/no branch, **before** dependent work; the number or the raw
response is pasted into the plan. Each measurement is a `0.x` PR row. No schema before the raw API response.
Check every constraint against measured durations ("deliver in 5 min" vs a
5–8 min export). *(An unmeasured upload limit failed in production.)*

## 7. Tests

- Test preservation from minute zero: removing or weakening an assertion names
  the behavior change.
- A static selector audit is not e2e; run the real suite once per UI tree.
- Map each stakeholder answer to the specs it breaks.
- e2e budget: ≤ 15 min per PR or shard; path filters include shared components;
  flake policy; settle helpers — never measure during an animation.
- A run that skips is not green. Acceptance says **zero skips in the specs this
  plan adds**, and one row owns declaring the credentials the suite needs. If the
  whole suite is already red for unrelated reasons, a row adds a way to run one
  spec, or no row can ever show green.
- Test artifacts carry sessions. A trace archive records auth headers and stored
  tokens; a search for the password does not see inside it. Turn traces off for
  uploaded reports or keep them out of the upload, and accept on a search for
  token strings, not for the password.
- Test data against shared or production backends: namespaced prefix, deleted in
  teardown, never in a consumer's queue or channel; name who sweeps leftovers.
  *(e2e specs left 38 projects in a production account.)*
- Async device/permission actions: latest wins, acquire before release, failure
  never tears down working state. Sheets/dialogs: focus enters, is trapped, returns.

## 8. Human gates are scheduled on day 1

Real-device proof, design sign-off, secrets, external manual config (OAuth
redirect URIs, DNS, allow-lists, store review), approvals: a name and a date,
scheduled first, **blocking the default flip**. Emulator tests cannot close a
device criterion. Agents run a week of PRs in a day; a gate "at the end of phase
3" never happens.
