---
name: technical-leadership
version: 1.0.0
min_mindforge_version: 10.3.0
status: stable
triggers: technical leadership, engineering management decision, team velocity improvement, technical vision setting, architecture governance, tech lead responsibilities, engineering culture, technical strategy, staff engineer guidance, principal engineer, tech leadership transition, engineering org design
---

# Technical Leadership

## When this skill activates

This skill activates when making engineering management decisions, setting technical vision for a team or organization, governing architectural standards, improving team velocity, or transitioning into technical leadership roles. It applies to tech leads, staff engineers, principal engineers, and engineering managers responsible for technical direction and team performance.

## Mandatory actions when this skill is active

### Before making any leadership decision

1. **Establish decision context** — Identify stakeholders, time horizon (tactical vs strategic), reversibility (one-way door vs two-way door), and blast radius. High-stakes irreversible decisions require more scrutiny than low-stakes experiments.
2. **Gather signal, not noise** — Talk to engineers who have touched the code recently, not those with opinions but no context. Review metrics (deploy frequency, MTTR, cycle time) before making velocity assessments.
3. **Write down your reasoning** — Document the problem, alternatives considered, tradeoffs, and decision rationale. Leadership decisions without artifacts create organizational amnesia.
4. **Identify your biases** — Are you anchoring on past experience? Optimizing for your personal preferences? Overweighting recency? Name the bias before it distorts the decision.

### During technical leadership activities

#### Vision & Strategy

- **Set technical vision in layers** — Near-term (3-6 months): concrete projects with clear outcomes. Mid-term (6-18 months): architectural bets and platform investments. Long-term (18-36 months): directional hypotheses, not detailed plans.
- **Make the implicit explicit** — Document coding standards, architecture principles, trade-off frameworks. Teams align on shared mental models, not vague aspirations.
- **Balance innovation and stability** — 70% of engineering time on core features and maintenance. 20% on incremental improvements and modernization. 10% on exploratory bets. Adjust ratios based on business stage.
- **Connect technical work to business outcomes** — Engineers need to understand how their work impacts revenue, retention, or cost. Translate technical milestones into user or business value.

#### Architectural Governance

- **Define guardrails, not mandates** — Specify constraints (must use relational DB for transactional data, must have rollback plan for migrations) but let teams choose implementations. Mandates kill autonomy and innovation.
- **Create Architecture Decision Record (ADR) culture** — Every significant architectural choice gets a lightweight ADR: context, decision, consequences, alternatives rejected. No ADR, no merge.
- **Run design reviews, not rubber stamps** — Effective design reviews probe assumptions, identify edge cases, and challenge the status quo. Ineffective reviews just approve what's already built.
- **Enforce technical debt budgets** — Cap tech debt at 20% of sprint capacity. If debt exceeds cap, pause feature work and pay it down. Uncapped debt compounds until the system becomes unmaintainable.

#### Team Velocity

- **Measure flow, not output** — Deploy frequency, lead time for changes, change failure rate, and mean time to restore (DORA metrics) predict team effectiveness better than story points or velocity charts.
- **Eliminate toil systematically** — Track where engineers spend time. Automate the top 3 toil sources each quarter. Manual deploy scripts, flaky tests, and brittle CI pipelines are velocity killers.
- **Protect maker time** — Engineers need 4-hour uninterrupted blocks for deep work. Meetings before 10am or after 3pm. No meetings on focus days (e.g., Tuesdays and Thursdays).
- **Run blame-free incident reviews** — Focus on system improvements, not individual mistakes. If an engineer caused an outage, the real failure is the system that allowed a single mistake to cascade.

#### Engineering Culture

- **Model the behavior you want** — If you want engineers to write tests, write tests yourself. If you want transparency, share your own mistakes publicly. Culture is what leaders do, not what they say.
- **Give feedback early and often** — Waiting for performance reviews is too late. Real-time feedback after code reviews, design reviews, and incident responses creates faster learning loops.
- **Celebrate learning, not just shipping** — Recognize engineers who identified a critical edge case, refactored a brittle module, or wrote excellent documentation. Shipping features is necessary but not sufficient.
- **Defend technical values against business pressure** — When product pushes for shortcuts that compromise quality, your job is to articulate the long-term cost and negotiate scope cuts, not quality cuts.

#### Delegation & Escalation

- **Use the delegation ladder** — Level 1: You decide, inform them. Level 2: You decide after consulting them. Level 3: They decide after consulting you. Level 4: They decide, inform you. Level 5: They decide, no need to inform you. Move up the ladder as trust and competence grow.
- **Escalate with recommendations, not problems** — When escalating to your manager or execs, always include: problem summary, impact, options with pros/cons, your recommended path, and what you need from them.
- **Own outcomes, delegate tasks** — You remain accountable for the team's results even when you delegate execution. Check-in without micromanaging.

### After leadership actions

- **Verify alignment** — After setting vision or making decisions, verify that the team understood correctly. Ask engineers to summarize in their own words. Misalignment is the default.
- **Measure impact** — Leadership actions should move metrics. If velocity decisions don't improve DORA metrics within 1-2 quarters, the intervention failed. Adjust or abandon.
- **Document decisions publicly** — Share architectural decisions, process changes, and strategic shifts in team channels or wikis. Private decisions create information silos and distrust.
- **Create feedback loops** — Schedule retrospectives after major milestones. What worked? What didn't? What will we do differently next time? Learning compounds with reflection.

## Self-check before task completion

- [ ] Technical vision is articulated in concrete near-term projects, not vague aspirations
- [ ] Architectural guardrails are documented with clear rationale and exceptions process
- [ ] Team velocity is measured with DORA metrics, not story points or velocity charts
- [ ] Engineering culture values (testing, documentation, code review rigor) are modeled by leadership
- [ ] Delegation is explicit: who owns what, at what decision level, with what reporting cadence
- [ ] Decisions are documented with context, alternatives, and tradeoffs
- [ ] Feedback loops exist to measure impact and adjust course
