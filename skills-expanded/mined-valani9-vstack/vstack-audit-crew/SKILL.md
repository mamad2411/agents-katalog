---
name: vstack-audit-crew
description: Multi-pattern health check for a multi-agent crew. Runs Lencioni (dysfunctions pyramid), Edmondson (psychological safety), Trust Triangle (logic / authenticity / empathy), Process Gain/Loss (coordination productivity), and Bias Stack (reasoning hygiene) against the same crew trace and synthesizes a single readout.
---

# /vstack-audit-crew

A 10-20 minute health check across the five dimensions that most multi-agent crews fail on. Use when the crew is "off" but the user can't point at one specific failure.

## When to invoke

- "The crew isn't working but I can't put my finger on it."
- "We've shipped 6 agents and they don't collaborate well."
- A quarterly / pre-launch / pre-handoff team review.
- After `/vstack-post-incident` if the incident exposed broader team dynamics rather than a single technical bug.

## Preflight

The audit needs a multi-agent crew interaction. Minimum surface:

- **Agents list** — names + brief role description (3-12 agents is the sweet spot; more than 20 means run `/vstack-bottleneck` first).
- **Messages** — the inter-agent message log for at least one substantive task. JSON, OpenTelemetry, or chat-log dump all work.
- **Goal** — what task the crew was solving.
- **Outcome** — how the task ended (success / partial / failure).

If the user has multiple crew runs, pick the most recent substantive one. Don't average across runs — each run's audit is its own readout.

## Workflow

### Step 1 — Run Lencioni (the pyramid that drives the order)

```
vstack_lencioni with:
  goal: <surfaced>
  agents: <agent names>
  messages: <agent message records>
  outcome: <surfaced>
  success: <bool>
  mode: standard
```

Lencioni's response carries the pyramid: absence of trust → fear of conflict → lack of commitment → avoidance of accountability → inattention to results. The lowest unhealthy layer is your *root* finding; everything above is symptom.

### Step 2 — Run the four supporting audits in parallel (conceptually)

Issue these four calls. If your MCP client supports parallel tool calls, fire them simultaneously; otherwise sequence them.

```
vstack_psych_safety        # Edmondson 7-item proxy + dissent / dissent-suppression detection
vstack_trust_triangle      # Frei & Morriss logic / authenticity / empathy
vstack_process_gain_loss   # Steiner: did the crew outperform best-individual, or pay coordination cost?
vstack_bias_stack          # Kahneman/Tversky: anchoring / availability / confirmation / sunk-cost
```

Each takes the same crew trace structure (mapped into the pattern's specific input model — most accept a generic `MultiAgentTrace` shape or close cousin).

### Step 3 — Cross-reference

Build a small table in your head:

| Pattern | Severity | Top finding |
|---|---|---|
| Lencioni | <severity> | <dominant_dysfunction> |
| Edmondson | <severity> | <psych_safety_score / suppression signal> |
| Trust Triangle | <severity> | <which leg is wobbling> |
| Process | <severity> | <gain or loss + magnitude> |
| Bias stack | <severity> | <top bias> |

Look for **chains**: if Lencioni surfaces "absence of trust" and Trust Triangle surfaces "authenticity gap" and Edmondson surfaces "low dissent rate", those three are the same problem at three resolutions. Tag the chain in your synthesis.

### Step 4 — Synthesize

Output a single executive readout. Format:

```
## Crew Health Audit — <crew goal, one line>

**Headline:** <one-sentence diagnosis: the deepest finding from Lencioni, with severity>

**Five-axis snapshot:**
- Trust & dysfunction: <Lencioni severity + layer>
- Psychological safety: <Edmondson severity + signal>
- Trust dimensions: <Trust Triangle severity + leg>
- Coordination: <Process Gain/Loss severity + direction>
- Reasoning hygiene: <Bias Stack severity + top bias>

**The chain:** <one sentence connecting the 2-3 patterns that surfaced the same root issue at different resolutions>

**Three highest-leverage interventions:** (deduped from each pattern's interventions[], ranked by estimated_impact)
1. <intervention> (from <pattern>)
2. ...
3. ...

**Where to look next:** <recommend the next vstack skill — usually /vstack-culture-check or /vstack-bottleneck — if a structural cause shows up>
```

Cap synthesis at ~500 words. Detection JSONs go in a collapsible section.

## Failure modes

- **The user can only produce 2-3 messages.** Run Lencioni + Trust Triangle only. The other three need more conversational substrate. Tell the user the audit is partial and what additional capture would unlock the rest.
- **The crew is single-agent.** This skill is wrong for the situation; pivot to `/vstack-pick-pattern` with a hint about Module 1.
- **One of the four supporting audits errors.** Continue with the other three; note in the readout that the fifth axis is missing.
- **All five come back severity=none.** Either the crew is genuinely healthy or the trace isn't substantive enough. Re-check trace quality (`vstack_aar` quick mode will surface that).

## Composition

- Upstream: `/vstack`, `/vstack-pick-pattern`, occasionally `/vstack-post-incident` follow-up.
- Downstream candidates by finding:
  - Culture / values gap surfacing → `/vstack-culture-check`
  - Structural / load issue surfacing → `/vstack-bottleneck`
  - Decision-pathology dominant → call `vstack_debate_pathology` + `vstack_devils_advocate` directly
- Compose with: `/vstack-baseline` after fixes are applied so the user can track whether the interventions stuck.

## What you don't do here

- Don't run more than 5 patterns. This is the audit budget. If a sixth seems needed, recommend a separate skill instead.
- Don't run any pattern in `forensic` mode by default. Five forensic calls is 20 LLM calls; that's a different product. Save forensic for individual deep-dives.
- Don't anonymize agents in the readout. If the user names them, the names are signal.
