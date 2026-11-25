---
name: fusion-panel
description: >-
  Run the canonical Fusion panel: dispatch the task blind and in parallel to all live CLIs
  (codex/gpt-5.5, copilot/gemini, opencode/glm, grok), then judge and synthesize one
  grounded answer. Includes the cheap variants — `vote` (model-free majority for verifiable
  answers) and `ranked` (pick the single best). Use for research, "compare", code with one
  clear deliverable, "get the panel's answer". Triggers: "panel", "fuse this", "ask all the
  models", "vote on this", "second opinion".
---

# Fusion — Panel

This is the **`panel`** entrypoint (and its cheap cousins `vote` / `ranked`). Load and run
**`fusion-orchestrate`** forcing `mode = panel` (or `vote`/`ranked` when the task fits).
This is the default, workhorse Fusion mode and the one that most directly reproduces the
benchmark's "diverse panel + synthesis beats one model" result.

## Mechanic (`references/collaboration-modes.md` §2, §5)
1. Build the panel prompt per `references/panel-doctrine.md`: task **verbatim** + the fixed
   neutral instruction, no personas. Paste local-file context the panelists can't see.
2. `fusion.sh panel "$PROMPT_FILE" "$OUT_DIR"` — all panelists run blind, in parallel.
3. Mark non-returning panelists **absent**. Read every returned `.out`.
4. **Judge** (`references/judge-rubric.md`): Track A (run-the-code-and-merge) for code,
   Track B (five-section synthesis) for research.

## Pick the right variant
- **`panel`** (synthesize) — open-ended, the answer benefits from a real merge.
- **`vote`** — the answer is a checkable value; tally answer-keys, report agreement ratio,
  **no judge call** (cheapest).
- **`ranked`** — you want the single best *whole* answer and synthesis would dilute it; pick
  the strongest candidate index and return it.

## Output
Verdict-contract format with the five-section analysis (or merge rationale for code).
Record the run with honest per-panelist ranks — that ranking is what teaches Fusion who
wins which task type. Optionally add one Codex subagent as a 5th blind panelist for the
self-fusion lift (keep it out of your judging context).
