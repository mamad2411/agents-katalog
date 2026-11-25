---
name: fast-context
description: Use this skill when you need semantic codebase context before planning, explaining, or changing project code. It runs a bundled local Fast Context script that calls Windsurf Devstral directly, avoiding the Fast Context MCP server while preserving natural-language repository search, recursive context gathering, and definition/signature completeness checks.
metadata:
  short-description: Semantic code context retrieval
---

# Fast Context

## Overview

Use Fast Context as the first pass for codebase-aware work: locating implementation paths, tracing flows, finding tests, and collecting the complete definitions needed before producing code or project-specific advice.

This skill runs `scripts/fast-context-search.mjs` directly from the installed skill directory. The script uses vendored Fast Context core logic from the upstream `v1.3.0-beta.2` source and Windsurf Devstral, but it does not require the Fast Context MCP server to be installed or enabled. It does not replace exact local inspection; use returned file paths and grep keywords to drive targeted `rg`, `sed`, and file reads.

## When To Use

- Before code changes, architecture suggestions, bug fixes, test plans, or explanations that depend on project-specific behavior.
- When the relevant files are unknown or the feature crosses several modules.
- When you need full definitions, signatures, call sites, configuration, routes, schemas, or tests.

Skip this skill for purely conversational tasks, tiny known-file edits, or third-party library documentation lookups. Use a documentation retrieval skill such as Context7 for current external API docs.

## Workflow

1. Build one natural-language query that names the user goal and asks for the exact context needed. Prefer "Where", "What", and "How" questions.
2. Resolve the installed skill directory and run `node <skill-directory>/scripts/fast-context-search.mjs` with `--project` set to the absolute project root and `--query` set to the natural-language search query.
3. Read the returned file ranges and use the suggested grep keywords with local tools to inspect exact definitions.
4. Run a completeness check: make sure all relevant classes, functions, variables, types, config, routes, call sites, and tests have been identified with full signatures.
5. If anything is missing, recursively query Fast Context again with the missing concept, symbol, or flow.
6. If ambiguity remains after retrieval, ask the user guiding questions before changing behavior.

## Default Command

```bash
node /path/to/installed/fast-context/scripts/fast-context-search.mjs \
  --project "/absolute/path/to/project" \
  --query "Where is <feature or behavior> implemented, and what full definitions, signatures, call sites, config, and tests are relevant to <user goal>?" \
  --max-results 10 \
  --max-turns 3 \
  --tree-depth 0 \
  --exclude ".git,node_modules,dist,build,coverage"
```

Use `max_results` 3-5 for focused symbol lookup, 10-20 for feature tracing, and 20-30 for broad exploration. Use `max_turns` 1 for quick lookup and 4-5 for complex cross-module tracing.

## Query Patterns

- Locate implementation: `Where is <feature> implemented? Include entry points, core functions/classes, data types, config, and tests.`
- Trace flow: `How does <user action or API call> flow through the codebase from entry point to persistence/output? Include full definitions and call sites.`
- Prepare a change: `What code must change to <requirement>? Find current behavior, extension points, validation, tests, and adjacent risks.`
- Find tests: `What tests cover <behavior>, and where should new coverage be added? Include fixtures and helpers.`

## Tuning And Fallback

- If results are too shallow, increase `max_turns` or `max_results`, or query a narrower symbol or flow.
- If the repo map is too large, reduce `tree_depth`, add `exclude_paths`, or use `repo_map_mode: "bootstrap_hotspot"`.
- If authentication fails, run the same script with `--check-key` to verify local Windsurf key discovery, then retry after Windsurf is logged in or `WINDSURF_API_KEY` is set.
- If the user explicitly needs the key, use `--print-key` to print it locally or `--key-env` to print an `export WINDSURF_API_KEY=...` command for the current shell. Treat the output as a secret.
- If Node dependencies are missing, run `npm install` in the installed Fast Context skill directory.
- If the script is unavailable or still fails, state that briefly and continue with local `rg --files`, `rg`, and targeted file reads.

## Reference

For the exact script parameter contract, response shape, and tuning notes, read `references/script-contract.md` only when needed.
