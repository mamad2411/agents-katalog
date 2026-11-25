---
name: worker-prompt-craft
description: Use when assigning work to a worker or subagent that cannot see the main conversation, especially when the prompt must be self-contained, precise, and resistant to ambiguity or lazy follow-up delegation
---

# Worker Prompt Craft

## Overview

Workers do not share your conversational context. A good worker prompt must stand on its own.

This skill follows the explicit prompt rules in `src/coordinator/coordinatorMode.ts`.

## Non-Negotiable Rule

Never assume the worker knows what you know from the user conversation.

Forbidden prompt shapes:

- "Fix the bug we discussed"
- "Based on your findings, implement the fix"
- "Make the changes from earlier"

Those prompts outsource context reconstruction to the worker and usually produce drift.

## Required Prompt Fields

Every worker prompt should include:

- the purpose of the task
- whether the task is read-only or may modify files
- exact paths, modules, or search scope
- line numbers, symbols, or error messages when known
- completion criteria
- required verification before reporting done
- exact artifact to return

## Purpose Statement

Open with why this task exists:

- "This research is for implementation planning."
- "This is independent verification before merge."
- "This is a narrow fix to the auth null check."

The purpose helps the worker choose the right depth.

## Research Prompts

Ask for:

- files
- lines
- symbols
- type signatures
- coverage gaps

Do not ask for edits in the same prompt unless that is truly the task.

## Implementation Prompts

Ask for:

- exact files to change
- exact behavior to preserve or introduce
- root cause, not just symptom
- tests or checks to run
- commit hash or diff summary if desired

## Verification Prompts

Ask for:

- independent execution
- adversarial probes
- command evidence
- PASS, FAIL, or equivalent verdict

Use a fresh verifier when independence matters.

## Continue Or Refresh

Continue the same worker when its existing context is an asset.

Spawn a fresh worker when:

- the old context is noisy
- the task changed shape
- you want a clean verifier
- the first attempt anchored on the wrong idea

## Minimal Good Example

Fix the null check in `src/auth/validate.ts:42`. `Session.user` can be `undefined` when the session is expired but the token is still cached. Return 401 with `"Session expired"` instead of dereferencing `user.id`. Update the relevant tests in `src/auth/validate.test.ts`. Run the targeted tests and report the commit hash.

## Anti-Patterns

- referring to "the bug" without naming it
- referring to "your findings" instead of synthesizing them
- mixing broad exploration and narrow implementation in one muddy prompt
- omitting what done looks like

## Done Condition

You have applied this skill correctly when a fresh worker could complete the task from your prompt alone without seeing any of the surrounding conversation.
