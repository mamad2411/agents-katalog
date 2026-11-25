---
name: appeal
description: >
  Review a standing verdict as a second panel, admitting new counters and evidence the first pass
  missed, then re-run and report what changed. Use when the user disputes a verdict, says it was
  too harsh or too generous, asks to appeal, asks for a second opinion on an analysis, or says the
  judge got it wrong.
argument-hint: "what the verdict got wrong, or leave empty to review the whole ruling"
---

# Appeal (Second Panel)

**Context:** $ARGUMENTS

The Roman Rota does not let the panel that issued a ruling hear its own appeal.
This skill is the second panel: it reviews the standing verdict on the record,
admits what the first pass missed, and re-runs. It is not a rubber stamp and it
is not a reversal engine — most appeals should confirm.

Read `${CLAUDE_PLUGIN_ROOT}/references/roman-rota.md` and
`${CLAUDE_PLUGIN_ROOT}/references/argument-semantics.md`.

## Workflow

### 1. Read the record, then seal it

Never re-argue from the conversation. Appeal from the graph.

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" verdict
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" transcript
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" lock --agent judge
```

`lock` seals the record: the engine will refuse `reset` and refuse edits to prior
testimony until `unlock`. This is enforced, not a convention — a sealed entity
cannot gain observations, so the history the appeal rules on cannot be rewritten
underneath it. New nodes and new relations remain allowed; that is the appeal.

If the graph is empty there is nothing to appeal — say so and stop.

### 2. Find the appealable error

A verdict is only overturned on a defect in the record, not on disagreement
with the conclusion. Look for exactly these:

| Ground | What it looks like in the graph |
| :--- | :--- |
| **Undefended claim** | a claim went `OUT` and no counter was ever registered against its attacker |
| **Unattacked attacker** | a weakness is `IN` only because nobody tested it |
| **Missing evidence** | a claim is `needs_more_work` as unsupported, but support exists and was never registered |
| **Ungrounded assumption** | a claim was demoted for resting on an assumption that evidence could ground |
| **Circular reasoning** | `circular_reasoning` is non-empty and the verdict ignored it |

If none of these hold, the appeal fails. Report the verdict as confirmed and
stop. **Confirming is the expected outcome** — an appeal court that reverses
everything is not a court.

### 3. Enter new material

Register what the first pass missed, attributed to the role whose case it
serves. Add only material you can actually defend:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<counter-id>" counter --obs "<why the attack fails>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<counter-id>" undermines "<weakness-id>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<evidence-id>" evidence --obs "<source>" --agent advocate
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<evidence-id>" supports "<assumption-id>" --agent advocate
```

An appeal can also go against the original appellant — if the first pass let a
claim through unchallenged, attack it now:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" add "<weakness-id>" weakness --obs "<what breaks>" --agent adversary
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" relate "<weakness-id>" undermines "<claim-id>" --agent adversary
```

### 4. Re-run, diff, and unseal

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" verdict
bun "${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts" unlock --agent judge
```

Compare against the verdict from step 1 and report **what moved and why**, in
terms of the graph:

> `cost-reduction` moved from `does_not_survive` to `survives_scrutiny`:
> `multi-cloud-abstraction` was entered against `vendor-lockin`, which is now
> `OUT`, so its attack no longer counts.

## Output format

1. **Standing verdict** — what the first pass concluded
2. **Ground for appeal** — which defect above, or none
3. **New material** — what was entered, and by which role
4. **Revised verdict** — the re-run result
5. **What moved** — each change, traced to the node that caused it
6. **What stands** — everything the appeal confirmed

If nothing moved, say so plainly. "The appeal is dismissed; the verdict stands"
is a complete and legitimate result.

## Rules

- Appeal from the record. If it is not in the graph, it is not before the court.
- The record is sealed by `lock` — the engine refuses `reset` and refuses edits
  to prior testimony while the appeal runs. Do not work around it with
  `DA_FORCE_RESET`; that discards the case. `unlock` when the ruling is delivered.
- Do not reverse on preference. Name the structural defect or confirm.
- Attribute new material to the role it serves, so the transcript stays honest
  about who argued what.

## Resources

- `${CLAUDE_PLUGIN_ROOT}/references/roman-rota.md` — load always. Mandatory
  opposition, and why appeals go to a different panel.
- `${CLAUDE_PLUGIN_ROOT}/references/argument-semantics.md` — load always. How
  labels are computed, so "what moved" can be explained mechanically.
- `${CLAUDE_PLUGIN_ROOT}/references/lawsuits-against-the-devil.md` — load when
  the verdict was dismissive rather than reasoned.
- `${CLAUDE_PLUGIN_ROOT}/scripts/argument-graph.ts` — `verdict` and
  `transcript` to read the record, `add` and `relate` to enter new material.
