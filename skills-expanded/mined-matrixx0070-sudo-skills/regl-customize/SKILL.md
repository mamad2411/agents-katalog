---
name: regl-customize
version: 1.0.0
description: Tune an existing regulatory-monitoring setup — adjust watchlists, cadence, digest scope, and escalation thresholds as the business and its exposure change.
author: matrixx0070
tags: [regulatory, legal, configuration, tuning, monitoring, personalization]
capabilities: []
---

## When to use

Use this when a regulatory pipeline already exists and needs adjustment: the business entered a new market, a docket went quiet, the digest is too noisy or too sparse, or escalation is firing on the wrong things. Reach for it to re-tune rather than rebuild.

**Not for:** first-time scoping (use regl-cold-start-interview), the analytical work (regl-policy-diff, regl-gap-surfacer), or one-off deadline tracking (regl-comments). Changes that alter what gets escalated to counsel must preserve the attorney-review gate — never tune it away to reduce noise.

## Method

1. Start from the current config: list active feeds, cadences, digest scope, and escalation rules before changing anything. Blind edits break coverage.
2. Identify the driver for the change: new/dropped exposure, signal-to-noise complaint, missed hit, or changed stakeholder needs. Tune to the driver, not to a hunch.
3. For coverage changes, add or retire feeds with an explicit exposure justification (add) or a confirmation the exposure is gone (retire) — never drop a feed just because it is quiet.
4. For noise changes, adjust cadence, dedup keys, or digest filters — not the escalation threshold. Reducing what reaches counsel is a safety change, not a tidiness one.
5. **Decision point:** any change that would narrow attorney escalation (fewer legal-risk items surfaced) requires explicit attorney sign-off; default is to keep the gate wide.
6. Record every change with rationale and date so the config has a history.
7. Validate after tuning: confirm a known-type hit still routes correctly before considering the change done.

## Example

> Driver: expanded to EU; digest too noisy. Changes: ADD GDPR/EDPB feed (exposure: now processing EU data). REDUCE cadence on dormant state-AG docket weekly→monthly (quiet 6 months, exposure unchanged, kept on list). TIGHTEN dedup to key on RIN (duplicate hits). Escalation threshold: UNCHANGED (kept wide). Validated: test NPRM hit still routes to regl-comments. Logged 2026-07-11.

## Pitfalls

- Retiring a "quiet" feed whose exposure still exists — silence is not safety.
- Cutting digest noise by narrowing attorney escalation instead of tuning filters.
- Editing config with no record, so coverage drifts untraceably.
- Skipping post-change validation, so a broken route ships unnoticed.

## Output format

```
CONFIG CHANGE — <setup name> | date <date>
Driver: <new exposure | noise | missed hit | stakeholder>
Changes:
  ADD/RETIRE feed: <source> — <exposure justification>
  CADENCE: <source> <old→new>
  FILTER/DEDUP: <change>
  ESCALATION: <unchanged | narrowed — attorney sign-off: name>
Validation: <known-hit route re-tested>
Rationale logged: <yes>
```

## Reference

**Rulemaking lifecycle:** tune cadence to where each agency sits in the cycle — daily on agencies with active NPRMs, sparse on those with only settled final rules and no pending dockets.

**Comment-period mechanics:** when adding exposure to an agency with an open comment window, ensure the deadline immediately flows into regl-comments and the digest; a newly added feed must not miss a closing period.

**Policy-diff method:** tuning changes inputs, not the diff logic — keep dedup keyed to docket/RIN so downstream diffs stay clean. Attorney-escalation gate: the escalation threshold is a safety control; widen it freely, but narrowing what reaches counsel requires attorney sign-off, never a noise-reduction shortcut.
