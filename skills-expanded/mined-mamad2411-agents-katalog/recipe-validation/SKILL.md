---
name: recipe-validation
description: Checklist for validating an OpenCookbook recipe. Use when reviewing a recipe before promotion, after edits, or for quality checking. Fix everything you can. Only flag issues that need the author's judgment.
license: CC0-1.0
metadata:
  author: JPEGtheDev
  version: "1.2"
---

# Recipe Validation

## When to Use This Skill

Use this when:
- A recipe was just created or edited
- Reviewing a recipe before promoting from `beta` to `stable`
- Doing a quality check across multiple recipes
- Something looks wrong and needs investigation

**Full rule details:** See [RULES.md](../../references/RULES.md) for the complete rule set with IDs and severity levels.

---

## The Fix-First Rule

**If you find a problem you can fix, fix it. Do not just list it.**

Only flag an issue for the author when:
- You don't know the correct value (e.g. "should this be 907g or 1000g?")
- The fix requires a judgment call or taste preference
- The information is simply missing and you can't look it up

After validation, the recipe should be **better** than when you started.

---

## Validation Checklist

Go through **every** category below, **one item at a time**. Do not skip categories.
Do not say "looks good" without checking each item. Fix what you can. Flag what you cannot.

### 1. File and Structure

- [ ] File extension is `.yaml`
- [ ] File is valid YAML (no syntax errors)
- [ ] `name` is present and descriptive
- [ ] `version` is present and **quoted** (`"1.0"` not `1.0`)
- [ ] `author` is present
- [ ] `description` is present and not empty
- [ ] `status` is one of: `stable`, `beta`, `draft`
- [ ] File is in the correct folder for its status
- [ ] Filename is `Title_Case_With_Underscores.yaml`

### 2. Ingredients

- [ ] At least one ingredient group with at least one item
- [ ] Every ingredient has `quantity` and `unit`
- [ ] Units are ONLY `g`, `ml`, or count words (`cloves`, `sprigs`, `whole`)
- [ ] **No imperial units** (`lbs.`, `cups`, `oz.`) — if found, convert to grams
- [ ] Every spice with `quantity < 10` and `unit: g` has a `volume_alt` field
- [ ] `heading: null` for the default group, descriptive string for sub-groups

### 3. Instructions

- [ ] At least one instruction section (unless `status: draft`)
- [ ] Steps are in a logical, executable order
- [ ] Every section has `type: sequence` or `type: branch`
- [ ] Branch sections with the same cooking choice share a `branch_group`
- [ ] Each branch is complete on its own (no branch depends on steps from another)
- [ ] All temperatures are dual-format: `°C (°F)`
- [ ] No step references an ingredient not in the `ingredients` list
- [ ] Every step is explicit enough for a novice — no implicit actions assumed (R3.7)

### 4. Food Safety

**These are ALWAYS errors if missing. Never skip this section for meat recipes.**

- [ ] Poultry → internal temp of **74°C (165°F)** stated in instructions
- [ ] Ground meats → internal temp of **71°C (160°F)** stated
- [ ] Whole cuts (beef/pork/lamb) → internal temp of **63°C (145°F)** stated
- [ ] Past-expiration ingredient advice includes a safety caveat
- [ ] Freezing instructions include maximum storage duration
- [ ] Flash-freeze steps describe the process (spacing, timing, transfer)

### 5. Cross-References

- [ ] All `path` values in `related[]` point to files that exist
- [ ] Paths use relative format (`./` or `../`)
- [ ] Paths end in `.yaml`, not `.md`
- [ ] Every ingredient whose `name` refers to another recipe in this repo has a `doc_link` field with the relative path to that recipe's `.yaml` file
- [ ] If a recipe was moved or renamed, all references to the old path across the repo have been updated

### 6. Text Quality

- [ ] No merged/concatenated words from copy-paste (e.g. "Fahrenheittested") — scan all pasted text
- [ ] No placeholder text (`TBD`, `TODO`) in stable or beta recipes
- [ ] Ingredient names are spelled correctly
- [ ] Step text is clear and unambiguous

### 7. Consistency

- [ ] Units are consistent throughout (no mixing g and oz for same ingredient type)
- [ ] Same ingredient uses the same name everywhere in the file
- [ ] `notes` field only present when status is `beta` or `draft`
- [ ] **No imperial units in text fields** (description, step text, ingredient notes, top-level notes) — check for `lb`, `oz`, `cup`, `tbsp`, `tsp`, `°F` alone — any found must be converted or removed
- [ ] All `nutrition_id` values reference actual entries in `docs/data/nutrition-db.json` — if a recipe introduces new ingredients, the DB entries must be added in the same PR
    - [ ] If `docs/data/nutrition-db.json` was changed in this PR, run `dotnet build` and confirm the wwwroot copy is generated at `visualizer/src/OpenCookbook.Web/wwwroot/data/nutrition-db.json` (and is not tracked in git)
---

## How to Report Issues

For things you **fixed**:
```
[FIXED] Missing volume_alt on 3g Black Pepper — added "3/4 tsp."
[FIXED] Temperature "425°F" → "218°C (425°F)"
```

For things **only the author can decide**:
```
[ASK] Ground beef listed as 907g — is this the intended amount? (Converted from 2 lbs)
[ASK] Chicken Wings spice quantities may need halving — needs testing to confirm.
```

---

## Promoting Beta → Stable

A recipe can move from `Recipes/Beta/` to `Recipes/` when ALL of these are true:

1. Every checklist item above passes
2. No open `[ASK]` items remain
3. The `notes` field is removed or empty
4. All quantities have been tested by the author
5. `status` is changed from `beta` to `stable`

---

## Improving the Rules

**This section is not optional.** If your validation pass reveals a gap, fix the system — not just the recipe.

1. Add a rule to [RULES.md](../../references/RULES.md) if the error class isn't covered
2. If a spice was missing, add it to [SPICE_CONVERSIONS.md](../../references/SPICE_CONVERSIONS.md)
3. Add a checklist item above if it catches a new class of error
4. Log the discovery in [lessons.md](../../lessons.md) with a prevention rule

If the same type of mistake keeps appearing, the system is broken — fix the system.
