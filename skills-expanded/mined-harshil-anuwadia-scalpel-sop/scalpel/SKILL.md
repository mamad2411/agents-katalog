---
name: scalpel
description: Standard Operating Procedure (SOP) for codebase agents. Use this for ANY codebase modification, restructuring, clean-up, feature addition, or bug fixing. Defines mandatory execution constraints and workflow gates.
---

# SKILL SPECIFICATION: SCALPEL ROUTING

## 1. INITIALIZATION SEQUENCE (BOOT)
You MUST load these files in this exact order before processing any codebase directive.
1. `PRINCIPLES.md` — The reasoning and philosophy behind the rules.
2. `CORE.md` — Non-negotiable operating rules.
3. `ANTI-PATTERNS.md` — Forbidden behaviors.
4. `checklists/pre-flight.md` — Execute verification gates.

## 2. OPERATION ROUTING TABLE
Identify the task type and load ALL matching scenario files.

| Task Category | Trigger / Keywords | File to Load |
| :--- | :--- | :--- |
| **New Feature** | "Add", "Create", "Build", "Implement new" | `scenarios/01-new-feature.md` |
| **Modify Existing** | "Update", "Change", "Extend", "Modify" | `scenarios/02-modify-existing.md` |
| **Removal** | "Delete", "Remove", "Drop", "Clean up" | `scenarios/03-remove-feature.md` |
| **Bug Fix** | "Fix", "Debug", "Resolve", "Error", "Failing" | `scenarios/04-debug-fix.md` |
| **Refactor** | "Refactor", "Restructure", "Clean" (Explicitly) | `scenarios/05-refactor.md` |
| **Cold Start** | "New project", "Just starting", no prior context | `scenarios/06-new-session.md` |
| **Ambiguity** | "How should I", Unclear scope, Multiple valid paths | `scenarios/07-ambiguous.md` |
| **Testing** | "Write tests", "Coverage", "Test suite" | `scenarios/08-write-tests.md` |
| **Dependencies** | "Upgrade", "Install", "Migrate to", "Bump" | `scenarios/09-dependency-upgrade.md` |
| **Legacy/Messy** | "Inconsistent", "No tests", "Spaghetti" | `scenarios/10-messy-codebase.md` |

*Conflict Rule: If a task spans multiple categories, load ALL relevant files. Rules combine. In case of conflict, `CORE.md` takes supreme precedence.*

## 3. DYNAMIC CHECKLIST GATES
Load these execution gates precisely when the trigger condition is met:

- **Condition:** Before writing any code. -> **Load:** `checklists/pre-flight.md`
- **Condition:** After deleting any code/file. -> **Load:** `checklists/removal-complete.md`
- **Condition:** Before making a structural/design choice. -> **Load:** `checklists/architecture-confirm.md`
- **Condition:** When reporting a task as complete. -> **Load:** `checklists/work-report.md`
- **Condition:** When a task must continue in a new session. -> **Load:** `checklists/session-handoff.md`

## 4. CRITICAL MANDATE
Never report a task as "complete" without executing `checklists/work-report.md`. A completion report that omits missing items or untested edge cases is a violation of operating discipline.

## 5. OPERATING MODES
Users can toggle latency vs. safety by setting a mode at the start of a session.

| Mode | Behavior | Use Case |
| :--- | :--- | :--- |
| **INTERACTIVE** (Default) | Strict gating. Stop and confirm before every structural change or ambiguity. | Default, high-risk codebases, junior agents. |
| **AUTONOMOUS** | Gate reduction. Proceed based on stated assumptions. Skips `pre-flight` confirmation pauses and minor ambiguity checks. ONLY stops to ask permission for `03-remove-feature` (deletion) or `architecture-confirm`. | Rapid prototyping, trusted sessions, low-risk changes. |

*Trigger:* If a user says "Proceed autonomously" or "Just do it", switch to **AUTONOMOUS**.

## 6. THE OVERRIDE PROTOCOL
If a core rule (CORE.md) conflicts with a direct user instruction:
1. Identify the specific rule (e.g., R16).
2. State the conflict clearly.
3. Ask the user to confirm with: **"OVERRIDE [Rule Number]"**.
4. Once provided, log the override in the final work report and proceed.
