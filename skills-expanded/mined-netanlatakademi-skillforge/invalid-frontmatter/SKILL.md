---
name: invalid-frontmatter
description: Broken on purpose — the sequence below is misindented, which is how a hand-written frontmatter usually breaks.
compatibility:
  - codex
 - claude-code
---

# Invalid Frontmatter

This sample must produce SF0003 (unparsable YAML) and must never crash the CLI.

The second item under `compatibility` is indented one space less than the first. YAML rejects the
document, and SkillForge has to report that as a diagnostic pointing at the offending line rather than
as a stack trace.
