---
name: vstack-culture-check
description: Two-layer culture audit. Schein's three-layer model (artifacts / espoused values / underlying assumptions) finds the gap between what the team says it does and what its behavior assumes; Robbins-Judge's 7-characteristic profile maps the overall culture type. Optionally adds McGregor (Theory X / Y) when the symptom looks orchestrator-driven.
---

# /vstack-culture-check

Use when the agent crew's *behavior* doesn't match the *intent* the team writes down, or when "feel" is wrong but no single failure surfaced it. This is the structural / values-layer skill, not the symptom-layer skill (`/vstack-audit-crew`).

## When to invoke

- "The team values fast iteration but the agents never ship."
- "We wrote a careful spec but the crew clearly ignores it."
- "It just doesn't feel like a <team identity> shop."
- "Why does this agent always do X when we told it to do Y?"
- Pre-investor / pre-stakeholder culture review.

## Preflight

Culture inference works on conversational substrate, not on single failures. Surface:

- **Crew identity** — what the team *says* it is (mission statement, README, team manifesto, founding story)
- **Behavior corpus** — at least 20-50 messages across multiple tasks, or a few hours of crew session traces
- **Espoused values** — anything written down: "we value X" docs, design principles, prompts
- **One specific gap** — the moment the user said "wait, that's not what we said we'd do"

If only the gap is available, run Schein in `quick` mode — it can do inference on a single contradiction. Don't insist on a full corpus.

## Workflow

### Step 1 — Schein iceberg (always primary)

```
vstack_schein_culture with:
  agent_id_or_crew: <name>
  task: <one of the tasks the crew worked on>
  observations: <verbatim records: artifact / espoused_value / behavior>
  outcome: <surfaced>
  success: <bool, optional>
  mode: standard
```

Schein's response gives three layer evidence sets (artifacts / espoused / underlying assumptions) plus an `alignment_drift_audit` showing where the layers diverge. The dominant finding is *which assumption-layer norm is overriding the espoused value*.

### Step 2 — Robbins-Judge 7-characteristic profile

```
vstack_robbins_culture with:
  <same trace shape>
  mode: standard
```

Robbins-Judge scores the crew on seven dimensions: innovation, attention to detail, outcome orientation, people orientation, team orientation, aggressiveness, stability. It produces a culture-type label (`innovative` / `stable_bureaucratic` / `outcome_obsessed` / etc) that the user can compare to *what they wanted to build*.

### Step 3 — Optional: McGregor (Theory X / Theory Y)

Run only if Schein surfaces an *orchestrator-trust* gap — assumptions like "agents need to be told what to do" or "agents will skip checks if not forced". Otherwise skip.

```
vstack_mcgregor with:
  trace: <orchestrator-agent dialogue surfaced from the corpus>
  mode: standard
```

The output places the orchestrator on the X (controlling, low-trust) — Y (autonomy-granting, high-trust) axis. Useful when the culture audit is really about an over-controlling top of the hierarchy.

### Step 4 — Synthesize

```
## Culture Check — <crew name>

**Espoused vs. assumed** (Schein):
- What the team *says* it values: <surfaced espoused value>
- What the behavior *assumes* instead: <Schein's identified hidden assumption>
- Gap severity: <severity>

**Culture profile** (Robbins-Judge):
- Seven-axis label: <type>
- Closest mismatch to stated intent: <one axis where the crew is most off-target>

**Orchestrator overlay** (McGregor, if ran):
- Theory X vs Y leaning: <one sentence>

**The headline:** <one sentence — the gap between intent and behavior, named>

**Three high-leverage interventions:** (Schein + Robbins playbooks, deduped, ranked)
1. <intervention with target layer/dimension>
2. ...
3. ...

**Reading:** <if Schein attached_playbooks include canonical anchors (Schein 1985 / 2010 / 2017, Robbins-Judge), list the most relevant 1-2>
```

Cap at ~450 words.

## Failure modes

- **Only a single artifact, no behavioral corpus.** Schein can still run in `quick` mode but won't surface assumption-layer drift; surface the limitation in the readout.
- **Robbins disagrees with Schein.** That's interesting, not an error. The two operate on different axes — Schein looks for layer mismatches, Robbins for type profile. Both can be wrong about different things; surface both verdicts.
- **The "culture" complaint is really a structural one.** If Schein's evidence keeps pointing at decision authority / reporting / load, hand off to `/vstack-bottleneck`.

## Composition

- Upstream: `/vstack`, `/vstack-audit-crew` (when an audit surfaced culture as the deep cause), `/vstack-pick-pattern`.
- Downstream: `/vstack-baseline` to track culture drift across releases.
- Compose with: `/vstack-post-incident` to ground the culture findings in a specific recent incident.

## What you don't do here

- Don't run all 4 patterns by default. McGregor is conditional.
- Don't synthesize as a personality verdict on the human team. The audit is on the crew (the agents). Even if the team's own culture is the upstream cause, name the *agent-system behavior* as the artifact you're auditing.
- Don't treat Robbins's culture-type label as prescriptive. It's descriptive; the intervention list points at how to nudge the profile.
