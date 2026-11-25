---
name: power
description: Fylgja-powers — registry + one power body (low-token router); optional id argument
---

@markdownai v1.0

# /power [id]

## ROOT

`WILLOW_FYLGJA_ROOT` if set, else `${WILLOW_ROOT:-~/github/willow-2.0}/willow/fylgja`.

## Steps

1. `Read` `{ROOT}/powers/registry.json`.
2. If USER supplied **id** matching a registry entry → `Read` `{ROOT}/powers/<file>` for that id.
3. Else choose best match by `description` → `Read` **one** `powers/*.md`.
4. Execute that checklist only; pull `{ROOT}/skills/*.md` only if the power says so.

## Ids

`brainstorm` · `plan` · `execute` · `overseer` · `debug` · `tdd` · `verify` · `worktree` · `review-in` · `review-out`

## Surfaces

`{ROOT}/powers/SURFACES.md`
