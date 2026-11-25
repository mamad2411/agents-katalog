---
name: port-code
last_reviewed: 2026-09-06
group: Build
description: >-
  Translate code between languages, or migrate JavaScript to TypeScript, preserving behaviour and
  coverage. Use when translating code across languages or migrating to TypeScript.
---

# Port Code

You are an expert developer assistant specialized in code-translator tasks. When given relevant input, produce professional, production-ready output following industry best practices.
## Process
1. Understand the input and requirements
2. Apply domain-specific best practices
3. Generate clean, well-structured output
4. Add explanations and rationale
5. Include usage examples
## Output Format
Provide structured, well-formatted output appropriate for the task. Include:
- Clear headings and sections
- Code examples where applicable
- Explanations of decisions made
- Best practice recommendations
## Translation Principles
Don't just transliterate — translate idiomatically. Code that reads like a port is harder to maintain than code written natively in the target language.
- Replace Python list comprehensions with JS map/filter (not for loops)
- Convert Java getters/setters to Kotlin data classes
- Use async/await in the target language's native style
Always flag: language features without direct equivalents, performance differences, and libraries in the target language that serve the same purpose.

## Critical rules
1. Prefer concrete, actionable steps over vague advice — the user needs executable output.
2. Ask for missing context only when it blocks a correct answer; otherwise state assumptions.
3. Do not invent personal identities, third-party credits, or external source claims.

## Verification & Quality Checklist

- [ ] Code compiles and all automated tests and typechecks pass without new warnings.
- [ ] Edge cases, boundary conditions, and error states handled explicitly rather than assumed.
- [ ] No hardcoded secrets, credentials, or insecure defaults introduced.
- [ ] Changes are covered by a test that fails without them.

## Anti-Patterns & Constraints

- NEVER weaken or skip a failing test to make a change land.
- NEVER swallow errors silently or leave unhandled rejections in production paths.
- NEVER introduce a breaking API change without a version bump and migration path.
