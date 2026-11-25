---
name: mad-build
description: |
  Four-step Claude + Codex collaboration for producing artifacts
  (code, drafts, analyses). Independent drafts → cross-review →
  revisions → merge.

  Triggers:
   - "MAD-build <task>"
   - "have Codex help me build X" / "have Codex help me draft Y"
   - "competition agent on <task>"
   - "let Codex try this too"
   - "do this with both AIs"

  For an adversarial audit of a research document (papers, grants,
  referee reports), use the mad-research skill instead.

  For a one-shot Codex call without protocol, use the codex-bridge
  skill instead.
---

# mad-build skill

A structured Claude + Codex collaboration on a creative or technical
artifact. Use when you want a second pair of eyes from a different
model on something you're making.

## When this skill is the right tool

- Writing code: "MAD-build an R script that does X."
- Drafting prose: "MAD-build a one-page summary of attention mechanisms."
- Designing a plan: "MAD-build a research design for testing Y."

## When this skill is NOT the right tool

- For a stress-test / referee report on a paper or grant, use
  `mad-research`.
- For a single ad-hoc Codex call, use `codex-bridge`.

## How it works (four steps)

1. Claude scaffolds `<project>/ASSIGNMENT.md` from the user's request.
2. Both agents draft independently (Claude writes `claude_v1/`, Codex
   via `codex exec` writes `codex_v1/`). Neither reads the other.
3. Each reviews the other's draft → `round1_feedback/`. **Strict
   rule:** each side reviews ONLY the other side's draft, never its
   own.
4. Each revises in response → `round2_revisions/`. **Do NOT skip
   this step.** If no changes are needed, document v2 = v1
   explicitly. Then Claude merges into `final/` and writes
   `README_DEBRIEF.md`.

See `prompts/mad_build_protocol.md` for the full operational protocol.

## Safety defaults

This skill uses `--sandbox workspace-write` by default (Codex needs
to write into the session folder). The bypass flag is behind an
explicit `--unsafe-yolo` opt-in. See `helpers/invoke_codex.md`.

## Files

```
mad-build/
├── SKILL.md                       # this file
├── prompts/
│   └── mad_build_protocol.md      # the 4-step operational protocol
├── helpers/
│   ├── invoke_codex.md            # verified codex exec patterns
│   └── doctor.md                  # pre-flight checks
└── README.md                      # what to install and why
```
