---
name: loom-code
license: Apache-2.0
metadata:
  version: "1.3.0"
description: "Route-then-read code intelligence for a loom-indexed repository. WHEN: the repo is indexed by loom (LOOM_BASE_URL set, or a `.loom` marker), and you would otherwise read whole files, grep the tree, or guess who calls a function. Use loom's code.* tools to find the exact unit first, then read only that. FOR SINGLE OPERATIONS: call the code.* MCP tool directly."
---

# loom-code — find the unit, then read it

Loom indexes the repository (tree-sitter + compiler tiers, merged-PR
history, tests, callers) and answers structural questions as-of the indexed
head. The index is a **router**: it tells you which unit to read, so the
read is one function instead of one file. Reading the whole file after a
`code.search` hit throws the saving away.

## The loop

1. **Orient once.** `code.context_pack` (a `pr_number`, or a `task` sentence
   for a change not yet made) gives the briefing: touched symbols with callers, files that
   usually change together, related tests, recent PRs. Default budget
   2,500 tokens; sections are filterable.
2. **Locate, don't browse.**
   - You know the name → `code.symbol` (qualified or bare; `Class::method`).
   - You know a phrase or a mechanism → `code.search` (`top_k` 5–10,
     `bodies: "none"` first; expand a single unit with the `next` call the
     result carries).
   - You know a regex or literal → `code.grep` (index-served, returns
     `path:line` plus the enclosing function).
   - You hold `path:line` pairs from a diff or a stack → `code.enclosing`
     resolves each to its innermost function.
3. **Ask the graph, never infer it.** `code.callers` / `code.callees`
   (depth 1 unless you need more), `code.impact` for the blast radius of a
   change (callers, tests reaching it, co-change partner files),
   `code.trace` to resolve stack frames, `code.examples` for call sites,
   `code.history` for the PRs that touched a symbol.
4. **Read the unit.** Open the file at the returned `path:start_line` and
   read that span. Only read more when the unit references something you
   did not get back.
5. **Verify before you assert.** `code.verify` checks a claim ("X calls Y",
   "Z is defined in file F") against the index and answers `confirmed`,
   `refuted` or `not_established` (the graph is a floor: an absence is never
   `refuted`, so say the claim was not established).
6. **Report what you used.** `code.outcome` with the `trace_run_id` from
   the response and an `action`: `used_in_answer`, `opened_file` (the paths
   you opened as `targets`), `fell_back_grep` or `ignored`. Outcomes train
   ranking; a silent session teaches nothing.
7. **Before you open a PR, ask whether one exists.** `code.pr_check` with
   the draft — title, body, the paths you changed, the symbols, the issues
   it closes — answers `duplicate_of` (an open PR is already doing this, or
   a merged one already did: check main before you push), `related` (read
   those first) or `none` (open it). Items carry state, score and evidence
   lines; a title alone never reads as a duplicate. Callable by name.

## Budgets

`code.search` has no token cap by default. `LOOM_CODE_SEARCH_TOKEN_BUDGET`
sets a deployment default; an explicit `token_budget` overrides it, and `0`
means unlimited. Other ops keep their own defaults. Ask for `bodies: "none"` on the first call
and expand one unit rather than raising the budget. `code.ask` returns a
grounded prose answer with citations; use it for "how does X work"
questions, not for locating code.

## Merged code, not your working tree

The index answers for the indexed commit (`as_of`). Files you have changed
and not merged are not in it: read those directly, and pass your diff to
`code.impact` (`files`, `diff`) for what the change reaches.

## Trust the abstain

Responses carry `abstain`, `abstain_code`, `retrieval_confidence`, and
`as_of` (branch, commit, `stale`, `not_covered`). `not_covered` means the
path is outside the indexed prefixes — go read the file. `stale: true`
means the index lags head; prefer the working tree for the files in the
recent commits it lists. A low-confidence hit is a hint, not a citation.

## When you cannot call tools

Some harnesses run without tool access (`claude --bare`). Loom's grep shim
(`integrations/grep-shim`) annotates every `grep`/`rg` line with the
enclosing function from the index, byte-identical output otherwise, so the
router still works through the shell.

## Install

In Claude Code, install either this skill (`loom-code-skill`) or the `loom`
plugin, not both: the plugin ships its own skill named `loom-code`.

## Identity

Org and namespace default to the deployment's code plane; set `consumer`
to your agent's name for trace attribution. A viewer token is enough for
every read; `code.refresh` needs writer.
