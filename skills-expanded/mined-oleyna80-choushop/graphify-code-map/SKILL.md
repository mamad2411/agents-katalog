---
name: graphify-code-map
description: Optional local code-map helper for unfamiliar or broad code slices. Use Graphify only through the code-only update path to create navigation evidence before review or implementation.
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: Graphify Code Map

## Triggers
- unfamiliar runtime slice
- broad route/service/storage review
- dependency or call-flow discovery across several files
- "построй карту кода", "code map", "Graphify"
- before a large review where structural navigation may save time

## When to Use

Use this skill when local source inspection is likely to be slow because the
slice spans multiple files or directories, and a structural graph can help
identify entrypoints, call paths, and high-degree modules.

Graphify output is navigation evidence only. It does not replace code review,
security review, acceptance criteria, tests, or runtime proof.

## When to Skip

Skip for:
- small tasks involving 1-3 files;
- docs-only work;
- security acceptance decisions that require direct code inspection;
- tasks where copying files to `/tmp` would include secrets, env files, logs,
  payload dumps, or private data;
- live DB, deploy, provider API, or client-facing actions.

## Workflow

1. Confirm Graphify is already installed locally and inspect CLI help in the
   current environment.
   - If missing, stop and ask before installing anything.
2. Check that Graphify/model API variables are not present by name before a
   code-only run.
   - Print variable names only, never values.
3. Create a temporary slice under `/tmp`.
   - Copy only approved code files.
   - Do not include docs, PDFs, images, env files, logs, DB dumps, transcripts,
     screenshots, or private payloads.
4. Run Graphify `update` on the `/tmp` slice only. Do not use `extract` unless
   a separate Work Block approves semantic LLM extraction.

```bash
.cache/graphify-venv/bin/graphify update /tmp/<slice> --no-cluster
```

5. Confirm the run stayed on the code-only path.
   - Expected CLI wording: `no LLM needed`.
   - Expected graph evidence: `input_tokens: 0` and `output_tokens: 0`.
6. Inspect `graphify-out/graph.json` for:
   - node/edge counts;
   - key entrypoints;
   - call paths;
   - high-degree modules;
   - missing or weak graph coverage.
7. Treat `explain` and `path` output as hints. Use `--graph
   /tmp/<slice>/graphify-out/graph.json` for follow-up commands and confirm
   important conclusions by reading the source files directly.
8. Remove accidental repo-root `graphify-out/*` artifacts if Graphify creates
   them during local experimentation.

## Guardrails

- No API keys, provider credentials, env values, or secrets may be used.
- Do not scan the full repository.
- Do not scan docs or non-code files; Graphify `extract` may send some non-code
  material to an external model backend.
- Do not install Graphify hooks, Codex/Claude integrations, or background
  watchers unless a separate Work Block approves that exact action.
- Do not treat Graphify output as authority for security, maintainability, or
  acceptance.
- Do not publish generated graph artifacts unless explicitly approved.

## Output

Report:
- scope copied to `/tmp`;
- command used;
- evidence that the code-only path was used, such as CLI `no LLM needed`
  wording and zero token counts;
- useful graph findings;
- limitations or missing coverage;
- whether Graphify changed the review/implementation plan;
- any generated repo-root artifacts cleaned up.

## Handoff

- **Success condition**: Graphify produced useful navigation hints through the
  code-only update path without API, secret, repo-root, or non-code exposure.
- **Next**: return to normal SDD planning, review, or implementation.
- **Auto-proceed**: YES, inside an approved read-only/local tooling Work Block.
- **Hard stop**: installing packages, enabling hooks/integrations, using API
  keys, scanning non-code/private files, or publishing artifacts.
