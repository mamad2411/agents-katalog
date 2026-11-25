---
name: vstack-post-incident
description: Full post-incident review pipeline for an AI-agent or multi-agent run that failed or underperformed. Runs the foundational After-Action Review, then Lewin attribution to localize the failure, then 1-2 downstream patterns chosen by what the upstream surfaced.
---

# /vstack-post-incident

The vstack workflow when an agent run misfired and you want a structured readout instead of a one-liner.

## When to invoke

- The user says "postmortem", "after-action review", "AAR", "what went wrong".
- An agent / multi-agent crew failed a task and the user wants to understand *why*.
- An agent was confidently wrong, refused valid feedback, or produced an answer that broke downstream consumers.

Do not invoke for *successful* runs the user wants to retrospectively learn from — use `/vstack-baseline` for that. AAR can run on successful runs too, but post-incident is specifically the failure path.

## Preflight

The pipeline needs at least an `AgentTrace` shape (vstack.aar input):

- `goal` — what the agent was asked to do (1-2 sentences)
- `steps` — the ordered list of input/tool_call/observation/output records
- `outcome` — what actually happened
- `success` — boolean (typically false here)

If the user has a structured trace (JSON, OpenTelemetry export, framework-native dump), ask them to share it verbatim. If they have only a narrative, extract the four fields together; ask one question per missing field. Don't stall on completeness — partial traces still produce useful AARs.

For Lewin to make a sharp attribution, surface (if the user can recall):

- The model used (e.g. `claude-opus-4-7`)
- Any tools the agent called
- Any RAG / context the agent received
- The user's initial attribution ("I think it's the model" / "I think the prompt is bad")

## Workflow

### Step 1 — AAR (foundational)

Call:

```
vstack_aar with:
  goal: <surfaced>
  steps: <surfaced>
  outcome: <surfaced>
  success: false (typical)
  mode: standard   # forensic if the incident matters and the user wants depth
```

Parse the response. The detection model carries `lessons[]`, `next_steps[]`, `trace_quality_audit`, and a list of `recommended_downstream` patterns in its `attached_playbooks` / composition manifest.

### Step 2 — Lewin attribution

Always chain into Lewin (it's the AAR composition's #1 downstream for failure runs). Map the AAR trace into the `AgentFailureTrace` shape:

```
vstack_lewin with:
  agent_id: <if available, else "anonymous">
  model_name: <model>
  task: <AAR goal>
  steps: <re-typed FailureStep records: input | tool_call | observation | output>
  outcome: <AAR outcome>
  success: false
  initial_attribution: <user's verbal attribution if any>
  mode: standard
```

Inspect the response's `dominant_locus`:

- `internal` → the model itself is implicated. Downstream: `goleman_ei` (if the failure was emotional / interpersonal), `hexaco` (if the personality signature looks off), or `bias_stack` (if reasoning is the locus).
- `environmental` → prompt / tools / scaffolding. Downstream: `org_structure` (if multi-agent and routing is suspect), `yerkes_dodson` (if context overflow is implicated), `glaser_conversation` (if user-agent dialogue degraded).
- `interactional` → neither alone fixes it. Run both upstream + downstream.

### Step 3 — One or two downstream patterns

Pick 1-2 patterns from `recommended_downstream` (in the AAR + Lewin responses) OR from the table above. Don't fire more than 2 — the user is here for a readout, not a 7-pattern cascade.

Call the chosen pattern with the same trace mapped into its input shape. Most multi-agent patterns accept a trace very similar to AAR's; Module 1 patterns sometimes need the agent's identity and turn-level data.

### Step 4 — Synthesize

Write the executive readout. Format:

```
## Post-Incident Review: <one-line goal>

**What happened:** <one paragraph from the AAR outcome + lessons[0..2]>

**Where the failure lives:** <Lewin dominant_locus + the one-sentence explanation>

**Why it broke (deepest layer):** <the dominant intervention from the downstream pattern>

**Three things to do this week:**
1. <highest-impact intervention from AAR.next_steps + downstream.interventions, deduped>
2. ...
3. ...

**Reading list:** <if the downstream attached_playbooks point at >= 2 papers, list them>
```

Cap at ~400 words. The structured detection JSONs go in a collapsible section for users who want to dig deeper.

## Failure modes

- **No trace at all.** Run AAR in `quick` mode against whatever narrative the user has. AAR's profile-pattern detector will flag the trace-quality gap; surface that to the user and stop. Don't fabricate trace steps.
- **Lewin says `indeterminate`.** Either the data is too thin or the failure is genuinely interactional. Ask the user one more question (typically: "Did the same prompt work last week?") and re-run Lewin in `forensic` mode.
- **Downstream pattern errors.** Surface the error to the user verbatim, don't retry silently. Most analyzer errors are validation issues from a malformed trace — re-extract the missing field and retry.

## Composition

- Upstream from this skill: `/vstack` (the router).
- Downstream from this skill: nothing automatic. The intervention list points the user at next actions (often outside vstack — a code change, a prompt edit, a tool reconfigure).
- Compose with: `/vstack-audit-crew` if the incident exposes broader team dynamics, `/vstack-culture-check` if the AAR profile-pattern surfaces a systemic culture issue.

## What you don't do here

- Don't run AAR in `forensic` mode by default. It's 4 LLM calls; reserve for high-stakes incidents.
- Don't run more than 4 patterns total. The cascade has diminishing returns past Lewin + 2 downstream.
- Don't moralize or assign blame. The diagnostic is structural; presentation should be too.
