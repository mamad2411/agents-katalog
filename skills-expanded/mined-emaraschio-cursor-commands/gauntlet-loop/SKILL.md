---
name: gauntlet-loop
description: >-
  Beat a real-world quality bar with a Gauntlet Loop: take a GOAL and a
  REAL-WORLD EQUIVALENT with an inspectable reference pack, decompose into
  independent parts, assign specialist builders, and gate each part behind a
  separate fresh-context critic. Pass only if better than the reference;
  otherwise return the largest specific gap. After all parts pass, run an
  integration critic on the whole. Optional budget ceiling, taste-domain
  pride gate, and gap ledger for resume. Builders never evaluate their own
  work. Use when the user invokes /gauntlet-loop or asks to run a gauntlet,
  builder/critic loop, or beat a real example.
disable-model-invocation: true
user-invocable: false
---
# Gauntlet loop

## Role

You run a **Gauntlet Loop**: raise quality by competing against a real example, not against a vague "make it better". You decompose the GOAL, assign specialist builders, and let **critics alone** decide when each part passes. A part passes only when the critic judges the generated artifact **better than the REAL-WORLD EQUIVALENT** (the reference). Equal or worse is fail. Otherwise the critic returns the **largest specific gap** and the builder iterates. After all parts pass, an **integration critic** grades the whole artifact against the whole reference pack. Do **not** let builders evaluate their own work.

## When to use

Use when the user invokes `/gauntlet-loop`, asks to beat a real-world equivalent, run a builder/critic gauntlet, or set a concrete quality bar via an excellent existing example. For a six-part Goal before autonomous work without a reference bar, use `define-agent-goal`. For post-build judgment autopsy, use `decision-audit`. For thinning instructions from a bare run, use `instruction-ablation`.

## Gauntlet charter

> Goal plus an inspectable reference pack. Decompose. Specialist builders. Fresh-context critics inspect and compare. Blind when possible. Pass only if better (equal fails). Else largest specific gap. Cap, stall, and budget. Integration critic on the whole. Pride gate on taste. Gap ledger for resume. Builders never grade themselves.

## Workflow

Run phases in order.

### Phase 0: Intake

1. Require two fields:
   - **GOAL**: the finished result to produce
   - **REAL-WORLD EQUIVALENT**: name, URL, attachment, or description of an excellent existing example that sets the quality bar (also called the **reference**)
2. Require an inspectable **reference pack**: files, screenshots, short clip, playable build, or repo path that a critic can open. A name alone is not a pack. The reference is the quality bar; the **reference pack** is what critics open. Assemble the pack at intake; critics receive only the pack (plus the unlabeled generated twin when blind).
3. If GOAL, REAL-WORLD EQUIVALENT, or a usable reference pack is missing, ask one focused question per gap. Do not invent the reference or a vague substitute bar.
4. Optionally accept:
   - iteration cap (default **5** rounds per part)
   - **BUDGET**: total rounds across all parts and/or wall-clock limit (default: none beyond the per-part cap)
   - constraints, scope limits
5. If the reference is named but **inaccessible** (dead link, missing attachment, no inspectable artifact) or a pack cannot be assembled, stop and ask how to obtain it. Do not invent a substitute bar or proceed on memory of a famous product alone.
6. If the work is production-destructive and constraints lack explicit consent for that blast radius, stop and ask before building.
7. On **resume** of a prior gauntlet, read the existing **gap ledger** first. Do not retry a gap already marked stalled without a changed approach.

### Phase 1: Decompose

1. Break the GOAL into **independent parts** (or the fewest weakly coupled parts you can).
2. For each part, state a **part quality bar**: what "better than the reference" means for that slice (feel, fidelity, completeness, polish).
3. Prefer parts that can build and critique in parallel. Note true dependencies and order those sequentially.
4. **Publish the part list**, then proceed unless the user objects or corrects the split. Do not wait forever for an explicit "go" if the split is already clear.

### Phase 2: Per-part loop

For each part, run this state machine (parallelize independent parts when the harness allows). Do **not** skip the critic when the user says "just ship" or "looks fine"; still run critique.

**States:** `build` → `critique` → `pass` | `iterate` | `terminal`

1. **build:** Assign a **specialist builder** (subagent when available; otherwise a focused builder prompt scoped to that part only). The builder produces the artifact and does **not** declare pass/fail against the reference.
2. **critique:** Assign a **separate critic** with **fresh context**. Prefer a subagent. If subagents are unavailable, run a **fresh-context simulation**: critic prompt receives only the artifact, the **reference pack** (or both unlabeled), and the part quality bar. No build transcript, no builder rationalizations. Record **critic mode**: `subagent` or `fresh-context simulation`.
3. The critic must **inspect the generated artifact itself** (read files, run/play when feasible, view the UI). Do not pass from a **builder summary alone**.
4. Compare **directly** against the reference pack (whole or the part-relevant slice). Never grade from memory of a famous product alone.
5. **Blind side-by-side when possible**: present both without saying which is generated. If blind comparison is not feasible (e.g. the reference is a live product the critic already knows), state that the comparison was **not blind**. Never claim blind when the critic was told which side is generated.
6. **Verdict:**
   - **pass** only if the generated artifact is **better than the reference** on the part quality bar.
   - **iterate** if equal or worse: identify the **largest specific gap** (one concrete, observable deficit versus the reference) and return to **build** with that gap only. Append the gap to the **gap ledger**.
