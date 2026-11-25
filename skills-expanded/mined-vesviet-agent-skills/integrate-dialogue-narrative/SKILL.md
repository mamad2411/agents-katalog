---
name: integrate-dialogue-narrative
description: Integrates branching narrative trees, deterministic condition flag evaluators, localization string tables, and Yarn Spinner or Ink runtime pipelines. Use when building dialogue systems, quest state machines, interactive cutscenes, or localized branching conversations.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Integrate Dialogue Narrative

Architect and integrate data-driven narrative and dialogue pipelines supporting Yarn Spinner or Ink scripts, sandboxed condition flag evaluation, localized string tables, and responsive typewriter presentation.

## Core Rules

- **Strict Content-Code Separation**: Author all narrative branching, speaker lines, and choice conditions in external data assets (`.yarn`, `.ink`, or structured dialogue graphs). Never hardcode conversation trees or raw display strings inside gameplay scripts.
- **Stable Localization Keys**: Address every dialogue line and UI choice by an immutable localization line ID (e.g. `line:npc_blacksmith_greeting_01`) mapped to locale string tables (`.csv`, `.po`, `Fluent`) so translations and typo fixes never break branching logic.
- **Sandboxed Condition & Command Dispatch**: Evaluate narrative variables and trigger scene side-effects (camera cuts, item grants, quest stage updates, animations) through registered, type-checked command bindings rather than arbitrary reflection or `eval()`.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing dialogue and narrative integrations.

## Suggested Process

### 1. Narrative Runtime & Variable Storage Setup
Integrate the narrative VM (Yarn Spinner, Ink, or custom AST runner) backed by a centralized `NarrativeVariableStorage` dictionary (`bool`, `int`, `float`, `string` flags). Synchronize this store directly with the save persistence layer.

### 2. Command & Function Binding Registration
Register deterministic external functions (`HasItem(id)`, `GetFactionRep(faction)`) and asynchronous sequence commands (`<<camera_focus target>>`, `<<play_emote actor_id smile>>`, `<<give_quest quest_id>>`) that pause dialogue progression until awaited presentation cues finish.

### 3. Typewriter Presentation & Input Handling
Render dialogue tokens using pre-laid-out rich text buffers (revealing characters via visible character count or vertex alpha rather than concatenating strings each frame, avoiding text reflow jitter):
- First confirm press during active typing immediately reveals the full line.
- Second confirm press advances to the next node or activates choice selection.

### 4. Localization & Automated Graph Verification
Extract string tables with speaker metadata and context comments for translators. Run a headless narrative linter in CI that compiles all dialogue scripts, verifies zero dead-end nodes or missing localization keys, and validates all command signatures.

## Output Contracts

When completing dialogue and narrative integration, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Branching dialogue scripts are externalized in data files with zero hardcoded prose in code
- [ ] All dialogue lines and choices resolve through immutable localization keys across locales
- [ ] Narrative conditions and scene commands execute via type-safe registered bindings
- [ ] Typewriter reveal uses visible-character indexing without mid-word line-wrap reflow jitter
- [ ] Narrative variable storage serializes cleanly into the game save persistence system
- [ ] Headless validation verifies all dialogue nodes, variable references, and localization keys

## Failure Modes

- **Hardcoded prose drift**: conversation lines are hardcoded in gameplay scripts, breaking localization and leaving branches invisible to translators. Mitigation: author all branching, lines, and conditions in external `.yarn`/`.ink`/graph data assets addressed by immutable line IDs.
- **Eval-based command dispatch**: narrative side-effects run through reflection or `eval()`, letting content files call arbitrary code. Mitigation: dispatch `<<camera_focus>>`-style commands only through registered, type-checked command bindings.
- **Dead-end nodes**: a branching graph ships with unreachable nodes, missing links, or missing localization keys, stalling the player mid-conversation. Mitigation: run the headless narrative linter in CI that compiles all scripts and verifies zero dead ends and key coverage.
- **Variable store desync**: `NarrativeVariableStorage` drifts from the save persistence layer, losing quest flags across sessions. Mitigation: synchronize the store directly with the save layer and serialize flags, visited nodes, and quest states in saves.
- **Typewriter reflow jitter**: per-frame string concatenation forces text re-layout, jittering word wraps mid-reveal. Mitigation: pre-lay-out rich text buffers and reveal via visible-character count or vertex alpha.
- **Input context collision**: dialogue advance presses leak into gameplay actions (or vice versa) when contexts overlap. Mitigation: switch to the dedicated `DialogueContext` while a conversation is active and restore the prior context on exit.
- **Localization key mutation**: renamed line IDs orphan existing translations and every locale. Mitigation: treat line IDs as immutable; CI key verification fails on orphaned or missing table entries.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: dialogue scripts from writers, mods, or DLC packs are external content that must not redefine game behavior. Mitigation: restrict them to the declared node/variable/command schema; anything outside registered bindings is rejected at compile time.
- **ASI05 RCE Guard**: never evaluate narrative expressions or commands via `eval()`/reflection. Mitigation: evaluate conditions and dispatch commands exclusively inside the sandboxed narrative VM with registered type-checked bindings.
- **ASI06 Context & Memory Poisoning**: narrative flags hydrated from saves are untrusted shared state; tampered values could force quest stages or unlock gated content. Mitigation: validate flag types and ranges on hydration and reject unknown keys.
- **ASI07 Inter-Agent Communication**: narrative state flows to UI rendering, save persistence, and input context roles. Mitigation: emit the schema-valid `implementation-result.json` contract so peers bind to the declared variable store and command API.
- **ASI09 Human-Agent Trust Exploitation**: do not claim all branches are reachable and localized without the linter pass. Mitigation: report actual CI narrative-lint results, including any suppressed dead-end or missing-key warnings.

## Related Skills

- **build-game-ui-ux**: rendering dialogue overlays, speaker portraits, and controller-navigable choice lists
- **implement-save-persistence**: serializing narrative flags, visited nodes, and quest states
- **abstract-input-actions**: switching to the Dialogue input context for advance and skip actions
