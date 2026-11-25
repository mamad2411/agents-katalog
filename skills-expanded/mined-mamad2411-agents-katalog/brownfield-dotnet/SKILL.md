---
name: brownfield-dotnet
description: "Knowledge base from \"Brownfield Application Development in .NET\" by Kyle Baley & Donald Belcham. Use when applying their frameworks for reviving brownfield/legacy .NET apps — version control, continuous integration, automated testing, code metrics, defect tracking, OO/SOLID, layering, inversion of control, MVP/MVC, data access/ORM, and external integration — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Brownfield Application Development in .NET
**Author**: Kyle Baley & Donald Belcham (Manning) | **Pages**: ~408 | **Chapters**: 13 | **Generated**: 2026-06-30

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference
- **With a topic** — ask about `continuous integration`, `inversion of control`, `ORM`, etc.; I find and read the relevant chapter
- **With a chapter** — ask for `ch09`; I load that specific chapter file
- **Browse** — ask "what chapters do you have?" for the full index

When you ask about a topic not covered in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**What is brownfield?** An *existing, actively-developed* codebase contaminated by poor practices but **salvageable through directed refactoring**. Distinct from greenfield (no history) and legacy (maintenance-only, "dealt with"). The whole book is about reviving it without a rewrite.

**Ecosystem before code (the book's structure).** Fix the *ecosystem* first (Part 1: version control → CI → tests → metrics → defect tracking), then the *code* (Part 2: OO → layering → IoC → UI → data access → integration). Reason: you can't safely change code you can't build, test, or measure. Adapt the order to your own biggest pain points.

**Pain Points & Friction drive prioritization.** A **pain point** is a process causing grief that pushes you to a better way; **friction** is anything slowing your normal workflow. They define *where* to work. Highest-pain, cross-discipline fixes give the biggest gains. On the 3rd repeat of any boilerplate, trigger a "hack alert."

**The Scale (not the Iron Triangle).** Balance time & resources (keep low) against quality & features (keep high). Add a feature → add time/resources or cut scope. The dev team influences everything **except cost**. Sell change to management in **cash dollars and risk**, proven with a small **time-boxed proof-of-concept**.

**Pay technical debt continuously**, never as a "big push" — time-box it each cycle (even ½ day/week). And refactor **one thing at a time, finished** — half-done refactorings add debt + inconsistency.

**The Check-In Dance.** Before every commit: get latest → merge → build → run tests → commit. Continuous Integration automates this on a server, shortening the **feedback loop** and giving the team a build "metronome." A broken build is the team's top priority — stop and fix.

**Test to escape "living in fear of change."** Untested code makes every edit risky. For legacy fixes, write a **characterization test first** (reproduce the defect), then fix. Distinguish unit from integration tests; split fast from slow builds.

**Measure to find hotspots.** Use the **Three CC's** — code Coverage, Cyclomatic complexity, Class coupling. Track **deltas over time**, never absolute targets. High complexity ∩ low coverage = refactor first. Coverage is a diagnostic, not a quota; never fail a build on a metric.

**Zero Defect Count.** Clear the backlog, then fix new defects immediately so the open count stays ~0 — make it cultural. Write defects with the **5 C's**: Concise, Clear, Complete, Constructive, Closed.

**Code-side toolkit (Part 2):**
- **OO/SOLID** (Ch 7): SRP, OCP, DIP, Law of Demeter; composition over inheritance; KISS/YAGNI/DRY.
- **Layering** (Ch 8): logical *layers* ≠ physical *tiers*. Use **Interface-Based Design** and **seams** to isolate; whittle one screen at a time. Wrap foreign systems in an **Anti-Corruption Layer** (Adapter).
- **Inversion of Control** (Ch 9): IoC (principle) ⊃ DIP (means) ⊃ DI (impl) → IoC container (tool). Incremental path: interfaces → invert → poor man's DI → container. Avoid service locator.
- **UI** (Ch 10): get logic out of code-behind. **MVP** (Passive View = max testable; Supervising Controller = lighter) or **MVC**. Separation of Concerns throughout.
- **Data access** (Ch 11): hand-rolled vs generated vs **ORM** (NHibernate); front everything with a **Repository** and inject it.
- **External integration** (Ch 12): wrap third-party/legacy APIs behind your own interface + DTOs; manage compile-time vs run-time risk.

**Change is "hearts and minds, not shock and awe."** Win one developer at a time; be the agent for change; discourage Hero Programmer Syndrome in favor of collective ownership.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-understanding-brownfield.md) | Understanding Brownfield Applications | 3 Components, Pain Points, Friction, The Scale, Technical Debt, Big Rewrite |
| [ch02](chapters/ch02-version-control.md) | Version Control in Brownfield Applications | Check-In Dance, File Locking vs Merging, folder structure |
| [ch03](chapters/ch03-continuous-integration.md) | Continuous Integration | Feedback Loop, CI Dance, Metronome, Broken-Build rules |
| [ch04](chapters/ch04-automated-testing.md) | Automated Testing | unit vs integration, test-before-fix, state/interaction tests, TAD vs TDD |
| [ch05](chapters/ch05-metrics-code-analysis.md) | Software Metrics and Code Analysis | Three CC's, cyclomatic complexity, coupling, delta monitoring |
| [ch06](chapters/ch06-defect-tracking.md) | Defect Tracking | Zero Defect Count, Deferred Defect, 5 C's |
| [ch07](chapters/ch07-oo-practices.md) | Bringing Better OO Practices | 4 OO fundamentals, SOLID, composition>inheritance, KISS/YAGNI/DRY |
| [ch08](chapters/ch08-re-layering.md) | Re-Layering Your Application | Tiers vs Layers, Interface-Based Design, Anti-Corruption Layer, seams |
| [ch09](chapters/ch09-inversion-of-control.md) | Inversion of Control | IoC/DIP/DI/container, poor man's DI, constructor injection |
| [ch10](chapters/ch10-ui-cleanup.md) | Cleaning Up the User Interface | MVC, MVP, Passive View, Supervising Controller, SoC |
| [ch11](chapters/ch11-data-access.md) | Re-factoring Data Access | hand-rolled/generated/ORM, Object/Relational Mapper, Repository |
| [ch12](chapters/ch12-external-integration.md) | Risk and Corruption: Managing External System Dependencies | Anti-Corruption Layer, proxy/adapter/façade, DTO, compile vs run-time risk |
| [ch13](chapters/ch13-keeping-momentum.md) | Keeping the Momentum | nudge-the-beast, culture of quality, tooling appendix |

