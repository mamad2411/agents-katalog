---
name: google-sre
description: "Knowledge base from \"Site Reliability Engineering: How Google Runs Production Systems\" by Betsy Beyer, Chris Jones, Jennifer Petoff & Niall Richard Murphy. Use when applying Google's SRE frameworks for SLOs and error budgets, toil, monitoring and alerting, on-call and incident management, postmortems, load balancing and overload/cascading failures, distributed consensus, data integrity, and launches — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Site Reliability Engineering: How Google Runs Production Systems
**Authors**: Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (eds.) | **Pages**: ~550 | **Chapters**: 34 + Appendices A–F | **Generated**: 2026-10-05

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `error budget`, `cascading failures`, `postmortem`, etc.; I find and read the relevant chapter
- **With chapter** — ask for `ch22`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**SRE = what happens when you ask a software engineer to design an operations team.** Run ops as a software problem; scale the service sublinearly with headcount.

### Risk, SLOs and error budgets (Ch 3, 4)
- **100% is the wrong target.** Each extra nine costs ~10× more and users behind a 99%-reliable phone/ISP can't perceive it. Make a service "reliable enough, but no more".
- **SLI → SLO → SLA.** SLI = measured indicator (latency percentile, availability, throughput, durability); SLO = target for it; SLA = contract with consequences. Use percentiles (p99), not averages. Keep an internal SLO tighter than the published one.
- **Error budget = 1 − SLO.** Monitoring (a neutral party) measures it; while budget remains, release; when spent, freeze launches and invest in reliability. It turns the dev-vs-ops fight over velocity into a shared, data-driven control loop.
- **Don't overachieve.** If you far exceed the SLO, dependents rely on it — inject planned outages (global Chubby).
- Prefer **aggregate availability** (successful/total requests) over uptime for distributed systems.

### Toil and the 50% cap (Ch 1, 5)
- **Toil** = manual, repetitive, automatable, tactical, no enduring value, grows O(n) with the service.
- **Cap ops work at 50%**; overflow goes back to the dev team ("give back the pager"). The other half is engineering that removes toil permanently.

### Monitoring (Ch 6, 10)
- **Four golden signals**: latency, traffic, errors, saturation.
- **Alert on symptoms ("what's broken"), not causes ("why").** Pages must be urgent, actionable, need human judgment, and be novel. Everything else is a ticket or a log line — the only three valid outputs.
- White-box (internal metrics) + black-box (prober) together. Counters over gauges; sum of rates, not rate of sums.

### Automation, release, simplicity (Ch 7, 8, 9)
- **Automation ladder**: none → external script → generic tool → internal to the service → **autonomous** system. Automation at scale fails at scale: validate inputs ("zero means all"), rate-limit, make it idempotent.
- **Release engineering**: self-service, high velocity, **hermetic builds**, policy enforcement; branch + cherry-pick; canary → progressive rollout; config is versioned like code.
- **Virtue of boring**: essential vs accidental complexity; deleting code ("negative lines") is progress; minimal APIs, small releases.

### Incidents and learning (Ch 11–16, 28)
- **On-call balance**: ≤25% of time on-call, ≤2 incidents per 12 h shift; ≥8 people single-site, 6 per site dual-site. Playbooks give ~3× better MTTR.
- **Troubleshooting**: triage (stop the bleeding) → examine → diagnose → test/treat → cure. Start with *what touched it last*; bisect; horses not zebras; negative results are magic.
- **Incident Command System**: IC, Ops lead, Communication lead, Planning lead; one command post; live incident document; explicit handoffs. Declare if a second team is needed, it's customer-visible, or unsolved after an hour.
- **Blameless postmortems** with predefined triggers, peer review and tracked action items. Practice with the **Wheel of Misfortune** and DiRT.

