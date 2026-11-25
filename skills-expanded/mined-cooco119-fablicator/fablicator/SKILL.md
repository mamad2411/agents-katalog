---
name: fablicator
description: >-
  Triage any task to the right model and, when Fable 5 fits, fabricate an optimized execution
  prompt for it. Use this skill WHENEVER turning a task or intent into an agent prompt, deciding
  which model an agentic task should run on (Sonnet 4.6 / Opus 4.8 / Fable 5), designing a
  long-running or autonomous agent run, setting up subagent orchestration, or asking whether a task
  is even worth running on a frontier agent model — even if the user never says "prompt," "Fable,"
  or "triage" explicitly. If someone describes work they want an agent to do and the route or model
  isn't already decided, reach for this skill.
license: MIT
---

# Fablicator

Turn a raw task into either (a) a **model recommendation** that routes the task away from Fable, or
(b) a **Fable execution prompt** assembled to match the task. Fablicator's whole job is to avoid two
failure modes: spending Fable on work a cheaper model handles better, and under-scaffolding a real
long-horizon job so Fable stalls or hallucinates progress.

## How to use

1. **Read `references/generator.md`.** It contains the generator system prompt — the triage matrix,
   the classification axes, and the conditional prompt skeleton. That file is the engine; this file
   just tells you when and how to run it.
2. **Run Step 0 — triage (gates everything).** Place the task on two axes, `path` (structured vs.
   dynamic) × `length` (short vs. long), with a risk pre-check that fires first:
   - touches offensive cyber / bio → Opus 4.8 + server-side fallback, stop.
   - short × structured → Sonnet 4.6.
   - short × dynamic → Sonnet 4.6, escalate to Opus if it stalls.
   - long × structured → Opus 4.8, or split into a deterministic workflow.
   - **long × dynamic → Fable 5** (the only cell that proceeds to prompt assembly).
3. **If not the Fable cell:** output the recommended model + a one-line rationale, offer to write a
   prompt for that model instead, and stop. Do not fabricate a Fable prompt.
4. **If the Fable cell:** classify the task (horizon / supervision / kind / risk / spec), set an
   effort level, and assemble the prompt from the ALWAYS blocks plus only the CONDITIONAL blocks
   whose triggers fired. Keep it lean — a clean 6-block prompt beats a bloated 12-block one.
5. **Output format (user-facing, language-matched):** reply in the task's own language (Korean task
   → Korean, English → English). Present exactly three friendly parts — **Recommended model** (the
   routed model), **Why** (one or two plain sentences, no jargon), and, *only for the Fable cell*, a
   labeled **Prompt** in a fenced code block. For non-Fable cells, skip the prompt and offer to write
   one tuned for the recommended model. Model names stay canonical (Fable 5 / Sonnet 4.6 / Opus 4.8);
   the assembled prompt's block headers stay English while its contents follow the task's language.

## What the generated prompt guarantees (for Fable-cell tasks)

The skeleton encodes the autonomous-stabilization lessons so long runs don't drift: an intent frame,
an observable definition-of-done, scope boundaries, and — when the run is async or long — progress
grounding against real tool results, checkpoint rules, an anti-stall autonomous reminder,
fresh-context verification, memory hygiene, and outcome-led communication. It never instructs the
agent to reproduce its internal reasoning (that trips Fable's refusal), and risk is handled upstream
at triage rather than in the prompt body.

## Notes

- `path` (is the route predetermined?) is distinct from `spec` (is the goal clear?). A goal can be
  crystal-clear yet require a route the model must invent — that still routes to Fable.
- long × structured: prefer an orchestrated pipeline of cheaper calls over one long Fable run.
- If a long autonomous run stalls (states intent, emits no tool call), a runtime "continue" /
  "go ahead end to end" unsticks it — an operator action, not a prompt change.
