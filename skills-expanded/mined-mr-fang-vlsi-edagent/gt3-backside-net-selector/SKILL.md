---
name: gt3-backside-net-selector
description: "Select backside-routing candidate nets after placement/postCTS using power-first criteria with timing-safety vetoes. Use when the task is to build or validate reusable net lists/patterns for targeted GT3 backside reroute, especially when dynamic-power reduction is the primary objective."
---

# GT3 Backside Net Selector

## Role Boundary

This skill owns net-selection only:
- consume placement/postCTS DEF and existing scorer evidence,
- run a power-first candidate screen,
- emit reusable net lists/patterns for targeted backside reroute,
- summarize why nets were selected.

This skill does **not** own:
- actual reroute execution,
- CTS/route submission,
- final PPA claims.

Those remain in `gt3-backside-route-policy` and `workflow-scoped-execution`.

## Use This Skill When

Use it for requests such as:
- "which nets should be moved to backside?"
- "select backside candidates after placement"
- "use dynamic power as the primary migration criterion"
- "prepare a targeted backside net list for Innovus reroute"

## Inputs

Provide or derive:
1. a DEF checkpoint (`placed.def` or `postcts.def`),
2. GT3 techlef if scorer PDK timing terms are wanted,
3. optional criticality/slack file,
4. optional activity file,
5. backside capacity contract.

## Knowledge And Tool Interaction

1. If the task needs shared KB/tool lookup before defining selection assumptions, delegate that step to `eda-context-accessor`.
2. Use existing scorer evidence and prior route summaries as the primary local evidence source for selector setup.
3. Record which selector assumptions, capacity contract, and evidence inputs produced the emitted net list.

## Output Contract

Return:
1. selected net list path,
2. escaped pattern list path,
3. summary path,
4. whether selection used real activity or uniform activity,
5. capacity used vs capacity budget.

## Operational References

1. Load `references/default-policy.md` when deciding objective priority, timing veto behavior, clock handling, or independence from route submission.
2. Load `references/tool-and-arguments.md` when preparing the selector command, optional inputs, or output artifact settings.
