---
name: agent-skill-kit-discoverability-linter
description: Score a SKILL.md description 0-100 for trigger quality, flag vague language, warn on vendor-specific frontmatter, and verify relative file references resolve. Use when the user asks to lint a skill, improve discoverability, score a description, or check why an agent never fires their skill.
tier: app
license: Apache-2.0
compatibility: requires `skills-ref` CLI
---

# Agent Skill Discoverability Linter

Wraps `skills-ref lint`. The first qualitative pass in the toolkit — beyond structural validation, it scores a description's likelihood of triggering the right agent activations.

## When to use

- "Why doesn't my skill ever fire?"
- "Improve this description"
- "Score my SKILL.md descriptions"
- "Lint my skill against vendor-neutrality"

## Sub-scores

| Sub-score          | Weight | What it rewards                                                       |
| ------------------ | ------ | --------------------------------------------------------------------- |
| keyword density    | 25     | Description tokens that also appear in the body (semantic overlap).   |
| action verbs       | 20     | First-token verb (12) + any-position verb (8) from action_verbs.txt.  |
| trigger phrases    | 20     | Presence of `use when`, `when`, `if`, or `for`.                       |
| specificity        | 20     | Avoidance of vague phrases (`helps with`, `general purpose`, etc.).   |
| length sweet spot  | 15     | 60-300 chars; linear ramp on either side.                             |

The score is clamped to 100.

## Issue codes emitted

- `L001_VENDOR_SPECIFIC_FIELD` (warn) — top-level frontmatter key matches a vendor prefix (`claude-`, `cursor-`, `devin-`, etc.). Recommend moving under `metadata`.
- `L002_DESCRIPTION_QUALITY` (warn) — a sub-score triggered a quality warning (vague phrases found, no action verb, no trigger phrase).
- `W002_BROKEN_REFERENCE` (warn) — same code the validator emits; the linter resolves all relative file references in the body and surfaces any that do not exist on disk.

## Worked example

Before (score: 18/100):

```
description: A useful tool that helps with stuff related to skills.
```

After (score: 82/100):

```
description: Score a SKILL.md description for trigger quality, flag vague language, and warn on vendor-specific frontmatter. Use when the user asks to lint a skill, improve discoverability, or check why their skill never fires.
```

## Invocation

```bash
skills-ref lint <skill-dir-or-tree> [--format json|human] [--explain] [--min-score N]
```

Common patterns:

```bash
# Single skill, full breakdown
skills-ref lint .agents/skills/my-skill --explain

# Tighten the bar for CI
skills-ref lint .agents/skills/ --min-score 60

# Machine-readable for the optimizer (Feature 06)
skills-ref lint .agents/skills/my-skill --format json
```

## Exit codes

- `0` — every scored skill scored at or above the threshold (default 40) and emitted no broken-reference warnings.
- `1` — at least one skill scored below the threshold, emitted `W002_BROKEN_REFERENCE`, or failed to parse.
- `64` — usage error.

## JSON shape

The `--format json` output is consumable by the description optimizer (Feature 06):

```json
{"breakdown":{"actionVerbs":20,"keywordDensity":25,"length":15,"specificity":20,"triggerPhrases":20},"issues":[],"path":"...","score":100}
```

## Limits

- The scorer is **deterministic** — no LLM in the loop. For LLM-driven rewrites, the optimizer (Feature 06) consumes this output.
- Vague-phrase, action-verb, and stop-word lists live in the package's `assets/` directory and are intentionally narrow. The lists are maintained on the mjs side and symlinked into the py side.
- Vendor-neutrality is intentionally narrower than the auditor's unauthorized-field check. The auditor flags any unauthorized top-level field as MEDIUM; this linter flags only vendor-prefixed unauthorized fields as warnings and points at `metadata`.

## Reference

Full specification: see the canonical spec at [../../../agentskills.io.md](../../../agentskills.io.md).
