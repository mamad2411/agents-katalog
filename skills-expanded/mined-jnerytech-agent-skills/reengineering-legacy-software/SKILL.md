---
name: reengineering-legacy-software
description: "Knowledge base from \"Re-Engineering Legacy Software\" by Chris Birchall (Manning, 2016). Use when applying Birchall's frameworks for legacy code, refactoring, re-architecting, the Big Rewrite, static analysis, dependency injection/seams, environment automation (Vagrant/Ansible), and CI/CD deployment, studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Re-Engineering Legacy Software
**Author**: Chris Birchall | **Pages**: ~234 | **Chapters**: 10 | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference
- **With a topic** — ask about `refactoring`, `the big rewrite`, `static analysis`, `Ansible`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch05`; I load that specific chapter file
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**The central decision: how to revitalize legacy.** Prefer the lowest-risk option that achieves the goal — **Replace (buy/OSS) → Refactor → Re-architect → Full Rewrite**. Refactor is the default. A full rewrite is justified ONLY when **both** conditions hold: refactoring was tried and failed, AND a paradigm/technology shift is required.

**Legacy is broad.** A legacy project = *any existing project that's difficult to maintain or extend* — not just old code. It spans code, infrastructure, and team culture. Indicators (not proof): OLD / LARGE / INHERITED / POORLY-DOCUMENTED. Counter-example: the Linux kernel is old + huge yet high-quality because of its review culture.

**Technical debt = a loan.** Quick "good enough" fixes incur interest (slower future work); unpaid debt compounds and forces complex workarounds that are themselves new debt. Pay it down deliberately.

**Measure before you touch (Ch2).** Don't refactor on emotion — stand up a measurement infrastructure first and let data pick targets and prove progress. For Java run **FindBugs → PMD → Checkstyle** in that order (bugs, then design, then formatting). Pick targets by **churn** (most-edited files via `git log --name-only | sort | uniq -c | sort -nr`) and by static-analysis hotspots. Automate inspection on every commit with **Jenkins** (continuous inspection); publish trend graphs; trigger with a VCS webhook, not polling.

**Refactoring discipline (Ch4).** Done right, refactoring is safe — refactor all day without a bug. Rules: small reversible steps; **never mix a refactor with a behavior change in one commit**; lean on the IDE but verify (compile, tests, grep); use the VCS as a giant undo; for big changes use the **Mikado Method**. To test untestable code, **introduce indirection** — extract an interface, delegate from a production impl, inject via a *protected* constructor (a **seam**), then mock it. Keep tests one modularity level *higher* than the code you change. Warm up by deleting **stale/dead/zombie/expired** code and **toxic tests**.

**Prioritize with three axes (Ch3): value / difficulty / risk.** Start with *low-hanging fruit* (low risk + low difficulty), then *pain points* (high value). Win the social/political battle first: refactoring must justify itself in business terms (specific, feature-named, measurable goals). For tiny changes use the **Secret 20% Project** (just do it, <20% of your time, share a prototype). Manage the **Traditionalist** (averse to change) and **Iconoclast** (over-refactors) — channel with code review + mandatory tests + sized diffs.

**Re-architecting = refactoring in the large (Ch5).** Change structure at module/service level while preserving behavior. Separate two decisions: *how the codebase is organized* (modules) vs *how the app is deployed* (one process vs services) — **modularize first**. Enforce module boundaries mechanically (interface-only compile artifacts + Guice DI), not by discipline. Validate boundaries with the **one-sentence-purpose test**. Migrate incrementally (**Strangler-style**); every network hop adds a new failure class; each service owns its own DB. There is no silver-bullet architecture.

**The Big Rewrite (Ch6) — last resort.** Decide and document the type up front: **black-box** (same behavior, new internals) / **brush-up** (+ normalized spec) / **quid pro quo** (+ new features to win sign-off). Write a **scope document** to fight feature creep. Make it **iterative with phased releases**: run old + new in **parallel** with two-way data sync, cut over incrementally, and **fail back** to legacy on any bug. Use old code as a low-level reference and tie-breaker, never as the architecture — mine VCS history to keep conditions that earned their place. Avoid Big Bang cutover.

**Automate the environment (Ch7–8).** Treat the dev environment as code: a README-as-onramp + **Vagrant** (VM) + **Ansible** (declarative, idempotent provisioning) → `git clone` to running env in one `vagrant up`. Then reuse the *same* playbook across DEV/TEST/PROD — encode all differences in **variables + per-environment inventory files**, never fork the playbook — for perfect **environment parity** (kills production-only bugs). Run provisioning from **Jenkins** for an audit trail and parity.

**Modernize build & deploy (Ch9).** Migrate to the org-standard build tool (Ant→Gradle) by adopting its directory conventions. Minimum CI = a test/build job + one-click TEST deploy. Automate **rolling PROD deploys** with Fabric (detach from LB → stop → checkout *tag* → start → healthcheck → reattach, one server at a time). **Releases are immutable** (never re-release); deployment ≠ release. Deploy scripts are code and rot — exercise them on a schedule.

**Stop writing legacy (Ch10).** The same disciplines prevent rot — cheapest built in early. Top lever: **disposable software** — build large systems from small, decoupled, replaceable components (rewritable in days). Plus: **living specification** (high-level tests CI enforces), **Darwinian documentation** (in-repo, delete stale), communication rituals (review, pairing, tech talks, hack days), periodic whole-codebase reviews, and "fix one window."

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-challenges-of-legacy-projects.md) | Understanding the Challenges of Legacy Projects | broad legacy definition, OLD/LARGE/INHERITED/POORLY-DOC, technical-debt-as-loan, tests-as-docs |
| [ch02](chapters/ch02-finding-your-starting-point.md) | Finding Your Starting Point | FindBugs→PMD→Checkstyle, continuous inspection, churn analysis, exploratory refactoring, characterization tests, Jenkins |
| [ch03](chapters/ch03-preparing-to-refactor.md) | Preparing to Refactor | value/difficulty/risk triage, refactor→incremental-rewrite→full-rewrite spectrum, Secret 20% Project, Traditionalist/Iconoclast |
| [ch04](chapters/ch04-refactoring.md) | Refactoring | separate refactor from feature, IDE/VCS leverage, Mikado Method, seams + dependency injection, test-level-higher, stale/toxic cleanup |
| [ch05](chapters/ch05-re-architecting.md) | Re-architecting | modularization, interface/impl artifacts + Guice, one-sentence-purpose test, SOA/microservices trade-offs, strangler migration |
| [ch06](chapters/ch06-the-big-rewrite.md) | The Big Rewrite | exhaust-options gate, black-box/brush-up/quid-pro-quo, scope document, parallel running + fail-back, translation layer |
| [ch07](chapters/ch07-automating-dev-environment.md) | Automating the Development Environment | README-as-onramp, Vagrant, Ansible roles, idempotent provisioning, infrastructure-as-code |
| [ch08](chapters/ch08-extending-automation.md) | Extending Automation to TEST/Staging/PROD | one playbook across envs, variables + inventory files, environment parity, Jenkins-runs-Ansible, immutable infrastructure |
| [ch09](chapters/ch09-modernizing-build-deploy.md) | Modernizing Build, Deploy & Workflow | Ant→Gradle migration, CI baseline + one-click deploy, rolling deploy with Fabric, release vs deployment |
| [ch10](chapters/ch10-stop-writing-legacy-code.md) | Stop Writing Legacy Code! | disposable software, living specification, Darwinian docs, communication rituals, fix-one-window |

## Topic Index

- **Ansible / playbooks / roles** → ch07, ch08
- **Architecture trade-offs (monolith/SOA/microservices)** → ch05
- **Bounded context / DDD** → ch05
- **Build tool migration (Ant→Gradle)** → ch05, ch09
- **Characterization tests** → ch02, ch04
- **Churn / hotspot analysis** → ch02
- **CI / Jenkins / continuous inspection** → ch02, ch08, ch09
- **Cutover / parallel running / fail-back** → ch06
- **Dependency injection / seams** → ch04, ch05
- **Deployment (rolling, Fabric, release vs deploy)** → ch09
- **Environment parity / config drift** → ch08
- **Exploratory refactoring** → ch02
- **God class / Util** → ch03, ch04, ch05
- **Immutable infrastructure / DevOps** → ch08
- **Legacy definition & characteristics** → ch01
- **Mikado Method** → ch04
- **Modularization / interface-impl artifacts / Guice** → ch05
- **Refactoring discipline & techniques** → ch04
- **Rewrite decision & types** → ch03, ch06
- **Scope document** → ch06
- **Static analysis (FindBugs/PMD/Checkstyle)** → ch02
- **Strangler pattern** → ch03, ch05, ch06
- **Technical debt** → ch01, ch03
- **Triage (value/difficulty/risk)** → ch03
- **Vagrant / dev env automation** → ch07
- **Value proposition / business buy-in** → ch03
- **Disposable software / preventing new legacy** → ch10

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions and chapter refs
- [patterns.md](patterns.md) — all techniques and migration patterns (when/how/trade-offs)
- [cheatsheet.md](cheatsheet.md) — decision rules, tool order, smells, deploy/provision quick reference

---

## Scope & Limits

Covers the book content only (Java/JVM-centric examples, 2016 toolchain — Vagrant, Ansible, Jenkins, Gradle, Guice, Fabric). For hands-on work in your codebase, combine with project-specific tools. Pairs naturally with `working-effectively-legacy-code` (Feathers) for the seams/characterization-tests depth. For topics beyond this book, ask the agent directly.
