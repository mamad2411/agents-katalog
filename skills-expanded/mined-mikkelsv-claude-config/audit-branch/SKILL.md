---
name: audit-branch
description: "Branch-level audit across architecture, code, docs, tests, file-sizes, and comments. Use whenever the user wants to audit or review a whole branch, says \"review everything I've changed\", or asks \"is this branch ready to merge?\". Phase 3a runs all 6 sub-skills in parallel (audits + refactors). Phase 3b conditionally runs refactor-file-sizes if 3a flagged cap violations. Mechanical findings inline; judgment routes to /resolve-audit-findings. Self-paces 1-3 passes, then closes with one /verify run (Phase 8) — the skill's only suite run."
---

# Audit Branch

Branch-level review combining architecture audit + refactor sweeps across code, docs, tests, file-sizes, and comments. Spawns up to 6 parallel sonnet sub-agents in Phase 3a; each applies its own mechanical findings inline and returns judgment findings in a structured note. Orchestrator synthesizes deferred findings into one report and hands disposition to `/resolve-audit-findings`. After inline edits land, verifies the build.

**Multi-pass — decided mid-stride.** Always runs at least 1 pass. After each pass, decide whether another is warranted based on what the pass actually surfaced — not the diff size upfront. Re-pass triggers (any one is enough):

- Verdict was **Needs work** or **Rethink**
- 5+ findings landed (applied or deferred) across the sub-agents
- A single sub-agent reported a structural finding that touched files outside its original scope (e.g. refactor-code applied changes that may have invalidated refactor-tests' assertions)
- **Phase 3b ran at all** — the next pass re-audits the post-split structure

Stop conditions:

- Verdict **Sound** with no deferred findings → done
- The latest pass surfaced nothing new (verdict OK, < 5 minor findings) → done
- Phase 6 build failed → stop and surface the break, don't compound it
- Hard cap at **3 passes** regardless

Phase 7 (rule candidates) and Phase 8 (`/verify`) both run once after the final pass — not per pass. Phase 7 pools candidates from all passes.

## Phase 1 — Scope

Capture the `main..HEAD` diff scope (merge-base, even with a dirty tree), using the project copy if it exists:

```bash
pwsh -NoProfile -File ".claude/scripts/git-diff-scope.ps1" -Scope branch
pwsh -NoProfile -File "$HOME/.claude/scripts/git-diff-scope.ps1" -Scope branch
```

Abort if `MODE: none`. Pass the captured scope to every sub-agent so each skips its own scope-detection step.

## Phase 2 — Resolve Sub-Skills

Sub-skills: `audit-architecture`, `refactor-code`, `refactor-docs`, `refactor-tests`, `audit-file-sizes`, `refactor-comments`, `refactor-file-sizes`. All seven are global; prefer a project fork if one exists.

All sub-skills are always run — resolve each SKILL.md **from disk**, never from the session's invocable-skill list. `disable-model-invocation: true` hides every sub-skill except `refactor-code` from that list, but their files are on disk and this orchestration always spawns them.

## Phase 3a — Parallel Audit

Spawn all 6 sub-skills below in **parallel** (one message, multiple `Agent` calls) with `model: "sonnet"`:

- `audit-architecture` — read-only
- `refactor-code` — source files (writes)
- `refactor-docs` — `.md` files (writes)
- `refactor-tests` — test files (writes)
- `audit-file-sizes` — read-only scan
- `refactor-comments` — source-file comments (writes)

`refactor-code` and `refactor-comments` may both write source files; a collided `Edit` fails and the agent retries with a fresh read.

Each agent's prompt:

1. Prepend the captured scope so the agent skips its own scope-detection step.
2. Pass the sub-skill's SKILL.md as the procedure.
3. **Apply mechanical findings inline** per the sub-skill's inline tier — comment hygiene, stale references, typos, unused imports, trivial dead code, etc. Read-only agents (`audit-architecture`, `audit-file-sizes`) apply nothing; they report.
4. **Defer judgment findings** to the structured note. Do NOT call `AskUserQuestion` (orchestrator owns Phase 5).
5. Return: `## Applied inline` (counts + brief `file:line` list), `## Deferred` (file, description, recommended fix per finding), `## Rule candidates`.

## Phase 3b — Conditional File-Size Refactor

Run only if Phase 3a's `audit-file-sizes` reported cap violations. Splits would invalidate other agents' in-flight reads, so this can't live in 3a.

- `refactor-file-sizes` — applies splits inline.

If audit-file-sizes had no findings, skip 3b entirely. The agent merges its `## Applied inline` and `## Deferred` halves into the unified report.

## Phase 4 — Unified Report

Each agent returns two halves. Synthesize:

### Applied inline

One line per area summarizing what already landed in the diff (e.g. `refactor-code: 8 inline fixes (unused imports × 5, stale comments × 3)`).

### Deferred (judgment findings)

One section per area listing remaining findings:

- **Architecture** — audit-architecture findings (boundaries, overengineering, alternatives).
- **Code Quality** — refactor-code judgment findings (extractions, structural changes).
- **Documentation** — refactor-docs reorg / new-doc findings.
- **Tests** — refactor-tests coverage gaps + assertion debates.

### Overall verdict

**Sound** / **Minor issues** / **Needs work** / **Rethink** — synthesize across both halves. Be direct.

## Phase 5 — Disposition (deferred items only)

If every sub-agent returned `Sound` or all findings landed in `## Applied inline` — just report; no further action this pass.

Otherwise, **invoke `/resolve-audit-findings`** with the deferred set. The skill researches each finding, applies inline when the solution is obviously better, and defers substantial findings to `plans/post-audit-{slug}.md`. Slug = current branch name (sans `implement/` prefix) or a short feature name. Surface its report (applied / deferred / skipped counts + paths) as part of this pass's output.

No `AskUserQuestion` prompt here — `/resolve-audit-findings` owns the apply/defer decision per finding. The user reviews the diff before committing.

## Phase 6 — Build Verify

After inline fixes have landed (whether from agents in Phase 3 or orchestrator in Phase 5), invoke `/build`. Report if the build broke — likely an agent edit that crossed from comments into code. No-op in no-build repos.

## Phase 7 — Rule Candidates

Pool the `## Rule candidates` blocks from all sub-agents. Log each qualifying candidate via `/rule-candidate` and append the standard "Rule candidates added" footer (`wf-surface-rule-candidates`). Skip if nothing qualifies — don't fabricate.

## Phase 7.5 — Was this branch already merged?

Establish merged-ness by content, not by `git branch --no-merged` / `git cherry` — a squash- or rebase-merged branch reads as unmerged forever.

Grep `main` for a signature symbol the branch introduced (a new function, type, or rule filename). Present on `main` → the content shipped, whatever the commit graph says. Absent → genuinely unmerged. `git fetch` first — a stale local `main` gives the same false reading.

## Phase 8 — Verify

Invoke `/verify` once after the final pass; pass the plan path when called from `/implement`, else `none`. Not a re-pass trigger.
