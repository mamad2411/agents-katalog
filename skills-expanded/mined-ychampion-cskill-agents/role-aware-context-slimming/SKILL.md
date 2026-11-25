---
name: role-aware-context-slimming
description: "Trim user and system context based on the agent\u2019s role so read-only helpers don\u2019t inherit stale git or CLAUDE metadata."
metadata:
  author: ychampion
---

# SKILL: Role-Aware Context Slimming
**Domain:** context-management  
**Trigger:** When an agent declares `omitClaudeMd` or runs as an Explore/Plan helper, slim the context before handing it to `runAgent`.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Use the `omitClaudeMd` flag (and the `tengu_slim_subagent_claudemd` feature gate) to strip `claudeMd` from the user context unless an override was explicitly provided. For read-only helpers such as Explore or Plan, drop the `gitStatus` entry from the system context because it is stale and bloats the payload. Always compute new context objects instead of mutating the originals so other agents can still read the full metadata set.

## Key Rules
- Only remove `claudeMd` when `agentDefinition.omitClaudeMd` is true, no user override is present, and the feature flag allows it, so you do not throw away intentional user context edits.
- Derive `userContextNoClaudeMd` by destructuring the base context and omitting `claudeMd` before assigning `resolvedUserContext`.
- Drop `gitStatus` from `resolvedSystemContext` any time `agentDefinition.agentType` is `Explore` or `Plan`, while leaving other system keys intact.
- Preserve the original contexts for the parent agent so they can continue to see the full metadata when needed.

## Example Application
When the CLI launches an Explore subagent, apply this skill to create `resolvedUserContext` without `claudeMd` and `resolvedSystemContext` without `gitStatus`, saving dozens of tokens and preventing stale git information from confusing the helper.

## Anti-Patterns (What NOT to do)
- Stripping `claudeMd` even though the caller supplied an override user context; that override often carries explicit corrections or clarifications.
- Forgetting to remove `gitStatus` for Explore/Plan agents, which bloats the prompt with stale files and slows down the API call.
