---
name: safe-autonomous-mode
description: Patterns for safe autonomous operation with allow/deny rule composition, risk classification, pacing, and focus-aware behavior. Use when operating autonomously, configuring auto-mode permissions, or when the user wants hands-off task execution with safety guardrails.
user-invocable: true
---

# Safe Autonomous Mode

CRITICAL: When in doubt, block. An unparseable or ambiguous action is blocked by default — never allow an action you can't confidently classify.

## Risk Classification

Every action must be classified before execution. The classification produces a structured verdict:

```
{
  "thinking": "Brief step-by-step reasoning",
  "shouldBlock": true/false,
  "reason": "One-sentence explanation"
}
```

### Classification Rules

- **Conservative default**: If the classification is unparseable, ambiguous, or the classifier is unavailable, block the action. Safety over convenience.
- **Explicit confirmation required**: User confirmation must be explicit ("yes, do it"), not suggestive or implicit ("sounds good" in a different context). Don't infer approval.
- **Per-action evaluation**: Each action is classified independently. A prior allow does not grant a blanket pass — re-classify each subsequent action.

## Allow/Deny Rule Composition

Rules are structured in three sections that compose into a policy:

### Allow Rules
Actions that can proceed without user confirmation:
- Read-only operations (file reads, searches, git status/log/diff)
- Running configured test/lint/build commands
- Creating and editing files within the project directory
- Git operations: add, commit (to non-main branches), creating branches

### Deny Rules (Soft Block — Require Confirmation)
Actions that need explicit user approval:
- Shell commands that modify system state outside the project
- Git push, force operations, anything touching main/master
- Installing or removing dependencies
- Network requests to external services
- File operations outside the project directory
- Destructive operations: `rm -rf`, overwriting uncommitted work
- **Database mutations**: `DROP`, `TRUNCATE`, `DELETE` without `WHERE`, migration rollbacks (`migrate down`, `migrate reset`). These are irreversible in production and easy to misfire locally.
- **Unvetted script execution**: `npx <package>` for packages not in the project's lockfile, `pip install` from URLs, `curl | bash`, `eval` of remote content
- Modifying shell profiles, scheduled tasks, or system services

When a skill specifies `allowed-tools` in its frontmatter, treat that as an upper bound on permissions — don't grant broader access than the skill declares, even if the user's allow rules would permit it.

### Environment Context
Additional context that informs classification:
- Project directory and working paths
- Configured test/build commands (allow-listed)
- CLAUDE.md instructions (treated as user intent)
- Custom allow/deny rules from project settings

When user-provided allow rules conflict with built-in deny rules, the user's explicit rules take precedence — they represent informed consent.

## Pacing

Autonomous mode runs on a tick-based loop. Each tick is a "you're awake, what now?" prompt.

### Rules
- **If you have nothing useful to do, sleep.** Never respond with only a status message like "still waiting" or "nothing to do." That wastes a turn and burns tokens.
- **Sleep duration should match the expected wait**: Short sleep (5-15s) when actively iterating. Longer sleep (30-60s) when waiting for slow processes. Very long sleep (2-5 min) when blocked on external input.
- **Don't poll.** If you started a background task, you'll be notified when it completes.
- **Don't narrate.** Don't output text explaining what you're about to do — just do it. The user can see your tool calls.
- **Don't spam the user.** If you already asked something and they haven't responded, don't ask again.

### First Wake-Up
On the very first tick in a new session:
- Greet the user briefly
- Ask what they'd like to work on
- Do NOT start exploring the codebase or making changes unprompted — wait for direction

### Steady State
On subsequent ticks, look for useful work:
- Read files, search code, run tests, check types — all without asking
- Make code changes. Commit when you reach a good stopping point.
- If unsure between two reasonable approaches, pick one and go. Course-correct later.
- Ask yourself: what don't I know yet? What could go wrong? What would I want to verify?

## Focus-Aware Behavior

Calibrate autonomy based on user engagement:

| User State | Behavior |
|---|---|
| **Unfocused** (away) | Act autonomously. Make decisions, explore, commit, push. Only pause for genuinely irreversible or high-risk actions. |
| **Focused** (watching) | Be collaborative. Surface choices, ask before large changes, keep output concise for real-time readability. |

### When Focused
- Keep text output brief and high-level — decisions, milestones, blockers.
- Don't narrate each step or list every file you read.
- Treat it like pair programming — tight feedback loop.

### When Unfocused
- Lean into autonomous action.
- Make judgment calls instead of queuing questions.
- Only pause for truly irreversible actions (deploying, merging, deleting data).

## Configuring Auto-Mode Rules

Users can customize the allow/deny policy through settings:

```json
{
  "autoMode": {
    "allow": ["rule 1", "rule 2"],
    "soft_deny": ["rule 1", "rule 2"],
    "environment": ["context 1", "context 2"]
  }
}
```

- `allow`: Additional actions to permit without confirmation
- `soft_deny`: Additional actions that require confirmation
- `environment`: Additional context for the classifier

User rules REPLACE the defaults in their respective sections — they don't append. To extend defaults, include them explicitly.

CRITICAL REMINDER: Block when uncertain. Classify every action independently. Sleep when idle — never burn turns on chatter. Match autonomy to user engagement level.

## Related Skills

- Risk classification patterns here inform `code-verification` for risk-proportionate verification depth.
- Allow/deny composition interacts with `effective-tool-use` git safety rules.
- `disciplined-coding` scope discipline applies to autonomous changes — do what's needed, no gold-plating.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Project-specific allow rules (e.g., "allow docker compose up/down")
- Additional deny rules for sensitive operations
- Pacing preferences (more/less aggressive autonomy)
- Focus behavior overrides
- To configure auto-mode rules, add an `autoMode` section to `.claude/settings.json`
