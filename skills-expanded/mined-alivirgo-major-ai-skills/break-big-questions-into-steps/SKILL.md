---
name: break-big-questions-into-steps
description: "Divide a complex question into manageable subtasks with clear dependencies and intermediate results."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["task-decomposition", "milestones", "step-wise-execution", "workflow", "productivity", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Break Big Questions Into Step-Wise Milestones (AI Skill)

## Overview
Asking an AI to execute a massive monolithic request in a single prompt (*"Write a complete multi-tenant SaaS application with Stripe billing, PostgreSQL, and React"*) causes **context saturation**. The model quickly runs out of output tokens, truncates code, skips critical error handling, and hallucinates dependencies.

The **Step-Wise Milestone Decomposition Framework** breaks overwhelming projects into sequential, verified atomic phases - ensuring maximum code quality, architectural coherence, and total human control.

---

## Monolithic Megaprompt vs. Milestone Execution

```
┌─────────────────────────────────────────────────────────────┐
│                 Monolithic vs. Step-Wise Flow               │
│                                                             │
│  Monolithic Prompt ("Build the entire app now"):            │
│  • Token exhaustion $\rightarrow$ truncated code files      │
│  • Skipped error handling and placeholder comments          │
│  • If a bug occurs at step 1, the entire app fails          │
│                                                             │
│  Step-Wise Execution (3-Milestone Gate):                    │
│  Phase 1: Architecture & Data Schema (Review & Approve)     │
│       │                                                     │
│  Phase 2: Core Backend Logic & API Routes (Test & Validate) │
│       │                                                     │
│  Phase 3: Frontend Integration & UI State (Polish)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Step-Wise Prompt Templates

### Pattern 1: The Milestone Roadmapper
Use this at the very beginning of any large project:

```markdown
I want to build / create [MASSIVE PROJECT].

Do NOT start generating the final code or content yet.
Step 1: Break this entire project down into 3 to 4 sequential, self-contained milestones.
For each milestone, define:
- Objective
- Deliverable
- Definition of Done (how we verify it works before moving to the next milestone)

Conclude by asking for my approval on Milestone 1.
```

---

### Pattern 2: The Gated Execution Prompt
Use this to advance through the project sprint-by-sprint:

```markdown
Milestone [X] is approved. 

Now, execute ONLY Milestone [X+1]: [NAME OF PHASE].
- Focus 100% of your output on this specific deliverable.
- Do not jump ahead to subsequent phases.
- Include full, production-ready code with complete error handling (no placeholders).
```

---

## Real-World Case Study

### Scenario: Creating an Automated Customer Email Drip Campaign

#### Monolithic Failure (Low Quality)
> **Prompt**: *"Write a complete 5-email onboarding sequence, the Zapier integration webhook logic, and the conversion tracking analytics schema for our app."*
>
> ❌ *Result: AI spits out five 30-word email drafts, a half-written Python webhook snippet with syntax errors, and runs out of tokens before finishing the analytics schema.*

#### Step-Wise Decomposition Success
> **Prompt**: *"We are building an automated onboarding email funnel. Let's break this into 3 phases: 1) Strategy & Triggers, 2) Copywriting, 3) Webhook automation. Start with Phase 1 only."*

**AI Phase 1 Deliverable**:
- Defines the 5 behavioral trigger events (e.g., `UserSignedUp`, `ProfileCompleted`, `FirstActionTaken`, `InactiveFor3Days`).
- Maps the delay timing and goals for each email.

**User Feedback**: *"Strategy approved. Now write the exact copy for Email 1 (`UserSignedUp`) only. Friendly, under 120 words."*

**Outcome**: Every component is polished, tested, and tailored without hitting token limits or losing quality.

---

## The Rule of 3 Decomposition Matrix

| Project Type | Milestone 1 | Milestone 2 | Milestone 3 |
| :--- | :--- | :--- | :--- |
| **Software Feature** | Database Schema & API Contract | Backend Route & Business Logic | Frontend UI & Error States |
| **Comprehensive Report** | Executive Outline & Data Sources | Chapter Drafting & Analysis | Final Synthesis & Slide Deck |
| **Marketing Campaign** | Customer Persona & Core Hook | Creative Copy & Asset Drafting | Distribution & Ad Placement |
