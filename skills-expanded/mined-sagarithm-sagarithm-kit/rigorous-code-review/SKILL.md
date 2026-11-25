---
id: "quality.code-review-and-quality"
name: "Rigorous Code Review & Quality Defense"
version: "1.2.0"
domain: "quality"
description: "Applies senior-engineer scrutiny to all code modifications. Enforces architectural fitness, zero-leak secret defense, minimal blast radius, and anti-rationalization pushback."
triggers:
  - "Reviewing pull requests or uncommitted changes"
  - "Pre-flight inspection before running verification gate"
  - "User asks to review code quality, security, or architecture"
---

# 🔍 Rigorous Code Review & Quality Defense

> **"Code review is not proofreading formatting; it is the final gatekeeper against architectural erosion, security vulnerabilities, and hidden technical debt."**

AI coding agents often fall into the trap of self-congratulation, reviewing their own code with superficial approval ("Looks great!"). Under Sagarithm Kit, code review is an adversarial, empirical audit that evaluates code across structure, security, performance, and correctness.

---

## 🛡️ The 5 Pillars of Code Review

1. **Architectural Purity**:
   - Are domain boundaries respected?
   - Did the author introduce any forbidden generic directories (`utils/`, `helpers/`, `misc/`)?
   - Is the dependency graph strictly acyclic (no circular imports)?
2. **Security & Secrets**:
   - Are there any high-entropy strings ($H \ge 4.5$) or potential API keys?
   - Is all external input strictly validated using schemas (e.g. Zod) at the system perimeter?
3. **Behavioral Integrity (Zero Assumed Success)**:
   - Does empirical test output prove that the new functionality works?
   - Are boundary conditions, empty states, and error throws covered?
4. **Type Algebra & Safety**:
   - Zero `any` or loose type assertions (`as unknown as T`).
   - Are state variations modeled using discriminated unions?
5. **Operational Hygiene**:
   - Are database queries indexed?
   - Are asynchronous operations bounded by cancellation tokens and timeout guards?

---

## 🛑 Anti-Rationalization Matrix

| Reviewer / Agent Excuse | Architectural Reality | Mandatory Action |
|---|---|---|
| *"The diff is small, so a thorough review isn't needed."* | Most critical outages and security exploits are 1-line changes. | Review every changed line with equal rigor. |
| *"The code compiles, so it must be correct."* | Compilation only guarantees type grammar, not semantic correctness or edge-case safety. | Demand automated behavioral test verification. |
| *"I'll clean up the formatting and comments in a later PR."* | Unmerged cleanup is almost never performed; dirty code invites more dirty code. | Enforce clean formatting and accurate docstrings before approval. |
| *"This warning is harmless; let's ignore it."* | Ignored warnings mask real runtime bugs and build failures on different platforms. | Zero-warning policy: fix the warning or explicitly suppress with justification. |

---

## 📋 Pre-Merge Review Checklist

```markdown
- [ ] No prohibited directories (`utils/`, `helpers/`, `misc/`) created or modified.
- [ ] No high-entropy tokens ($H \ge 4.5$) or plain-text secrets present.
- [ ] Circular dependency checks pass (`sagarithm verify`).
- [ ] Test coverage accompanies all modified business logic.
- [ ] Documentation / README synchronized with modified public APIs.
```
