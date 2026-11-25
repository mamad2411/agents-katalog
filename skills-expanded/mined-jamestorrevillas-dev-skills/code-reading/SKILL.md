---
name: code-reading
description: Use this skill when navigating unfamiliar codebases, understanding legacy code, onboarding to a new project, or reverse-engineering how something works. Trigger on keywords: unfamiliar code, legacy code, understand this codebase, how does this work, new project, onboarding, read code, trace through, what does this do.
---

# Code Reading

## Core Principle
Code is read 10x more than it's written. Reading code is a skill you actively develop — not a passive activity.

---

## Codebase Onboarding Order

Always explore a new codebase in this order:
1. **README** — What does it do? How do I run it?
2. **Package/dependency files** — What tools and frameworks are used?
3. **Entry point** — Where does execution start? (main.ts, index.js, app.py)
4. **Core domain models** — What are the main data structures?
5. **Key user flows** — Trace one important feature end-to-end
6. **Tests** — Tests reveal intended behavior and edge cases
7. **Config/env files** — What is configurable? What are the environments?

---

## Code Tracing Method

For understanding a specific flow:
```
1. Start from the trigger (user action, API call, scheduled job)
2. Follow the execution path step by step
3. Note: what data flows in? what comes out?
4. Identify where external systems are called
5. Mark where business logic lives vs. infrastructure
```

---

## Questions to Ask While Reading

- What is this component responsible for? (single responsibility check)
- What does it need to run? (dependencies)
- What does it produce/return?
- What could make it fail?
- Why was it written this way? (check git blame/history for context)

---

## Using AI for Code Reading

```
"Explain what this function does, including:
- What it takes as input
- What it returns  
- Any side effects
- Non-obvious behavior I should know about"

"Walk me through how [feature] works, 
starting from [entry point] to [output]"

"What would I need to understand to safely 
modify [specific part] of this code?"
```

---

## Navigating Large Codebases

- **Search patterns** — use grep/ripgrep to find usages of a function/class
- **Git blame** — who changed this and why?
- **Git log** — when was this introduced? what changed over time?
- **Tests** — run tests while reading to see what behavior is expected
- **Dependency graph** — which modules depend on what?

---

## Warning Signs While Reading

- Functions longer than 50 lines (doing too much)
- Deep nesting (> 3 levels) — logic is hard to follow
- Many parameters (> 4) — likely needs refactoring
- Comments explaining WHAT (should be obvious) vs WHY (actually useful)
- No tests — higher risk, be extra careful when modifying
