---
description: 
globs: 
alwaysApply: true
---
# 👨‍💻 Developer Communication & Implementation Guidelines

This document outlines explicit expectations and rules for the coding agent assigned to the Doctor CRM project. These are non-negotiable practices to ensure alignment, consistency, and clarity throughout the build process.

---

## 📌 1. Avoid Independent Assumptions

**Do not make assumptions or take unilateral decisions.**

* If there’s a missing piece of information or ambiguity in the requirements, **pause** and **escalate the question**.
* Always **discuss** with me (the product owner) before proceeding with your own understanding.
* Example: If a field label is missing or a status transition seems ambiguous, confirm with me rather than guessing.

> ✅ Rule: *When in doubt, ask before you code.*

---

## ⚖️ 2. Discuss Trade-offs Before Choosing Between Multiple Approaches

If you encounter multiple possible ways to implement a feature:

* Do **not pick one by default**.
* Instead, list the approaches and explain their **pros, cons, and technical trade-offs**.
* Then **present them to me** for discussion and decision.

> ✅ Rule: *Every architectural or UX/UI choice that has alternatives should go through approval.*

---

## ❓ 3. Ask if You Are Uncertain About Architecture or Design Decisions

* If you are unsure about a flow, interaction pattern, data structure, API shape, or architectural component — **do not assume or pick randomly**.
* Ask for clarification or propose an idea and request feedback.
* It's perfectly okay to not know something — but it is **not okay to decide alone**.

> ✅ Rule: *No decision is better than the wrong decision — until reviewed.*

---

## 🎨 4. Follow the Provided Frontend & Backend Specifications Religiously

### ✅ Frontend:

* Follow the **design system** as documented:

  * Use **shadcn** and **Tailwind CSS** only.
  * Implement **spacing**, **typography**, **glassmorphism**, and **component structure** as defined.
  * Do not introduce any custom styling, colors, or components unless explicitly approved.
* Use only approved **fonts**, **icons**, and **patterns**.
* Maintain **minimalist aesthetic** throughout.
* Do not use Typescript anywhere in the project. Use javascript only

### ✅ Backend:

* Follow the **schema**, **API contracts**, and **folder structure** exactly as defined.
* Do not rename, restructure, or re-architect anything.
* Implement API routes, field names, and response structures to spec.

> ✅ Rule: *Deviation = Discussion + Approval. No silent changes.*

---

## 🧪 Summary Checklist

| Principle                   | Required Action                  |
| --------------------------- | -------------------------------- |
| Missing info                | Ask the product owner            |
| Multiple possible solutions | Discuss trade-offs before coding |
| Architecture unclear        | Ask before deciding              |
| Frontend/Backend specs      | Follow exactly — no deviation    |

By following these principles, you help ensure that the build is accurate, collaborative, and free from rework. These practices are not only encouraged — they are **mandatory**.
