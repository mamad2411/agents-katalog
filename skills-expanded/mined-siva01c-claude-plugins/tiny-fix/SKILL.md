---
name: tiny-fix
description: >
  Low-ceremony workflow for trivial, low-risk changes: typos, comments,
  CSS/styling tweaks, string changes, single-line fixes with no logic
  impact. Use to avoid the overhead of the full feature workflow when the
  change cannot break anything. If during the fix the change turns out to
  touch logic, security, config, or schema, stop and escalate to the
  feature-workflow skill.
---

# Tiny Fix

Not every change needs the full phased workflow. Applying heavyweight
process to a typo wastes time and tokens. This skill is the deliberately
minimal path — with a tripwire for when a "tiny" fix turns out not to be.

## Qualifies as tiny

- Typos in strings, comments, or documentation
- CSS/SCSS styling tweaks with no template logic changes
- Renaming a label, adjusting copy text
- A single-line change with no branching-logic impact

## Does NOT qualify (escalate to feature-workflow)

- Anything touching routing, permissions, forms, or user input handling
- Config entity changes (they need export + review)
- Schema or entity changes (they need update hooks)
- Changes to conditionals, loops, or return values
- "While I'm here" refactors — those are features, not fixes

## Procedure

1. Confirm the change qualifies as tiny (list above). If not — or if you
   only discover mid-edit that it doesn't — stop and switch to the
   `feature-workflow` skill.
2. Make the change. Nothing else: no drive-by refactoring, no formatting
   sweeps across the file.
3. Sanity check: `drush cr` if templates/CSS aggregation are involved;
   reload the affected page.
4. Commit with a one-line message. Done.

## Hard rule

The escalation tripwire is the whole point of this skill. A tiny fix that
grew is not a tiny fix — never finish a change under this skill that no
longer meets the qualification list.