### Reliability under load (Ch 19–22)
- Edge: DNS + anycast/VIP with consistent hashing. Datacenter: **deterministic subsetting** + **weighted round robin**; **lame-duck** draining.
- **Overload defense stack**: per-customer quotas → client-side **adaptive throttling** (K=2) → **criticality** shedding → graceful degradation → retry budgets (≤3/request, <10% of requests) with jittered exponential backoff → **deadline & cancellation propagation** → "overloaded; don't retry".
- **Cascading failures** spread via positive feedback (CPU → latency → memory → GC → CPU). Emergency moves: add capacity, stop health-check kills, restart, drop traffic, degrade, kill batch, block the query of death. Load-test to find the cliff before users do.

### Critical state and data (Ch 23–26)
- Use **proven distributed consensus** (Paxos/Raft/Zab) as a **Replicated State Machine** for leader election, locks, config; 2f+1 replicas (5 typical) across failure domains. Never hand-roll heartbeats/STONITH.
- Distributed cron: Paxos-backed, two sync points per launch, **fail closed**.
- **Data integrity = recoverability**, not backups. Soft deletion → tiered backups → replication → out-of-band validation; **test restores**. Replication spreads corruption.

### Scaling the organization (Ch 27–32)
- **Launch Coordination Engineering** + a checklist where every item traces to a past disaster; feature flags and gradual rollouts.
- **Polarize time**: one person on interrupts, everyone else in flow on projects.
- **PRR** before onboarding a service; evolve to early engagement and shared **frameworks/platforms** with a common control surface.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction.md) | Introduction | 50% cap, error budget, alert/ticket/log |
| [ch02](chapters/ch02-production-environment.md) | The Production Environment at Google | Borg, BNS, Colossus/Bigtable/Spanner, GSLB, N+2 |
| [ch03](chapters/ch03-embracing-risk.md) | Embracing Risk | Error budget, cost of a nine, service tiers |
| [ch04](chapters/ch04-service-level-objectives.md) | Service Level Objectives | SLI/SLO/SLA, percentiles, safety margin |
| [ch05](chapters/ch05-eliminating-toil.md) | Eliminating Toil | Toil definition, 50% cap |
| [ch06](chapters/ch06-monitoring-distributed-systems.md) | Monitoring Distributed Systems | Four golden signals, symptoms vs causes |
| [ch07](chapters/ch07-evolution-of-automation.md) | The Evolution of Automation at Google | Automation classes, autonomous systems |
| [ch08](chapters/ch08-release-engineering.md) | Release Engineering | Hermetic builds, cherry-picks, Rapid, config mgmt |
| [ch09](chapters/ch09-simplicity.md) | Simplicity | Virtue of boring, negative lines of code |
| [ch10](chapters/ch10-practical-alerting.md) | Practical Alerting from Time-Series Data | Borgmon rules, sum of rates, Alertmanager |
| [ch11](chapters/ch11-being-on-call.md) | Being On-Call | Balanced on-call, 25% rule, overload/underload |
| [ch12](chapters/ch12-effective-troubleshooting.md) | Effective Troubleshooting | Hypothetico-deductive loop, triage, bisection |
| [ch13](chapters/ch13-emergency-response.md) | Emergency Response | Test/change/process-induced emergencies |
| [ch14](chapters/ch14-managing-incidents.md) | Managing Incidents | ICS roles, incident doc, declaration criteria |
| [ch15](chapters/ch15-postmortem-culture.md) | Postmortem Culture | Blameless postmortem, triggers, review |
| [ch16](chapters/ch16-tracking-outages.md) | Tracking Outages | Escalator, Outalator, tagging |
| [ch17](chapters/ch17-testing-for-reliability.md) | Testing for Reliability | Test hierarchy, canary fault order, barriers |
| [ch18](chapters/ch18-software-engineering-in-sre.md) | Software Engineering in SRE | Intent-based capacity planning (Auxon) |
| [ch19](chapters/ch19-load-balancing-frontend.md) | Load Balancing at the Frontend | DNS LB, anycast, VIP, consistent hashing |
| [ch20](chapters/ch20-load-balancing-datacenter.md) | Load Balancing in the Datacenter | Lame duck, subsetting, weighted RR |
| [ch21](chapters/ch21-handling-overload.md) | Handling Overload | Adaptive throttling, criticality, retry budgets |
| [ch22](chapters/ch22-cascading-failures.md) | Addressing Cascading Failures | Load shedding, deadlines, emergency steps |
| [ch23](chapters/ch23-distributed-consensus.md) | Managing Critical State: Distributed Consensus | Paxos, RSM, quorum placement |
| [ch24](chapters/ch24-distributed-cron.md) | Distributed Periodic Scheduling with Cron | Fail closed, Paxos sync points |
| [ch25](chapters/ch25-data-processing-pipelines.md) | Data Processing Pipelines | Workflow MVC, exactly-once |
| [ch26](chapters/ch26-data-integrity.md) | Data Integrity | Recovery over backup, defense in depth, 24 failure modes |
| [ch27](chapters/ch27-reliable-product-launches.md) | Reliable Product Launches at Scale | LCE, launch checklist, feature flags |
| [ch28](chapters/ch28-accelerating-sres-to-on-call.md) | Accelerating SREs to On-Call and Beyond | Learning checklist, Wheel of Misfortune, shadowing |
| [ch29](chapters/ch29-dealing-with-interrupts.md) | Dealing with Interrupts | Polarizing time, flow state |
| [ch30](chapters/ch30-operational-overload.md) | Embedding an SRE to Recover from Operational Overload | Three-phase embedding, kindling |
| [ch31](chapters/ch31-communication-collaboration.md) | Communication and Collaboration in SRE | Production meetings, cross-site collaboration |
| [ch32](chapters/ch32-evolving-engagement-model.md) | The Evolving SRE Engagement Model | PRR, early engagement, frameworks |
| [ch33](chapters/ch33-lessons-other-industries.md) | Lessons Learned from Other Industries | Preparedness, postmortems, automation, decisions |
| [ch34](chapters/ch34-conclusion.md) | Conclusion | 747 cockpit analogy |
| [ch35](chapters/ch35-appendices.md) | Appendices A–F | Availability table, best practices, incident doc, postmortem, launch checklist, meeting minutes |

