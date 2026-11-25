---
name: steelman
description: >
  Build the strongest possible version of an argument, then argue the complete opposite with equal conviction. Use when the user asks to steelman something, argue both sides, make the strongest case, or understand the best version of an opposing view.
argument-hint: "idea, argument, or position to steelman"
---

# Steelman

**Context:** $ARGUMENTS

Build the strongest version of the argument AND the strongest contrary case. Two deliverables, not one.

## Workflow

### 1. Check for existing state

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" show
```

If a graph already exists from a prior run, **add to it** — the other agents' work lives there. Only reset when starting a genuinely new subject, and say so first:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" reset
```

### 2. Build the steelman

Read `${CLAUDE_PLUGIN_ROOT}/references/steelmanning.md`.

Restate the idea in its STRONGEST form:
- Remove weak phrasing the proponent would fix if pointed out
- Add supporting evidence they may have missed
- Identify the core claims and the assumptions they rest on
- Present the version that the idea's smartest, most informed defender would present

For each claim and assumption, register in the graph:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<claim-id>" claim --obs "<fact 1>" "<fact 2>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<assumption-id>" assumption --obs "<fact>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<claim-id>" assumes "<assumption-id>" --agent advocate
```

**Ground what you assert.** A claim with no `supports` edge cannot survive — it is reported as unsupported, not as winning. Register the evidence and precedent that back each claim, and ground the assumptions too:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<evidence-id>" evidence --obs "<source and figure>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<evidence-id>" supports "<claim-id>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<precedent-id>" precedent --obs "<who did this before, and what happened>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<precedent-id>" supports "<claim-id>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<evidence-id>" supports "<assumption-id>" --agent advocate
```

Present the steelman to the user.

### 3. Build the contrary case (Dissoi Logoi)

Read `${CLAUDE_PLUGIN_ROOT}/references/dissoi-logoi.md`.

Apply the formula: "X can be Y and not-Y." Argue the complete opposite case with equal conviction. Not a weak rebuttal, a full-throated argument that the idea is wrong.

Register counter-arguments in the graph:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<counter-id>" counter --obs "<fact>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<evidence-id>" evidence --obs "<fact>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<counter-id>" undermines "<claim-id>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<evidence-id>" supports "<counter-id>" --agent advocate
```

Present the contrary case to the user.

### 4. Show where each side is strongest

Run `analyze` to see the structural picture:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" analyze
```

Summarize: which claims have strong support, which assumptions are ungrounded, where reasonable people could disagree.

## Output format

Present two clearly labeled sections:

**The Strongest Case FOR:** (the steelman)
**The Strongest Case AGAINST:** (dissoi logoi)
**Where Each Side Is Strongest:** (from graph analysis)

## Resources

- `${CLAUDE_PLUGIN_ROOT}/references/steelmanning.md` — load always. Defines what steelmanning is, the straw man / weak man / hollow man anti-patterns to avoid, and the principle that you must address the strongest form of the argument.
- `${CLAUDE_PLUGIN_ROOT}/references/dissoi-logoi.md` — load always. The Greek tradition of contrasting arguments, Schiappa's formula, Protagoras' principle that every argument has two contradicting sides.
- `${CLAUDE_PLUGIN_ROOT}/references/argument-semantics.md` — load always. How the verdict is computed: attacks from defeated nodes stop counting, so counters decide outcomes.
- `${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts` — run throughout to register claims, assumptions, counters, evidence, and their relations.

## Gotchas

- The steelman must be genuinely strong. If a proponent would read it and say "that's not my best argument," you failed. Spend real effort here.
- The contrary case must be argued with equal conviction. If it reads like a straw man rebuttal, redo it.
- Graph entity names should be short kebab-case identifiers, not full sentences. Observations carry the detail.
- The graph state persists in /tmp. If another skill (crucible, verdict) runs after this, it reads the same graph. This is by design.
