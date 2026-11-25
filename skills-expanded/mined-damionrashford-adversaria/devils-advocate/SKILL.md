---
name: devils-advocate
description: >
  Full adversarial analysis of any idea, proposal, or argument. Runs steelman, crucible, and verdict in sequence for a complete challenge drawing from 10 reasoning traditions. Use when the user asks to play devil's advocate, run a full challenge, or says 'tear this apart' or 'give me the full treatment'.
argument-hint: "idea, plan, or argument to challenge"
---

# Devil's Advocate (Full Analysis)

**Context:** $ARGUMENTS

Run a complete adversarial analysis by orchestrating all three sub-skills in sequence. Each builds on the shared argument graph.

## Workflow

### Phase 1 — Steelman + Contrary Case

Read `${CLAUDE_PLUGIN_ROOT}/references/steelmanning.md` and `${CLAUDE_PLUGIN_ROOT}/references/dissoi-logoi.md`.

Reset and initialize:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" reset
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" reset
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" init "<subject>" --total 7
```

If the user asked to *watch* the analysis, start the live transcript in the background first — never otherwise, since it opens a browser:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/transcript.ts" serve &
```

Build the strongest version of the argument, then argue the complete opposite with equal conviction. Register both in the graph as you go — a claim that never reaches the graph cannot be defended in Phase 3.

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<claim-id>" claim --obs "<fact>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<assumption-id>" assumption --obs "<fact>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<claim-id>" assumes "<assumption-id>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<evidence-id>" evidence --obs "<source>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<evidence-id>" supports "<claim-id>" --agent advocate
```

Ground every assumption you can. An assumption with no `supports` edge demotes the claim resting on it.

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" think 1 "<steelman>"
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" think 2 "<contrary case>"
```

Present both to the user before continuing.

### Phase 2 — Crucible

Read `${CLAUDE_PLUGIN_ROOT}/references/socratic-method.md`, `${CLAUDE_PLUGIN_ROOT}/references/crucible.md`, and `${CLAUDE_PLUGIN_ROOT}/references/red-team.md`.

Ask 3-5 Socratic questions targeting specific assumptions. Run structural analysis:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" analyze
```

Use the gaps to drive the hostile review. Register every weakness as a node that attacks what it damages — an unattached weakness changes no verdict.

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<weakness-id>" weakness --obs "<what breaks>" --agent adversary
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<weakness-id>" undermines "<claim-id>" --agent adversary
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<claim-a>" contradicts "<claim-b>" --agent adversary
```

A failure mode **attacks** — use `undermines`. `if_fails` is different: it means "if the source fails, the target fails", so it links two claims where one carries the other. Do not point `if_fails` from a weakness at a claim; that makes the claim depend on the weakness holding, which inverts the result.

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<load-bearing-claim>" if_fails "<dependent-claim>" --agent adversary
```

Then answer your own attacks honestly. A weakness with a surviving counter or mitigation stops counting against the claim — that is the mechanism, not a courtesy:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<counter-id>" counter --obs "<why the attack fails>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<counter-id>" undermines "<weakness-id>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<mitigation-id>" mitigates "<weakness-id>" --agent advocate
```

Identify 3-5 failure modes. If multiple independent failure modes exist, branch:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" think 3 "<socratic questions>"
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" think 4 "<crucible findings>"
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" think 5 "<red team findings>"
```

**REVISION CHECK:** If the crucible reveals the steelman was too generous, revise:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" revise 1 "<revised steelman>" --reason "<what changed>"
```

### Phase 3 — Verdict

Read `${CLAUDE_PLUGIN_ROOT}/references/social-gadfly.md`.

Name the one uncomfortable truth nobody wants to say. Then run the structural verdict:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" think 6 "<gadfly sting>"
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" verdict
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" think 7 "<verdict>"
```

## Output format

Present the full analysis with clear sections:

1. **The Strongest Case:** (steelman)
2. **The Strongest Case Against:** (dissoi logoi)
3. **Socratic Questions:** (3-5 questions targeting assumptions)
4. **Weakest Points:** (crucible findings from structural analysis)
5. **Failure Modes:** (red team, with branches if multiple)
6. **The Uncomfortable Truth:** (gadfly sting)
7. **Verdict:** Survives / Does not survive / Needs more work

Optionally render the full chain and graph:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts" render
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" export
```

## Resources

References (load the file matching the current phase):
- `${CLAUDE_PLUGIN_ROOT}/references/steelmanning.md` — load in Phase 1.
- `${CLAUDE_PLUGIN_ROOT}/references/dissoi-logoi.md` — load in Phase 1.
- `${CLAUDE_PLUGIN_ROOT}/references/socratic-method.md` — load in Phase 2.
- `${CLAUDE_PLUGIN_ROOT}/references/crucible.md` — load in Phase 2.
- `${CLAUDE_PLUGIN_ROOT}/references/red-team.md` — load in Phase 2.
- `${CLAUDE_PLUGIN_ROOT}/references/social-gadfly.md` — load in Phase 3.
- `${CLAUDE_PLUGIN_ROOT}/references/polemic.md` — load when the gadfly sting needs rhetorical force.
- `${CLAUDE_PLUGIN_ROOT}/references/devils-advocate.md` — load for Nemeth's warning about inauthentic dissent.
- `${CLAUDE_PLUGIN_ROOT}/references/roman-rota.md` — load when multi-level appellate review structure is relevant.
- `${CLAUDE_PLUGIN_ROOT}/references/lawsuits-against-the-devil.md` — load when the idea seems too absurd or sacred to challenge.
- `${CLAUDE_PLUGIN_ROOT}/references/argument-semantics.md` — load always. How the verdict is computed: attacks from defeated nodes stop counting, so counters decide outcomes.

Scripts:
- `${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts` — run throughout. `analyze` before Phase 2, `verdict` in Phase 3.
- `${CLAUDE_PLUGIN_ROOT}/scripts/thought-chain.ts` — run at every phase. `revise` when later phases invalidate earlier ones. `branch` for multiple failure modes.

## Gotchas

- **Nemeth's warning is real.** Inauthentic, going-through-the-motions dissent makes people MORE entrenched. Every objection must cite a specific mechanism of failure.
- **Steelman FIRST, always.** If you attack a weak version, the entire analysis is worthless.
- **Run `analyze` before the crucible.** The graph catches structural gaps prose misses.
- **Revise when warranted.** A linear pass that never revisits is weaker than one that evolves.
- **The gadfly sting is not another weakness.** It's the foundational uncomfortable truth.
- **Graph entity names: short kebab-case.** Observations carry the detail.
