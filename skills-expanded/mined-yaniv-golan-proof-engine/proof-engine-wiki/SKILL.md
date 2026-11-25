---
name: proof-engine-wiki
description: >
  Attach Proof Engine proofs to LLM-wiki claims. Use for ingest (extract
  claims, look up or commission proofs, rewrite pages with badges) and lint
  (re-verify citations, detect contradictions, report stale proofs) steps in
  wiki pipelines. Trigger phrases: "ingest wiki page", "lint wiki",
  "{{prove:}} markers", "verify wiki citations".
license: MIT
metadata:
  author: Yaniv Golan
  version: "0.1.0"
compatibility: >
  Requires Python 3.11+ and the proof-engine-wiki package installed
  (`pip install proof-engine-wiki`). Optional: a configured registry in
  `~/.config/proof-engine/registries.toml` for `--registry-only` mode.
---

# proof-engine-wiki

Hooks Proof Engine verification into LLM-wiki ingest and lint operations.

## When to use

Invoke this skill when:
- A new source has been added to a wiki and its draft pages contain `{{prove:}}` markers.
- A periodic lint pass is running — re-verify citations, flag contradictions.
- A user asks "is this claim actually proven?" while editing a wiki page.

## When NOT to use

- To write proofs from scratch — that is the `proof-engine` skill (the parent).
- To extract claims from unmarked prose — this skill only processes explicit `{{prove:}}` markers. Auto-extraction is out of scope for v0.1.

## Workflow

1. Read the wiki page or directory.
2. Run `proof-engine-wiki ingest <path>` (or `lint`, as appropriate).
3. Review the output plan; commit the rewritten pages.

Full runbooks in `references/ingest-runbook.md` and `references/lint-runbook.md`.
