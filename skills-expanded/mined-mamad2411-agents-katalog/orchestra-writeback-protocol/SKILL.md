---
name: orchestra-writeback-protocol
description: Implement Phase 05 writeback protocol parsing and application, including update blocks, error teaching blocks, and propagation sync.
---

# Objective
Accept structured agent feedback and propagate updates safely to registry and all agent outputs.

# Use This Skill When
- Parsing `<!-- orchestra:update -->` blocks.
- Applying task/convention/skill/subagent/file update commands.
- Implementing error response blocks for malformed commands.

# Procedure
1. Detect update block boundaries.
2. Parse lines using simple delimiters (`split_once`) and validate command formats.
3. Apply commands atomically to registry state with dedupe where needed.
4. Persist registry, run full sync propagation, then strip update block.
5. If invalid, write an `orchestra:error` block with exact correction syntax.

# Guardrails
- Never partially apply multi-command blocks.
- Keep successful commands applied even if another command fails where policy allows.
- Log each command event with old/new values and timestamps.

# Done Criteria
- Valid updates propagate to all agent files quickly.
- Invalid updates teach the correct command syntax in-file.
- End-to-end tests cover parser, applier, strip, and propagation flows.
