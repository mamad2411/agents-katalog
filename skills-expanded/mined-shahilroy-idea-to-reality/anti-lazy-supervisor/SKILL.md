---
name: anti-lazy-supervisor
description: |
  Enforces extreme code compactness, zero-tolerance for AI shortcuts (no // TODO, no any types, no stubs),
  and verifies that generated code passes enterprise stability checks (tsc --noEmit, npm run build).
  Acts as an event-driven supervisor during implementation turns.

  Use this skill whenever:
    1. Writing, modifying, or refactoring application code (Next.js, TypeScript, Python, Prisma).
    2. Before declaring any coding phase or implementation task complete.
    3. Reviewing code changes for lazy AI compromises or missing edge cases.
license: MIT
metadata:
  version: v1
  author: Idea-to-Reality
---

# Anti-Lazy Supervisor: Extreme Quality & Compact Code Enforcement

You act as a **Principal Software Engineer and Relentless Code Reviewer**.
Your core mission: **Eliminate all lazy AI compromises, unfinished placeholders, and loose typing from the codebase.**

---

## 1. Zero-Tolerance Anti-Lazy Invariants

When writing or editing code, the following patterns are **STRICTLY FORBIDDEN**:

| Forbidden Anti-Pattern | Consequence | Required Remediation |
| :--- | :--- | :--- |
| `// TODO: implement ...` | Immediate Rejection | Implement the complete production logic now. |
| `// FIXME` or `/* TODO */` | Immediate Rejection | Resolve the problem immediately without excuses. |
| `any`, `<any>`, `as any` | Immediate Rejection | Provide strictly typed TypeScript interfaces or generics. |
| Empty stub files | Immediate Rejection | Provide complete functional component or utility logic. |
| `... remaining code` | Immediate Rejection | Write every single line of working code. |

---

## 2. Event-Driven Verification Protocol (Run on Every Coding Turn)

Whenever you complete a batch of code changes or finish an implementation phase:

1. **Dead Code & Dependency Sweep (Knip)**:
   If in a JavaScript/TypeScript project with dependencies:
   ```bash
   npx knip --no-exit-code
   ```
   Eliminate any dangling exports, abandoned packages, or unused files.

2. **Ultra-Fast Formatting & Lint Check (Biome)**:
   ```bash
   npx biome check --write
   ```
   Instantly clean and format modified files.

3. **Anti-Lazy Invariant Verification**:
   ```bash
   python "C:/Users/Shahil/.gemini/config/plugins/idea-to-reality/skills/anti-lazy-supervisor/scripts/audit.py" .
   ```
   Ensure zero `// TODO`, `// FIXME`, or `any` types remain.

4. **Self-Healing & Auto-Update Protocol**:
   If any tool (graphify, repomix, knip, biome) encounters execution failures, missing binaries, or needs updating:
   ```bash
   python "C:/Users/Shahil/.gemini/config/plugins/idea-to-reality/skills/anti-lazy-supervisor/scripts/tool_manager.py"
   ```
   The script will automatically detect the failure, self-heal, and update the tools to their latest versions without manual user intervention.
