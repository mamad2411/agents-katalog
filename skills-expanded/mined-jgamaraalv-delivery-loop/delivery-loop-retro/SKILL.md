---
name: delivery-loop-retro
description: >-
  Write a structured retrospective of a delivery-loop run (frontend-delivery-loop,
  backend-delivery-loop, or fullstack-delivery-loop) that judges what went well, what
  went badly, where time/roundtrips/tool calls were wasted and in which skill or agent,
  how the agents integrated, and the session id + trace file paths — then save it as a
  Markdown report for skill-evolution-factory to act on. Use this the moment a delivery
  loop finishes (or stalls), whenever the user says "retro", "post-mortem", "retrospectiva",
  "feedback loop", "evaluate the loop", "how did the loop go", "what should we improve in
  the loop/agents", or asks to grade/critique a frontend/backend/fullstack delivery-loop
  run. Run it even if the user only gestures at it — a finished loop is the trigger.
---

# Delivery-Loop Retro

## What this is

A delivery loop (`frontend-`/`backend-`/`fullstack-delivery-loop`) just ran — an
orchestrator drove a team of specialist subagents through test → diagnose → fix →
review → re-test until ship-ready. This skill turns that run into a **rigorous,
evidence-backed retrospective** whose entire purpose is to **make the next run
better**. The report you write is not for a human to admire and forget; it is the
**input to `skill-evolution-factory`**, which mutates the load-bearing lines of the
loop skills and persona files and measures the delta. So every criticism you make
must point at a *specific file and a specific instruction the factory can change.*

You are the analyst, not the orchestrator. You did not (necessarily) drive the loop;
your job is to reconstruct what happened from the evidence, judge it honestly, and
hand the plugin maintainers a list of changes worth measuring.

## When you run

The natural trigger is **immediately after a loop reaches its boundary** —
"tests green + reviews clean + production-ready", or a stall the user wants
diagnosed. You normally run **in the same session that drove the loop**, so you
have live memory of the dispatches *and* the durable trace on disk. If you're
pointed at a *past* session instead, pass its id to the collector (see below);
everything else is the same.

## The output, and where it goes

One Markdown report per loop run. Resolve the destination **once, in this order**:

1. If a `docs/feedbackloops/` directory exists at the plugin's dev checkout root
   (i.e. `${CLAUDE_PLUGIN_ROOT}/docs/feedbackloops/`), write there. This is where
   `skill-evolution-factory` reads its inputs.
2. Else write to `<host-repo>/docs/feedbackloops/` (the project the loop ran in)
   and **tell the user** the dev checkout wasn't found, so they can move it.

Create the directory if missing. Filename:
`<YYYY-MM-DD>-<loop>-<change-slug>-<session8>.md` — e.g.
`2026-06-18-frontend-delivery-loop-gated-nav-3e3febb7.md`
(`<session8>` = first 8 chars of the session id; `<change-slug>` = the OpenSpec change
or feature the loop delivered, kebab-cased).

## How to write the report

### Step 1 — Collect the trace (deterministic, do this first)

