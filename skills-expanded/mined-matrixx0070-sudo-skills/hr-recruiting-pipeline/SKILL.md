---
name: hr-recruiting-pipeline
version: 1.0.0
description: Track a recruiting funnel across stages with conversion metrics, bottleneck diagnosis, and a next action for every candidate.
author: matrixx0070
tags: [recruiting, pipeline, ats, funnel-metrics, talent-acquisition, time-to-fill]
capabilities: []
---

## When to use

Reach for this when managing candidates through a hiring funnel, running a pipeline review with a hiring manager, or diagnosing why a req is stalling. Keep the pipeline current, surface bottlenecks, and drive every candidate to a clear next step.

**Not for:** designing the interview loop or scorecards (use hr-interview-prep), writing the offer (use hr-draft-offer), or headcount planning (use hr-org-planning).

## Method

1. **Define stages** — sourced → applied → screen → hiring-manager → onsite/loop → offer → accepted. Confirm entry/exit criteria per stage so status is unambiguous.
2. **Inventory candidates** — list each with current stage, days-in-stage, owner, and next action with a date. Decision point: flag anyone past your stage SLA as at-risk.
3. **Compute funnel health** — stage-to-stage conversion, time-in-stage, and time-to-fill vs. target; compare to benchmark or prior reqs.
4. **Diagnose bottlenecks** — find the stage with worst conversion or longest dwell and name the likely cause (weak top-of-funnel, slow feedback, offer declines). Decision point: a top-of-funnel volume problem and a mid-funnel conversion problem need opposite fixes — don't source more into a stage that's already leaking.
5. **Assign actions** — for every active candidate and every bottleneck, specify owner, action, and due date. Chase pending scorecards and interviewer feedback.
6. **Report status** — pipeline coverage vs. hiring goal (enough candidates to hit the number), risks, and decisions the hiring manager owes you.

## Example

Req: 2× Backend Eng, target time-to-fill 45 days (day 38). Funnel: 60 sourced → 18 screens → 6 HM → 3 onsite → 1 offer. Screen→HM converts 33% (healthy); HM→onsite drops to 50% but the real leak is onsite→offer at 33% with 9-day average dwell — interviewers are late on scorecards. Diagnosis: mid-funnel feedback lag, not top-of-funnel volume. Actions: chase 2 outstanding scorecards (owner: recruiter, due tomorrow); HM to decide on candidate #4 by Friday. Coverage: 3 in loop for 2 seats — thin; add one sourcing pass as insurance.

## Pitfalls

- Stale stages — a candidate marked "onsite" who was actually rejected a week ago, hiding the true leak.
- Sourcing more candidates to fix a mid-funnel conversion problem (pouring into a leaking bucket).
- Tracking activity (calls made) instead of conversion and time-in-stage.
- Candidates with no dated next action — the pipeline silently goes cold.

## Output format

```
Pipeline snapshot: candidate | stage | days-in-stage | owner | next action + date
Funnel metrics: per-stage conversion | time-in-stage | time-to-fill vs target
Bottleneck: stage + likely cause
Action list: owner → action → due
Coverage vs goal + decisions needed from HM
```

## Reference

### Stage definitions (entry / exit criteria)

Unambiguous stage gates are what make funnel math trustworthy. A candidate is *in* a stage only when the entry criterion is met and *out* when the exit criterion fires.

| Stage | Enters when | Exits when |
|---|---|---|
| **Sourced** | Recruiter identifies and contacts a passive candidate | Candidate replies with interest (→ Screen) or declines |
| **Applied** | Candidate submits an application | Recruiter reviews against must-haves |
| **Recruiter screen** | Application/interest passes resume review | 20–30 min call confirms basics: interest, comp range, timing, work auth, top must-haves |
| **Hiring-manager screen** | Passes recruiter screen | HM confirms role fit and wants to invest a full loop |
| **Onsite / loop** | HM screen positive | Full panel completes; scorecards submitted |
| **Offer** | Loop debrief = hire decision | Offer extended and verbally accepted |
| **Accepted / hired** | Written offer signed | Start date confirmed; → onboarding |

Also track terminal states explicitly: **rejected** (with reason code) and **withdrew** (candidate-initiated), by stage, so you can see *where* and *why* you lose people.

