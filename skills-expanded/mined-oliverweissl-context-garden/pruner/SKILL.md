---
name: pruner
description: Pick the smallest set of file:line ranges relevant to a concrete task (bug, compiler error, failing test, change) in a large Python or C/C++ repository, instead of grep-exploring or reading whole files. Skip when the task or traceback already names the file.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/bin/pruner *), Bash("${CLAUDE_SKILL_DIR}/bin/pruner" *)
---

# pruner

!`"${CLAUDE_SKILL_DIR}/bin/pruner" mode --banner`

Agents that do not expand the line above (e.g. Codex): run
`<this-skill-dir>/bin/pruner mode --banner` first and follow it.

Offline indexer + lexical/structural relevance scorer (keyword overlap,
call graph, error-stack membership, test relationships; no embeddings,
no LLM). How scores work: `references/scoring.md`.

`pruner` is not on PATH: run `<this-skill-dir>/bin/pruner`.

1. Select a slice:
   ```
   <this-skill-dir>/bin/pruner select --task "<what you're doing>" --budget <N> \
     [--error "<traceback>" | --error-file <path>] [--changed <files...> | --auto-changed]
   ```
   If you have an error, always pass `--error`; error-stack membership is
   the strongest relevance signal.
   First run builds a SQLite index under `.pruner/`; later runs re-parse
   only changed files. Output lists `required_context`,
   `supporting_context`, `relevant_tests`, `relevant_config` as exact
   `file:start-end` ranges with a reason each. Read those ranges, not whole
   files.
2. The slice is a starting point, not a fence. If confidence is
   `low`/`medium` (a `hint:` line is printed) or the slice doesn't explain
   the behavior, fall back to targeted grep and reads.
3. Missing a dependency? Don't re-run `select` from scratch or fall back to
   open-ended exploration: check `omitted_candidates`, then
   `bin/pruner expand <slice_id> --add <id or file:start-end>` (or
   `--file <path> --lines A:B`). The token budget is hard-enforced: `select`
   never returns more than `--budget` tokens and `expand` refuses to exceed
   it unless you pass `--budget-extra N`.
4. `bin/pruner show <slice_id>` / `list` re-print saved slices without re-scoring.
5. With the plugin, an error pasted into the prompt is sliced automatically
   (context starting "pruner (ran automatically ..."): start from that
   slice, `expand` it rather than re-running `select`.

Full CLI (`--graph`, `--parser`, tree-sitter backend, language scope):
`references/schema.md`.