## Topic Index

- **Adaptive throttling** → ch21
- **Alerting / paging** → ch06, ch10, ch11
- **Automation** → ch07, ch13, ch33
- **Availability table (nines)** → ch03, ch35
- **Backups / restore** → ch26
- **Black-box vs white-box monitoring** → ch06, ch10
- **Borg / Borgmon** → ch02, ch10
- **Canary** → ch08, ch17, ch27
- **Capacity planning / N+2** → ch02, ch18, ch35
- **Cascading failures** → ch22
- **Configuration management** → ch08, ch17, ch35
- **Consensus (Paxos/Raft)** → ch23, ch24
- **Criticality / load shedding** → ch21, ch22
- **Cron** → ch24
- **Data integrity** → ch26
- **Deadlines / retries / backoff** → ch21, ch22
- **DiRT / disaster testing** → ch11, ch13, ch33
- **Error budget** → ch01, ch03, ch04
- **Four golden signals** → ch06
- **Incident management (ICS)** → ch14, ch35
- **Interrupts / on-call load** → ch11, ch29, ch30
- **Launches / LCE / checklist** → ch27, ch35
- **Load balancing** → ch19, ch20
- **Onboarding SREs / training** → ch28
- **PRR / engagement model** → ch32
- **Pipelines** → ch25
- **Postmortems** → ch15, ch16, ch35
- **Production meetings** → ch31, ch35
- **Release engineering** → ch08
- **Simplicity** → ch09
- **SLI / SLO / SLA** → ch04
- **Testing** → ch17
- **Toil** → ch05
- **Troubleshooting** → ch12

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides

---

## Scope & Limits

This skill covers the book content only (Google practices circa 2016; tools like Borgmon have since evolved into Monarch/Prometheus-style systems). For hands-on implementation in your codebase,
combine with project-specific tools. For topics beyond this book, check related skills
or ask the agent directly.
