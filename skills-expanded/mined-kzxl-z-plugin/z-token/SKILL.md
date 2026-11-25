---
name: z-token
description: Slash command and mode controller for Z-Token (compact context, oversized-read guard, capped search, lean builds, and visual telemetry dashboard). Triggered by /z-token [on|lite|ultra|off|status|dashboard].
---

# Z-Token Skill

Provides operational control and dynamic strictness levels for the Z-Token optimization framework.

## Operating Levels

- **`on`** (Default): Activates full z-token directives across communication, context caching, tool batching, and code generation.
- **`lite`**: Applies communication and artifact concision only; leaves tool execution and context exploration unconstrained.
- **`ultra`**: Activates telegraphic mode on low-stakes communication surfaces (~60% token reduction), while preserving full verbatim precision on high-stakes code and commands.
- **`off`**: Temporarily suspends z-token rules. Triggered by `/z-token off` or "verbose mode".
- **`status`**: Reports active mode and current token management directives.
- **`dashboard`**: Generates `~/.zero-token/z-dashboard.html` and opens the visual token telemetry & cost dashboard from any workspace via `diet(scope: "dashboard", open: true)`.

---

## Ultra Mode Specification (Surface-Scoped)

When `/z-token ultra` is selected:

### Low-Stakes Surfaces (Telegraphic)
Applies to: Chat responses, progress updates, and conversational status notes.
- **Lead immediately with the core answer**: No preamble, greetings, or pleasantries.
- **Drop function words**: Omit non-essential articles (`a`, `the`), auxiliary verbs (`is`, `are`, `will`), and pronouns when semantic meaning remains intact.
- **Use sentence fragments and shorthand**: Favor concise arrow chains (`Input -> Process -> Result`) and standard abbreviations (`fn`, `param`, `cfg`, `res`).
- **Eliminate formatting fluff**: Avoid decorative headers, bold markers on single lines, or emojis.

### High-Stakes Surfaces (Never Telegraph)
Never apply telegraphic fragments to:
- Executable code, diffs, and scripts.
- Shell commands, command-line arguments, and flags.
- File paths, URLs, symbols, classes, and variable names.
- Exact error messages, stack traces, and test assertions.
- Architectural design documents, sub-agent prompts, and security policies.

---

## Command Handling

- `/z-token on`: Confirms activation of standard Z-Token rules.
- `/z-token lite`: Switches to communication-only token savings.
- `/z-token ultra`: Switches to aggressive telegraphic output mode for low-stakes text.
- `/z-token off`: Pauses z-token optimizations.
- `/z-token status`: Displays current level and operational recommendations.
- `/z-token dashboard`: Calls the `z-token` MCP tool `diet` with `{ scope: "dashboard", open: true }` to build and open `~/.zero-token/z-dashboard.html` directly from any workspace (zero need to `cd` into the `z-plugin` repository).

---

## Guardrails
1. Concision applies to external communication and context representation, **never** to the internal reasoning or analysis required to reach a correct solution.
2. Security boundaries, tests, and financial/data-integrity checks must never be skipped or degraded to save tokens.
