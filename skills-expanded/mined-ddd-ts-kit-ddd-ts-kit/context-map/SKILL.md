---
name: context-map
description: >-
  Use when two contexts depend on each other, a context needs data or a reaction from
  another, when choosing upstream, downstream and pattern (customer-supplier, conformist,
  anti-corruption layer, open-host service, shared kernel, published language), or on
  context/* rules.
argument-hint: "[downstream upstream]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(npx ddd-ts-kit list *)
  - Bash(npx ddd-ts-kit docs)
  - Bash(npx ddd-ts-kit docs --check)
  - Bash(npx ddd-ts-kit check *)
---

# Context map

Relationship under discussion: `$ARGUMENTS`

A relationship is declared, never implied by an import. The pattern is the owner's decision:
it says who adapts to whom, which is a matter of teams as much as of code. The exchange itself
is built with skill `ddd-ts-kit:integration-event`.

## 1. List the collaborations

From the policies and read models of the discovery ("whenever X happened, then Y"; "needs to
see Z"), or from `npx ddd-ts-kit list`. For each: who knows a fact first (the
**upstream**), who needs it (the **downstream**), and what crosses.

| Need of the downstream | What crosses | Built later with |
|---|---|---|
| react to something that happened | an integration event | `generate integration-event`, `generate integration-handler` |
| data to decide, often | a local projection fed by events | the same, plus a read model |
| an answer now | a read contract behind a port of the caller | `generate gateway` |
| change the other's state in one transaction | nothing can: one context, or a process in steps | back to `ddd-ts-kit:bounded-contexts` |

## 2. Choose the pattern

| Pattern | Choose when | Cost |
|---|---|---|
| `published-language` | default: the upstream publishes contracts made for its consumers | the upstream keeps them stable and versioned |
| `customer-supplier` | the downstream's needs are planned into the upstream's work | coordination between the two owners |
| `conformist` | the downstream accepts the upstream model as it is | the downstream moves when the upstream does |
| `anti-corruption-layer` | the upstream model is foreign, legacy or generic: the downstream translates it | a translator to maintain in `infrastructure/anti-corruption/` |
| `open-host-service` | the upstream serves many consumers through one protocol | a public contract, hard to change |
| `shared-kernel` | two contexts co-own a small model | joint ownership of every change; justify it. Its values are generated there (`generate value-object shared-kernel <Name> --term ...`), its terms in its own `CONTEXT.md` |

No cycle. If A needs B and B needs A, ask in this order
(`docs/guides/cycle-between-contexts.md`): 1. one language, one model? then one context,
divided into modules of the model so that it stays readable (`generate module`,
`move-to-module`); 2. can one direction become an event? 3. is a concept missing, often a third
context? Refusing the cycle is a choice of the kit (every context stays extractable), not a
rule of DDD: Evans's Partnership is between teams; describe it in the written part of the map,
and still pick one direction in the config. A `generic` context is upstream of the others, behind an
anti-corruption layer when its model is not yours.

## 3. Write it

Before the bootstrap, `docs/architecture/context-map.md`:

```markdown
# Context map (draft)
| Downstream | Upstream | Pattern | What crosses | Why this pattern |
|---|---|---|---|---|
| billing | ordering | published-language | event `ordering.order.placed` | billing reacts, ordering knows nothing of invoices |
```

The bootstrap turns each row into `--upstream <upstream>:<pattern>` and moves the last column
to `docs/context-map.md`, then deletes the draft.

After the bootstrap, the relationships live in `contexts.<downstream>.upstreams` of
`ddd-ts-kit.config.json` (the owner confirms the edit; a new context takes
`--upstream <ctx>:<pattern>` at creation, and an existing one gains a new upstream by the same
command, `generate context <name> --classification <its classification> --upstream
<ctx>:<pattern>`; the pattern of a declared pair changes in the config only). Then
`npx ddd-ts-kit docs` redraws the diagram and the table between the markers of
`docs/context-map.md`. Write outside the markers, and only
what the diagram cannot say: the reading guide (three lines on the main flow), why each
debated boundary, why each pattern other than `published-language` and what it costs, known
tensions with the signal that would trigger a split or a merge.

Finish with
`npx ddd-ts-kit check --rule context/no-cycle --rule context/declared-relationship --rule config/valid`.

## Done when

Put this to the owner: **does every arrow have a pattern, a named contract and a reason,
and is there no cycle?** On a yes, the next step is `ddd-ts-kit:bootstrap`, which the user
starts.
