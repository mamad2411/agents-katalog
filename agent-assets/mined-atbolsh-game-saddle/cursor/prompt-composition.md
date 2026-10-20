---
description: Compose system prompts from shared named blocks; never duplicate prompt prose
alwaysApply: true
---

# Prompt composition — no copy-pasted prompt blocks

System prompts are code. Apply the same anti-duplication discipline to prompt
prose that you apply to functions:

- **One concept, one block.** Any concept that appears in two or more system
  prompts (game world description, move-token protocol, privileged geometry,
  tool descriptions, tip-writing policy, ...) lives in exactly ONE named
  module-level string constant (`_BLOCK_*` in `agent/modes.py`), and every
  prompt that needs it composes it in (`"\n\n".join(...)`).
- **Never copy-paste paragraphs between mode prompts.** If two prompts need
  slightly different wording of the same idea, either parameterize the block
  or factor out the truly-shared part; do not fork the text.
- **Prefer recomposition over new modes.** Before writing a new standalone
  `SYSTEM_PROMPT_*`, check whether the new behavior is an existing mode's
  blocks plus one short scope paragraph. Mode explosion — many
  slightly-different prompts with unmemorable subtle differences — is the
  failure mode this rule exists to prevent.
- **Edits propagate by construction.** Fixing a fact (e.g. the geometry
  conventions) in its block must fix every mode that uses it; if you find
  yourself making the same prompt edit in two places, the blocks are wrong.
