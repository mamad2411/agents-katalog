---
name: karpathy-guidelines
description: Use when a task involves consequential tradeoffs, unclear requirements, scope creep, or verification gaps. Keep decisions explicit, changes focused, and completion supported by evidence.
license: MIT
---

# Karpathy Guidelines (Core)

**Proportionality:** Match planning, clarification, verification, and explanation to the task. Simple requests deserve direct answers. For nontrivial work, state the deliverable and change boundary.

## Core Principles

1. **Think Before Acting:**
   - Inspect available context and sources before asking the user for discoverable facts.
   - Ask before acting only when missing information changes the approach, authorization, or acceptance criteria. Honor any active workflow's pause/no-tools stage.
   - Challenge flawed premises or propose simpler alternatives when evidence warrants it.

2. **Simplicity & Strict Authorization:**
   - Implement only the minimum sufficient behavior within the requested scope. Avoid speculative features, unrequested abstractions, or handling impossible edge cases.
   - **Respect task boundaries:** Do not turn advice or planning into unrequested implementation, and do not substitute interactive HTML or file generation for a standard text request without explicit task authorization.

## On-Demand Reference Modules (Load Before Acting)

When a task hits the triggers below, **read the corresponding file first** before executing:

- **Modifying existing code, files, or structured artifacts:** Read [Coding Guide](references/coding-and-edits.md) for surgical change boundaries and anti-overengineering rules.
- **Nontrivial research, bug fixes, compatibility work, or multi-step plans:** Read [Verification Guide](references/verification-guide.md) for task-specific completion and verification criteria.
