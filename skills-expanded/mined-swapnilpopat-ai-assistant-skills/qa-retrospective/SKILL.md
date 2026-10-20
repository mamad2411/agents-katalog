---
name: qa-retrospective
description: Run a focused QA retro — defect leakage, flake budget, test debt, on-call pain — with concrete actions and accountable owners. Use after each release, incident, or sprint.
source: self
date_added: 2026-05-01
---

# QA Retrospective

A QA retro is a structured look at how the team produced (or failed to produce) trustworthy quality signal. It produces ≤ 3 owned actions, not a list of complaints.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Cadence | After each release + monthly + post-incident |
| Format | 60–75 min, time-boxed; remote-first w/ Miro/FigJam or Markdown |
| Inputs | Release dashboard, defect leakage, flake rate, MTTR, on-call diary, customer tickets |
| Output | ≤ 3 actions w/ owners + due dates + measurable goals |
| Tracking | Action register reviewed at next retro; closed-loop or de-prioritized with rationale |

## When to Use

- After every release (lightweight 30 min if uneventful).
- After any sev-1/2 incident (post-incident specific).
- Monthly cross-team to surface patterns across releases.
- After a milestone (launch, migration, framework upgrade).

## Inputs to Gather (24h ahead)

- Defect leakage to prod (count + severity)
- Flake rate per suite, top offenders
- CI duration trend (per suite, per PR p95)
- MTTR for last N defects discovered post-merge
- On-call pages count and themes
- Customer-reported issues (from support / Sentry / NPS)
- Test coverage / mutation score deltas
- People signals: surveys, anonymous comments

## Format (75 min)

1. **Frame (5 min)** — goal, scope, ground rules ("focus on signals/systems, not people").
2. **Data review (10 min)** — share the dashboard; everyone in observe mode.
3. **Generate (15 min, silent)** — sticky notes in 4 columns:
   - What worked
   - What hurt
   - What surprised
   - What we should try
4. **Cluster + Vote (10 min)** — group themes; dot-vote top 3.
5. **Discuss (20 min)** — for each top theme: ask "5 whys" or run a quick fishbone.
6. **Decide (10 min)** — exactly 1–3 actions, each with **owner**, **due date**, **measurable outcome**.
7. **Close (5 min)** — review prior actions; commit to bring action register to next retro.

## Action Quality Bar

A retro action is acceptable when **all** are true:

- An owner is named (not "the team").
- A measurable outcome is defined ("flake rate from 1.4% → ≤ 0.8%").
- A due date is set.
- It fits in the agreed maintenance budget.
- It's tracked publicly.

Reject actions that are aspirational ("be more careful").

## Worked Example

```
QA Retro — release 2026.18 (orders-api v3.14)
Inputs:
  Defects in prod (S1–S2):  2 (1 duplicate-charge, 1 tax-fallback)
  Flake rate this release:  1.6% (target 1.0%)
  CI suite p95:             11m (target 10m)
  Customer tickets:         12 (3 directly tied to leakage)
  On-call pages:            4 (2 redirected to perf)

Themes (after cluster + vote):
  1. Idempotency tests missing for new POST routes (linked to leakage #1)
  2. Test data builders inconsistent across services (linked to flake)
  3. Pre-launch bug bash skipped for time

Actions (3):
  [ ] Add idempotency contract tests for all POSTs in orders-api
      Owner: @sam  Due: 2026-05-15  Goal: 100% POSTs covered
  [ ] Centralize test-data builders (factories pkg) + migrate top 2 services
      Owner: @alex Due: 2026-05-22  Goal: flake on those suites < 0.5%
  [ ] Bug-bash gate enforced via release checklist
      Owner: @priya Due: 2026-05-04  Goal: 0 missed bashes next 3 releases

Prior actions review: 2/3 closed; 1 carried forward (with new ETA).
```

## Anti-patterns to Watch

- "Action: discuss in another meeting" — that's not an action.
- Action backlog ignored from one retro to the next — kills the practice.
- Retro becomes blame session — refocus on systems and signals.
- All actions about "more tests" — sometimes the answer is fewer/better tests.
- Single voice dominates — use silent generation and dot voting.

## Output Format

```
QA Retro — <release/sprint> — <date>
Attendees: <names>
Inputs:
  ...metrics...
Themes (top 3 by votes):
  1. ...
  2. ...
  3. ...
Actions (max 3):
  - <verb + outcome> | Owner: <name> | Due: <date> | Goal: <measurable>
Prior actions:
  - <name>: <closed | carried | dropped + reason>
Next retro: <date>
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Long agenda, no decisions | Time-box; ≤ 3 actions; reject vagueness |
| No data | Bring real metrics; opinions without data are noise |
| Same actions every time | Root-cause via 5 whys / fishbone, not symptoms |
| Actions die after the meeting | Public action register; reviewed first thing next retro |
| Blame-y tone | Norm: signals & systems, not people |
| Optional attendance | Treat as mandatory for engineering + QA leads |

## References

- *Agile Retrospectives* — Derby & Larsen
- Google SRE Workbook — Postmortem culture (template applicable)
- Atlassian retrospective templates
- *The Five Dysfunctions of a Team* — Lencioni
