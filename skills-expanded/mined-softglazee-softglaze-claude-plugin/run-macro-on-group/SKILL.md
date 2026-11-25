---
name: run-macro-on-group
description: "Runs a saved SoftGlaze Browser macro across the profiles in a group within the plan limits and reports passed and failed profiles. Use when the user asks to run a SoftGlaze macro on a group or many profiles."
argument-hint: "<macro> <group> [profiles at once]"
arguments: [macro, group, concurrency]
disable-model-invocation: true
---

# Run a macro on a group

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

Macro: $macro. Group: $group. Profiles at once: $concurrency (empty means the plan's default).
If the macro or group is empty, ask the user.

1. Find the macro with list_macros and read it with get_macro so you can describe what it does.
2. List the group's profiles with list_profiles and check them with profile_health; leave out any
   whose proxy is failing and tell the user which.
3. Call workspace_summary to see the plan's parallel limit; a higher number is reduced to it.
4. Tell the user: the macro, the number of profiles, how many at a time, and roughly how long it
   will take. Then call run_macro.
5. Follow it with get_run_status until it ends, then report passed and failed profiles and the first
   error of each failure.
6. If something goes wrong across many profiles, stop it with stop_run straight away and tell the
   user.
