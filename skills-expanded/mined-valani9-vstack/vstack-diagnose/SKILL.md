---
name: vstack-diagnose
description: The fast path. Throw one agent or multi-agent trace at vstack and get a ranked, cross-pattern findings report back in a single call. The runner infers the trace shape (individual / team / org) and runs the right bundle — or a named recipe for a specific failure mode — without the user having to know the pattern catalogue.
---

# /vstack-diagnose

The "just run it" skill. Where `/vstack-pick-pattern` interviews the user and *recommends* patterns, and `/vstack-post-incident` runs a deliberate AAR → Lewin → downstream pipeline, this skill does the one thing people most often want: take a trace, run the right bundle, hand back a ranked report. One tool call.

## When to invoke

- "Here's a trace — what's wrong with it?"
- "Run vstack on this." / "Diagnose this run."
- The user already has a structured trace and wants findings, not an interview.
- A failure mode the user can name in one phrase ("it's stuck in a loop", "the agents are arguing", "it silently failed") — map that phrase to a recipe.

If the user wants to *understand which pattern to use* before running, route to `/vstack-pick-pattern`. If they want a deep, narrated post-mortem with interventions, route to `/vstack-post-incident`. This skill is the quick triage in between.

## Preflight

The runner accepts a generic trace object. Surface whatever the user has:

- `goal` — what the agent/crew was asked to do
- `steps` — the ordered action/observation records (or `messages` for a crew)
- `outcome` — what actually happened
- `success` — boolean

The runner **infers the trace shape** from the trace's attributes (e.g. an `agents`/`messages` list → team; an `org_chart`/`reports_to` → org; otherwise individual). You rarely need to set `shape` by hand. If the user has a JSON trace file, take it verbatim — don't re-key it.

Cost note: the CLI defaults to `--client none`, which runs the deterministic analyzers but skips paid LLM calls. Only pass a real client (`anthropic` / `openai` / `ollama`) when the user wants LLM-backed findings and has the matching key set.

## Workflow

### Step 1 — Decide: default bundle or named recipe?

If the user named a failure mode, route it to a recipe. Browse the catalogue with `vstack-recipes` (or `vstack-diagnose --list-recipes`):

| User said… | Recipe |
|---|---|
| "stuck in a loop", "keeps retrying the same thing" | `stuck_in_loop` |
| "the agents are arguing / can't agree" | `agents_arguing` |
| "it failed but didn't say why", "silent failure" | `silent_failure` |
| "one agent is the bottleneck", "throughput tanked" | `bottleneck_agent` |
| "feedback isn't landing" | `bad_feedback_loop` |
| "the culture/behavior drifted" | `culture_drift` |
| "it's confidently wrong", "overconfident" | `overconfidence_spiral` |
| "it just agrees with everything", "sycophantic" | `sycophancy_drift` |
| "it keeps refusing valid asks" | `refusal_cascade` |
| "it declared done before it was done" | `premature_completion` |
| "it's misusing tools" | `tool_misuse` |

No clear recipe? Omit `recipe` and let the runner pick the shape-appropriate default bundle.

### Step 2 — Run it (one call)

Via MCP:

```
vstack_diagnose with:
  trace: <the trace object>
  shape: <omit to infer; or individual | team | org>
  recipe: <omit, or one of the recipe names above>
  mode: standard          # quick for a fast pass, forensic for depth
```

Or via the CLI when the user is in a shell:

```bash
vstack-diagnose --trace trace.json                       # infer shape, default bundle
vstack-diagnose --trace trace.json --recipe stuck_in_loop
vstack-diagnose --trace trace.json --client anthropic --mode forensic
```

If one pattern in the bundle errors, the rest still run; the failure is reported in the response's `errors` — surface it, don't retry the whole bundle silently.

### Step 3 — Rank and read out

The report ranks findings by severity across the whole bundle. Produce a tight readout:

```
## Diagnose — <one-line goal>  (<shape>, <recipe or "default bundle">)

**Top findings:**
1. **<pattern friendly name>** (<severity>) — <one-line finding>
2. **<pattern>** (<severity>) — <one-line finding>
3. …                                  (cap at the top 3-5)

**Headline:** <the single highest-severity finding, in one sentence>

**Next step:**
- If one finding clearly dominates → run that pattern in `forensic` mode, or route to the matching deep skill.
- If the trace is a real incident worth a full post-mortem → hand off to `/vstack-post-incident`.
- If it's a crew-wide pattern → hand off to `/vstack-audit-crew`.
```

Keep it under ~250 words. The full report JSON goes in a collapsible block.

## Failure modes

- **No structured trace, only a narrative.** Extract the four fields (`goal`/`steps`/`outcome`/`success`) together, then run in `quick` mode. Don't fabricate steps.
- **Runner can't infer the shape.** Ask one question: "one agent, a crew, or an org structure?" and pass `shape` explicitly.
- **All findings come back severity=none.** Either the run is genuinely healthy or the trace is too thin. Note which, and suggest `/vstack-baseline` if they want to bank it as a healthy reference.
- **User wants the recipe catalogue.** `vstack-recipes` lists them; `vstack-recipes --show <slug>` explains one; `vstack-recipes --match "<free-text failure>"` routes a description to a recipe.

## Composition

- Upstream: `/vstack` (router), or invoked directly when the user has a trace in hand.
- Downstream by finding: `/vstack-post-incident` (full AAR), `/vstack-audit-crew` (crew-wide), `/vstack-bottleneck` (load/structure), `/vstack-culture-check` (values/behavior gap).
- Compose with: `/vstack-scorecard` to turn one-off diagnose reports into a tracked per-agent grade, and `/vstack-baseline` to detect drift over time.

## What you don't do here

- Don't interview. If the user wanted to be interviewed they'd be in `/vstack-pick-pattern`. Run first, ask only if the trace can't be parsed.
- Don't run forensic mode by default — it's the most expensive path. Standard first; escalate one dominant finding if it matters.
- Don't start a paid LLM call without the user opting into a client. The default deterministic pass is free and often enough for triage.
