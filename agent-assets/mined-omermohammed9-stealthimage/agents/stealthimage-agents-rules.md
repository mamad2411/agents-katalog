# StealthImage — Agent Registry
> **ALWAYS-ON** — This file is loaded automatically for every task and implementation session.

This directory contains all agent configuration files for the StealthImage project.
Each agent is scoped to a specific concern and must follow the **Quota Governor Rules** below.

---

## Registered Agents

| Agent File | Role | Scope |
|---|---|---|
| `quota-governor.md` | Enforces token/cost constraints across all agents | Global |
| `architect.md` | Maintains system map, dependency graph, and cross-module contracts | Architecture |
| `embedder-agent.md` | Implements and tests all embedder modules | `embedders/` |
| `extractor-agent.md` | Implements and tests all extractor modules | `extractors/` |
| `server-agent.md` | Implements the Flask C2 server and dashboard | `server/` |
| `utils-agent.md` | Implements crypto, obfuscation, detection, polyglot utils | `utils/` |
| `payload-agent.md` | Implements the data stealer payload and dropper variant | `payloads/` |
| `test-agent.md` | Writes and runs all unit and integration tests | `tests/` |
| `docs-agent.md` | Maintains README, comments, and legal disclaimers | `*.md`, headers |

---

## GSD Workflow Integration

This repository uses GSD as a structured AI coding workflow layer. GSD is not the project authority and does not require Google Antigravity; `.agents/` remains the source of truth.

Before implementation, always inspect:

- `.agents/rules/AGENTS.md`
- `.agents/workflow.md`
- `.agents/project-context.md`
- `.agents/system-map.md`
- `.agents/tasks_status_matrix.md`
- `.agents/AUDIT_REPORT.md`
- `.agents/gsd-integration.md`
- `GSD_PROJECT_RULES.md`
- `.gsd/SPEC.md`
- `.gsd/ROADMAP.md`
- `.gsd/STATE.md`

Required execution flow:

```text
SPEC -> PLAN -> EXECUTE -> VERIFY -> DOCUMENT -> COMMIT
```

Every completed task must update project governance files if it changes behavior, architecture, commands, dependencies, security posture, or implementation status.

Upstream GSD files that mention Antigravity, Gemini, Claude, or another runtime are adapter guidance only. Do not use upstream install/update workflows to overwrite this repository's `.agents` governance.

---

## Quota Governor Rules (ALL AGENTS MUST FOLLOW)

### 1. Model Frugality
- **Default low-risk model/mode**: `gpt-5.4-mini` low for docs, prompt cleanup, status checks, small config edits, and GSD bookkeeping.
- **Default implementation model/mode**: `gpt-5.4` medium for normal feature work, route fixes, dashboard changes, tests, and moderate refactors.
- **High-reasoning model/mode**: `gpt-5.4` high for multi-file dependency debugging (3+ files), security/auth/HMAC/privacy/telemetry/GeoIP contract work, architecture planning, complex crypto, or structural refactoring across module boundaries.
- **Exceptional fallback**: `gpt-5.5` high only when `gpt-5.4` high is insufficient or the task is highest-risk. Document the reason in `.gsd/STATE.md` or task notes.
- **Never escalate** for: formatting, renaming, comment writing, boilerplate, YAML/config edits, markdown cleanup, or routine GSD state updates.

### 2. Output Minimalism
- **Never rewrite existing code blocks** unless explicitly asked. Output diffs or targeted line replacements only.
- **No verbose narration** — suppress step-by-step commentary. Deliver only actionable output.
- **No preamble** — skip "I'll now create..." statements. Go directly to the artifact/code.

### 3. Tool Call Economy
- **Batch independent reads**: Open multiple files simultaneously rather than sequentially.
- **No redundant reads**: If a file was read in this session, use cached knowledge.
- **No speculative exploration**: Only read files directly needed for the current task.
- **Prefer grep over full file reads** when searching for a specific symbol or pattern.

### 4. Task Scope Discipline
- Each agent **only touches files within its declared scope**.
- Cross-scope changes require **architect-agent coordination** — never unilateral modification.
- If scope is ambiguous, **ask one clarifying question** before acting.

### 5. Planning Before Execution
- For any task touching 3+ files, produce a **mini implementation plan** (≤ 10 bullet points) before writing code.
- Get explicit approval before executing the plan.
- Track progress in `task.md`.

### 6. Dependency Respect
- Always consult `system-map.md` before adding a new import or dependency.
- Never add a new PyPI package without updating `requirements.txt` and `system-map.md`.
- Use `.venv` — never install globally.

### 7. Security/Ethics Boundary
- All generated code **must include the standard StealthImage educational header**.
- No code may be modified to remove attribution, disable logging, or bypass detection modules.
- The defensive modules (`utils/detection.py`, `extractors/svg_cleaner.py`) are protected — never weaken them.

### 8. Auto-Update Obligation *(CRITICAL — ALWAYS ENFORCED)*
After **any** implementation task that adds, removes, or modifies files or features:
1. **Update `system-map.md`** — change file status from `planned` → `implemented`, update dependency graph if changed.
2. **Update `project-context.md`** — update the Phase Status Tracker table and note any design decisions made during implementation.
3. **Update `README.md`** — reflect new CLI usage, new modules, or changed behavior.

These three updates are **not optional**. No task is considered complete until all three files are updated.

### 9. Always-On Rules
The following files are **mandatory reading** at the start of every session:
- `.agents/rules/AGENTS.md` ← this file
- `.agents/rules/strict-resource-management.md`
- `.agents/rules/code-standards.md`
- `.agents/rules/documentation-drift-guard.md`
- `.agents/rules/security-engineering-rules.md`
- `.agents/system-map.md`
- `.agents/project-context.md`
- `.agents/gsd-integration.md`

Do NOT begin any implementation without having read the required governance files.

### 10. Golang Migration & AI Documentation
All new Go modules (`go-stego`, `go-c2`, `go-tunnel`) and their Python wrappers must include docstrings formatted for AI ingestion to maintain the `ai_handoff_synthesis.md` loop. Follow strict memory safety when interacting with CGO or passing buffers between Python and Go.
