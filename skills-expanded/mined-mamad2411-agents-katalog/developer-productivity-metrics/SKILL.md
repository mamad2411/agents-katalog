---
name: developer-productivity-metrics
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: developer productivity metrics, DORA metrics implementation, developer experience survey, flow metric, cognitive load measurement, engineering effectiveness, developer satisfaction, deployment frequency, lead time metric, change failure rate, developer velocity, engineering metric dashboard
---

# Skill — Developer Productivity Metrics

## When this skill activates

This skill activates when the user is designing or implementing developer productivity measurement systems. This includes DORA metrics (deployment frequency, lead time, change failure rate, MTTR), developer experience surveys, flow metrics, cognitive load measurement, engineering effectiveness tracking, developer satisfaction scoring, velocity metrics, and engineering metric dashboards.

## Mandatory actions when this skill is active

### Before writing any code

1. Identify the goal of measurement: improve developer experience, justify platform investment, identify bottlenecks, or benchmark against industry.
2. Survey developers to understand perceived friction points before instrumenting metrics (avoid measuring the wrong thing).
3. Establish a baseline for each metric category (DORA, flow, satisfaction) to track improvement over time.
4. Define metric ownership: who monitors, who acts on findings, and what decision-making authority they have.
5. Commit to "metrics for improvement, not punishment" — avoid individual developer tracking or performance reviews based on these metrics.

### During implementation

- **DORA Metrics (Four Keys):**
  - **Deployment Frequency:** Count deployments to production per day/week. Elite: multiple per day. High: once per day to once per week.
  - **Lead Time for Changes:** Time from commit to production deploy. Elite: under 1 hour. High: under 1 day.
  - **Change Failure Rate:** Percentage of deployments causing incidents. Elite: 0-15%. High: 16-30%.
  - **Mean Time to Restore (MTTR):** Time from incident detection to resolution. Elite: under 1 hour. High: under 1 day.
- **Flow Metrics (SPACE Framework):**
  - **Satisfaction:** Developer experience survey (quarterly, 10-15 questions, NPS score). Track: tooling satisfaction, cognitive load, collaboration quality.
  - **Performance:** DORA metrics + throughput (PRs merged, features shipped per sprint).
  - **Activity:** Commits, PRs, code reviews. Use as context, not performance indicator.
  - **Communication:** PR review time, unblocking time, documentation quality.
  - **Efficiency:** Time in flow state (4+ hours uninterrupted), meeting load, context switches per day.
- **Cognitive Load Measurement:** Survey-based (scale 1-10): "How many systems do you need to understand to complete typical tasks?" "How often do you context switch?" "How easy is it to find information?"
- **Engineering Effectiveness Dashboard:** Single dashboard showing DORA metrics, flow metrics, developer satisfaction, and trend lines. Refresh daily. Include comparisons to industry benchmarks (DORA State of DevOps Report).
- **Avoid Vanity Metrics:** Lines of code written, commits per day, hours logged. These measure activity, not impact. Focus on outcomes (features shipped, incidents prevented, time saved).
- **Privacy Guardrails:** Aggregate metrics at team level (minimum 5 developers). Never track individual developer productivity. Anonymize survey responses.

### After implementation

- Verify DORA metrics are auto-collected from CI/CD pipelines and incident management systems (no manual entry).
- Confirm developer experience surveys run quarterly with at least 70% response rate.
- Validate that engineering effectiveness dashboard refreshes daily and includes trend lines.
- Ensure metrics are reviewed in team retrospectives with action items to address bottlenecks.
- Check that metrics are never used for individual performance reviews (enforce via policy).

## Self-check before task completion

- [ ] DORA four keys are auto-collected and tracked (deployment frequency, lead time, change failure rate, MTTR).
- [ ] Developer experience survey runs quarterly with 70%+ response rate.
- [ ] Flow metrics cover satisfaction, performance, activity, communication, and efficiency.
- [ ] Cognitive load is measured via survey and tracked over time.
- [ ] Engineering effectiveness dashboard refreshes daily and shows trend lines.
- [ ] Metrics are aggregated at team level (minimum 5 developers) to protect individual privacy.
- [ ] Metrics are reviewed in retrospectives with action items to improve developer experience.