7. **terminal** (stop iterating this part) when:
   - verdict is **pass**, or
   - **iteration cap** reached (default 5 rounds, or intake override), or
   - **stall**: the **same gap repeats twice** with no measurable improvement, or
   - **BUDGET** exhausted (total rounds or wall-clock): report `fail (budget)`.
8. Do not invent a pass to escape the cap or budget. Do not soft-pass on "close enough". On terminal fail, report `fail (capped)`, `fail (stalled)`, or `fail (budget)` and continue other parts only if budget remains.

### Phase 3: Integration critic

After every part has reached a terminal state:

1. If any part failed (capped, stalled, or budget), skip integration and go to Deliver with outstanding parts listed.
2. If all parts **pass**, assemble the whole artifact and run one final **integration critic** (fresh context, whole artifact vs whole reference pack, blind when possible, same critic-mode rules).
3. Integration **pass** only if the whole is better than the reference. Equal or worse: return the largest cross-part gap to the affected part(s) and re-enter the per-part loop for those parts. Integration rounds count toward the iteration cap and BUDGET and obey stall rules.
4. The gauntlet is not "done" until the integration critic passes or terminals. Do not declare done from part-local passes alone.

### Phase 4: Deliver

Post the report using the template below. Include the gap ledger. End with a halt line for stalled, capped, or budgeted parts. For **taste domains** (UI, game feel, writing), after the machine passes (including integration), ask the **pride gate** before ship. For objective domains, state "not a taste domain" instead of asking.

## Deliverable template

```markdown
# Gauntlet loop

## 1. Intake
- GOAL: ...
- REAL-WORLD EQUIVALENT: ...
- Reference pack: ... (files / screenshots / clip / build / repo path)
- Iteration cap: N (default 5)
- BUDGET: none | total rounds / wall-clock

## 2. Parts

| Part | Quality bar (vs reference) | Dependencies |
|------|----------------------------|--------------|
| ... | ... | none / part-X |

## 3. Results

| Part | Rounds | Critic mode | Blind? | Verdict | Largest remaining gap |
|------|--------|-------------|--------|---------|------------------------|
| ... | k/N | subagent / fresh-context simulation | yes / no (why) | pass / fail (capped) / fail (stalled) / fail (budget) | ... or none |

## 4. Integration critic
- Critic mode / blind / verdict / largest cross-part gap (or skipped: outstanding part failures)

## 5. Gap ledger

| Part | Round | Gap returned | Verdict |
|------|-------|--------------|---------|
| ... | ... | ... | pass / iterate / fail (capped) / fail (stalled) / fail (budget) |

## 6. Outstanding
Parts that did not pass: gaps, recommended next move, or "all passed".

## 7. Halt
Approve outstanding parts, raise the cap or BUDGET, or revise the reference bar before I continue looping.
Pride gate (taste domains): proud of this versus the reference? (yes/no), or "not a taste domain".
```

## Safety

- Redact secrets, tokens, credentials, PII, and PHI in intake, artifacts, and reports.
- Do not run production-destructive actions unless constraints explicitly consent.
- Do not claim a critic pass without inspecting the artifact and comparing to the reference pack.
- Do not fabricate blind comparison when it was not blind.
- Do not skip the critic because the user said the work looks fine.
- Do not soft-pass to land under BUDGET.

## Distinction from other commands

- **`define-agent-goal`**: forward six-part Goal before autonomous work. This skill adds a **real-world quality bar** and builder/critic adjudication.
- **`decision-audit`**: post-build choice autopsy. This skill runs **during** construction against a reference; the pride gate here is taste vs the reference, not a full decision ledger.
- **`instruction-ablation`**: thins instructions from a bare run. This skill raises artifact quality against an example.
- **`prompt-eval-debug`**: tiny eval suite for a pasted prompt. This skill gauntlets **artifacts**, not prompt wording alone.
- **`thermo-nuclear-code-quality-review`**: maintainability review of existing code. This skill is a **build-and-beat** loop, not a review-only pass.

## Guardrails

- **GOAL and REAL-WORLD EQUIVALENT required.** Ask one focused question per missing field; never invent the reference.
- **Do not let builders evaluate their own work.** Hand the artifact to a separate critic with fresh context.
- **Critic uses fresh context.** Critic receives only the artifact, the reference pack (or both unlabeled), and the part bar.
- **Pass only if better than the reference.** Equal or worse is fail; return the largest specific gap; never soft-pass on close enough.
- **Largest specific gap, not vague feedback.** Name one concrete, observable deficit versus the reference.
- **Blind side-by-side when possible.** Unlabeled comparison when feasible; otherwise state the comparison was not blind; never claim blind when labeled.
- **Cap and stall, never infinite loop.** Stop at the iteration cap or when the same gap repeats twice with no improvement.
- **Do not skip the critic.** Still run fresh-context critique when the user says just ship or looks fine.
- **Inaccessible reference blocks intake.** Stop and ask how to obtain it; do not invent a substitute bar.
- **Reference pack required.** A name alone is not a pack; assemble inspectable files/screenshots/clip/build/repo path or block; never grade from memory.
- **Integration critic before done.** After all parts pass, run an integration critic on the whole; part-local passes alone are not done.
- **Budget ceiling stops the loop.** When BUDGET is exhausted, terminal as fail (budget); do not soft-pass to finish under budget.
- **Pride gate on taste domains.** After the machine passes, ask proud of this versus the reference before ship; objective domains state not a taste domain.
- **Gap ledger for resume.** Record round/gap/verdict per part; on resume read the ledger and do not retry a stalled gap without a changed approach.
