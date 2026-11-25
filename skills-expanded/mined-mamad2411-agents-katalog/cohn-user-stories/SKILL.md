---
name: cohn-user-stories
description: "Knowledge base from \"User Stories Applied: For Agile Software Development\" by Mike Cohn. Use when applying Cohn's frameworks for writing user stories, the 3 Cs, INVEST, user role modeling, story-point estimation, planning poker, release/iteration planning, velocity, acceptance testing, or stories with Scrum/XP — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# User Stories Applied: For Agile Software Development
**Author**: Mike Cohn | **Pages**: ~291 | **Chapters**: 21 + Appendix A | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference
- **With a topic** — ask about `INVEST`, `estimating`, `velocity`, `splitting stories`, `proxies`, or another indexed topic; I find and read the relevant chapter
- **With a chapter** — ask for `ch08`; I load that specific chapter file
- **Browse** — ask "what chapters do you have?" for the full index

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**A user story** = a short description of functionality valuable to a user or purchaser. Write it as **"As a *(role)*, I want *(function)* so that *(value)*."** If you can't write the "so that," the story lacks clear value. Requirements are a *communication* problem; the card is thin on purpose.

**The 3 Cs (Ron Jeffries)** — a story has three parts: **Card** (a one-line reminder), **Conversation** (the detail, deferred until it matters), **Confirmation** (acceptance tests, on the card's back). The card is a *promise to have a conversation*, never a contract.

**INVEST (Bill Wake)** — a good story is **I**ndependent, **N**egotiable, **V**aluable, **E**stimable, **S**mall, **T**estable. Use it as a checklist; each failing letter implies a fix (dependent → combine/re-split; not estimable → spike or split; vague → add tests). See cheatsheet for the fix-by-symptom table.

**Who does what** — the **customer team** (users, product manager, testers) *writes and prioritizes* stories and *writes acceptance tests*; the **developer team** *estimates* and builds. On a priority conflict the customer decides — but only ever with developer estimates in hand ("cost changes priority").

**User role modeling (Constantine & Lockwood)** — never write every story from one generic "user." Before writing stories: **brainstorm** role cards → **organize** spatially → **consolidate** (merge equivalents, rip up duplicates and success-irrelevant roles) → **refine** with attributes. Promote 1–2 vital roles to **personas** (name + backstory + photo, backed by research); use **extreme characters** sparingly to surface overlooked stories.

**Trawling for requirements (Robertson & Robertson)** — requirements aren't "captured," they're *trawled*: repeated passes, coarse net first, revisited continuously because stories mature, change, and die. Techniques: **interviews** (default), **observation** (reveals the need behind the stated need), **story-writing workshops with low-fidelity prototyping** (fastest, highest-volume), **questionnaires** (only to prioritize existing stories). Ask **open-ended, context-free questions**.

**User proxies** — *a real user beats a proxy any time*; developers are usually worse proxies than the proxies. When forced to use proxies, combine *different* types so biases cancel, and use salespeople/managers as conduits to real users, not the sole voice.

**Splitting stories — slice the cake (Bill Wake)** — split a too-big story into thin *vertical* slices through all layers, each independently usable. Never split horizontally ("build form" + "save to DB"). Compound epic → split by create/edit/delete or data; complex epic → timeboxed **spike** + development story.

**Estimating in story points** — estimate *relative size*, not time, on the scale **½ 1 2 3 5 8 13 20 40 80**. Use **planning poker**: private estimate → simultaneous reveal → high & low explain → re-vote, ≤3 rounds, converge reasonably. The team that will do the work estimates; the customer answers questions but never estimates. **Triangulate** against already-sized stories. Constraints = 0 points.

**Velocity** — story points of *completed* stories per iteration; it converts points to a calendar. Count only finished stories (passed acceptance tests) — never partials, never re-score. Don't trust velocity before 2–3 iterations.

**Release planning** — (1) ask a target date *range*; (2) customer prioritizes (value + risk + estimates), use **MoSCoW** (Must/Should/Could/Won't); (3) estimate; (4) get velocity (history > trial iteration > guess of ⅓–½ developer-days); (5) iterations = points ÷ velocity; (6) fill iteration "piles" to velocity. Communicate "ready in ~5–7 iterations," never a fixed date. Flex **scope**, not date or quality.

**Iteration planning** — discuss each prioritized story → **disaggregate** into tasks → one developer **accepts** each → estimate accepted tasks in **ideal hours** → sum to catch over-commitment. One name per task, but ownership stays fluid and team-owned.

**Acceptance testing** — the **customer** writes tests, on the card back, *before/while coding*; they define "done." Cover happy path + edge + explicit failure cases. Stop when a test adds no clarification; automate with **FIT/FitNesse**. Writing tests *is* a requirements conversation.

**Why stories win** — they shift focus from a shared *document* to a shared *understanding*: comprehensible to everyone, right-sized for planning, support deferring detail and participatory/opportunistic design. Stories ≈ one use-case scenario; story + tests ≈ a use case — but smaller, less complete, transient. Focus on the user's **goal**, not a "shall" list of attributes.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-overview.md) | An Overview | 3 Cs, story-driven workflow, velocity/piles |
| [ch02](chapters/ch02-writing-stories.md) | Writing Stories | INVEST, splitting epics (compound/complex), spike, combining |
| [ch03](chapters/ch03-user-role-modeling.md) | User Role Modeling | role modeling 4 steps, role cards, personas, extreme characters |
| [ch04](chapters/ch04-gathering-stories.md) | Gathering Stories | trawling, interviews/questionnaires/observation/workshops, lo-fi prototyping |
| [ch05](chapters/ch05-user-proxies.md) | Working with User Proxies | proxy taxonomy + biases, constituting the customer team, user task force |
| [ch06](chapters/ch06-acceptance-testing.md) | Acceptance Testing User Stories | two-step testing, customer test questions, FIT/FitNesse |
| [ch07](chapters/ch07-good-story-guidelines.md) | Guidelines for Good Stories | goal stories, slice the cake, closed stories, constraint cards |
| [ch08](chapters/ch08-estimating-stories.md) | Estimating User Stories | story points, planning poker, triangulation, ideal time |
| [ch09](chapters/ch09-planning-release.md) | Planning a Release | release sequence, MoSCoW, value+risk priority, initial velocity |
| [ch10](chapters/ch10-planning-iteration.md) | Planning an Iteration | iteration planning, disaggregation, accept responsibility |
| [ch11](chapters/ch11-velocity.md) | Measuring & Monitoring Velocity | measuring velocity, planned-vs-actual, cumulative, burndown |
| [ch12](chapters/ch12-what-stories-are-not.md) | What Stories Are Not | goals-vs-list test, story≈scenario, essential use case, IEEE 830 |
| [ch13](chapters/ch13-why-user-stories.md) | Why User Stories? | adequate stories+conversation, opportunistic & participatory design |
| [ch14](chapters/ch14-story-smells.md) | A Catalog of Story Smells | smell→symptom→cause→remedy, "use a smaller card" |
| [ch15](chapters/ch15-stories-with-scrum.md) | Using Stories with Scrum | story-constrained product backlog, sprint cycle |
| [ch16](chapters/ch16-additional-topics.md) | Additional Topics | constraint cards for NFRs, usage-centered design, cards vs. software, bugs as stories |
| [ch17](chapters/ch17-example-user-roles.md) | The User Roles *(example)* | role modeling applied (South Coast Nautical Supplies) |
| [ch18](chapters/ch18-example-stories.md) | The Stories *(example)* | story-writing workshop → 27 story cards |
| [ch19](chapters/ch19-example-estimating.md) | Estimating the Stories *(example)* | planning poker, estimation-driven splitting, estimate table |
| [ch20](chapters/ch20-example-release-plan.md) | The Release Plan *(example)* | MoSCoW, guessed velocity, two-iteration allocation |
| [ch21](chapters/ch21-example-acceptance-tests.md) | The Acceptance Tests *(example)* | customer tests on card backs, tests simplify design |
| [ch22](chapters/ch22-appendix-a-xp-overview.md) | Appendix A: Overview of XP | twelve practices, four values, the Planning Game |

## Topic Index

- **3 Cs (Card/Conversation/Confirmation)** → ch01, ch06
- **Acceptance tests** → ch06, ch21; (XP) ch22
- **Bugs as stories** → ch16
- **Closed stories** → ch07
- **Constraints / nonfunctional requirements** → ch07, ch16, ch02
- **Customer / customer team** → ch01, ch05; (Scrum PO) ch15; (XP) ch22
- **Disaggregation / tasks** → ch10
- **Epics** → ch01, ch02, ch13
- **Estimating / story points** → ch08, ch19
- **Extreme Programming / Planning Game** → ch22, ch01
- **FIT / FitNesse** → ch06
- **Goal stories** → ch07
- **INVEST** → ch02, ch07
- **MoSCoW** → ch09, ch20
- **Personas** → ch03, ch17
- **Planning poker** → ch08, ch19
- **Prioritization** → ch09, ch20, ch14
- **Release planning** → ch09, ch20
- **Iteration planning** → ch10
- **Scrum** → ch15
- **Slice the cake / splitting stories** → ch07, ch02, ch14, ch19
- **Smells** → ch14
- **Spike / timebox** → ch02, ch22
- **Story vs. use case / IEEE 830 / scenario** → ch12, ch13
- **Trawling / gathering stories** → ch04
- **Triangulation** → ch08
- **User proxies** → ch05
- **User role modeling / roles** → ch03, ch17
- **Velocity / burndown** → ch11, ch08, ch09
- **Why user stories (advantages)** → ch13
- **Writing stories** → ch02, ch07

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions and chapter refs
- [patterns.md](patterns.md) — all techniques (role modeling, trawling, splitting, planning poker, release/iteration planning…)
- [cheatsheet.md](cheatsheet.md) — decision rules, INVEST fix-table, smell diagnosis, estimating/planning thresholds

---

## Scope & Limits

This skill covers Cohn's *User Stories Applied* (2004). For hands-on backlog work in your own tracker, combine with project tools. Deeper estimation/planning math is expanded in Cohn's later *Agile Estimating and Planning*; deeper Scrum mechanics live in dedicated Scrum sources. For topics beyond this book, ask the agent directly.
