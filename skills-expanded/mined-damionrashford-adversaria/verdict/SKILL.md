---
name: verdict
description: >
  Deliver a structured verdict on any idea, argument, or proposal, identifying what survives scrutiny, what doesn't, and what needs more work. Includes the gadfly sting, the one uncomfortable truth nobody wants to say. Use when the user asks for a verdict, bottom line, final assessment, 'what survives', or 'give it to me straight'.
argument-hint: "idea, argument, or proposal to judge"
---

# Verdict

**Context:** $ARGUMENTS

Deliver the final judgment. What survives, what doesn't, and the uncomfortable truth.

## Workflow

### 1. Check for existing graph state

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" show
```

If a graph exists from prior `/steelman` or `/crucible` runs, use it. If empty, build one from scratch by identifying the idea's claims, assumptions, evidence, weaknesses, and counter-arguments:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" reset
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<claim-id>" claim --obs "<fact>" --agent judge
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<assumption-id>" assumption --obs "<fact>" --agent judge
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<weakness-id>" weakness --obs "<fact>" --agent judge
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<claim-id>" assumes "<assumption-id>" --agent judge
```

### 2. Gadfly sting

Read `${CLAUDE_PLUGIN_ROOT}/references/social-gadfly.md`.

Name the ONE thing nobody wants to say about this idea. Not a weakness (those are tactical), the foundational uncomfortable truth that would remain even if everything else went right.

Ask yourself:
- What is everyone avoiding saying?
- What assumption is so foundational that questioning it feels rude?
- What would a persistent, unsilenceable critic keep coming back to?

If the gadfly sting reveals something that changes the structural picture, register it:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<counter-id>" counter --obs "<the uncomfortable truth>" --agent judge
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<counter-id>" undermines "<claim-id>" --agent judge
```

### 3. Structural verdict

Run the graph verdict:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" verdict
```

The verdict is computed by grounded semantics, not by counting attacks. Each claim lands in exactly one bucket:

| Key | Means |
| :--- | :--- |
| `survives_scrutiny` | supported, and every attacker was itself defeated. `survived_attacks` says how many it withstood |
| `does_not_survive` | defeated by an attacker that still stands. `reason` names it |
| `needs_more_work` | attacks unresolved, or resting on something unestablished, or unsupported |
| `unmitigated_weaknesses` | weaknesses still standing — nothing countered or mitigated them |
| `circular_reasoning` | dependency cycles, if any |

`open_reservations` on a surviving claim lists minor attacks still standing — nitpicks that could not defeat it but belong in the ruling. Mention them. Report these as the script computed them. Do not re-derive a verdict from your own reading of the argument — the whole point is that the ruling comes from the record.

### 4. Present the verdict

## Output format

**The Uncomfortable Truth:** One sentence. The gadfly sting.

**Survives Scrutiny:** Claims that were attacked and held, or that stand on unchallenged support. Say what defeated each attacker — "survives because X was countered by Y" is the citation.

**Does Not Survive:** Claims with a surviving attacker. Name the attacker. These need to be dropped or reworked.

**Needs More Work:** Three different situations, and they need different advice — say which applies. Unresolved attacks (the attackers are themselves contested), a dependency that was never established, or no supporting evidence at all. State what would settle it.

**Unmitigated Weaknesses:** Exposed risks nothing answered. What has to happen before this moves forward.

**Circular Reasoning:** If non-empty, name the cycle. A claim propped up by what it props up is not established.

Optionally export the full graph for the user:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" export
```

## Resources

- `${CLAUDE_PLUGIN_ROOT}/references/social-gadfly.md` — load always. Socrates as the stinging fly, the cost of silencing uncomfortable questioners, the distinction between tactical weaknesses and foundational truths.
- `${CLAUDE_PLUGIN_ROOT}/references/polemic.md` — load when the gadfly sting needs rhetorical force or the user asks for a forceful take. Constructive polemic exposes genuine errors without demonizing.
- `${CLAUDE_PLUGIN_ROOT}/references/argument-semantics.md` — load always. How the verdict is computed: attacks from defeated nodes stop counting, so counters decide outcomes.
- `${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts` — run `verdict` for structural analysis, `export` for full graph markdown.

## Gotchas

- **The gadfly sting is not another weakness.** Weaknesses are tactical (the API might go down). The gadfly names a foundational truth (the team doesn't actually want this to succeed). If your gadfly sting could appear in a list of weaknesses, it's not stinging enough.
- **If a graph exists from prior skills, use it.** The verdict is strongest when it reads a graph built by `/steelman` and `/crucible`. Running verdict standalone works, but the graph will be thinner.
- **The verdict script's output is structural, not rhetorical.** It tells you what survives based on graph topology. Your job is to synthesize that into a human-readable judgment.
- **Don't soften the gadfly.** Socrates was executed for it. The uncomfortable truth is uncomfortable. Name it plainly.
