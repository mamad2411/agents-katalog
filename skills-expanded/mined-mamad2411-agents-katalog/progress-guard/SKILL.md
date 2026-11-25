# Progress Guard Skill

## Purpose
Prevents the agent from getting stuck in repetitive loops by detecting when it's not making progress and forcing a different approach.

## Rules

### When to Activate
- Run the same command/operation 3+ times without results
- Check the same status multiple times without changes
- Keep trying the same approach when it fails
- Spend more than 5 minutes on a single verification step

### When to Break
- Stop immediately when no progress is detected
- Switch to a different approach or tool
- Ask for direction if stuck
- Report the problem instead of continuing the loop

### Examples
- ❌ Don't: Keep running `grep` to check for files that don't exist
- ✅ Do: Just use `sed` to replace the text regardless
- ❌ Don't: Keep verifying the same thing over and over
- ✅ Do: Actually make the changes instead of checking

## Implementation
This skill runs automatically on every session. When you detect a potential loop, immediately stop and report the issue instead of continuing.
