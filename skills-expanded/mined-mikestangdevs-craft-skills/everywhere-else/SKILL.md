---
name: everywhere-else
description: "Use right after fixing a bug or pattern in one place, before reporting done. Enumerates the sibling sites that share the pattern (templates, endpoints, components, fixtures, configs) by search, audits each for the same defect, fixes the affected ones, and reports which were checked and clean. Use when 'fixed' touched one file among many look-alikes."
---

# Everywhere Else

## The failure mode this fixes

A bug gets found in one scenario, one endpoint, one template — and fixed *there*. The report says "fixed," the test goes green, everyone moves on. But the codebase has nineteen siblings built by the same hand, from the same copy-paste, with the same defect — and the fix just made instance #7 correct while #1–6 and #8–20 still lie. The user discovers this one sibling at a time, each discovery costing a full debugging session that ends in "oh, it's the same bug again."

Agents are biased toward the point fix: the task said "fix the chart in scenario 12," so scenario 12 gets fixed and the task is "done." Nobody asked the question that turns a point fix into a real fix: **is this defect a member of a population?**

## When to Use This Skill

- You just fixed a defect in one instance of anything that has siblings — handlers, templates, scenarios, components, parsers, fixtures, migrations, configs
- The fix corrected a *pattern* (wrong field semantics, missing null check, stale API shape) rather than a one-off typo
- The codebase contains parallel surfaces that must stay consistent (every page that renders X, every job that emits Y)
- A report is about to say "fixed" and the diff touches one file in a directory of twenty look-alikes
- The user asks "did you do that anywhere else?" — if they have to ask, the skill fired too late

**Don't use when:** the defect is genuinely unique to its site (a typo in one string), or the "siblings" only superficially resemble each other and share no logic or origin. Don't let the sweep balloon into a refactor of every file it visits — the sweep checks for *this* defect, not all defects.

## Instructions

### 1. Classify the fix: typo or pattern?

After any fix, ask what kind of wrong it was. A one-off mistake stays a point fix. But if the defect came from a misunderstanding (wrong unit, wrong field meaning, wrong API contract), a copy-paste lineage, or a convention everyone followed — the same wrongness exists wherever that understanding was applied.

### 2. Enumerate the population — by search, not memory

Don't list the siblings you can think of; *find* them. Grep for the pattern (the function call, the field name, the structural shape), list the directory of parallel implementations, check every consumer of the API that changed. Write the population down as a checklist with a count. "All the templates" is a feeling; "23 files matching `templates/*.py`, 9 contain `year_in_service`" is a population.

### 3. Audit every member, don't pattern-match blindly

Visit each site and check whether the defect is present *there*. Some siblings will have diverged and be fine; some will be broken differently. A mechanical find-and-replace across the population is its own bug factory — the sweep is an audit that produces fixes, not a regex that produces edits.

### 4. Fix the source of the pattern, if there is one

If all N siblings share the defect, the best fix is often one level up: the shared helper, the base class, the schema validation, the code generator, the doc that taught everyone the wrong convention. Fix the origin so the population can't regrow the defect, then fix the existing instances.

### 5. Report coverage, including the clean ones

"Fixed in scenario 12" and "fixed in scenario 12; audited the other 19 — 6 had the same defect (fixed), 13 verified clean" are different claims. The second is the deliverable. Naming the clean ones matters: it's the difference between "I swept" and "I stopped looking."

## Output format

```
Population sweep: <defect> first found in <site>
Population: <how enumerated — search/glob/list> → <N members>
Affected: <list — each fixed>
Clean: <list — verified, not assumed>
Origin fix: <shared helper/schema/docs fixed so it can't recur | none exists>
Verification: <suite/spot-check run across the population>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| The point fix victory lap | "fixed" when one of twenty instances was fixed. |
| Memory-based enumeration | sweeping the siblings you remember instead of the ones that exist. |
| Regex surgery | blind find-and-replace across the population without auditing each site. |
| Sweep scope creep | "while I'm in here" refactoring every file the sweep visits. Check for *this* defect; file the rest. |
| Silent partial coverage | sweeping 8 of 20 siblings and reporting it as a sweep. Truncated coverage gets named or it's a lie of omission. |

## Mental Model

> A defect found in one instance of a pattern is a sample, not the population. You haven't fixed the bug until you know how many places it lives — and the only way to know is to count.
