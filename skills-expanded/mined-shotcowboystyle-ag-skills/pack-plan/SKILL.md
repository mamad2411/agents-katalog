---
name: pack-plan
description: Solve the allocation of items to bags and packing cubes against the binding baggage limits, then turn the solution into instructions a person can follow while packing. Use when the user asks how to pack, how to distribute weight between bags, whether everything will fit, or how to get under the limit. Runs scripts/pack_solver.py and writes plan.yaml.
allowed-tools: Read, Write, Edit, Bash(python3 *), Bash(ls *), Grep, Glob
---

# Pack Plan

`$TPA` below is this plugin's `new-workspace` skill directory — the folder holding its `SKILL.md`,
`scripts/`, `schema/`, `typst/` and `template/`. Find it by name in your tool's skills folder (some
tools prefix it, e.g. `travel-packing-assistant__new-workspace`) and set `TPA` once per session.

Two halves, and they are different problems. The solver answers **what goes in which bag** —
an arithmetic question with a defensible optimum. This skill answers **how to pack it** — a
physical question the arithmetic knows nothing about.

## Preconditions

Refuse to produce a final plan, and say why, if:

- The checked allowance for any segment has `confidence: assumed`. Plan against a guessed limit
  and the plan inherits the guess without showing it.
- No bag has a tare weight. Every allowance is gross.
- `reconcile.py` reports `inventory incomplete` on a bag. A solver optimising over 60% of a
  bag's mass produces confident nonsense.

A *provisional* plan on incomplete data is fine and often useful — produce it, label it
provisional in the report and in `plan.yaml`'s warnings, and say exactly what would make it
final.

## Running the solver

```bash
python3 $TPA/scripts/pack_solver.py . --json
```

Options worth knowing:

- `--objective max-min-headroom` (default) — spread the load so no bag sits on its limit. The
  right default: airport scales and home scales disagree by a few hundred grams routinely, and
  headroom is what absorbs that.
- `--objective consolidate` — fill fewer bags, for a traveller who would rather leave a bag at
  home or avoid a second checked-bag fee.
- `--overflow` — when it does not all fit, also emit the ranked drop list that
  `/travel-packing-assistant:leave-behind` reads.

The solver is deterministic: same inputs, same plan, every run. If a re-run produces a
different allocation, an input changed — find out which before showing the new plan, because a
packing list that quietly reshuffles between readings is worse than no packing list.

## Reading the output

`plan.yaml` gives per bag: allowance, tare, contents, projected gross, headroom, status.

Status bands are deliberately conservative — `tight` means under 1.5 kg of headroom, not
"over". Report a `tight` bag as a real finding, not a pass. The gap between a home reading and
an airport reading is routinely half a kilogram, and it is always in the wrong direction.

If items land in `unassigned`, the pack is infeasible as specified. Say so plainly, give the
shortfall in kilograms, and offer the three levers: another bag (price it with
`/travel-packing-assistant:overage`), less stuff (`/travel-packing-assistant:leave-behind`), or moving weight onto
the body — worn coats, boots and a loaded jacket are not weighed, and on a genuinely marginal
bag this is worth 2–4 kg for free.

## The physical half

The solver's answer is a set of lists. Turn it into instructions, in this order:

**Cubes carry the structure.** Where the user has packing cubes, use them as the unit of
instruction: one category per cube where the count allows, cube labelled, contents listed.
The gain is not compression — most cubes compress little — it is that a bag can be opened,
inspected and re-packed at a counter or a customs table without becoming a pile. That matters
precisely on the trips where the weight is tight.

**Weight low and towards the wheels.** In an upright case, dense items go against the wheel
end, so the case stands and rolls rather than tipping. In a backpack, dense items ride high and
close to the spine.

**Distribute by shape, then check by weight.** Fill the corners with soft items before adding
the next hard one; a case that is 2 kg under its limit but cannot close has not been solved.

**Cabin bag rules that override the optimum.** Regardless of what the arithmetic prefers, the
cabin bag carries: passports and documents, medication with its prescription, keys, all
lithium power banks and spare batteries, valuables and irreplaceables, one change of clothes,
and anything the trip fails without. The cabin bag is the traveller's insurance against a
checked bag that does not arrive, and that is worth more than a kilogram of balance.

**Liquids split at the security line, not at the bag.** Anything over 100 ml goes checked
regardless of weight; the cabin liquids bag is a separate constraint the solver does not model.

## Procedure

1. Read `allowances.yaml`, `bags.yaml`, `inventory.yaml`. Check the preconditions.
2. Run the solver. If `unassigned` is non-empty, re-run with `--overflow`.
3. Read `plan.yaml`.
4. Report, arithmetic first: a bag-by-bag table of allowance / projected gross / headroom /
   status, then total across bags, then the warnings.
5. Give the physical instructions per bag, cube by cube.
6. Name the next step: `/travel-packing-assistant:docs` to render the counter card and packing list, or
   `/travel-packing-assistant:overage` if any bag is over.
