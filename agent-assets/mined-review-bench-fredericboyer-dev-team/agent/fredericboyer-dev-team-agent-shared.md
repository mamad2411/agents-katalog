---
name: shared-protocol
description: Shared protocol sections (challenge classification, learnings output, memory guardrails, progress reporting) referenced by all agent definitions. Not an agent — do not spawn directly.
---

# Shared Agent Protocol

This file contains protocol sections shared across all dev-team agents. Individual agent definitions reference this file and override sections as needed.

## Memory hygiene

Read your MEMORY.md at session start. Remove stale entries (overruled challenges, outdated patterns). If approaching 200 lines, compress older entries into summaries.

## Role-aware loading

Shared context (learnings, process) is loaded automatically via `.claude/rules/`. For cross-agent context, scan relevant tag entries in other agents' memories.

## Progress reporting

When running as a background agent, write status to `.dev-team/agent-status/<agent>.json` at each phase boundary (see ADR-026). Clean up the status file on completion. Emit console phase markers for log readability using the format `[AgentName] Phase N/M: Description...` and `[AgentName] Done — <summary>`.

## When writing tests

- **Test isolation**: No shared state between tests. No execution order dependencies. Each test sets up its own context and tears it down.
- **Meaningful assertions**: Every test must assert something specific. A test that runs without meaningful assertions provides false confidence.
- **Anti-mocking**: Push back on over-mocking. If you need 6 mocks to test one function, the function has too many dependencies — fix the design, not the test. Testability is a design quality.
- **Test naming as documentation**: Test names should describe the expected behavior, not the implementation. A failing test name should tell you what broke.
- **Fixture and teardown**: Setup should be minimal and explicit. Teardown should be reliable. Shared fixtures must be immutable.

## Challenge protocol

When reviewing another agent's work, classify each concern:
- `[DEFECT]`: Concretely wrong. Will produce incorrect behavior. **Blocks progress.**
- `[RISK]`: Not wrong today, but creates a likely failure mode. Advisory.
- `[QUESTION]`: Decision needs justification. Advisory.
- `[SUGGESTION]`: Works, but here is a specific improvement. Advisory.

Rules:
1. Every challenge must include a concrete scenario, input, or code reference.
2. Only `[DEFECT]` blocks progress.
3. When challenged: address directly, concede when wrong, justify with a counter-scenario when you disagree.
4. One exchange each before escalating to the human.
5. Acknowledge good work when you see it.
6. **Silence is golden**: If you find nothing substantive to report, say "No substantive findings" and stop generating additional findings. You must still complete the mandatory MEMORY.md write and Learnings Output steps. Do NOT manufacture `[SUGGESTION]`-level findings to fill the review. A clean review is a positive signal, not a gap to fill.

## Learnings Output (mandatory)

After completing work, you MUST:
1. **Write to your MEMORY.md** (`.claude/agent-memory/<agent>/MEMORY.md`) with key learnings from this task. The file must contain substantive content — not just headers or boilerplate. Include agent-specific findings (see your agent definition for what to record).
2. **Output a "Learnings" section** in your response summarizing what was written:
   - What was surprising or non-obvious about this task?
   - What should be calibrated for next time? (e.g., assumptions that were wrong, patterns that worked well)
   - Where was this recorded? (`agent memory` for agent-specific calibration / `team learnings` for shared process rules / `ADR` for architectural decisions)

### What belongs in memory

**Write:**
- Stable patterns and conventions (frameworks, architecture decisions, naming patterns)
- Calibration data (challenges accepted/overruled, with reasoning)
- Architectural boundaries and constraints
- Non-obvious project-specific knowledge that cannot be derived from code

**Do NOT write:**
- Specific numeric counts (test count, ADR count, agent count, file count) — these are volatile and trivially derivable on demand
- Version numbers that change frequently
- Information already captured in ADRs or `.claude/rules/dev-team-learnings.md`
- Trivially observable facts derivable from config files (e.g., "uses TypeScript" when tsconfig.json exists)

If you skip the MEMORY.md write, the pre-commit gate will block commits that include implementation files without corresponding memory updates. Use `.dev-team/.memory-reviewed` to override if no learnings apply.
