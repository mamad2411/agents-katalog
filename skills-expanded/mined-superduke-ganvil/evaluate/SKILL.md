---
name: evaluate
description: >
  Evaluate existing code using the ganvil evaluation framework. Automatically
  determines if the project is frontend, backend, or fullstack and applies the
  appropriate evaluator with four-dimension scoring. Use to QA-check any existing
  project or codebase.
argument-hint: "[frontend|backend|auto] optional description of what to focus on"
---

# Ganvil Evaluate — Standalone QA Evaluation

Evaluate an existing project or codebase using the ganvil evaluation framework, without requiring a prior plan or build.

## What to Do

1. Determine the project type:
   - If `$ARGUMENTS` starts with "frontend" or "backend", use that classification
   - Otherwise, examine the project structure to auto-detect:
     - Has `package.json` with frontend frameworks (React, Vue, Svelte, etc.) → FRONTEND
     - Has backend files (Python, Go, Rust, Java server code, `requirements.txt`, `Cargo.toml`, etc.) → BACKEND
     - Has both → evaluate as FULLSTACK (backend first, then frontend)

2. Create `ganvil-artifacts/` directory if it doesn't exist.

3. **For frontend evaluation**: Delegate to the **frontend-evaluator** agent.
   - The evaluator will start the application, interact via browser, and score on:
     - Design Quality (≥7 to pass)
     - Originality (≥7 to pass)
     - Craft (≥6 to pass)
     - Functionality (≥7 to pass)
   - Output: `ganvil-artifacts/frontend-evaluation.md`

4. **For backend evaluation**: Delegate to the **backend-evaluator** agent.
   - The evaluator will start the server, run tests, hit API endpoints, and score on:
     - API Correctness (≥7 to pass)
     - Data Integrity (≥7 to pass)
     - Code Quality (≥6 to pass)
     - Functional Completeness (≥7 to pass)
   - Output: `ganvil-artifacts/backend-evaluation.md`

5. **For fullstack evaluation**: Run both evaluators, backend first.

6. Summarize the evaluation results, highlighting:
   - Overall pass/fail per dimension
   - Critical bugs found
   - Top recommendations for improvement

## Usage

```
# Auto-detect project type and evaluate
/ganvil:evaluate

# Evaluate only the frontend
/ganvil:evaluate frontend

# Evaluate with focus
/ganvil:evaluate frontend focus on mobile responsiveness and accessibility

# Evaluate backend
/ganvil:evaluate backend focus on API error handling
```

## Note

This skill evaluates code as-is. It does not require a `ganvil-artifacts/spec.md` or sprint contracts — the evaluator will assess the project against general quality standards. However, if a spec exists from a prior `/ganvil:plan`, the evaluator will use it for more targeted evaluation.
