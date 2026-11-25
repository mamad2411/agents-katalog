---
name: study-guide
description: "Writes study guides with key concepts, review questions, memory aids, and exam preparation strategies."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Study Guide

## When to Use This Skill

Use this skill when you need to:
- Create a study guide that consolidates key concepts from a course or training
- Build review materials with questions, memory aids, and practice exercises
- Design exam preparation documents with study strategies and focus areas
- Produce reference sheets learners can use during and after a program

**DO NOT** use this skill for full course content, lesson plans, or assessments. This is a supplementary resource that helps learners review and retain what they have already been taught.

---

## Core Principle

A STUDY GUIDE IS A MAP, NOT A TEXTBOOK — IT TELLS LEARNERS WHAT MATTERS MOST, HOW TO REMEMBER IT, AND WHERE THEY ARE WEAKEST SO THEY CAN STUDY SMART, NOT JUST STUDY MORE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Subject matter** | "What course, module, or topic should this study guide cover?" | No default — must be provided |
| **Source material** | "Share the course outline, lesson notes, or key topics to include." | No default — must be provided |
| **Purpose** | "Is this for an exam, certification, self-review, or ongoing reference?" | Self-review |
| **Learner level** | "Are learners beginners, intermediate, or advanced in this topic?" | Intermediate |
| **Format preference** | "Do you want a structured document, flashcard set, or one-page cheat sheet?" | Structured document |

**GATE: Confirm the brief and receive source material before proceeding.**

---

## Phase 2: Organize

### Study Guide Structure

```
1. Overview — what the guide covers and how to use it
2. Key Concepts — organized by topic with definitions and examples
3. Frameworks and Models — visual summaries of key frameworks
4. Review Questions — self-test per topic area
5. Memory Aids — mnemonics, acronyms, and association techniques
6. Common Mistakes — what learners typically get wrong
7. Quick Reference — one-page cheat sheet of the most important points
```

### Topic Prioritization

Rank every topic as:
- **Must know** — core concepts tested or applied frequently
- **Should know** — important context that supports core concepts
- **Nice to know** — supplementary details that add depth

Focus 70% of the study guide on "must know" topics.

**GATE: Present the topic list with priority rankings for approval.**

---

## Phase 3: Write

### Key Concepts Section

For each concept:

```
### [Concept Name]
**Definition:** [One clear sentence]
**Why it matters:** [Business application in one sentence]
**Example:** [Concrete, real-world example]
**Remember:** [Memory aid — acronym, analogy, or association]
```

### Review Questions

Write 3-5 questions per major topic:
- Mix question types: definition recall, application scenarios, compare/contrast
- Include answers on a separate page or in a collapsible section
- Mark difficulty level (basic, intermediate, advanced)

```
**Q:** [Question text]
**Difficulty:** [Basic / Intermediate / Advanced]
**A:** [Answer]
**Why:** [Brief explanation of why this answer is correct]
```

### Memory Aids

For complex frameworks or multi-step processes, create:
- **Acronyms** — first-letter memory devices (e.g., AIDA for Attention, Interest, Desire, Action)
- **Analogies** — connect new concepts to familiar things
- **Visual maps** — describe a diagram or flowchart the learner can sketch
- **Chunking** — group related items into 3-5 categories

### Quick Reference Sheet

One page maximum with:
- Key definitions (10-15 max)
- Core formulas or frameworks
- Common mistakes to avoid
- Decision-making shortcuts

---

## Phase 4: Polish

### 1. Study Plan

Provide a recommended study schedule:

```
## Suggested Study Plan

**Day 1:** Read through key concepts (30 min)
**Day 2:** Answer review questions without looking at notes (20 min)
**Day 3:** Review wrong answers, revisit weak areas (20 min)
**Day 4:** Quiz a partner or recite key frameworks aloud (15 min)
**Day 5:** Review quick reference sheet only (10 min)
```

### 2. Self-Assessment Checklist

```
## Am I Ready?
- [ ] I can define all "must know" concepts without looking
- [ ] I can apply each framework to a real scenario
- [ ] I scored 80%+ on the review questions
- [ ] I can explain each concept to someone with no background
- [ ] I know which topics I am weakest on and have reviewed them twice
```

### 3. Quality Check

- Every "must know" topic has a concept entry, review question, and memory aid
- Review questions have complete answers with explanations
- Quick reference fits on one printable page
- No jargon is used without a definition provided earlier in the guide

---

## Example 1: Digital Marketing Fundamentals Study Guide

```
### Customer Acquisition Cost (CAC)
**Definition:** The total cost to acquire one new customer.
**Why it matters:** If CAC exceeds customer lifetime value, you lose money on every sale.
**Example:** Spent $500 on ads, got 10 customers = $50 CAC.
**Remember:** CAC = "Cash to Acquire a Customer"
```

## Example 2: Business Finance Basics Quick Reference

```
## Quick Reference
- Revenue - Expenses = Profit
- Gross Margin = (Revenue - COGS) / Revenue
- Break-even = Fixed Costs / (Price - Variable Cost per Unit)
- Rule of thumb: Keep CAC below 1/3 of LTV
```

---

## Anti-Patterns

- **Rewriting the entire course** — a study guide summarizes and reinforces, it does not reteach. Keep it concise.
- **No prioritization** — treating every topic equally means learners waste time on low-value details.
- **Questions without answers** — review questions are useless if learners cannot check their work.
- **Walls of text** — use tables, bullets, and formatting. Study guides must be scannable.
- **No memory aids** — definitions alone do not stick. Every core concept needs a hook for recall.
- **Skipping the quick reference** — the one-page cheat sheet is often the most-used part of the entire guide.

---

## Recovery

- **No source material provided:** Ask the user to list the 10 most important topics from memory. Build the guide from that list.
- **Too many topics:** Enforce the must/should/nice framework. Cut "nice to know" topics entirely if the guide exceeds 10 pages.
- **User wants flashcards only:** Create Q&A pairs in a format compatible with Anki or Quizlet (front/back format).
- **Subject matter is highly technical:** Add a glossary section at the top with all specialized terms defined before diving into concepts.