## Topic Index

- **Adapter / Anti-Corruption Layer** → ch08, ch12
- **Agent for change / selling to management** → ch01, ch13
- **Automated testing / unit vs integration** → ch04
- **Continuous integration / build server** → ch03
- **Cyclomatic complexity / coupling / coverage** → ch05
- **Data access / ORM / NHibernate / Repository** → ch11
- **Defect tracking / Zero Defect Count** → ch06
- **Dependency Injection / IoC container** → ch09
- **DTO / external systems / web services** → ch12
- **Layering / tiers vs layers / seams** → ch08
- **MVC / MVP / Passive View / presenter** → ch10
- **OO fundamentals / SOLID / SRP / DIP** → ch07, ch09
- **Pain points / friction / technical debt** → ch01
- **Tooling (NUnit, NDepend, Castle Windsor, etc.)** → ch13
- **Version control / Check-In Dance / branching** → ch02

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and patterns (when/how/trade-offs)
- [cheatsheet.md](cheatsheet.md) — decision rules, thresholds, tooling, tells & smells

---

## Scope & Limits

Covers the book's content only (2010, .NET/ASP.NET WebForms era — tooling names are period-specific). The principles (CI, testing, IoC, layering, ORM, ACL) remain current; map period tools to modern equivalents (e.g. ASP.NET Core MVC, xUnit, GitHub Actions, EF Core) when applying to today's stacks. For hands-on changes in your codebase, combine with project-specific tools.