Run the bundled collector from the **host repo root** (the project the loop ran in).
It resolves the session id, transcript path, and a precise per-subagent roster
(tokens, wall-clock, tool-call counts) from the harness transcript, plus each
persona's persisted episode:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/.claude/skills/delivery-loop-retro/scripts/collect_trace.py"
# add --session <id> to target a past run; --json for the raw summary; --help for flags
```

Paste its Markdown **Trace index** verbatim into the report's appendix — it is your
session-id + trace-paths deliverable and the spine of your metrics. Don't hand-tally
what the script already counts; spend your effort on *why* the numbers look like they
do.

The collector is the floor, not the ceiling. The richest evidence is the
**per-subagent return content** and the **roundtrips between dispatches**, which
live in the transcript and in your own memory of the run. `references/evidence-sources.md`
maps every signal — the transcript anatomy, the `toolStats`/`toolBreakdown` that
exposes a persona burning tool calls, the agent-memory episodes (`taskId`, `objective`,
`specDrift`, `notes`), and the OpenSpec change/vault artefacts. **Read it before you
judge** so you cite mechanisms, not impressions.

### Step 2 — Judge along the axes that matter

Reconstruct the run, then form a defensible verdict on each axis. For every claim,
hold yourself to: *what exactly happened, in which dispatch, costing what, and which
skill/agent line is responsible.* The retro doc at
`docs/retro-frontend-delivery-loop-2026-06-05.md` is the bar — notice how each point
names a mechanism (a Radix uncontrolled flip, a `.toastRegion:empty` a11y regression)
and a cost, never a vibe.

- **What worked** — and *why it worked*, so the factory doesn't accidentally erode it.
  A good thing you can't explain is a good thing you'll lose in the next edit. This section is
  **load-bearing downstream**: `skill-evolution-factory` turns each named positive into a *guard
  fixture* — a behaviour the baseline passes that any promoted edit must still pass — so the goal of
  "push the negatives → 0 without losing the positives" is enforced mechanically. Name each positive
  concretely enough that it could be turned into a pass/fail check (the behaviour, the dispatch/episode
  that shows it, the mechanism), not as vague praise. **Favour positives a fresh model would NOT do on
  its own** — a project-specific convention, a named path, a rule the loop only follows because an
  instruction says so. A positive that's just generic good practice (a competent agent does it anyway)
  makes a weak guard: the factory can't protect a behaviour that won't regress when its instruction is
  removed. The load-bearing positives are the non-obvious ones.
- **What went badly** — defects that escaped, wrong verdicts, gates that missed,
  fixers that decided scope they shouldn't have.
- **Friction & waste** — the heart of the report. Where did the loop spend time,
  tokens, and tool calls it didn't need to? Look hard at: high tool-call/long-duration
  dispatches (a driver re-learning the MCP sandbox; a fixer re-discovering
  architecture); **roundtrips** (finding → fix → re-review ping-pong, a fixer blocked
  on an artifact another in-flight task promised, a reviewer re-flagging the same
  thing); redundant dispatches; `AskUserQuestion` rounds that interrupted for
  decisions the user rubber-stamped. **Attribute each one to the responsible
  skill/reference/persona line** — that attribution is what the factory consumes.
- **Agent integration** — how the team composed. Diagnose-vs-fix discipline (did
  reviewers/drivers stay diagnose-only; did fixers avoid deciding what was wrong);
  handoffs and `SendMessage` resumes; parallel-wave file ownership (any clobbering or
  near-miss); whether the orchestrator routed findings to the right fixer; whether
  context was lost across a dispatch boundary. Both what clicked and what ground.

### Step 3 — Turn every negative into an improvement target

This is what separates this report from a diary. For each problem worth fixing,
produce a row the factory can act on directly. A target that doesn't name a file and
an instruction is **not done** — keep working it until it does.

```markdown
## Improvement targets for skill-evolution-factory

