---
name: design-state-interaction-spec
description: Use when approved behaviour needs a requirement-linked, state-complete, accessible interaction contract.
---

# Specify states and interaction

## Inputs
Applicable requirements, current journey, project components, and platform, accessibility, responsive, localisation, content, and motion constraints.

## Procedure
1. Give each visible requirement a stable ID. Enumerate entry, loading, empty, confirmation, pending, success, invalid, permission refusal, conflict, partial failure, unknown outcome, offline, recovery, cancellation, and repeated-action states; justify every material exclusion.
2. Record each state's entry condition, visible outcome, enabled/disabled/hidden actions with reasons, transitions, persistence expectation, and requirement links.
3. Exercise repeated activation, navigation while pending, delayed responses, stale data, and results arriving after the view changes.
4. Specify heading/body/control/status copy, destructive safeguards, and recovery; route policy-bearing copy to Product.
5. Specify initial/resulting focus, focus order and restoration, keyboard activation, escape/cancel behaviour, and trap prevention.
6. Specify announcements, urgency, deduplication, and when silence is correct.
7. Record responsive, localisation, and reduced-motion implications without fabricating visual approval.

## Output
A requirement coverage matrix, state/transition catalogue, content and action table, focus/keyboard contract, announcement plan, recovery rules, and policy-gap register.

## Stop condition
Stop when policy controls a state or disclosure, or an applicable state lacks an observable outcome, action rule, focus/keyboard treatment, announcement decision, or recovery path.
