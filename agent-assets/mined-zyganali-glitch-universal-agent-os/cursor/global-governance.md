---
description: English locale Cursor-native governance rule.
globs:
alwaysApply: false
---

# Cursor Governance Rule

This rule binds Cursor's fast editing flow to the donor hierarchy.
`GLOBAL_AGENT_OPERATING_RULES.md` and `AGENTS.md` remain higher authority; this rule does not narrow them. It makes the fast-edit behavior explicit so speed does not bypass plan discipline.

## 1) Load Order
1. `GLOBAL_AGENT_OPERATING_RULES.md`
2. `AGENTS.md`
3. `AGENT_OS_PLAN_TEMPLATE.md`
4. the active plan
5. this rule

## 2) Why Cursor Needs Distinct Discipline
Cursor is optimized for quick navigation, rapid edits, and suggestion-heavy iteration.
That convenience can tempt the agent to treat plan updates as secondary. This rule exists to prevent that drift.

## 3) Required Cursor Behavior
- start with `MODE`, scope lock, allowlist/denylist, and the active micro-phase
- in a new repo, align with the user first, then write or harden the repo-root planning template, then create the roadmap portfolio
- do not edit code before a plan exists
- preserve the single-writer rule on shared plan/config/template files
- do not claim closure outside `Plan -> Evidence -> Test`

## 4) Fast Edit, Slow Closure Rule
Editing may be fast in Cursor; closure may not be.
After each meaningful change:
- state file impact clearly
- reevaluate test and gate impact
- synchronize plan surfaces atomically

## 5) Atomic Update Rule
- update header + phase plan + backlog + request + task + gate + risk + handoff/checkpoint together
- record discovered work as tracked items
- archive completed plans in the same closure edit

## 6) Evidence and Gate Expectation
Because Cursor can make change suggestions feel deceptively finished, the agent must also state:
- which diff family changed
- which test/gate ran or must run next
- which risk remains open
- whether selftest / related-test impact exists

## 7) Triple-Sync and Release Note
If the request involves push/deploy/repo-sync, a locally successful edit is not enough.
Do not claim completion until local repo, remote target, and live release snapshots are proven aligned.

## 8) Prohibitions
- placeholder/stub/fake completion
- drift outside the allowlist
- hiding test impact
- collapsing the donor spine into a marketing summary
- default billing/auth activation
- using fast editor flow as an excuse for untracked scope expansion

## 9) Anti-Patterns
- editing first and postponing plan sync
- treating a plausible suggestion as evidence
- allowing active micro-phases to grow without control
- failing to report role/fallback structure to the user

## 10) Expected Output
Under this rule, Cursor-based agent output should make it obvious:
- what work was done
- which files were affected
- what gate/evidence status exists
- which risks remain
- what the next micro-phase is

The goal of this rule is not to restrict Cursor. It is to stop fast edits from becoming ungoverned edits.