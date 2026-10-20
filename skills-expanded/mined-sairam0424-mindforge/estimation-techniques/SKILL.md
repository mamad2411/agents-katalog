---
name: estimation-techniques
version: 1.0.0
min_mindforge_version: 10.1.0
status: stable
triggers: estimation technique, story points, planning poker, reference class forecasting, cone of uncertainty, velocity projection, t-shirt sizing, three-point estimate, estimation accuracy, estimation calibration, effort estimation, time estimation
---

# Estimation Techniques

## When this skill activates

This skill activates when the team needs to estimate effort, duration, or complexity
of work items. It provides multiple estimation techniques, guidance on when to use each,
and frameworks for improving estimation accuracy over time through calibration and
reference class forecasting.

## Mandatory actions when this skill is active

### Before

1. **Clarify what is being estimated** — Effort (person-days), duration (calendar time),
   complexity (relative sizing), or cost (dollars)? These are different things.
2. **Identify the audience** — Who needs this estimate and what decision will it inform?
   (Sprint planning vs. budget approval vs. roadmap planning require different precision.)
3. **Gather reference data** — Pull historical velocity, past estimates vs. actuals for
   similar work, and team availability for the period.

### During

4. **Select appropriate technique based on context:**

   - **Story Points (relative sizing):**
     Compare work items to known reference stories. "Is this bigger or smaller than
     the login feature we built last sprint?" Use Fibonacci sequence (1, 2, 3, 5, 8, 13)
     to force recognition that large items have more uncertainty.
     Best for: Sprint planning, backlog prioritization.

   - **Planning Poker:**
     Each estimator independently selects a card. Reveal simultaneously. If estimates
     diverge by >2x, the highest and lowest explain their reasoning. Re-estimate.
     Convergence indicates shared understanding. Divergence reveals hidden complexity
     or misunderstanding. Best for: Team alignment on scope understanding.

   - **Three-Point Estimate:**
     Optimistic (O) + Most Likely (M) + Pessimistic (P).
     Weighted average: (O + 4M + P) / 6.
     Standard deviation: (P - O) / 6.
     Present as range, not single number. Best for: Executive communication,
     project planning with uncertainty bounds.

   - **T-Shirt Sizing (S / M / L / XL):**
     Rough relative sizing for large backlogs. Fast, low-ceremony. Good for roadmap-
     level planning where precision is not needed. Convert to approximate days only
     when pressed (S=1-2d, M=3-5d, L=1-2w, XL=3-4w — calibrate to your team).
     Best for: Roadmap planning, early-stage estimation.

   - **Reference Class Forecasting:**
     Do NOT ask "how long do I think this will take?"
     Instead ask "how long did SIMILAR work actually take in the past?"
     Search for completed work of similar scope, technology, and team composition.
     Use the actual duration distribution as the forecast basis.
     Best for: Overcoming optimism bias, project-level estimates.

5. **Apply the Cone of Uncertainty:**
   - Initial concept: estimate accuracy is 4x (could be 4x longer or 0.25x shorter)
   - After requirements: 2x range
   - After detailed design: 1.5x range
   - After implementation started: 1.25x range
   - Communicate which stage you are at and the corresponding uncertainty range.
   - Never present early-stage estimates as precise numbers.

6. **Velocity-based projection:**
   - Average velocity over last 3-5 sprints (discard outliers)
   - Remaining story points / average velocity = estimated sprints remaining
   - Present as range: (remaining / max velocity) to (remaining / min velocity)
   - Account for known disruptions (holidays, planned absences, onboarding)

7. **Common estimation pitfalls to avoid:**
   - Anchoring — First number mentioned biases all subsequent estimates
   - Planning fallacy — People consistently underestimate (use reference class data)
   - Scope creep — Estimate what is defined NOW, flag unknowns separately
   - Precision theater — "14.5 days" implies false precision; use ranges
   - Forgetting overhead — Testing, code review, deployment, documentation are work too
   - Hero assumptions — Estimate for average team member, not the fastest

8. **Calibration practices:**
   - Track estimate vs. actual for every completed item
   - Review accuracy quarterly — are you consistently over or under?
   - Adjust multiplier based on historical bias (if you are consistently 1.5x under,
     multiply estimates by 1.5)
   - Share calibration data with the team to build collective estimation skill

### After

9. **Record the estimate with context** — Document: what was estimated, technique used,
   assumptions made, uncertainty range, and who participated.
10. **Track actuals** — When work completes, record actual effort/duration alongside the
    estimate for future calibration.
11. **Retrospect on accuracy** — Periodically review estimation accuracy trends. Celebrate
    improvement in calibration, investigate systematic biases.

## Self-check before task completion

- [ ] Estimation technique selected intentionally (not just defaulting to one)
- [ ] Estimate presented as range, not single number
- [ ] Cone of uncertainty stage identified and communicated
- [ ] Reference class data consulted where available
- [ ] Common pitfalls actively guarded against (especially anchoring and planning fallacy)
- [ ] Assumptions and unknowns documented alongside the estimate
- [ ] Overhead included (testing, review, deployment, documentation)
- [ ] Historical calibration data referenced if available
- [ ] Tracking mechanism in place to compare estimate vs. actual