| # | Symptom (observed, with cost) | Target file | Section / load-bearing line | Proposed change (falsifiable) | Evidence |
|---|---|---|---|---|---|
| 1 | playwright-expert spent 247 tool calls / 29min re-discovering the MCP sandbox limits | `.claude/agents/frontend/playwright-expert.md` | the "live drive" grounding block | State the known sandbox limits (no `URL`/`Buffer`/`atob`/`setTimeout`; FS at repo root) inline so the driver doesn't probe for them | dispatch #18; episode `…_behaviour…txt` |
```

Rules that make a target usable:
- **Open the real file and read the instruction before you propose changing it.** This is
  the single highest-leverage habit, and the one that most often saves the factory's
  budget. The naive retro proposes "state X in the persona" — but X is frequently *already
  there*, and the real failure is that it's buried, unenforced, or contradicted elsewhere.
  Proposing to add something that exists is worse than no target: the factory spends a full
  tournament proving a no-op. So for every target, read the actual lines, **quote the
  current instruction verbatim**, and frame the change as a *delta against that quote*
  ("line X already says '…' — the fix isn't to add it, it's to hoist it out of a run-on
  bullet into a standalone pre-flight so it's salient"). A target you wrote without opening
  the file is a guess.
- **Anchor to quoted text, not just a line number.** Line numbers are convenient but rot —
  the files get edited (including *by the factory*), and a stale number points at the wrong
  place. The factory re-locates load-bearing blocks by *content*. So cite the **section
  heading and a short quoted phrase** of the instruction as the durable anchor; add the
  line number as a secondary convenience, not the sole locator.
- **Name the real file.** Loop workflow lives in `.claude/skills/<loop>/SKILL.md` and
  its `references/*.md`; persona behaviour lives in `.claude/agents/<area>/<persona>.md`.
  Point at the one that actually carries the instruction — the factory mutates *lines*,
  so "improve the loop" is useless; "the wave-gate rule in `references/review-gate.md`"
  is actionable. Use `references/evidence-sources.md` for the file map if unsure.
- **Make the change falsifiable.** Phrase it as a hypothesis the factory can test:
  "stating X inline will stop the driver probing for it," not "make the driver better."
- **Generalize, don't overfit.** You're proposing edits that fire across *every future
  run*. Fix the class ("fixers copy design snippets verbatim, latent bugs and all → tell
  the architect to mark snippets normative-vs-illustrative"), not the one instance.
- **Cite evidence** — dispatch number, episode filename, or transcript moment — so a
  maintainer can verify the symptom before paying to evolve against it.
- **Don't invent problems.** A clean run with no high-value targets is a finding; say so
  rather than padding the list. The factory wastes budget chasing non-discriminating
  edits.

### Step 4 — Assemble and save

Write the report to the resolved path using the structure below, then tell the user
the path and give a 3-5 line verbal summary (loop, result, top 1-2 improvement
targets). The full annotated template with an example lives in
`references/report-template.md`; the canonical skeleton is:

```markdown
# Delivery-Loop Retro — <loop> · <change-slug>

**Repo:** … · **Branch:** … · **Date:** … · **Result:** <ship-ready | stalled @ …>
**Session:** `<id>` · **Loop shape:** <waves / dispatches / review rounds in one line>

## 1. Metrics            ← from the collector's Trace index, plus what you add
## 2. What worked (and why)
## 3. What went badly
## 4. Friction & waste    ← per-incident, attributed to a skill/agent line, with cost
## 5. Agent integration
## 6. Improvement targets for skill-evolution-factory   ← the hand-off table (Step 3)
## 7. Appendix — evidence
   - Trace index (collector output, verbatim)
   - Notable subagent returns / episodes / Urgent findings
```

## The quality bar

- **Evidence or it didn't happen.** Every positive and negative cites a dispatch, an
  episode, a finding, or a transcript moment. No unsupported adjectives.
- **Cost-quantified.** Friction without a number ("slow", "wasteful") is unactionable.
  Attach tokens, tool calls, wall-clock, or roundtrip count — the collector gives you
  all four per dispatch.
- **Attributed.** Every improvement target names the file and instruction to change.
- **Honest about the clean parts.** Protecting what worked matters as much as fixing
  what didn't — an unexplained strength gets edited away. And don't manufacture targets
  to look thorough.
- **Self-contained.** A maintainer who never saw the run should be able to read the
  report, open the cited traces, and agree with each target without asking you anything.

## Files in this skill

- `scripts/collect_trace.py` — deterministic trace collector (session id, transcript
  path, per-subagent roster with tokens/duration/tool-calls, episode roster, loop
  detection). Stdlib-only, best-effort, never aborts the retro.
- `references/evidence-sources.md` — where every signal lives and how to read it: the
  transcript anatomy, agent-memory episodes, OpenSpec change/vault artefacts, and the
  file map (which skill/agent file carries which behaviour) you target in Step 3.
- `references/report-template.md` — the full annotated report template with a worked
  example, modelled on `docs/retro-frontend-delivery-loop-2026-06-05.md`.
