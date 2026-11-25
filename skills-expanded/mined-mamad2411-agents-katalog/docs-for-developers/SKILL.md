---
name: docs-for-developers
description: "Knowledge base from \"Docs for Developers: An Engineer's Field Guide to Technical Writing\" by Jared Bhatti, Zachary Sarah Corleissen, Jen Lambourne, David Nunez & Heidi Waterhouse. Use when applying their frameworks for developer documentation — user research, content types, drafting, editing, code samples, visuals, publishing, feedback, metrics, information architecture, and maintenance — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Docs for Developers: An Engineer's Field Guide to Technical Writing
**Authors**: Jared Bhatti, Zachary Sarah Corleissen, Jen Lambourne, David Nunez, Heidi Waterhouse (foreword by Kelsey Hightower) | **Pages**: ~241 | **Chapters**: 11 (+ appendices) | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `code samples`, `information architecture`, `triage`, `metrics`, etc.; I find and read the relevant chapter.
- **With a chapter** — ask for `ch07`; I load that chapter file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**The thesis**: documentation is engineering work. Treat it like code — research before building, draft, review/test, ship with the release, then measure and maintain. **A document is good when it fulfills its purpose.**

**The curse of knowledge** (Ch 1) — you assume others know what you know; it's the obstacle behind every bad doc. Break it with **user research** and **empathy**. Document **needs, not wants**. Condense research into **personas**, **user stories** (`As a [user], I want [activity] so that I can [goal]`), **journey maps**, and a **friction log** (use your own product as a user; log expected vs. actual).

**The documentation pipeline** — Research → Plan → Draft → Edit → Code samples → Visuals → Publish → Feedback → Measure → Organize → Maintain. Each chapter is one stage.

**Content types** (Ch 2) — pick the pattern that fits the user's use case: code comments (the *why*), README, getting started (fastest path to working), conceptual (how it works, no impl details), **tutorial** (learn in a sandbox) vs. **how-to** (do real work), reference (API/glossary/troubleshooting), changelog/release notes. Produce a **documentation plan** = content outline (title + type + description).

**Drafting** (Ch 3) — start with **Audience / Purpose / Pattern**; the **title = the goal** (one goal per doc; verb=task, noun=reference). Outline first ("pseudocode"), reorder for **flow of information**, then expand. **Write for skimming**: readers consume ≤28% of a page in an **F-pattern** — front-load the first 3 paragraphs, break up text, one action per procedure step + a verify step. First drafts are allowed to be bad.

**Editing** (Ch 4) — separate from writing. Four **passes in order**: Technical accuracy → Completeness → Structure → Clarity & brevity. Build a review process (self → peer → technical). Give feedback by **plussing** (Pixar): only criticize an idea if you add a constructive suggestion.

**Code samples** (Ch 5) — the gold readers hunt for. Every sample: **Explained, Concise, Clear**; executable ones also **Usable** (descriptive placeholders, never `foo`/`bar`) and **Trustworthy** (tested, production-ready). One use case per page; range of complexity. *Think before you automate.*

**Visual content** (Ch 6) — high-risk/high-reward. Score on **Comprehension, Accessibility, Performance**. One idea per diagram ("simplify to amplify"); boxes-and-arrows / flowcharts / swimlanes; describe in body text; SVG; 4.5:1 contrast. **Beware video** — expensive, decays fast.

**Publishing** (Ch 7) — build a **content release process** (when/who/where/tools/announce); ship docs **with** the code; one **final approver**; test the docs; **meet users where they are**; publish and iterate.

**Feedback** (Ch 8) — give users scalable channels, then **triage**: Valid? → Actionable (Original + Reproducible + Scoped)? → Priority (P0–P3)? Always follow up.

**Measuring quality** (Ch 9) — **functional quality** (Accessible, Purposeful, Findable, Accurate, Complete) outranks **structural quality** (the **3 Cs**: Clear, Concise, Consistent). Align org/reader/doc goals; baseline, contextualize, cluster metrics, mix qual+quant. Track **Time to Hello World (TTHW)**.

