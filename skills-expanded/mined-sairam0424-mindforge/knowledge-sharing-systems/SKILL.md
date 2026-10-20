---
name: knowledge-sharing-systems
version: 1.0.0
min_mindforge_version: 10.1.0
status: stable
triggers: knowledge sharing, documentation culture, brown bag session, tech talk, decision log, tribal knowledge, bus factor, knowledge base design, knowledge transfer system, institutional memory, expertise sharing, learning organization
---

# Knowledge Sharing Systems

## When this skill activates

This skill activates when designing, evaluating, or improving how knowledge flows
within an engineering organization. It addresses bus factor reduction, documentation
culture, decision logging, and systematic approaches to converting tribal knowledge
into institutional memory.

## Mandatory actions when this skill is active

### Before

1. **Assess current state** — Where does knowledge currently live? (People's heads,
   Slack threads, outdated wikis, code comments, nowhere?) Map the gaps.
2. **Identify bus factor risks** — Which components/systems have only 1-2 people who
   understand them? These are critical vulnerabilities.
3. **Understand failure modes** — What happens when the knowledge holder is unavailable?
   How long does it take a new person to become productive in each area?

### During

4. **Categorize knowledge types and appropriate capture methods:**

   - **Explicit knowledge** (can be written down):
     - Architecture Decision Records (ADRs) for non-obvious choices
     - API documentation generated from code
     - Runbooks for operational procedures
     - README files for project context and setup
     - Design documents for complex features

   - **Tacit knowledge** (hard to articulate, best transferred person-to-person):
     - Pair programming sessions (regular rotation)
     - Shadowing on-call rotations
     - Code review as teaching (explain the WHY in review comments)
     - Mob programming for complex problems
     - Recorded debugging sessions showing thought process

   - **Tribal knowledge** (exists only in collective memory, needs active capture):
     - "Why does this system do X?" interviews with long-tenured engineers
     - Archaeological code tours (walk through old systems, document context)
     - Decision archaeology (reconstruct rationale for old choices)
     - Oral history capture before people leave

5. **Implement knowledge sharing systems:**

   - **Decision logs** — Lightweight ADRs for all non-obvious choices. Template:
     Context, Decision, Consequences, Status. Write at decision time, not after.
     Low ceremony, high value.

   - **Tech talks** — Bi-weekly internal presentations (30 min max). Rotate presenters.
     Record all sessions. Topics: recent incidents, new technologies, deep dives
     into system internals, lessons learned.

   - **Onboarding paths** — Curated reading lists per domain/team. Progressive
     complexity (week 1: overview, week 2: deep dive, week 3: contribute). Include
     "who to ask" for each topic.

   - **Brown bag sessions** — Informal lunch-and-learn. Low pressure, high exploration.
     Can be external topics, book discussions, or show-and-tell of side projects.

   - **Documentation sprints** — Dedicate one sprint per quarter to documentation
     catch-up. Treat docs as first-class deliverables, not afterthoughts.

6. **Bus factor reduction strategies:**
   - Pair programming rotation — No one works alone on critical systems for >2 weeks.
   - Cross-team shadowing — Engineers spend time embedded in other teams quarterly.
   - Documented decisions — If only one person knows WHY a decision was made, it is
     organizational debt.
   - Recorded walkthroughs — Screen-record explanations of complex systems. 10-minute
     videos are more accessible than 50-page docs.
   - Code ownership rotation — Periodically reassign code review duties to spread
     understanding.

7. **Metrics to track:**
   - **Bus factor per component** — Number of people who can independently maintain
     each critical system. Target: minimum 3.
   - **Time-to-productive** — How long until a new joiner can ship independently?
     Track trend over time.
   - **Documentation freshness** — When was each critical doc last updated? Flag
     anything >6 months stale.
   - **Knowledge sharing participation** — Who presents tech talks, who reviews across
     teams, who pairs with new joiners?

### After

8. **Establish cadence** — Knowledge sharing is not a one-time project. Set recurring
   schedules for tech talks, documentation reviews, and bus factor assessments.
9. **Reward sharing** — Include knowledge sharing in performance reviews. Recognize
   people who write great docs, mentor others, or reduce bus factor.
10. **Audit quarterly** — Review bus factor scores, onboarding feedback, and
    documentation freshness. Invest where gaps persist.

## Self-check before task completion

- [ ] Bus factor assessed for all critical systems (target: minimum 3 per component)
- [ ] Knowledge types categorized with appropriate capture methods
- [ ] Decision log system implemented (lightweight ADRs at minimum)
- [ ] Onboarding path documented for each team/domain
- [ ] Regular cadence established for tech talks or equivalent
- [ ] Documentation freshness tracked with staleness alerts
- [ ] Time-to-productive measured and trending downward
- [ ] Knowledge sharing recognized in performance evaluation
- [ ] Tribal knowledge capture plan for single-points-of-knowledge
