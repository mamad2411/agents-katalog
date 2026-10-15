---
name: application-lifecycle-trace
description: "Show case application lifecycle"
tools:
  [vscode, execute, read, agent, edit, search, web, browser, neon/search, todo]
---

#### **Title: PRD Generation**

#### **Guardrails**

- Trace only flows supported by source, docs, tests, or explicit user context.
- Label inferred lifecycle steps as assumptions.
- Keep the trace focused on primary flows. Do not add speculative components.
- Do not modify source code.

**User Story:** _As a developer, I want to provide a high-level feature idea and receive a structured, unambiguous PRD so that a junior developer can implement it with minimal oversight._

---

#### **Layer 1: User Journey (Flowchart)**

---

#### **Layer 2: Component Architecture**

| Component                   | Logic Source      | Responsibility                         | Key Reference      |
| --------------------------- | ----------------- | -------------------------------------- | ------------------ |
| **User Interface**          | System Prompt     | Capture intent and selections          | `Prompt Entry`     |
| **Clarification Processor** | `Rule: Process`   | Generate lettered/numbered questions   | `PRD Mode: Step 2` |
| **Generation Engine**       | `Rule: Structure` | Format data into standard PRD sections | `PRD Structure`    |
| **Storage Manager**         | `Rule: Output`    | Write Markdown to specific directory   | `/tasks/prd-*.md`  |

---

#### **Layer 3: Sequence Diagram**

**Key Design Patterns Used:**

1. **Stateful Interaction:** The system pauses for user feedback (Clarification Step) before proceeding to final generation, ensuring accuracy.
2. **Template Method:** The PRD follows a rigid, predefined structure regardless of the feature content to ensure consistency.
3. **Persistence Ignorance:** The logic focuses on document structure, while the storage rule dictates the final file path and naming convention.

---

#### **Data Structures**

---

#### **Quick Reference**

- **Event Triggers:** User prompt containing "new feature" or "PRD".
- **File Format:** Standard GFM (GitHub Flavored Markdown).
- **Error Handling:** If requirements are ambiguous, the AI **must** re-trigger the clarification loop.
- **Validation:** Final PRD must be legible by a "Junior Developer" profile.

---

#### **Related Lifecycles**

1. **Task Decomposition:** Converting a PRD into a `tasks-prd-*.md` file.
2. **DAP Implementation:** Creating a Deployment Action Plan for schema changes.
3. **System Onboarding:** Generating `use_cases.md` from repo analysis.

---

**Next Step:** I can now save this lifecycle trace to `.planning/memory/system/001_lifecycle_prd_generation.md`. Would you like me to finalize the file creation?
---

> **Install:** ``npx skills add ChristopherAlphonse/calphonse-skills --skill application-lifecycle-trace``