**Information architecture** (Ch 10) — **sequences / hierarchies / webs** (usually combined). Assess (Keep/Remove/Review/Merge/Split + content gaps) → card-sort → migrate with redirects. **Landing pages** route; **navigation cues** orient — both used sparingly.

**Maintenance & deprecation** (Ch 11) — the #1 failure cause. User impact analysis per change; release docs with the feature (Kubernetes model); assign **owners**; automate **toil** (freshness checks, link checkers, prose linters, ref generators); **deprecate** with callouts + migration guide, then **delete** with notice + redirects.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-understanding-your-audience.md) | Understanding your audience | curse of knowledge, personas, user stories, journey maps, friction log |
| [ch02](chapters/ch02-planning-your-documentation.md) | Planning your documentation | content types, use cases, documentation plan |
| [ch03](chapters/ch03-drafting-documentation.md) | Drafting documentation | audience/purpose/pattern, outline-as-pseudocode, writing for skimming, callouts |
| [ch04](chapters/ch04-editing-documentation.md) | Editing documentation | four editing passes, peer/technical review, plussing |
| [ch05](chapters/ch05-integrating-code-samples.md) | Integrating code samples | executable vs explanatory, ECCUT principles, tooling |
| [ch06](chapters/ch06-adding-visual-content.md) | Adding visual content | comprehension/accessibility/performance, diagram types, simplify-to-amplify |
| [ch07](chapters/ch07-publishing-documentation.md) | Publishing documentation | content release process, final approver, meet users where they are |
| [ch08](chapters/ch08-gathering-and-integrating-feedback.md) | Gathering & integrating feedback | feedback channels, triage, CSAT, user council |
| [ch09](chapters/ch09-measuring-documentation-quality.md) | Measuring documentation quality | functional vs structural, 3 Cs, TTHW, metric clusters |
| [ch10](chapters/ch10-organizing-documentation.md) | Organizing documentation | information architecture, sequences/hierarchies/webs, landing pages, card sorting |
| [ch11](chapters/ch11-maintaining-and-deprecating-documentation.md) | Maintaining & deprecating | user impact analysis, doc owners, toil automation, deprecation |
| [ch12](chapters/ch12-appendices-hiring-and-resources.md) | Appendices: hiring & resources | documentarian, Diátaxis, Good Docs Project, tool list |

## Topic Index

- **Accessibility** → ch06, ch09
- **API documentation / reference** → ch02, ch05, ch11
- **Callouts / warnings** → ch03
- **Card sorting** → ch10
- **Code samples** → ch05
- **Content types** → ch02
- **Curse of knowledge** → ch01
- **Deprecation / deletion** → ch11
- **Diagrams (boxes/flowcharts/swimlanes)** → ch06
- **Editing passes** → ch04
- **Feedback / triage** → ch08
- **Findability** → ch09, ch10
- **Friction log** → ch01
- **Functional vs structural quality / 3 Cs** → ch09
- **Getting started docs** → ch02
- **Information architecture** → ch10
- **Landing pages / navigation cues** → ch10
- **Maintenance / toil / automation** → ch11
- **Metrics / TTHW** → ch09
- **Outline / drafting** → ch03
- **Personas / user stories / journey maps** → ch01
- **Plussing / giving feedback** → ch04
- **Publishing / release process** → ch07
- **README** → ch02
- **Skimming / F-pattern** → ch03
- **Templates** → ch03
- **Tutorials vs how-to guides** → ch02
- **User research** → ch01
- **Video content** → ch06
- **When to hire / documentarian / resources** → ch12

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — decision rules, thresholds, tells & smells

---

## Scope & Limits

This skill covers the book's content only — a process-and-craft field guide for developer documentation. It is tool-agnostic by design; for specific tooling, combine with project-specific docs and the resources in ch12. For agile user-story depth, see related skills [[cohn-user-stories]] and [[crafting-user-stories]].
