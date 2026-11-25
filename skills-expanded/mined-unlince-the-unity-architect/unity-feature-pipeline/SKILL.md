---
name: unity-feature-pipeline
description: Comprehensive workflow for conceiving, documenting, and implementing new features in Unity. Enforces a design-first approach with three mandatory phases.
---

# Skill: Unity Feature Pipeline (Product Architect)

The complete workflow for conceiving, documenting, and implementing new features and systems in Unity. Use ALWAYS when the user proposes building something new. This skill prevents "spaghetti code" by forcing design before programming, using a component-oriented approach and maintaining a real-time Ubiquitous Language Glossary.

---

## ⚖️ The Iron Laws

As an AI agent, you are FORBIDDEN from writing implementation code if the design and breakdown phases have not been completed.

1. **Zero Premature Code:** Do not propose C# classes until Phase 3 (Issue Slicer) is finished.
2. **Component-Based Architecture:** All features must be sliced into small, isolated components.
3. **Mandatory Execution Order:** You must follow these phases in strict order.

---

## 🔬 Pipeline Phases (Routing)

Guide the user through these phases in order. Read the corresponding sub-modules to execute each phase.

### Phase 1: Requirement Gathering (The Grill)
Before accepting a vague idea, you must ask the hard questions to discover edge cases.
* 👉 **Read `01-quest-giver.md` for the strict interrogation protocol.**

### Phase 2: Design Documentation (The GDD)
Once doubts are resolved, consolidate the information into a Design Document (PRD/GDD) that acts as a contract.
* 👉 **Read `02-gdd-writer.md` for the documentation template.**

### Phase 3: Task Breakdown (The Issue Slicer)
With the GDD approved, translate the document into atomic and vertical technical tasks (Issues).
* 👉 **Read `03-issue-slicer.md` for the issue creation rules.**

### Phase 4: Implementation (Architecture & Coding)
Only when the user selects a specific Issue to begin, can you start writing code. At that moment, leave this pipeline and proceed with the architecture standard.
* 👉 **Switch to `unity-architecture-and-best-practices` for implementation.**

---

## 🛑 STRICT SYSTEM DIRECTIVE

If the user makes a vague or general request for a new system, IMMEDIATELY START PHASE 1 by reading `01-quest-giver.md`. DO NOT proceed to write scripts until the entire pipeline is complete and a specific Issue has been selected.
