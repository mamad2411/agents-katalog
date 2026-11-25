---
name: obsidian-notes-karpathy
description: Diagnose and route ambiguous, workflow-level Karpathy-style LLM Wiki requests inside Obsidian. Use this skill when the user talks about the workflow as a whole, mentions Andrej Karpathy's markdown-wiki pattern, "LLM Wiki", a "living book", "not RAG", "AI knowledge base", "personal wiki", "second brain", "PKM workflow", asks what step to run next, or describes symptoms like "my notes are rotting", "knowledge base feels disconnected", "broken Obsidian index", "知识库工作流", "不是 RAG", "会自动生长的书", "笔记越来越乱", or "我该先做哪一步". Prefer the operation-specific skills when the user already clearly means init, compile, query, or health.
---

# Obsidian Notes Karpathy

Package-level entry point for the Karpathy-style knowledge-compilation workflow.

Use this skill when the user talks about the workflow as a whole, not just one operation. Your first job is to diagnose the current lifecycle stage. Your second job is to route to the correct operational skill.

## Read before routing

Read these shared references first:

- `./references/file-model.md`
- `./references/lifecycle-matrix.md`
- `./references/search-upgrades.md`
- `./references/activity-log-template.md`

If the target vault already exists, inspect:

- local `AGENTS.md`
- local `CLAUDE.md` if present, and surface its absence as a repair target rather than a standalone blocker
- the top of `wiki/index.md`
- the most recent entries in `wiki/log.md` when available

If `./scripts/detect_lifecycle.py` exists, run it against the target vault first and treat its JSON output as the default structural diagnosis. Override the default only when the user's symptoms clearly point to a different lifecycle step.

## Lifecycle signals

Diagnose the vault using signals, not just user phrasing.

Prefer the shared lifecycle matrix and the deterministic lifecycle script over ad-hoc guessing.

### Init signals

Route to `kb-init` when the target does not yet express the contract:

- no `raw/`
- no `wiki/`
- no `outputs/`
- no required local `AGENTS.md`
- ambiguous duplicate case-variant guidance files such as both `AGENTS.md` and `agents.md`
- missing or obviously partial KB support files that make the workflow structurally incomplete
- the user explicitly wants to repair a half-initialized vault before doing normal work

### Compile signals

Route to `kb-compile` when the vault exists and new source material appears to be waiting for compilation:

- new or changed files directly under `raw/`
- new or changed files under `raw/articles/`, `raw/papers/`, `raw/podcasts/`, or optional `raw/repos/`
- PDF papers under `raw/papers/`, which should be compiled by using `alphaxiv-paper-lookup` only when the PDF resolves to a deterministic paper handle, otherwise falling back to `pdf`, then reporting missing companion skills if needed
- missing summaries for recent raw notes
- the user asks to ingest, digest, compile, refresh, sync, summarize, or turn clips into notes

### Query signals

Route to `kb-query` when the compiled layer already exists and the user wants to extract meaning or generate an artifact:

- answer a question from the vault
- compare concepts, sources, or positions
- write a report, article, thread, slides, or talk outline from the notes
- search the vault or summarize what the vault already knows

### Health signals

Route to `kb-health` when the compiled layer feels stale, contradictory, disconnected, or weakly maintained:

- the user says the notes feel disconnected, outdated, contradictory, or messy
- stale Q&A or drift is more likely than missing compilation
- the user asks for contradictions, orphan notes, stale claims, alias drift, or missing cross-links
- the user reports broken Obsidian rendering, malformed indices, or pages that look syntactically wrong even though the files still exist

## Ambiguous cases

When the user asks "what should I do first?" or gives symptoms rather than a command:

- choose `kb-init` first if the vault looks only partially initialized or the support layer is missing
- do not choose `kb-init` only because `CLAUDE.md` is missing if the rest of the vault is already usable; surface that as a repair recommendation instead
- choose `kb-compile` first if recent raw material has clearly not been compiled yet
- choose `kb-health` first if the main symptom is compiled-layer drift, contradiction, stale Q&A, or weak linking
- choose `kb-query` if the vault already looks compiled and the user wants conclusions, comparison, or outward-facing content

State the assumption you made if the lifecycle diagnosis is inferred rather than explicit.

If the structural diagnosis says `query-ready` but the user's main complaint is drift, contradiction, broken rendering, or weak links, explicitly override to `kb-health` and say why.

## Package doctrine

- Treat `raw/` as immutable source material.
- Treat `wiki/` as the compiled, LLM-owned artifact.
- Treat `outputs/qa/` as persistent research memory, not disposable chat residue.
- Treat `outputs/content/` and sibling output folders as publishable derivatives of the wiki.
- Treat `wiki/index.md` and `wiki/log.md` as complementary navigation surfaces: content-first and time-first.
- Prefer simple markdown indices, backlinks, and properties before heavier search infrastructure.
- Preserve the canonical `wiki/indices/` convention, but tolerate legacy `wiki/indexes/` when a vault already uses it.

## Output requirements

When the user asks what to do next, answer with:

1. the lifecycle stage you detected
2. the concrete signals that led you there
3. the operational skill you are routing to
4. the next concrete action in the vault
5. any assumption you had to make about compile state, vault health, or missing support files
6. any companion-guidance repair target, such as a missing `CLAUDE.md`, that should be fixed later with `kb-init`
