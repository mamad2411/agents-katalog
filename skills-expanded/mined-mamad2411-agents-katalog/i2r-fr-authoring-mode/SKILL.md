---
name: i2r-fr-authoring-mode
description: Produces atomic, EARS-patterned functional requirements from an INVEST story; one requirement = one behaviour; outputs 04-functional.json.
when_to_use: Loaded by i2r-functional-author when authoring or repairing stage 04-functional.json.
user-invocable: false
---

# i2r-fr-authoring-mode

**Purpose:** Turn a scoped feature (from 03-scope.json) into atomic, EARS-patterned functional requirements. One `requirements[]` item = one observable system behaviour. Produces `04-functional.json` that passes `i2r.py validate --stage 4`.

---

## Core discipline (read first)

1. **WHAT/WHY only — never HOW.** Apply the stack-swap test before finalising every requirement: if swapping the database or framework would force an edit to the `system_response`, delete the HOW and rewrite. Violation = `IMPLEMENTATION_LEAK` (BLOCKER).
2. **One behaviour per requirement.** The word "and" or "or" in `system_response` is a signal to split. Violation = hidden conjunction; flag and split.
2b. **Climb the RML ladder before authoring each FR** (root skill `requirements-minimalism.md`). Does this behaviour need its own requirement, or is it gold-plating / a duplicate of another FR / a re-statement of a platform-or-standard given that belongs in CONSTRAINTS? Author the minimum set that captures the scoped capability — minimal in count, never minimal in rigour. The safety floor (validation / data-loss / security / accessibility / explicit asks) is never minimized away.
3. **Every capability needs an unwanted-behaviour sibling.** For each happy-path requirement, write at least one `unwanted`-pattern sibling covering the error or edge condition (empty result, invalid input, timeout).
4. **Source every requirement.** `source` ∈ `{stated, assumed, decision}`; `source_ref` → exact pointer into `raw/` (file + line). Never fabricate; never silently promote an assumption to `stated`.

---

## Step-by-step authoring procedure

```
1. Read 03-scope.json → in_scope[] items become capability clusters.
2. For each capability cluster:
   a. Identify the actor, trigger, and observable response. RML check: if this capability already has an FR with the same observable response, reference it instead of writing a near-duplicate.
   b. Choose the EARS pattern (see references/ears-rules.md).
   c. Draft: trigger / system_name / system_response / rendered sentence.
   d. Assign id: <CAT>-NN (CAT = UPPER category slug matching the capability).
   e. Tag source + source_ref.
   f. List acceptance_ids (forward refs; AC-<FR_ID>-NN to be filled by i2r-acceptance-author).
   g. Write an unwanted sibling for every event_driven / state_driven / optional requirement.
3. Validate via: Bash(python scripts/i2r.py validate --stage 4).
4. Fix all schema violations before writing the final file.
```

---

## Required output structure

The output `04-functional.json` must carry `_meta` (§4 of CONTRACT.md) plus `requirements[]`. Every item must satisfy all required fields in `schemas/04-functional.schema.json`.

---

## Key references (depth lives here)

| File | What it teaches |
|---|---|
| `references/ears-rules.md` | The 6 EARS patterns; canonical sentence template; how to fill each field |
| `references/invest-rules.md` | INVEST criteria for the upstream story; how to confirm the story is sound before decomposing |
| `references/atomic-requirement-rules.md` | One-behaviour rule; conjunction flags; unwanted-sibling rule; source-tagging discipline |
| `references/TEMPLATE.json` | Blank FR item with all required keys — copy-paste start point |
| `references/GOOD_EXAMPLE.json` | Strong FR anchored on ORDER-01 (atomic, EARS, sourced, no implementation leak) |
| `references/BAD_EXAMPLE.md` | 2–3 bad FRs with diagnosis and corrected versions |

---

## Hard limits

- `placeholder_scan` rejects: `TBD`, `TODO`, `FIXME`, `nice to have`, `fast`, `secure`, `scalable`, `robust`, `etc.` — in any requirement field other than `rationale`. A hit → `PLACEHOLDER` (BLOCKER).
- Never emit phases, tasks, architecture, UI mockups, or code.
- Never reference a specific framework, database, table, endpoint, algorithm, or file path inside a requirement value.

Sources: EARS (Alistair Mavin); PM Skills INVEST story framework; product-on-purpose template + example anchoring; ponytail laziness ladder (→ RML).
