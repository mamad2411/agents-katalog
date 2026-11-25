---
name: release-notes
description: Draft release notes from merged pull requests when the user asks for a changelog or release summary.
some-future-field: true
metadata:
  author: example-org
  version: "1.0"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./.claude/hooks/check.sh"
---
Collect merged pull requests with `scripts/collect.sh` and group them by label.
