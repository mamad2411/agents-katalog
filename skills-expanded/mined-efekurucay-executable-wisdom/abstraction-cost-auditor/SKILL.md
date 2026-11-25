---
name: abstraction-cost-auditor
description: Review code, refactors, helpers, services, repositories, APIs, modules, design patterns, and architecture decisions through the cost of abstraction. Use when asked whether code should be modularized, abstracted, extracted, simplified, inlined, generalized, refactored, or when reviewing overengineering, clean code, reusable code, contracts, layers, or architecture.
---

# Abstraction Cost Auditor

## Purpose
Use this skill to decide whether a proposed abstraction is actually useful or whether it only makes the local code look cleaner while increasing global complexity.

The core philosophy:

- Mental abstraction is good: it helps the engineer move between levels of detail.
- Code abstraction is not automatically good: it must pay for itself.
- Every interface creates a contract.
- Every contract has maintenance, testing, cognitive, runtime, and debugging cost.
- Reuse is not free. Generality is not free. Layers are not free.

## When to use this skill
Use this skill for requests like:

- “Bunu modüler yapmalı mıyım?”
- “Bu helper mantıklı mı?”
- “Bu architecture enterprise mı?”
- “Bu soyutlama fazla mı?”
- “Bu service/repository/controller ayrımı doğru mu?”
- “Bu kodu refactor eder misin?”
- “Clean code açısından incele.”
- “Pattern doğru mu?”
- “Bunu reusable yapalım mı?”
- “Bunu tek yerde toplamak iyi fikir mi?”

## Non-negotiable principles

1. Do not praise abstraction just because it looks clean.
2. Do not reject abstraction just because it adds a layer.
3. Always compare **local simplification** against **global cost**.
4. Always identify the contract created by the abstraction.
5. Always ask: “What real variation is this abstraction protecting us from?”
6. Prefer concrete code paths over theoretical flexibility.
7. Prefer domain vocabulary over generic technical wrappers.
8. Do not recommend a pattern unless the problem shape actually needs it.
9. If the abstraction is only used once, it needs a stronger reason than reuse.
10. If the abstraction hides important runtime behavior, treat that as a risk.

## Review process

### 1. Identify the abstraction boundary
Find what is being hidden behind a name, interface, method, component, helper, module, service, hook, repository, DTO, adapter, pipeline stage, or prompt layer.

Answer:

- What is the caller allowed to know?
- What is the callee hiding?
- What assumptions cross the boundary?
- What state, data, errors, timing, or side effects are now invisible?

### 2. Separate mental abstraction from code abstraction
Classify the change:

- **Mental abstraction only:** a diagram, naming improvement, explanation, comment, grouping, or conceptual model.
- **Code abstraction:** a new method, class, interface, generic, layer, wrapper, dependency, service, pipeline, or framework boundary.

Mental abstraction can be encouraged freely. Code abstraction must be audited.

### 3. Run the “inline experiment” mentally
Pretend the abstraction is removed and its implementation is placed directly at the call site.

Look for:

- duplicate null checks
- duplicate validation
- duplicate error handling
- duplicate mapping
- branches that never apply in this call path
- generic options that are unused
- parameters that exist only for imaginary future callers
- tests that exist only because the abstraction boundary exists
- naming that is clearer at the call site than inside the abstraction

If inlining makes the real behavior easier to understand, the abstraction is suspicious.

### 4. Audit the contract
For every abstraction, describe the contract in plain language:

- Inputs
- Valid states
- Invalid states
- Output
- Errors
- Side effects
- Ownership/lifetime
- Sync/async behavior
- Security assumptions
- Performance assumptions

Then classify each part:

- **Explicit in code**: enforced by type, validation, or test.
- **Implicit in developer’s head**: risky.
- **Duplicated across layers**: possible abstraction tax.
- **Unclear**: likely future bug.

### 5. Check whether the abstraction pays rent
An abstraction is usually justified when at least one is true:

- There are multiple real call sites with meaningful shared behavior.
- The boundary protects a volatile dependency.
- The boundary encodes a real domain concept.
- The boundary improves testability of important behavior.
- The boundary separates different rates of change.
- The boundary prevents security or data integrity mistakes.
- The boundary enables a pipeline where stages can be independently inspected.
- The boundary makes the next likely change easier, not just an imaginary change.

An abstraction is suspicious when:

- It is created only because “clean code says so.”
- It hides a simple operation behind a generic name.
- It introduces a layer that mirrors another layer exactly.
- It creates DTOs that copy the same shape without semantic value.
- It turns one obvious flow into many files.
- It makes debugging require jumping through many locations.
- It needs many tests for behavior that used to be obvious.
- It is generic before there are real variants.

### 6. Evaluate the LLM risk
When code is AI-generated, be extra suspicious of:

- impressive but unnecessary layers
- generic abstractions with no real callers
- invented architectural conventions
- duplicated validation in multiple files
- wrappers around wrappers
- “enterprise-looking” structure with weak domain meaning
- abstractions that make the diff bigger but the behavior unchanged

Ask the assistant to prove the abstraction through concrete call paths, not through style arguments.

## Output format

Always answer in this order:

### Verdict
One of:

- Keep the abstraction
- Simplify the abstraction
- Inline it
- Split it
- Delay the abstraction
- Add an abstraction
- Not enough evidence

Add a one-sentence reason.

### Abstraction Boundary
- What is hidden:
- Who calls it:
- What contract it creates:
- What behavior becomes harder to see:

### Local Win vs Global Cost
| Local simplification | Global cost |
|---|---|
|  |  |

### Contract Audit
| Contract item | Explicit / implicit / duplicated / unclear | Risk |
|---|---|---|
|  |  |  |

### Inline Experiment
Explain what would happen if the abstraction were inlined. Mention which lines/checks/branches might disappear.

### Recommendation
Give the smallest practical change.

### Better Shape
Show a proposed structure, naming, or code sketch only if useful.

### Test / Verification Notes
List what should be tested and what can be safely left untested.

## Style rules

- Be direct and engineering-focused.
- Prefer Turkish unless the user writes in English.
- Avoid generic clean-code slogans.
- Use concrete names from the user’s code.
- If code is missing, still reason from the described shape and clearly mark assumptions.
- Do not over-optimize. The goal is clarity with justified boundaries.

## Example

### Input
“Login API için AuthService, AuthManager, AuthRepository, AuthMapper ve LoginResult DTO oluşturdum. Enterprise mı?”

### Output shape

### Verdict
Simplify the abstraction. The login flow has real security boundaries, but five layers may be hiding a single critical path.

### Abstraction Boundary
- What is hidden: credential validation, user lookup, cookie/session creation, error mapping.
- Who calls it: AuthController or Auth API endpoint.
- What contract it creates: valid credentials in, authenticated session or typed failure out.
- What behavior becomes harder to see: which layer owns lockout, cookie creation, and failed-login logging.

### Local Win vs Global Cost
| Local simplification | Global cost |
|---|---|
| Controller looks clean | Debugging jumps through five files |
| Mapper standardizes response | DTO may only mirror one use case |
| Repository hides SQL | Auth-specific security rules may be split from the flow |

### Recommendation
Keep one explicit boundary: `AuthService.LoginAsync`. Delay `AuthManager` and `AuthMapper` unless there are real alternate login flows.
