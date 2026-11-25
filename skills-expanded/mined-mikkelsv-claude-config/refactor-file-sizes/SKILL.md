---
name: refactor-file-sizes
description: "Audit AND execute file-size refactors — finds violators plus their coupling, dispatches Sonnet sub-agents per batch, build-verifies, and proposes candidate rules from observed gotchas. Use when the user wants to act on size violations — \"split this file\", \"fix the size-cap violations\", or after /audit-file-sizes reports hard-cap hits. For the read-only check only, use /audit-file-sizes."
disable-model-invocation: true
---

# Refactor File Sizes

Sweep for files over the 800-line hard cap and split them. The audit phase identifies violators plus cross-file coupling. The execute phase fans out parallel Sonnet sub-agents — one per batch, with the relevant rule named in its prompt — so per-agent context stays fresh and drift is bounded. The skill does not commit; review the diff, then `/commit`.

## Mode

- **`/refactor-file-sizes`** (no args) — whole-tree sweep.
- **`/refactor-file-sizes <path>`** — scope to a directory.

## Phase 1 — Audit

1. **Resolve `check-file-sizes.ps1`.** If `.claude/scripts/check-file-sizes.ps1` exists, run `pwsh -NoProfile -File ".claude/scripts/check-file-sizes.ps1"`; else `pwsh -NoProfile -File "$HOME/.claude/scripts/check-file-sizes.ps1"`. Per `meta-project-local-skill-copies`, project copies are deliberate forks that may carry a customized extension list.
2. Run it (no args: no params; path arg: `-Path <dir>`). Parse the JSON. `-NoProfile` keeps a user profile from polluting the output.
3. **Drop** `justified` entries (SIZE-EXEMPT) and `soft` entries — only hard-cap violators (>800 lines) are in scope.
4. **Coupling detection.** For each pair of violators, `Grep` the basename (no extension) of one in the other's content. If matched, mark them coupled. Coupled violators group into one batch; standalone violators are their own batch. This grep is loud and cheap — false positives are fine, over-grouping is harmless, under-grouping risks broken consumers.
5. Report: `N violators in M batches`.

## Phase 2 — Scope decision

If `M > 8`, ask via `AskUserQuestion`: "Found M batches. How many to address now?" with options like "All", "Top 5 by size", "Top 3", "Let's discuss." Otherwise proceed with all batches.

## Decomposition strategy — choose per batch

**Decide this first:** before splitting, pick *how* to split by looking at the file's **entrypoints** (who imports it). This determines the shape of the result.

- **Default: true split (redistribute references).** Break into sub-modules and update each consumer to import the specific one it needs. No aggregator left behind. Cleaner dependency graph, no wiring glue. **Prefer this.**
- **Facade/barrel only when fan-in is high.** If many consumers reach the file through one stable surface and rewriting those imports is large churn, keep the original path as a thin re-export over the new sub-files.
- **Determiner:** few consumers, or consumers referencing disjoint subsets → true split. Many consumers through one broad surface → facade. When torn, lean true split — the facade's wiring is a bug surface (below).

### Facade wiring is a bug surface

If a facade splits a module whose pieces call *each other*, every internal cross-sub-module reference needs an explicit injector wired in the orchestrator after load — not a direct import. A dropped injection compiles and boots fine, then throws only when the stitched path first runs. After any facade split, grep the moved function's call sites for cross-module refs, confirm each has an injector plus orchestrator wiring, and **exercise each stitched runtime path — not just app boot.**

## Phase 3 — Parallel sub-agent fan-out

For each batch in parallel:

1. **Determine languages** from the batch's file extensions, and map them to the project's own split-pattern rules in `.claude/rules/` — read them at runtime rather than assuming a stack. Sub-agent sessions don't auto-load project rules, so name the rule paths explicitly in the prompt.
2. **Spawn a Sonnet agent** (`model: "sonnet"` per `wf-agents-on-sonnet`) whose prompt:
   - Lists the batch files + line counts + coupling notes.
   - Names the rule file(s) to read **first**, before any edits.
   - States the **Decomposition strategy** above, including the facade injector requirement and which runtime paths must be exercised.
   - States project conventions (build-file ordering, public-surface preservation) — do not modify files outside the batch unless a consumer breaks, and then list it.
   - **Redistributing references across files is a mechanical multi-file rewrite**, so `wf-blanket-rename-safety` applies in full — exclude vendor and generated paths, don't clobber language built-ins, scope any doubling-collapse narrowly, and verify the write actually landed. Cite that rule rather than restating its bullets.
   - **DO NOT run the build** — parallel agents would fight build outputs. Defer to Phase 4.
   - **DO NOT commit.** Leave changes unstaged.
   - Return: file list with new line counts, grouping rationale (one sentence per new file), consumer files touched and why, and any *new* gotchas not already covered by the named rules.

## Phase 3.5 — A split must clear the cap, not relocate it

Before treating a split as done, verify each *extracted* file also clears the cap — not just the shrunken original. A split can drop the original below the threshold while leaving a new file above it, and that file is easy to overlook because the headline number reads like success. If an extracted file is still oversized, split it again or justify a `SIZE-EXEMPT` marker. Recount with the script, not by hand.

## Phase 4 — Consolidated build verify

Invoke `/build` once all sub-agents finish. If errors, list them by file; don't auto-retry — surface to the user. `/build` no-ops gracefully in no-build repos. Per `wf-check-the-artifact-not-the-self-report`, read the diff rather than trusting the agents' summaries.

## Phase 5 — Rule capture

Collect "new gotchas" reported by sub-agents. For each distinct pattern seen twice or more (or once on a high-confidence call), draft candidate-rule **content** suitable for `/rule-candidate`. Don't auto-invoke it — a single size-refactor run surfaces many false positives, so surface the proposals in the report and let the user triage.

## Phase 6 — Report

```text
Refactor File Sizes — N batches processed

Splits:
  - <batch summary, 1 line each>

Build: <PASS / FAIL — N errors>

Candidate rule proposals (from this run's observations):
  - <slug> — <one-line directive>

Next: /commit to land, or revert via `git checkout .` if anything looks off.
```

## Notes

- SIZE-EXEMPT files are skipped entirely; the script handles this. To exempt a file, add `// SIZE-EXEMPT: <reason>` in its first 10 lines.
- Path-scoped project rules load in the main session when matching files are read, but **not** in sub-agent sessions — so the agent prompt must name the rule path explicitly.
- Drift protection comes from each sub-agent starting fresh with the rule in its prompt; the skill itself doesn't need to restate rules between iterations.
