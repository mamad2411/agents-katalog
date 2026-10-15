---
name: paleo-auto
description: 'Use when you want automatic token-saving without manual skill selection. Auto-detects long sessions (>15 turns), high token usage, or bulky context — then auto-enables paleo + paleo-trim-context + paleo-converse + paleo-budget at safe defaults. User does not need to think about which skill is active. Off: "disable paleo-auto" / "manual paleo".'
version: 2.5.0
license: MIT
metadata:
  hermes:
    tags: [tokens, auto, compression, efficiency, automation, session]
    related_skills: [paleo, paleo-trim-context, paleo-converse, paleo-budget]
---

# paleo-auto
Zero-touch token savings. Enable once, stay on — paleo-auto watches your session and activates the right skills at the right time.

## What it does
- **Automatic activation.** No manual triggers needed. Detects session conditions and enables skills.
- **Picks the right combo.** Not all skills needed all the time — paleo-auto picks per-condition.
- **Safe defaults.** Never applies ultra or hard-strict modes unless asked. Always starts at `full` or `soft`.

## Auto-detection triggers

| Condition | Detection | Action |
|---|---|---|
| Session length >15 turns | Count user/assistant exchanges | Enable `paleo` (full) + `paleo-trim-context` |
| Repeated tool output (same tool called 3+ times with similar results) | Compare last 3 tool outputs | Enable `paleo-summary` (full) |
| Context approaching warning (>60% capacity) | Estimate context usage | Enable `paleo-converse` (full, N=8) + `paleo-trim-context` |
| High token cost model detected (GPT-4, Claude Opus, etc.) | Model name check | Enable `paleo-budget` (soft, 3000 tokens) + `paleo` (full) |
| Bulky output returned (single tool result >2000 tokens est.) | Output size check | Enable `paleo-summary` (lite) for subsequent similar calls |
| User sends "long session" / "chatty" / "lagging" | Keyword match | Enable all 6 skills at `full` defaults |
| Session startup (fresh new session) | First 2 turns | Enable `paleo` (full) only — low overhead baseline |

## Default combo per scenario

| Scenario | Active skills | Why |
|---|---|---|
| Fresh session | `paleo` (full) | Low overhead baseline, catches wordy responses |
| Long session | `paleo` (full) + `paleo-trim-context` + `paleo-converse` (N=6) | Context hygiene + history compression |
| Expensive model | `paleo` (full) + `paleo-budget` (soft, 3k) | Cap costs on pricey models |
| Debugging/tools-heavy | `paleo-summary` (full) + `paleo` (full) | Shrink bulky tool output |
| User says "lagging" / "chatty" | All 6 at `full` defaults | Max savings, immediate |

## Rules
- Never override a user's explicit skill activation. If user says `paleo ultra`, keep it.
- Never apply `ultra` or `hard`/`strict` modes automatically — only `lite`/`full`/`soft`.
- If user disables a skill (e.g. "stop paleo"), respect it for the rest of the session.
- Report changes: "🦴 paleo-auto: enabled paleo + trim-context (session length 22 turns)" — one line, non-intrusive.
- Re-evaluate every 5 turns or on context-warning signal.

## Switch
- On: `paleo-auto` · `auto paleo` · `enable auto-save`
- Off: `disable paleo-auto` · `manual paleo` · `stop auto`
- Status check: `paleo-auto status` → list currently active skills + why

## Gotchas
- paleo-auto is an ORCHESTRATOR, not a replacement. It delegates to the 6 sibling skills — don't re-implement their rules here.
- Don't fight user overrides. Use explicitly set = respect it.
- Detection is approximate (turn count, output size estimation) — false positive is fine, false negative is tolerable. Err on the side of activating.
- Startup cost: loading paleo-auto adds ~300 tokens of context. Only keep active if the session will benefit from it (usually >10 turns).
