---
name: mkt-email-sequence
version: 1.0.0
description: Design a multi-email nurture or lifecycle sequence with copy, timing, branching logic, exit conditions, and directional benchmarks.
author: matrixx0070
tags: [marketing, email, lifecycle, automation, nurture, drip]
capabilities: []
---

## When to use

Use this when you need more than one email — an onboarding, nurture, re-engagement, or promotional sequence where timing, order, and branching decide whether it converts.

**Not for:** a single broadcast or one-off email (use mkt-draft-content), or reporting on a sequence that already ran (use mkt-performance-report).

## Method

1. Define the sequence goal, the enrollment trigger (signup, download, cart abandon, inactivity), and the target conversion event.
2. Map the contact's state at entry and the belief or action that must change by exit.
3. Plan the arc. Decide how many emails and give each one job (welcome, educate, prove, handle objection, offer, urgency). Decision point: do not ask for the sale before trust exists — earlier emails give, later ones ask.
4. Write each email: subject plus alternate, preview text, concise body, one primary CTA.
5. Set timing. Assign delays between steps; keep cadence tighter early, looser later.
6. Add branching: define behavior paths (opened/clicked vs. not, converted vs. not) and what changes on each.
7. Define exit conditions (converted, unsubscribed, hard bounce, goal met) so no one gets irrelevant mail.
8. Attach directional benchmarks so results can be judged.

## Example

Trigger: free-trial signup, goal = paid conversion, 4 emails. E1 (0h) welcome + first quick win. E2 (day 2) show the "aha" feature. E3 (day 5) case-study proof + objection handling. E4 (day 7) offer + urgency. Branch: if E2 clicked but no activation, insert a "stuck? here's how" email; if converted, exit immediately.

## Pitfalls

- Pitching in email one before any value or trust is established.
- Uniform delays that ignore the contact's momentum — space by behavior, not a fixed drip.
- No exit conditions, so converted or unsubscribed users keep receiving the sequence.
- Presenting benchmark ranges as promises; label them directional estimates.

## Output format

```
Sequence: <name> | Goal | Trigger | Target event

Overview:
| # | Purpose | Delay | Subject | CTA |

Full copy (per email):
E<#>: subject + alt / preview / body / CTA

Branching: <condition → path>
Exit conditions: <...>
Benchmarks (directional): open % / click % / conversion %
```
