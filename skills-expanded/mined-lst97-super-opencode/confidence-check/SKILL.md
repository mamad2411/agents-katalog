---
name: confidence-check
description: Pre-execution risk assessment to prevent hallucinations and architectural drift.
---

# Confidence Check Skill

## Purpose

To calculate a probabilistic "Success Score" (0.0 - 1.0) **before** generating code. This acts as a circuit breaker for the `execution` mode.

**ROI Metric**: A 200-token analysis prevents 2,000+ tokens of incorrect code generation and subsequent debugging time.

## When to Use

- **Automatic Trigger**: Before any `write_file` operation affecting > 50 lines of code.
- **Manual Trigger**: When requirements are vague (e.g., "Fix the bug").
- **Agent Handoff**: When `pm-agent` assigns a task to `backend` or `frontend`.

## The 5 Pillars of Confidence

| Pillar | Weight | Verification Action | Related Agent |
| :--- | :--- | :--- | :--- |
| **1. Context Awareness** | 25% | Have I read *all* related files? (grep/read_file) | `pm-agent` |
| **2. Specification** | 25% | Do I have a clear Interface/Schema? (Zod/Types) | `architect` |
| **3. Ground Truth** | 20% | Do I have *current* docs? (No hallucinations) | `researcher` |
| **4. Pattern Matching** | 15% | Does this match existing project style? | `review` |
| **5. Impact Analysis** | 15% | Do I know what this might break? | `quality` |

## Scoring & Protocols

### 🟢 High Confidence (≥ 0.90)

**Action**: **PROCEED** to `execution` mode.
- *Definition:* You have the file paths, the schema is defined, you have verified the library version, and you have a rollback plan.

### 🟡 Medium Confidence (0.70 - 0.89)

**Action**: **REFINE** before coding.
- *Protocol:* Identify the weak pillar and fix it.
  - *Weak Docs?* -> Trigger `researcher` to fetch API refs.
  - *Weak Specs?* -> Trigger `architect` to define the interface.
  - *Weak Context?* -> Run `grep` to find usages.

### 🔴 Low Confidence (< 0.70)

**Action**: **HALT**.
- *Protocol:* Do not write code. Return control to `pm-agent` or ask the user clarifying questions.
  - *Example:* "I cannot proceed. I do not know the expected return type of the API, and I cannot find a design pattern for this module."

## Execution Template

*Copy this mental scratchpad into your context window before coding.*

```markdown
## 🛡️ Pre-Flight Confidence Check

### 1. Context Audit (25%)
- [ ] Mapped dependency tree? (Yes/No)
- [ ] Checked for duplicate logic via `grep`? (Yes/No)
- **Score: __ / 0.25**

### 2. Spec Validation (25%)
- [ ] Is the Input/Output clearly typed (TypeScript/Zod)?
- [ ] Does an ADR or RFC exist for this?
- **Score: __ / 0.25** -> *If 0, consult `architect`*

### 3. Documentation Reality (20%)
- [ ] Did I look up the library docs *today*?
- [ ] Am I guessing the API syntax?
- **Score: __ / 0.20** -> *If 0, consult `researcher`*

### 4. Local Patterns (15%)
- [ ] Am I using the project's established styling/naming?
- **Score: __ / 0.15**

### 5. Risk Assessment (15%)
- [ ] If this fails, does the app crash or just error out?
- [ ] Do I have a test case ready to verify this?
- **Score: __ / 0.15** -> *If 0, consult `quality`*

### 🏁 Final Score: [ 0.00 - 1.00 ]
**Verdict:** [ PROCEED / REFINE / HALT ]
```

## Scenario Examples

### Scenario A: Adding a new API Endpoint

* **Context**: Read `server.ts`? Yes.
- **Spec**: No request schema defined. (**0**)
- **Docs**: Know Express well. (0.2)
- **Pattern**: Copied existing controller style. (0.15)
- **Risk**: Low. (0.15)
- **Total**: **0.75 (Medium)**
- **Action**: *STOP. Call `backend` agent to define Zod schema first. Then Proceed.*

### Scenario B: "Fix the white screen"

* **Context**: No error logs provided. (**0**)
- **Spec**: Unknown. (**0**)
- **Docs**: N/A.
- **Total**: **0.15 (Low)**
- **Action**: *HALT. Ask user for logs or reproduction steps. Trigger `brainstorming` mode.*
