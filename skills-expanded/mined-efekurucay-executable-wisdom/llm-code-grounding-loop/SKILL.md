---
name: llm-code-grounding-loop
description: Ground AI-generated code, refactors, architectural suggestions, and implementation plans in real project constraints. Use when working with LLMs on coding tasks, asking an assistant to implement features, reviewing AI-generated code, preventing hallucinated architecture, translating vague requirements into code, or forcing the assistant to reason across requirement, API, runtime, data, and failure layers.
---

# LLM Code Grounding Loop

## Purpose
Use this skill when an LLM is helping write or change code. Its job is to prevent “beautiful but floating” AI output: code that sounds architectural, looks clean, but is not grounded in the actual repo, runtime, data flow, framework conventions, or failure modes.

This skill adapts the old hardware/abstraction lesson to the LLM era:

- The new abstraction layer is natural language.
- The LLM can generate plausible code without understanding the real platform.
- Therefore every LLM-produced solution must move up and down abstraction levels before it is trusted.

## Core philosophy

- Do not accept code because it sounds senior.
- Do not accept architecture because it looks enterprise.
- Do not let the LLM stay at the “idea” level.
- Force the assistant to name the concrete files, call paths, data shapes, contracts, runtime behavior, and verification steps.
- Natural language is now part of the programming interface; treat prompts like contracts.

## When to use this skill
Use this skill for requests like:

- “Bu görevi AI’ya yaptıracağım, prompt hazırla.”
- “LLM’in yazdığı kodu kontrol et.”
- “Bu implementasyon doğru mu?”
- “Bunu nasıl yaptırmalıyım?”
- “AI çok fazla dosya değiştirdi, mantıklı mı?”
- “Bu mimari hallucination mı?”
- “Feature implement plan çıkar.”
- “Refactor yaptıracağım ama saçmalamasın.”
- “Kodlama sürecimde bana yardımcı olacak skill istiyorum.”

## The grounding ladder
Every solution must be checked across these levels:

1. **User intent level**: What is the actual business/user problem?
2. **Product behavior level**: What should the user see or experience?
3. **API/contract level**: What inputs, outputs, errors, permissions, and states exist?
4. **Project pattern level**: How does this repo already solve similar problems?
5. **Runtime level**: What actually runs? Browser, server, MVC action, API route, background job, DB transaction, cloud function?
6. **Data level**: What tables, DTOs, objects, JSON, files, cache keys, or tokens move through the system?
7. **Failure level**: What can break? Empty data, invalid state, permission, network, concurrency, timeout, duplicate submit, partial write?
8. **Verification level**: How do we prove it works?

## Process

### 1. Restate the task as a contract
Before writing code, state:

- Goal
- Inputs
- Outputs
- Non-goals
- Constraints
- Existing patterns to follow
- Files likely affected
- Risks

If the user already gave this information, do not ask again. Use it.

### 2. Inspect the existing architecture mentally or from provided code
Before proposing a new layer, identify:

- existing folder conventions
- existing naming conventions
- existing API/client patterns
- existing auth/session/error patterns
- existing database access style
- existing UI/component style

If this is unknown, explicitly mark it as unknown and avoid inventing conventions.

### 3. Prefer minimal grounded change
Default to the smallest change that fits the existing project.

Reject AI overproduction:

- unnecessary managers/services/factories
- duplicate DTOs
- generic wrappers
- invented folders
- broad refactors while implementing a narrow feature
- rewriting working architecture to match a blog-post pattern

### 4. Force a call-path trace
For every proposed implementation, produce a trace like:

`User action → UI handler → API/client call → controller/route → service/use case → database/external dependency → response → UI state`

If a step is missing, the implementation is not grounded.

### 5. Force a data-shape trace
Name the exact shapes:

- request body
- response body
- DTO/entity/table fields
- validation rules
- error shape
- loading/success/error UI state

### 6. Force a failure-mode pass
Check:

- invalid input
- unauthenticated user
- unauthorized user
- missing row
- duplicate request
- expired token/session
- DB failure
- network failure
- race condition
- stale UI state
- partial success

Only include relevant failures. Do not bloat.

### 7. Force verification
Every final answer should include:

- manual test steps
- automated tests if useful
- commands to run if known
- what to inspect in logs/network/database
- rollback/safety notes if risky

## Output format

### Grounded Implementation Contract
- Goal:
- Non-goals:
- Existing pattern to follow:
- Likely files:
- Main risk:

### Abstraction Ladder Check
| Level | Decision |
|---|---|
| User intent |  |
| Product behavior |  |
| API/contract |  |
| Project pattern |  |
| Runtime |  |
| Data |  |
| Failure |  |
| Verification |  |

### Call Path Trace
Write the concrete path in one line.

### Data Shape Trace
List request, response, entity/DTO, and error shapes.

### Minimal Change Plan
Numbered implementation steps.

### Anti-Hallucination Checks
List anything the assistant must not invent.

### Verification
Manual and automated checks.

## Prompting rules for LLM-assisted coding
When creating prompts for another AI coding agent, always include:

1. The exact goal.
2. The existing pattern to inspect first.
3. The files/modules likely involved.
4. The instruction to avoid broad refactors.
5. The instruction to preserve behavior not mentioned.
6. The call-path trace requirement.
7. The verification requirement.
8. The output/diff expectations.

## Style rules

- Be skeptical but productive.
- Prefer Turkish unless the user writes in English.
- Do not ask for confirmation when the user has already given enough context.
- Do not invent repo facts. Mark assumptions.
- Act like a senior reviewer sitting next to the developer.

## Example prompt this skill might generate

```text
You are working in an existing codebase. First inspect the current pattern for similar CMS API + React UI flows. Implement only the password reset request flow.

Goal:
- User enters email.
- API creates a single-use reset token record.
- Raw token is never stored.
- UI shows a safe success message regardless of whether the email exists.

Constraints:
- Follow existing controller/API/client/query-key patterns.
- Do not introduce new architecture layers unless the existing project already uses them.
- Do not refactor unrelated auth code.
- Preserve existing cookie/session behavior.

Before coding, output:
1. Existing pattern found
2. Call path trace
3. Data shape trace
4. Files you will edit
5. Risks

After coding, output:
1. Summary of changes
2. Manual test steps
3. Any assumptions
```