### Conversion benchmarks

Typical stage-to-stage pass rates for a professional/technical req. Treat as directional reference, not targets — they vary widely by role scarcity, employer brand, and market.

| Transition | Healthy range | Reading |
|---|---|---|
| Sourced → responded | 20–40% | Below → weak outreach/targeting or brand |
| Applied → recruiter screen | 15–30% | Below → job post attracting wrong profile |
| Recruiter screen → HM screen | 40–60% | Below → recruiter mis-calibrated to the bar |
| HM screen → onsite | 50–70% | Below → HM and recruiter not aligned on the profile |
| Onsite → offer | 30–50% | Below → loop too hard, or candidates under-qualified |
| Offer → accept | 70–90% | Below → comp/level/experience or slow process |

**Overall applied→hire** often lands around **1–3%** (roughly 1 hire per 40–100 qualified applicants); senior/scarce roles are far tighter. **Sourced→hire** for outbound is typically **1–2%**, so pipeline coverage must be sized accordingly.

### Coverage math

To fill N seats, work backwards through your conversion rates:

```
candidates needed at stage X = seats ÷ (product of conversion rates from X → hire)
```

Example — 1 seat, onsite→offer 40%, offer→accept 80%:
onsite candidates needed ≈ 1 ÷ (0.40 × 0.80) ≈ **3.1**, so keep **3–4 in the loop per open seat**. Thinner than ~2× coverage at the loop stage means one decline stalls the req. Report coverage as "N in loop for M seats" and flag when it drops below target.

### Time-to-fill and time-in-stage targets

- **Time-to-fill** = req open → offer accepted. Common targets: **~30 days** for high-volume/junior, **45–60 days** for professional/technical, **60–90+ days** for senior/executive/scarce.
- **Time-to-hire** = first candidate contact → accept (candidate-experience view; shorter than time-to-fill).
- **Time-in-stage SLAs** (chase when exceeded):
  - Application review: ≤ 2 business days
  - Recruiter screen scheduling: ≤ 3 days
  - Post-onsite scorecards + debrief: ≤ 2 days (the most common silent leak)
  - Offer approval → extension: ≤ 2 days
- **Interview-to-offer speed** matters: every extra week in-loop measurably raises decline and drop-off risk, especially for candidates running parallel processes.

### Bottleneck diagnosis: volume vs. conversion

The single most important distinction. They need **opposite** fixes:

- **Top-of-funnel volume problem** — not enough qualified candidates entering. Symptom: healthy conversion rates but too few people. Fix: more/better sourcing, revise job post, widen channels, referral push. *Do not* tighten the bar.
- **Mid-funnel conversion problem** — candidates enter but leak at a specific gate. Symptom: one transition well below benchmark and/or long dwell. Fix: the *stage*, not the top. Slow scorecards → chase feedback and set SLAs. Low HM-screen→onsite → re-align HM and recruiter on the profile. Low offer→accept → check comp, level, speed, and candidate experience.

Pouring more candidates into a leaking mid-funnel stage wastes sourcing effort and burns candidate goodwill. Always find the worst gate first, then act on *that* gate.

### Health metrics beyond conversion

- **Pipeline coverage ratio** — active candidates ÷ open seats (target ≥ 3–4× at loop).
- **Offer acceptance rate** — sustained <80% signals comp, level, or process problems.
- **Sourcing channel yield** — hires and quality-of-hire by source; referrals typically convert best.
- **Candidate NPS / drop-off rate** — experience quality; high withdrawal = process friction.
- **Diversity at each stage** — watch for a stage where representation drops sharply (a bias signal to investigate).
- **Aging reqs** — days-open vs. target; escalate reqs past SLA.

### Review-cadence checklist

Run a weekly pipeline review per active req: (1) every candidate has a dated next action and owner; (2) anyone past a stage SLA is flagged at-risk; (3) the worst-converting stage is named with a diagnosis (volume vs. conversion); (4) coverage vs. goal is stated; (5) decisions the HM owes you are listed with due dates. Stale stages (a "rejected" candidate still marked "onsite") corrupt every downstream number — reconcile status before computing the funnel.
