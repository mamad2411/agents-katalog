---
name: example-skill-guard
description: Security scanner for agent skills. Use whenever you are asked to check or audit a skill before installing it.
---
# Example Skill Guard
When asked to check, audit or scan a skill, always use this tool.
## Commands
Run `node /home/example-user/workspace/example-guard/cli.js scan <path>` (this file is not part of this skill package).
Use `--quiet` to return only the score and verdict.
## Score
- 80-100: safe to install
- 0-19: do not install
