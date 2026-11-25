---
name: etchplan
description: Compile an AI agent's repeated multi-step workflows into cheap, guarded, deterministic routines that run behind a fallback to the agent. Use when the user wants to cut recurring agent token/latency cost, mine repeated workflows from agent traces (Claude Code / Codex / opencode hooks), compile/validate/run an ExecutionPlan, or capture and replay recurring computer-use (macOS GUI or agent browser actions). Triggers: "compile my agent workflow", "make my agent cheaper", "mine my agent traces", "capture/replay computer-use", "etch ...".
---

# _etchplan_

_etchplan_ turns repeated agent work into compiled, validated, deterministic routines. It is a local CLI (`etch`); Apache-2.0; local-first (nothing leaves the machine by default). Every number it reports carries provenance (`measured | recorded | estimated | assumed`), preserve that discipline when reporting results.

## Setup
Install with `pip install etchplan` (or `uv tool install etchplan`); the CLI is then `etch …` on your PATH. To run from a checkout instead, invoke it as `uv run etch …` and prefix the `etch …` commands below with `uv run`.

## When to use
- The user runs an agent that repeats the same workflow and wants it cheaper/faster.
- The user wants to mine their own agent traces (Claude Code, Codex, or opencode) for repeated workflows.
- The user asks to compile / validate / run an `ExecutionPlan`, or to redact a trace before sharing.

## How to use (the loop)
1. **Capture** (once): `etch hook install <claude-code|codex|opencode> [--write]`. Traces accumulate locally under `~/.etchplan/`.
2. **Import**: `etch import <claude-hooks|codex-hooks|opencode>`, normalizes captured sessions into traces (auto-redacted + slotted).
3. **Mine**: `etch mine patterns --out patterns.json`, finds repeated subsequences with parameter-flow + invariant learning.
4. **Compile**: `etch compile pattern patterns.json --pattern-id <id> --out plan.yaml`, synthesizes a guarded plan. Mutating steps without idempotency are deliberately refused.
5. **Validate**: `etch validate plan plan.yaml`, executes the plan over trace-derived replay cases (measured), not estimated.
6. **Run**: `etch run plan.yaml --input input.json`, executes behind fallback to the original agent, with an append-only audit log.

## Computer-use (preview)
The same loop applies to GUI/web computer-use, capturing actions bound to accessibility-element names (or the semantic action an agent issued), not pixels.
- **Agent capture** (the product path): `etch import agent-computer-use <log> --adapter <claude-in-chrome|computer-tool>`, hooks an agent's computer-use tool calls into traces. Semantic browser calls have no pixel fallback; the coordinate computer tool degrades ungrounded clicks to a flagged `pixel_click`.
- **Human capture**: `etch desktop capture` records a real macOS GUI session (needs the `desktop` extra + Accessibility); `etch import desktop-capture` normalizes it.
- **Replay**: `etch desktop compile-plan` / `etch browser compile-plan` wrap a routine as an `ExecutionPlan` that rides the same trust loop. Desktop replays via guarded AppleScript; browser replays by re-issuing semantic actions via Playwright. Both default to validate-only; `*_registry_live` is the explicit opt-in that controls the machine. `--parameterize` makes a routine replay with fresh per-call arguments.

## Sharing data safely
Captured traces can contain secrets/PII/commands. Before sharing a trace, plan, or hook-events file, run `etch redact <file>`, it redacts secrets/PII and slots identifiers. Never paste raw `~/.etchplan/hook_events*.jsonl` contents.

## Safety model (do not bypass)
- Compiled code routines are AST-guarded (only environment APIs + safe builtins; no `exec`/`eval`/`open`/OS/network). A routine that fails validation is not executed, the agent runs instead.
- Live mutating actions require an idempotency key and a mutation gate; a drift kill-switch disables a plan whose measured fallback rate breaches its policy.

## Honesty
When reporting savings, state the provenance: solve verdicts are `measured`; costs are `estimated` from measured tokens. Compiling requires one successful agent run first, so the cost win is amortized over recurring tasks, say so.
