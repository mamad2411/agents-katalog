---
name: agents-md-edit
description: >
  Use before changing AGENTS.md — a workflow rule, a stage table, a glossary
  entry, or a maintainer note. Do not use for CLAUDE.md (it is a pointer and
  holds no content) and do not use for the generated harness mirrors under
  .claude/, .codex/, .cursor/, or .hermes/.
---

# agents-md-edit

`AGENTS.md` has two audiences in one file. Put your sentence in the wrong half
and it either ships to every Forge user or disappears at the next regenerate.

## The two blocks

- `<!-- FORGE:START -->` … `<!-- FORGE:END -->` — **the product contract.**
  It is rendered by Forge and it ships to users. It must read as if written for
  someone who has never seen this repository: no `scripts/`, no `lefthook.yml`,
  no `.agents/skills`, no machine paths, no maintainer trivia. Never hand-edit
  it to record something you learned while building Forge.
- `<!-- USER:START -->` … `<!-- USER:END -->` — **ours.** The maintainer
  contract: what we never compromise on, the glossary, the hit-every-surface
  checklist, the ways to hurt yourself, the dev runbook.

The renderer preserves the USER block across regeneration. `smartMergeAgentsMd`
extracts it by regex and re-emits it, so its content survives `forge setup`
regardless of where you put it — but it is re-emitted **above** the FORGE block,
so do not depend on its position. [verified 2026-08-13 — `lib/smart-merge.js`]

## Before you write a line

1. **Which audience?** If the sentence names a repo-local path, a script, a
   hook file, or a test, it belongs in the USER block or in
   `.forge/contributor-skills/`. Product-facing text names commands, not files.
2. **What is the evidence?** Every rule carries a provenance tag —
   `[Forge #N ×n]` for a mined correction, `[verified DATE]` for something read
   out of running code, `[imported]` for a borrowed default with no local
   incident. Untagged rules get deleted at the next re-mine. [§5.9-8]
3. **Does it beat the default?** Delete any sentence a competent agent would
   have followed anyway. Prompt the behaviour you want; naming the banned
   behaviour drags it into context.
4. **Is it short?** If a rule needs paragraphs to defend, it is the wrong rule.

## Committing it

`AGENTS.md` is protected state. Read `protected-commit` before you stage it —
as of 2026-08-13 the gate has no writer that can authorize an `AGENTS.md`
commit, including a USER-block-only edit. Never reach for `--no-verify`.

## Never

- Never put content in `CLAUDE.md`. It loads `AGENTS.md` and holds nothing.
- Never edit a generated mirror (`.claude/skills`, `.codex/skills`,
  `.cursor/skills`, `.hermes/skills`, `.agents/skills`). Edit the canonical
  source and run the generator; drift is a test failure, not a nuisance.
  [Forge product-vs-maintainer confusion ×5]
- Never let internal-only reasoning justify a maintainer assumption in shipped
  text. A hardcoded local path in shipped config has already happened here twice.

## Done when

The change sits in the correct block, carries a provenance tag, reads in plain
English, and either passed the protected-state gate or is reported as blocked.
