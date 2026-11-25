---
name: weigh-bags
description: Record scale readings for each bag — empty (tare), outbound, current, final — and reconcile them against the itemised inventory to find unaccounted weight. Use when the user gives a bag weight, says how heavy something is, weighs their luggage, or asks how close to the limit they are. Appends to bags.yaml and runs scripts/reconcile.py.
allowed-tools: Read, Write, Edit, Bash(python3 *), Bash(ls *), Grep
---

# Weigh Bags

`$TPA` below is this plugin's `new-workspace` skill directory — the folder holding its `SKILL.md`,
`scripts/`, `schema/`, `typst/` and `template/`. Find it by name in your tool's skills folder (some
tools prefix it, e.g. `travel-packing-assistant__new-workspace`) and set `TPA` once per session.

Turns scale readings into the numbers the plan is checked against, and finds the gap between
what the inventory says a bag contains and what it actually weighs.

## The four phases

| phase | what it is | why it matters |
| --- | --- | --- |
| `empty` | the bag on the scale with nothing in it — its tare | every allowance is gross weight, so tare comes straight off the usable capacity |
| `outbound` | what it weighed leaving home | the baseline the return leg is measured against |
| `current` | where it stands now, mid-trip | the working number for a re-pack |
| `final` | the check-in reading | the ground truth; record it, it is what makes the next trip's estimates good |

Readings **append**. Never overwrite an earlier weighing — the history across a multi-leg trip
is the data, and a bag that gained 4 kg between `outbound` and `current` is telling you
something a single current reading cannot.

## Getting a reading the user can trust

- **Hook/luggage scale** — right tool. Lift smoothly and read at rest; a jerked lift reads
  high by a kilogram or more. Take two readings and use the second.
- **Bathroom scale, by difference** — weigh the person, then the person holding the bag,
  subtract. Works, but bathroom scales typically quantise to 0.1–0.5 kg and the error applies
  twice, so treat the result as ±1 kg and leave the headroom to match.
- **Kitchen scale** — for items, not bags.

Whatever the method, ask what the resolution is once and record it in `scales[]`. A reading of
"23" from a scale that rounds to the nearest kilogram is not the same fact as 23.0 kg from a
scale that reads to 100 g, and the difference is exactly the size of the margin people get
caught by.

## Reconciliation

After recording, run:

```bash
python3 $TPA/scripts/reconcile.py . --json
```

It computes, per bag, `gross − tare − cube tare − itemised contents = unaccounted`, and
classifies:

- **consistent** — the inventory explains the bag.
- **partial inventory** — a real but modest gap. Normal. Say what it is in kilograms and treat
  the *measured* weight as authoritative for planning, not the itemised sum.
- **inventory incomplete** — the gap is large enough that the plan cannot be trusted. The fix
  is to add the missing items, not to add a fudge factor.

When the residual has the same sign and similar size on **every** bag, that is the signature of
a miscalibrated scale rather than missing items; `reconcile.py` will suggest a `bias_kg`. Show
the suggestion, explain what it means, and let the user decide whether to write it into
`bags.yaml`. Never apply a calibration correction silently — a systematic offset applied to a
correct scale produces a plan that is wrong on every bag at once.

## Which number the plan uses

Where a bag has both a measured gross weight and an itemised total, the **measured weight
wins**, and the difference is carried as unaccounted mass. That is the conservative choice: it
is the number the airport scale will agree with.

## Procedure

1. Read `bags.yaml`. If a bag has no `empty` weighing, ask for its tare before anything else —
   without it every downstream figure is off by the weight of the suitcase.
2. Record the readings the user gives, with the phase, the date and the scale id.
3. Run `reconcile.py`.
4. Report per bag: gross, allowance, headroom, status, and the unaccounted mass. Lead with the
   arithmetic — gross minus allowance — before any interpretation.
5. If any bag is over, or inside 1.5 kg of its limit, name it and offer `/travel-packing-assistant:plan`
   to redistribute or `/travel-packing-assistant:overage` to price the alternatives.
