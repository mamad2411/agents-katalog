---
name: reverse-engineering-api-setup
description: Use when an authorized API compatibility or debugging task needs the external reverse-api-engineer tool.
x-alice-class: reverse
---# reverse-api-engineer setup

Use this Skill to install and operate the external `reverse-api-engineer` tool for authorized API compatibility, migration, testing, or debugging work. The external tool is installed separately and is not embedded in this Skill.

## Source boundary

- Official project: https://github.com/kalil0321/reverse-api-engineer
- Reviewed commit: `02fc798318b6954519850b455fdad5f8248ab911`
- Upstream license: MIT

## Setup

1. Use an isolated Python environment or `uv tool` installation.
2. Install from the official project or its published package.
3. Install the browser runtime only if the authorized workflow requires browser capture.
4. Verify the executable and record its version before collecting traffic.
5. Store captures in a customer-controlled workspace and remove secrets before sharing results.

```bash
uv tool install reverse-api-engineer
playwright install chromium
reverse-api-engineer --help
```

Only inspect endpoints, sessions, and traffic you are authorized to test. Never place API keys, cookies, access tokens, or customer credentials in prompts or reusable Skill files.
