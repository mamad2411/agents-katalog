---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

---

This is the lightweight, no-dependencies grilling option — use it for early, raw ideation before any domain docs exist. Once the project has a domain glossary or ADRs under `.context/`, prefer **grill-with-docs**, which additionally challenges the plan against that documented language and captures resolved terms and decisions as you go.

When a grilling session has hardened an idea into something worth building, hand it to **to-prd** to write it up as a PRD under `.context/prd/`, then **to-issues** to slice it into iudex tickets.
