---
name: code-verify-and-clean-skill
description: |
  Provides automated and manual verification, linting, formatting, and behavioral analysis of code.
  Ensures code correctness, eliminates dead code, enforces clean architecture, and verifies rendering/execution
  using testing tools, compilers, and browser-based DevTools.
  Use when: verifying code correctness, running linters/formatters, cleaning up technical debt,
  refactoring modules, validating UI rendering, testing API integrations, and analyzing runtime errors.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Browser
---

# Code Verification & Cleaning Skill

Transform chaotic development cycles into deterministic, highly stable software systems through rigorous automated checks, strict code sanitation, and live execution audits.

## When to Use This Skill

- **Pre-Merge Verification:** Confirming changes actually compile and completely pass test suites before declaring a task finished.
- **Code Cleaning & Sanitization:** Eliminating dead code, unused imports, redundant parameters, and refactoring deep cognitive nesting.
- **Runtime and UI Diagnostics:** Leveraging DevTools/Browser environments to check for rendering fidelity, memory leaks, and broken network pipelines.
- **Automated Ecosystem Linting:** Running stack-specific formatters and compilers to guarantee static compliance.

## Core Principles

### 1. The "Trust But Verify" Runtime Standard
An expert agent never assumes written code is functional code just because it looks flawless.
- **Execute:** Boot servers, compile modules, or run interpreters instantly.
- **Observe:** Open target layouts via the `Browser` tool to dynamically catch visual or architectural breaks.
- **Isolate:** Capture stack traces, errors, and system warnings directly from the environment.

### 2. Radical Code Cleaning (Anti-Bloat Strategy)
Code should be lean, modern, and easily maintainable.
- Prune unused components, imports, variables, and structural dead-ends.
- Refactor complex `if-else` blocks or logic trees into explicit early returns.
- Always check if custom logic can be replaced by utilizing shared global utilities.

```markdown
❌ Bad (Dirty & Unverified Architecture):
try {
  const res = await fetch('/api/data');
  const data = await res.json();
  this.setState({ data: data, loading: false });
} catch(e) {}

✅ Good (Cleaned, Verified, & Structured Safely):
try {
  const res = await fetch('/api/data');
  if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
  const data = await res.json();
  this.setState({ data, loading: false });
} catch (error) {
  logger.error("Failed to dynamically fetch operational data:", error);
  this.setState({ error: error.message, loading: false });
}

### 3. Severity Tiers & Validation Markers

Enforce structural barriers during execution routines:

🔴 [breaking-error] - Code crashes, fails type checks, breaks UI workflows, or exhibits dynamic security loops. (Blocks merge)
🟡 [code-smell] - Code functions properly but introduces technical debt, bloat, or violates efficiency guidelines
🟢 [refactored] - Cleanups automatically deployed by the agent (formatting updates, typo fixes)
Verification & Cleaning Pipeline
Phase 1: Static Analysis & Compiling (Automated Passes)

Trigger the repository’s native formatting pipeline using Bash (e.g., npm run lint, cargo fmt, flake8).

Wipe away all auto-fixable syntax variations instantly.

If an explicit pipeline suite is present, invoke scripts/verify-pipeline.sh to automate pre-checks.

Phase 2: Structural Sanitation Review

Scan every altered module for clarity patterns:

Modular Breakdown: Ensure single responsibility guidelines. If a script exceeds standard bounds, divide it into neat subsystems.
Reusability Check: Audit cross-cutting directories. Do not reinvent components or utility math already present in the workspace.
Phase 3: Live DevTools & Browser Audits (Frontend Verification)

Whenever a client interface layer is mutated:

Initialize local preview servers using Bash.
Deploy the Browser / DevTools Tool directly to the rendered address.
Console Inspections: Read console.error and console.warn outputs. Resolve React hydrations or hidden exceptions immediately.
Network Validations: Trace payloads. Ensure no 400/500 triggers fire on interface actions.
Tool-Specific Execution Guides
Tool	Action Standard	Expected Outcome
Bash	Run tests, linters, and native package builders	Zero errors, clear build telemetry, verified tests
Browser / DevTools	Capture runtime layouts, read consoles, review network pipelines	Functional UI, clean logs, standard status returns
Grep / Glob	Scan workspace structures for existing code blocks or setups	Eliminates logic duplication across modules
WebFetch	Query framework docs for syntax specs or deprecations	Prevents structural hallucinations of system libraries
Cross-Cutting Reference Modules
Topic	Reference File	Key Target Areas
Dynamic Verification	reference/devtools-verification.md	Headless browser workflows, layout auditing, console checks
Code Cleaning Standards	reference/code-cleaning-universal.md	Technical debt elimination, structural complexity reduction
Security Verification	reference/security-verification.md	Input injection blocks, client-side exposure auditing, token security
Additional Resources & Assets
reference/devtools-verification.md
reference/code-cleaning-universal.md
reference/security-verification.md
assets/verification-checklist.md
assets/review-template.md