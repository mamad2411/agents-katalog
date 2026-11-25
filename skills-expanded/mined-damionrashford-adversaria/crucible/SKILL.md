---
name: crucible
description: >
  Stress-test any idea, proposal, or plan by finding its weakest points, probing hidden assumptions with Socratic questions, and identifying failure modes through red team analysis. Use when the user asks to stress-test, poke holes, find weaknesses, red team, challenge, or ask 'what could go wrong' or 'what am I missing'.
argument-hint: "idea, plan, or proposal to stress-test"
---

# Crucible

**Context:** $ARGUMENTS

Find everything wrong with this idea. Socratic questioning, hostile review, and adversarial simulation.

## Workflow

### 1. Initialize (or pick up existing graph)

Check if a graph already exists from a prior steelman:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" show
```

If empty or no prior state, build the graph from scratch. Identify the idea's core claims and assumptions and register them:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" reset
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<claim-id>" claim --obs "<fact>" --agent adversary
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<assumption-id>" assumption --obs "<fact>" --agent adversary
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<claim-id>" assumes "<assumption-id>" --agent adversary
```

If a graph already exists, use it directly.

### 2. Socratic Elenchus (probe assumptions)

Read `${CLAUDE_PLUGIN_ROOT}/references/socratic-method.md`.

Apply Vlastos' steps:

1. Identify the thesis (what the idea claims)
2. Identify premises the proponent would agree with
3. Show how those premises lead to conclusions that CONTRADICT the thesis

Ask 3-5 penetrating questions. Each question targets a specific assumption. Present the questions to the user.

### 3. Structural analysis

Run the graph analysis to find gaps the questions should have exposed:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" analyze
```

This reveals `ungrounded_assumptions` (nothing supports them), `unstable_claims` (with `failed_dependencies` naming what they rest on that isn't established), `exposed_weaknesses` (still standing — nothing countered them), `most_contested_claims`, `circular_reasoning` (dependency cycles), `orphaned_entities` (attached to nothing), and `labels` — the current `IN`/`OUT`/`UNDECIDED` standing of every node.

Read `labels` before attacking. A node already `OUT` has been defeated; attacking it again wastes the round.

### 4. Hostile review

Read `${CLAUDE_PLUGIN_ROOT}/references/crucible.md`.

For each stakeholder who would need to approve or fund this idea, ask: what is their harshest possible question? Can the idea survive it as stated?

Register weaknesses found:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<weakness-id>" weakness --obs "<what makes it weak>" --agent adversary
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<weakness-id>" undermines "<claim-id>" --agent adversary
```

Rate each attack when you register it: `--strength decisive` only when the point, if true, ends the argument by itself; `--strength minor` to put a nitpick on the record without pretending it is fatal; omit the flag for a serious attack (the default). Minors never defeat — they surface as reservations for the judge. One objection, one node.

**A weakness must attack something.** Register it with `undermines` pointed at the claim it damages. A weakness with no outgoing attack is inert — it appears in the graph and changes no verdict, which is the single easiest way to do this work and have it count for nothing.

Use `contradicts` when two claims cannot both be true, and `if_fails` only between claims where one carries the other — `A if_fails B` reads "if A fails, B fails". Never point `if_fails` from a weakness; that makes the target depend on the weakness holding, inverting the result.

### 5. Red team (failure modes)

Read `${CLAUDE_PLUGIN_ROOT}/references/red-team.md`.

Identify 3-5 ways this idea fails. For each failure mode:

- What happens?
- How likely is it?
- How bad is it?
- Is there a defense?

If mitigations exist, register them:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<mitigation-id>" mitigation --obs "<how it helps>" --agent adversary
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<mitigation-id>" mitigates "<weakness-id>" --agent adversary
```

### 6. Present findings

Run analysis again to see the updated picture:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" analyze
```

## Output format

Present three sections:

**Socratic Questions:** 3-5 questions and the assumptions they target
**Weakest Points:** What a hostile reviewer would attack (from structural analysis + review)
**Failure Modes:** How this fails, likelihood, severity, and whether defenses exist

## Resources

- `${CLAUDE_PLUGIN_ROOT}/references/socratic-method.md` — load always. Vlastos' elenchus steps, the maieutic method, Boghossian's warning about humiliation vs. productive discomfort.
- `${CLAUDE_PLUGIN_ROOT}/references/crucible.md` — load always. The stress-test review board method, NASA/Pentagon origin, the principle that the review must be MORE adversarial than the real presentation.
- `${CLAUDE_PLUGIN_ROOT}/references/red-team.md` — load always. RAND Corporation origins, Israel's Ipcha Mistabra, groupthink as the enemy, reconnaissance before attack.
- `${CLAUDE_PLUGIN_ROOT}/references/argument-semantics.md` — load always. How the verdict is computed: attacks from defeated nodes stop counting, so counters decide outcomes.
- `${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts` — run throughout to register weaknesses, mitigations, and analyze structural gaps.

## Gotchas

- **Run `analyze` before writing findings.** The graph catches things intuition misses: assumptions with zero supporting evidence, claims that depend on contradicted assumptions.
- **Nemeth's warning applies here too.** Generic "but what if it fails?" is worthless. Every objection must cite a specific mechanism of failure.
- **If a graph already exists from a prior `/steelman`, use it.** Don't rebuild from scratch. The crucible builds on what steelman established.
- **Graph entity names: short kebab-case identifiers.** Observations carry the detail.
- **The graph persists per project between skill runs.** If `/verdict` runs after this, it reads the same graph.
