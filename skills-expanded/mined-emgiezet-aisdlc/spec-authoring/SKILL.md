---
name: spec-authoring
description: >
  Write specs that are fuel for agents rather than documents for humans — a fixed section
  layout with stable, testable UC ids that drive implementation, tests, and QA. Use when
  writing or reviewing a spec in specs/<TICKET>/spec.md, turning a ticket or a written request into
  acceptance criteria an agent can execute unattended, deciding whether a spec is ready to
  queue, or splitting an oversized spec.
---

# Spec Authoring

A spec in `specs/<TICKET>/spec.md` is the input to `/sdlc:implement`, `/sdlc:qa`, and the
`aisdlc` queue. Nobody reviews the plan mid-run — approving the spec *is* the approval, so
whatever the spec fails to say, the agent will invent.

Human-facing planning belongs elsewhere: decomposition of a vague ticket, design discussion,
the narrative of why. A spec is narrower — a contract with observable acceptance criteria, sized
for one unattended run and one pull request.

## Format

Fixed sections, in this order. Template: [`references/spec-template.md`](references/spec-template.md).

```yaml
---
ticket: ABC-123
title: Expose an account's balance to its owner
status: draft          # draft → approved (a human sets approved; the queue refuses drafts)
stacks: [backend]
---
```

1. **Problem** — 2–4 sentences: what is broken or missing, and for whom, in the product's own
   vocabulary (if the project has a glossary skill, use its terms). No solution.
2. **Scope** — `In:` and `Out:` bullet lists. `Out:` is the load-bearing one; it is how you
   stop an agent from redesigning an adjacent module.
3. **Context** — file and symbol references into the repo, the contract operation ids, and the
   recorded decisions that constrain this change. Point at code; never describe code in prose.
   `.claude/sdlc.md` says whether this project has a contract directory or ADRs at all — omit
   what does not exist rather than inventing a path.
4. **Acceptance criteria (UC table)** — the heart of the spec, see below.
5. **Non-functional** — only constraints that change the implementation: latency budget,
   transaction boundaries, idempotency, tenancy isolation, audit requirements, numeric precision.
   Omit the section rather than filling it with "should be fast".
6. **Open questions** — anything unresolved. **A spec with open questions cannot be
   `approved`.** Resolve them or move them to `Out:`.

## The UC table

| id | actor | action | expected observable result | test |
|----|-------|--------|----------------------------|------|
| UC-1 | account owner | `GET /v1/accounts/a-1001/balance` | 200, `balance` is an integer in minor units, `currency` present | integration |
| UC-2 | account owner | `GET /v1/accounts/unknown/balance` | 404, shared error envelope with code `account_not_found`, no other field | unit |
| UC-3 | other user | requests an account they do not own | 403, nothing about the account leaks into the body | unit |

Rules:

- **Atomic.** One actor, one action, one result. "Creates and notifies and audits" is three rows.
- **Observable.** The result is something a test can read: status code, database row, rendered
  text, emitted event, log entry. "Handles the case correctly" is not a result.
- **Stable ids.** `UC-<n>` ids are referenced from test names, `qa-report.md`, and PR
  comments. Append new ones; never renumber, never reuse a retired id.
- **Negative cases are first-class.** Every validation rule and permission boundary that
  matters gets its own UC. A spec of only happy paths produces an implementation of only
  happy paths.
- **`test` column is the tier, and a floor not a cap** — `unit` (default: in-process, fakes, no
  socket or database), `integration` (a persisted row, migration, transaction boundary or
  contract is the thing being proven), `e2e` (a flow named under `Critical journeys:` in
  `.claude/sdlc.md`; at most one per spec when that is `none`). Pick the lowest tier that can
  observe the stated result — `dense-testing`'s `references/test-tiers.md` has the decision list.
  `dense-testing` defines how many more tests the change needs beyond one per UC.

## Sizing

One spec is one queue task is one pull request. The plan may be as large as the problem; the
pull request may not — a slice a reviewer cannot hold is a slice that gets approved unread.

**Split when any of these is true**, before writing the spec rather than after the branch grew:

| Signal | Threshold | Why |
|---|---|---|
| Use cases | > ~8 | more than one reviewable outcome |
| Stacks | > 2 | two review audiences, two CI matrices |
| Added lines (estimate) | > the repo's `Added lines` budget (default 400) | defect finding degrades past ~400 reviewed lines (SmartBear/Cisco) |
| Files | > the `Files` budget (default 15) | review attention falls ~8.7% per extra file; latent-bug risk is lowest near 10 (arXiv 2609.22610, 330k PRs) |
| Modules (first two path segments) | > the `Modules` budget (default 3) | cross-subsystem co-changes are the defect-prone ones (D'Ambros 2009) — a design signal, not a size one |
| Fan-out | many modules, few lines each | shotgun surgery: extract the seam as its own slice, then move one caller group per slice |
| Ordering | a row that cannot be tested until another row ships | that row belongs to a later slice |

Estimate honestly: paths named in `## Context` plus their call sites, compared with the three
most similar past commits (`git log -- <dir>`, then `git show --numstat`). Record the result as
a `Change budget:` line under `## Scope`; `scope-check` enforces it on the branch and the queue
stops before ship past the repo's hard ceiling (default 3000 added lines).

**Split into `specs/<TICKET>-a/`, `-b/`, …** — walking skeleton first, each independently
shippable, each keeping the product working. `/sdlc:decompose` does this mechanically, picks
the seam, and preserves UC ids across slices; `/sdlc:spec` calls it when its own estimate is
over budget. A mechanical codemod is always its own slice with its own wider budget: a rename
across 200 files is reviewable by pattern, the same rename mixed with logic is not.

## Anti-patterns

| Smell | Why it breaks unattended runs |
|-------|-------------------------------|
| Prose paragraphs describing behaviour | The agent cannot tell requirement from background; it satisfies the sentence it noticed |
| UC without an observable result | Nothing to assert, so the agent writes a test that asserts its own implementation |
| Describing existing code instead of linking it | Drifts silently, and the description is what the agent trusts |
| Renumbered UC ids | Breaks the test-name and QA-report traceability chain |
| `status: approved` with open questions | The agent invents the answers, in the worst plausible way |
| Implementation instructions in the spec | Freezes an approach the code may have outgrown; state the *result*, let the playbook pick the how |

## Review checklist

- [ ] Every UC atomic, with a result a test can read
- [ ] Negative and authorization cases present, not just happy paths
- [ ] `Out:` scope lists the adjacent things not to touch
- [ ] Context points at files and contract operations, not prose descriptions
- [ ] No open questions left when flipping to `approved`
- [ ] ≤ 8 UCs, ≤ 2 stacks, and an estimate inside the change budget — or split
- [ ] `Change budget:` line present under `## Scope`
- [ ] UC ids stable versus the previous revision
