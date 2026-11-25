---
name: team-access-review
description: "Read-only review of which SoftGlaze Browser team members used which profiles and groups, with suggestions to tighten access. Use when the user asks who can open which profiles, or for a team or access review."
---

# Review team access

Follow the softglaze-browser skill: read `softglaze://memory/workspace` and
`softglaze://guide/how-softglaze-works` first and follow them. Anything that changes something asks
the user for approval in the SoftGlaze app, so tell them what you are about to change and why first.
Stop every profile you start when you are done.

This is read-only: do not change anything.

1. Call workspace_summary for the team size and plan.
2. Call list_profiles (page through all) and note each profile's group and whether it is shared.
3. Call get_activity for the last 200 actions and note who launched or edited which groups recently.
4. Report: groups, how many profiles each has, and which members used them recently.
5. Suggest tightening where it helps, for example operators who used client groups they should not,
   unused shares, or profiles without a group. Member and role changes are made by the Owner in the
   app; you cannot make them.
