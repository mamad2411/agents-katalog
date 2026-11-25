---
name: proof-usage
description: Look up and apply the cooked, indexed proof playbook built from proof-material. Use when the user is proving a theorem, planning a proof, seeking reusable proof moves by task shape, assumptions, tags, desired move, or material source ID, or adapting cooked local moves and macro strategies with public source attribution.
---

# Proof Usage

## Overview

Use this skill as the final agent-facing proof playbook. It stores cooked entries synthesized from `proof-material`, not raw source extraction notes.

Start at [references/index.md](references/index.md). The index routes by problem shape, assumptions, desired proof move, tags, and source material IDs.

## Pipeline Position

`proof-usage` is the final lookup stage:

```text
proof-cooker -> proof-usage -> current proof task
```

Its job is usability. A theorem-proving agent should search this playbook first, apply a cooked entry when assumptions match, and follow material IDs back to `proof-material` only when source-level context is needed.

## Library Modules

- [references/index.md](references/index.md): first stop for routing and search.
- [references/source-map.md](references/source-map.md): maps cooked entries back to stable proof-material IDs and public sources.
- `references/local-moves/`: local lemmas, estimates, concentration steps, convexity conversions, parameter balances, and restart controls.
- `references/strategies/`: macro proof architectures, auxiliary-model arguments, staged algorithms, and role-separation templates.
- [references/techniques.md](references/techniques.md) and [references/strategies.md](references/strategies.md): legacy compatibility files retained while older cards are migrated or linked.

## Usage Workflow

1. Parse the user's proof target.
   - Identify the object being bounded, constructed, localized, decomposed, or compared.
   - Note assumptions such as linearity, convexity, error-bound conditions, bounded features, filtration, Bellman structure, duality, or self-normalized processes.
2. Search the index.
   - Match by task shape first, then assumptions, desired move, tags, and material IDs.
   - Load only the category files that match the current proof target.
3. Adapt the cooked entry.
   - Translate notation into the user's setting.
   - Check required assumptions and failure modes before using the move.
   - Follow `Material sources` back to `proof-material` only when source-level details are needed.
4. Be honest about fit.
   - If a move requires stronger assumptions than the user has, say so.
   - If no entry fits, explain the closest partial analogy and what additional lemma would be needed.

## Cooked Entry Contract

Each cooked entry should include:

- `Category`
- `Use when`
- `Required assumptions`
- `Core move`
- `Self-contained statement or template`
- `How to adapt`
- `Failure modes`
- `Related entries`
- `Material sources`
- `Public attribution`

## Maintenance

- `proof-cooker` owns taxonomy updates, de-duplication, source-map maintenance, and migration from legacy files.
- Cooked entries must link to one or more stable material IDs.
- Keep raw extraction notes, DeepSeek transcripts, local OCR dumps, source-local clutter, private paths, account names, and unpublished project details out of this skill.
