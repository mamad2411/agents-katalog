---
name: commit-quality
description: Write high-quality commits. Use when authoring or reviewing commit
  messages and granularity.
metadata:
  tags: commit, quality
---

# Commit Quality

## Use this skill when
- Splitting work into logical commits
- Writing clear conventional messages
- Making history navigable

## Do not use this skill when
- Squashing an entire feature into one dump
- Automated repo trivia

## Instructions
1. Commit small logical units that each keep the build green.
2. Use conventional commits: type(scope): summary.
3. Explain the why in the body when non-obvious.
4. Keep commits focused; avoid mixing refactor + feature + fix.
5. Reference issues and link external context.
6. Avoid committing secrets, huge binaries, or junk.

## Checklist
- Each commit is coherent
- Messages explain why
- No secrets/binaries

## Output Format
- Commit plan | message convention | review checklist

## Common Mistakes
- “wip” and “fix” as the entire message
- Grandma-sized commits bundling everything
- Committing generated junk
