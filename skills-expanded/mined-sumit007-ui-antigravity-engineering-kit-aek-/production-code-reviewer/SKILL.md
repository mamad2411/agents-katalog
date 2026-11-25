---
name: production-code-reviewer
description: Conduct rigorous, production-grade code reviews evaluating architecture, memory safety, asymptotic complexity, security vulnerabilities, test coverage, and backwards compatibility.
---

# Production Code Reviewer Skill

## Purpose
Directs thorough code reviews against enterprise production release criteria, performance invariants, and security hygiene.

## When to Use
- Reviewing pull requests and code modifications before merging to `main`.
- Auditing new dependencies for maintenance, licensing, and vulnerability advisories.
- Evaluating computational complexity ($O(N)$ vs $O(N^2)$), memory allocations, and error paths.

## Engineering Workflow
1. **Systematic Audit Checklist**:
   - Correctness: Does the implementation satisfy all requirements without side effects?
   - Safety: Are there injection vectors, unchecked unwraps, or concurrency races?
   - Efficiency: Are allocations bounded and cache-friendly?
   - Tests: Are unit and integration tests passing with >80% coverage?
2. **Review Output**:
   - Provide concrete, line-referenced actionable feedback with minimal conversational filler.

