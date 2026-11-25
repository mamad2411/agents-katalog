---
name: crafting-user-stories
description: "Knowledge base from \"The Art of Crafting User Stories\" by Christopher Lee. Use when applying Lee's frameworks for writing user stories, INVEST, the 3 Cs, acceptance criteria, personas/empathy maps, prioritization (MoSCoW, WSJF, RICE, Kano), story-point estimation/planning poker, story splitting, and backlog refinement — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# The Art of Crafting User Stories
**Author**: Christopher Lee (Packt, 2023) | **Pages**: ~192 | **Chapters**: 9 | **Generated**: 2026-06-26

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `INVEST`, `WSJF`, `story splitting`, `personas`, etc.; I read the relevant chapter.
- **With a chapter** — ask for `ch04`; I load that file.
- **Browse** — ask "what chapters do you have?" for the index.

When you ask about a topic not in Core Frameworks, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### Writing the story
- **Story template**: `As a [persona], I want [goal], so that [benefit].` If you can't state the "so that", it's not user-focused yet. If it's full of UI/tech detail, you lost the user — restart from the persona.
- **Three core components**: Persona (who) · Action (what) · Goal/benefit (why).
- **3 Cs** (Card, Conversation, Confirmation): the card is a *placeholder for a conversation*; confirmation = acceptance criteria. A story is not a spec.
- **INVEST** — accept a story only if it's **I**ndependent, **N**egotiable, **V**aluable, **E**stimable, **S**mall, **T**estable. Fails most often on Small (it's an epic → split) and Testable (no acceptance criteria → add them).
- **Acceptance criteria**: state observable, user-visible outcomes, not implementation. Without them you can't tell when a story is done.

### Knowing the user (Ch 2)
- **Persona** (research-based, aggregate, 1-page) fills the "As a..." slot — don't guess it.
- **Empathy map**: Says / Thinks / Feels / Does → surfaces the *why* behind behavior.
- **User journey map (CUJ)**: steps + emotions across touchpoints → finds friction.
- Pick research by question: **qualitative** (interviews) for depth, **quantitative** (surveys/analytics) for scale.

### Prioritizing (Ch 4)
- **MoSCoW**: Must / Should / Could / Won't — fast stakeholder alignment.
- **WSJF** = `(Business Value + Opportunity Enablement + Time Criticality + Risk Reduction) / Job Size` — highest first, for ROI/economic value.
- **RICE** = `Reach × Impact × Confidence / Effort`.
- **Kano**: Basic (must exist) · Performance (more=better) · Delight (differentiators). Cover basics, invest in delighters; delighters decay to expected over time.

### Estimating (Ch 4, Ch 6)
- **Story points** (relative effort, not hours) + **planning poker**: private pick → simultaneous reveal → discuss outliers → re-vote. Forecast with **velocity** (trust after ~3 sprints). A wide vote spread = hidden scope disagreement.

### Refining & splitting (Ch 6)
- **Story splitting** by: workflow steps · business rules · data variations · operations (CRUD) · UI/roles. Every slice must stay independently valuable — never split by tech layer.
- **DoR** gates entry to a sprint (clear, estimated, criteria, dependencies); **DoD**/criteria gate "done".
- **Backlog refinement** is continuous: clarify → split → estimate → re-order.

### Stakeholders (Ch 5)
- **Power/Interest matrix** & **salience model** to map and engage stakeholders; involve them in criteria, prioritization, and estimation. Story workshops + the **Three Amigos** (business, dev, test) beat solo-authored stories.

### Top anti-patterns
Writing epics as stories · dropping the user · no acceptance criteria · unprioritized backlog · solo authoring (no collaboration) · stereotype-based personas.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction-to-user-stories.md) | Introduction to User Stories | Story template, INVEST, Persona/Action/Goal |
| [ch02](chapters/ch02-understanding-the-user-perspective.md) | Understanding the User Perspective | Personas, Empathy map, Journey map, UCD, Design sprint |
| [ch03](chapters/ch03-writing-effective-user-stories.md) | Writing Effective User Stories | Story anatomy, Acceptance criteria, Job stories, 3 Cs |
| [ch04](chapters/ch04-prioritizing-and-estimating-user-stories.md) | Prioritizing & Estimating | MoSCoW, WSJF, RICE, Kano, story points |
| [ch05](chapters/ch05-working-with-stakeholders.md) | Working with Stakeholders | Power/Interest matrix, Salience model, workshops |
| [ch06](chapters/ch06-refinement-and-continuous-improvement.md) | Refinement & Continuous Improvement | DoR, Story mapping, Planning poker, splitting |
| [ch07](chapters/ch07-user-stories-in-practice.md) | User Stories in Practice | Creation pipeline, 3 Cs, TaskTracker case study |
| [ch08](chapters/ch08-expert-interviews.md) | Expert Interviews | Three Amigos, story-as-placeholder, completeness curve |
| [ch09](chapters/ch09-conclusion.md) | Conclusion | INVEST, 3 Cs, prioritization stack, DoD |

## Topic Index

- **3 Cs (Card/Conversation/Confirmation)** → ch03, ch07, ch09
- **Acceptance criteria** → ch01, ch03, ch06
- **Backlog refinement / DoR / DoD** → ch06
- **Design sprint** → ch02
- **Empathy map** → ch02
- **INVEST** → ch01, ch09
- **Job stories / Jobs-to-be-Done** → ch03
- **Kano model** → ch04
- **MoSCoW** → ch04, ch05
- **Personas** → ch01, ch02
- **Planning poker / story points / velocity** → ch04, ch06
- **Prioritization (overview)** → ch04, ch05
- **RICE** → ch04
- **Stakeholder mapping (Power/Interest, salience)** → ch05
- **Story mapping** → ch04, ch06
- **Story splitting** → ch06, ch07
- **Story template / anatomy** → ch01, ch03
- **Three Amigos** → ch08
- **User journey map (CUJ)** → ch02
- **User research** → ch02
- **WSJF** → ch04

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — every technique with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — decision tables: INVEST filter, which prioritization, how to split, anti-pattern smells

---

## Scope & Limits

Covers the book's content only. For hands-on backlog work, pair with your tracker (Jira/Linear/etc.). For deeper agile process beyond stories, see related skills (`cohn-user-stories`, `specification-by-example`, `programacao-extrema`).
