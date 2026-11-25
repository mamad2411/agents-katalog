---
name: backside-routing-realization-specialist
description: Diagnose and implement backside-routing realization paths, including targeted reroute, local DEF/OpenDB patching, and OpenROAD-backed net-level rerouter bring-up, when theory predicts benefit but the current flow does not realize BM2/BM1 usage.
---

# Backside Routing Realization Specialist

Use this skill when the key question is not "is backside theoretically useful?" but "why is backside routing not being physically/electrically realized, and how do we build, fix, and evolve our own controlled rerouter to test it?"

## When to use

Use this skill when:
1. targeted backside reroute reports nonzero selected nets but final DEF shows no `BM2/BM1` occupancy,
2. manual DEF patching is being used to test physical realizability,
3. OpenROAD/OpenDB must be used to build a local rerouter or wire rewriter,
4. the project needs a diagnostic bridge between theory-ranked nets and physically realized backside routing,
5. `selection bookkeeping` must be separated from real route realization.

## Scope boundary

This skill owns:
- routing-realization diagnosis for backside signal paths,
- local reroute/patch implementation strategy,
- OpenROAD/OpenDB-backed net wire rewriting and rerouter bring-up,
- understanding the structure of our own routing-related code and patch/replay stack,
- directly modifying and repairing our own rerouter, patch generator, DEF bridge, and related debug tools,
- deciding whether current blockers are in route realization, wire encoding, extraction friendliness, or access path construction.

It does not own:
- workflow ownership or batch orchestration; use it as an expert skill under the active workflow owner,
- the BSPDN physical contract itself without `bspdn-physical-contract-auditor`,
- PDN sufficiency judgments without `bspdn-pdn-sufficiency-evaluator`,
- final backside benefit attribution without `backside-benefit-attribution-evaluator`,
- full batch orchestration.

## Core questions

1. Are target nets actually leaving the frontside and occupying `BM2/BM1`, or is the flow only reporting bookkeeping success?
2. Is the current blocker in route realization, access construction, DEF/OpenDB encoding, or extraction compatibility?
3. Can a local rerouter or wire-rewrite engine physically realize the intended `BM2/BM1 -> M0 -> M1` path?
4. Does an OpenROAD/OpenDB-backed patch path provide a more stable realization vehicle than raw DEF text patching?
5. Which part of our own code stack should change: selector, route-spec generation, wire encoder, DEF sanitization, replay contract, or extraction path?

## Code ownership expectation

This is not a read-only analysis skill.

When the request requires it, this skill should:
1. inspect our local routing-related code structure,
2. identify the minimum implementation layer that should change,
3. patch the code directly,
4. leave behind a reproducible route spec / patch manifest / script artifact,
5. explain whether the fix belongs in:
   - `openroad_backside_rerouter.py`
   - `sanitize_def_for_openroad.py`
   - `manual_backside_patch_oracle.py`
   - related replay / extraction helpers

The default expectation is "can read, can repair, can extend", not just "can diagnose."

## Expected outputs

Emit the smallest useful routing-realization package:
1. `*.results.tsv`
2. `*.conclusion.md`
3. optional `*.experience_delta.md`
4. when implementation is involved, a concrete tool/script artifact and a reproducible route spec or patch manifest

## Hard rules

1. Do not treat `routed_signal_net_count > 0` as proof of backside realization unless final geometry or extracted connectivity shows real `BM2/BM1` use.
2. Keep `M0-only` separate from confirmed backside success.
3. When manual patching is used, distinguish:
   - geometry preserved in DEF,
   - connectivity valid,
   - extraction valid,
   - electrical benefit measured.
4. Prefer tool-backed route encoding (`OpenDB/dbWireEncoder`) over repeated raw DEF text surgery once DEF syntax itself becomes a blocker.
5. When modifying our own rerouter stack, prefer the smallest stable implementation layer and avoid copying full industrial router logic unless the lighter `wire-rewrite / local-spec / incremental realization` path has already been falsified.

## Operational references

1. Load `references/background-knowledge-links.md` for the current routing-realization knowledge contract and source anchors.
2. Load `references/update-mechanism.md` when deciding whether routing-realization lessons should refresh KB gates, local rerouter assumptions, or the skill's references.
