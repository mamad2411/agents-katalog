---
name: vgrep
description: Semantic codebase search. Use when intent matters more than exact tokens; complements grep/rg.
---

## When to use

- Locating code by intent: "where do we handle auth", "find the retry/backoff logic", "code similar to X".
- Onboarding into an unfamiliar repository where you don't know the exact identifiers.
- Cross-referencing a concept that appears under many different names.

For exact strings, regex, or symbol lookups, prefer `rg` / `grep`.

## Steps

1. `vgrep status` — confirm an index exists. If it errors with "not initialized", run `vgrep init --force`.
2. `vgrep search "<intent>" -k 5` — returns the top-k semantic chunks as `path:start-end` with a similarity score and a code preview.
3. `cat <path>` (or `head -n N <path>` / `tail -n +N <path>`) to expand context around a hit.
4. Iterate: refine the query phrase based on what hits returned. Multiple short, distinct queries beat one long compound query.

## Output format

```
<path>:<startLine>-<endLine>  <score>
<code preview, up to 8 lines>
```

Lower scores in vgrep are better (cosine distance).

## Notes

- Only files matched by `.vgrep/config.json` profiles are indexed; default profile is `code`.
- `.vgrepignore` controls exclusions (gitignore syntax).
- Re-run `vgrep init` after large refactors; it's incremental (Merkle-diffed).
