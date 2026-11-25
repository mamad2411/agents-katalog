---
name: estimate-work
description: Produces grounded effort estimates for a task/feature — decomposing into subtasks, assigning size (story points or t-shirt S/M/L), surfacing assumptions, unknowns, and risk buffers, and giving an optimistic/likely/pessimistic range instead of a single false number.
when_to_use: User asks 'how long / how big / how many points', wants a sprint or scoping estimate, or wants a feature broken into sized chunks before planning. Pairs with write-plan and write-prd.
---

## When to Use

- "How long will X take?" / "How big is this?" / "How many points?"
- Scoping a feature before a sprint, or splitting it into sized chunks for planning.
- Comparing two approaches by cost before committing.

Do NOT use when the ask is "just build it" with no scoping need — go straight to write-plan. Do NOT invent a deadline; estimate effort, not calendar dates (velocity and availability are the caller's to apply).

## Steps

1. **Read the actual code first — estimate from the repo, not from the prompt.** Locate the files the change touches (grep for the feature/module, read the entry points, the data model, the call sites). An estimate written before looking at the code is a guess. If the codebase is unfamiliar, spend the first pass mapping where the change lands.

2. **Decompose into discrete subtasks** that each map to a verifiable outcome — not phases. Bad: "backend / frontend / testing". Good: "add `status` column + migration", "expose it in the list endpoint", "render the badge", "wire the filter". Each subtask should be independently sizable and ideally ≤ 1 size class on its own. If a subtask is L or bigger, split it — large items hide the most error.

3. **Size each subtask with the basis stated.** Pick ONE scale and stay in it:
   - **T-shirt:** S = touch 1–2 files, known pattern, no new interface. M = a few files + tests, one new interface. L = cross-cutting, new component, or unfamiliar area. XL = must be split (don't size it, split it).
   - **Story points (Fibonacci 1/2/3/5/8):** anchor to a reference task the caller already knows, not to hours.
   - State the basis in one clause: "M — new endpoint + RLS policy + tests, pattern exists in `orders`".

4. **List assumptions and unknowns separately** — each as a line that says how it moves the estimate. Assumption = something you're treating as true to size at all ("auth/permissions already exist", "no data migration of existing rows"). Unknown = something you genuinely can't size yet ("does the 3rd-party API page its results? if yes +1 size"). Unknowns are the real cost drivers; name them explicitly.

5. **Give a range, never a point value.** For each subtask and for the total, give **optimistic / likely / pessimistic**. Optimistic = everything as assumed. Likely = your honest center. Pessimistic = the named unknowns resolve the hard way. Add a **risk buffer** to the total proportional to the unknowns — roughly +15% mostly-known, +30–50% with live unknowns or unfamiliar code. Sum subtask ranges; don't hand-wave a single total.

6. **Flag the biggest risk drivers and what would shrink the range.** Name the 1–3 items that dominate the spread, and the concrete action that collapses each: a time-boxed **spike** ("4h spike: confirm the API pagination shape"), a **decision** the caller must make ("sync vs async — async is +L"), or a missing input ("need the final schema"). This is the highest-value output: a wide range with a clear "do this to narrow it" beats a fake-precise number.

7. **Output a tidy table + one-line summary.** Table columns: `Subtask | Size | Basis | Key unknown`. Then a total range line and a one-sentence summary (e.g. "Likely M-sized / 8 pts; the API pagination unknown is what could push it to L — resolve with a 4h spike"). Round at sane granularity; avoid false precision like "6.5 points" or "11.3 hours".

## Common Errors

- **Single number with no range.** "About 3 days" is a promise, not an estimate. Always optimistic/likely/pessimistic.
- **Estimating the happy path only.** The likely number must include review, tests, edge cases, and rework — not just "type the code". Most real cost is in the last 20%.
- **Phase-based decomposition** ("design / build / test") — these aren't sizable units and hide where the work actually is. Decompose by deliverable.
- **Hours masquerading as points.** Story points are relative complexity, not disguised time. Don't multiply points by a fixed hour rate inside the estimate.
- **Burying unknowns in prose.** If a risk isn't on its own line with a size impact, it will be forgotten and blow the estimate. List, don't narrate.
- **Padding silently.** A buffer that's hidden inside each number is undebuggable. State the buffer as an explicit line item with its reason.
- **Estimating without reading the code.** The #1 source of bad numbers. "Add a field" is S if the pattern exists and L if it triggers a migration + cache invalidation + API version bump — you only know which by looking.
- **Splitting forever.** Decomposition has a floor: stop at the smallest independently-shippable unit. Sub-S fragments add noise, not accuracy.

## Verify

Before returning, the estimate passes only if:
- [ ] Every subtask maps to a concrete deliverable, and none is sized XL (all XL split).
- [ ] Every subtask and the total have a 3-point range, not a single value.
- [ ] Assumptions and unknowns are listed separately, each with a stated size impact.
- [ ] The total range = sum of subtask ranges + a named, explained buffer.
- [ ] The 1–3 dominant risk drivers are flagged, each with a spike/decision/input that would shrink the range.
- [ ] No false precision (no decimals on points; hours rounded to a sane grain).
- [ ] The basis for each size traces to something real in the repo, not the prompt wording.
