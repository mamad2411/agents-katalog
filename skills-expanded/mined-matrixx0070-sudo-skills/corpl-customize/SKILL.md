---
name: corpl-customize
version: 1.0.0
description: Adapt the corporate-legal skill set to a specific firm, deal, or jurisdiction — house style, templates, thresholds, and escalation routing.
author: matrixx0070
tags: [corporate-legal, customization, templates, house-style, configuration, escalation]
capabilities: []
---

## When to use

Use this once, at the start of working with a new firm, legal team, or recurring deal type, to tune how the other corpl- skills behave: which templates and clause libraries to follow, what materiality thresholds apply, house drafting conventions, and who the escalation attorney is. It makes downstream output match the team's standards instead of generic defaults.

**Not for:** running an actual matter (use the specific corpl- skill after customizing); overriding the attorney-escalation gate — customization can tighten it but never remove it; inventing legal positions. This skill records preferences and routing; it does not make legal judgments.

## Method

1. **Capture house style.** Preferred defined-term conventions, resolution phrasing, minute detail level, date/number formatting, and any firm template set to mirror.
2. **Set materiality thresholds.** Dollar and term thresholds for "material" contracts, disclosure-schedule inclusion, and diligence-issue severity — these vary by deal size and must be explicit.
3. **Record jurisdiction defaults.** Entity home state(s), governing-law preferences, and which local formalities apply (e.g., DGCL for Delaware corporations).
4. **Define the escalation routing.** *Decision point:* name the supervising attorney(s) and the categories that always escalate (conflicts, privilege, novel questions, conflicted-director votes, anything sent externally). The gate is mandatory; customization only sets who and what triggers it.
5. **List available templates and clause libraries** the team wants used, and any prohibited language.
6. **Record confidentiality/privilege defaults** — labeling conventions and distribution limits.
7. **Write the profile once, confirm with the team, and reference it from each matter.**

## Example

Profile for a mid-market PE fund's outside counsel: house style mirrors the firm's DE merger template; materiality threshold $250K contract value or any change-of-control clause; jurisdiction default Delaware (DGCL); escalation attorney = deal partner, always-escalate = conflicts, financial-assistance questions, and any counterparty-facing document; templates = firm forms F-3/F-7; all diligence work product labeled "Privileged & Confidential — Attorney Work Product."

## Pitfalls

- **Leaving thresholds implicit.** "Material" means nothing until a number and criteria are set.
- **Customizing away the gate.** You may make escalation stricter, never looser or absent.
- **A profile no one confirmed.** Guessed house style produces confidently wrong drafts.
- **Stale profiles.** Deal size, jurisdiction, and personnel change — re-confirm per engagement.

## Output format

```
CORPL PROFILE — <firm / team / deal type>
House style: defined terms / resolution phrasing / minute detail / formatting / template set
Materiality thresholds: $<amount> | criteria: <...>
Jurisdiction defaults: entity state(s) / governing law / local formalities
Escalation routing: attorney = <name> | always-escalate categories = <...>
Templates & clause libraries: <...> | prohibited language: <...>
Confidentiality defaults: labeling / distribution limits
Confirmed by: <name> — <date>
```

## Reference

Customization tunes the shared corpl- conventions: house style, materiality thresholds, jurisdiction defaults, template libraries, and escalation routing. The attorney-escalation gate is a fixed floor — profiles may add always-escalate categories but may never disable review or external send-off approval. Store the profile with the matter workspace and re-confirm it whenever the firm, deal type, or supervising attorney changes.
