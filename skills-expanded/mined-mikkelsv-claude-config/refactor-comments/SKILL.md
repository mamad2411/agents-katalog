---
name: refactor-comments
description: "Sweep code comments against the arch-docs-over-inline rubric — mechanical inline edits via parallel Sonnet agents in non-overlapping file partitions, build-verified after; supports --dry-run for review-only. Use whenever the user wants comment cleanup or hygiene, says comments are stale/noisy/redundant, or as part of a branch audit."
disable-model-invocation: true
---

# Refactor Comments

Sweep source files for verbose, stale, or low-density comments per `arch-docs-over-inline` (rubric) and `cq-comments-track-code` (protection list). Both rules auto-load; this skill orchestrates the sweep. Agents edit comments only; build verifies after. The skill does not commit — review the diff first, then `/commit`.

**Orchestrator-only** — it must spawn the partition sub-agents, never run the sweep inline; `disable-model-invocation` reflects that.

## Mode

- **`/refactor-comments`** (no args) — whole-codebase sweep. 4 Sonnet agents in parallel, two rounds.
- **`/refactor-comments <path>`** — scoped sweep. 1–2 Sonnet agents, one or two rounds based on scope size.
- **`/refactor-comments --dry-run`** — report-only. Same partitions and agents, but agents return structured findings instead of editing. Use for the inaugural run; switch to default once you trust the output.

## Partitions (non-overlapping; no two agents touch the same file)

Derive them at runtime: glob the project's top-level source directories and group them into 2–6 roughly balanced partitions. **They must not overlap** — two agents editing one file will clobber each other. If `.claude/skill-config/refactor-comments.md` names a partition table, use it instead of deriving; a curated split usually balances better than a mechanical one.

Excluded everywhere: `bin/`, `obj/`, `node_modules/`, generated CSS and build output, and files whose first 10 lines contain `SIZE-EXEMPT:` (intentionally large; defer comment hygiene to their own audit).

## Steps

1. **Size the problem first.** Run `pwsh -NoProfile -File "$HOME/.claude/scripts/audit-comment-blocks.ps1" -Path <scope>` (or `pwsh -NoProfile -File ".claude/scripts/audit-comment-blocks.ps1" -Path <scope>` if that project copy exists). It returns `{findings:[{path,startLine,lineCount}], totalScanned}` — runs of consecutive comment-only lines, sorted longest first. This is **quantify-only**: a long run isn't automatically wrong, since `arch-docs-over-inline` is a qualitative rubric. Use it to aim the sweep at the worst files and to have a before/after number. A `totalScanned` of 0 means the scope resolved to nothing — treat that as a bug, not a clean result.

   Also run a plan-reference count if the project has a checker (e.g. `.claude/scripts/check-plan-citations.ps1`, emitting `{paths:{dead,live},labels,deadCount,liveCount,labelCount}`). Feed its file list to the partition agents as concrete targets — this class is mechanical to find and easy to miss by eye.
2. **Determine scope + partition.** Path mode narrows to that path; no-args uses the partitions above. For `--dry-run`, partition strategy is identical.
3. **Spawn Sonnet agents in parallel** (one per partition), `model: "sonnet"` per `wf-agents-on-sonnet`. Each agent's prompt must include:
   - **Rubric** — read `arch-docs-over-inline` for the 5 practices (link don't inline, why-only, name identifiers as greppable anchors, invariants as checkable claims, no history prose).
   - **Protection list** — read `cq-comments-track-code`, plus any project overlay in the project's own `.claude/rules/`. Load-bearing comments must NOT be cut. Sub-agents don't auto-load project rules, so name the rule paths explicitly in the prompt.
   - **Action only when unambiguous.** **CUT**: WHAT-narration, signature paraphrase, migration history ("Phase 3 introduced…", "Stage N retires…"), typos in comments, PR/issue references, and every plan reference — a `plans/*.md` path or a plan label like `Task 3` / `Defect B` (see "Plan references are always a finding" below; keep the fact, cut the pointer). **SLIM**: load-bearing line buried in restatement (keep the why, cut the rest). **KEEP**: protection list + invariants + cross-file links + workarounds-with-condition.
   - **Stay strictly in your partition** — don't read or edit files outside it.
   - **Comments only** — never edit code. If a "comment" looks like commented-out logic, leave it.
   - **Return a one-paragraph summary**: "Cut N comments, slimmed M, kept K; flagged X borderline (with brief `file:line` list)."
   - For `--dry-run`: return structured `file:line | verdict (CUT/SLIM/KEEP) | proposed | rationale` instead of editing.
4. **(Default) Round 2** — re-spawn the same agents on the same partitions. Same prompt; LLM non-determinism alone surfaces more candidates, and Round 2 sees Round 1's cleaned state. Skip on `--dry-run`.
5. **Build verify** — invoke `/build`. A break signals an agent slipped from comments into code; report it and stop before commit. `/build` no-ops gracefully in no-build repos.
6. **Report** — collate agent summaries + totals across rounds. Per `wf-check-the-artifact-not-the-self-report`, read the diff before trusting those summaries: confirm the touched-file set stayed inside each partition and that no code changed.

## Plan references are always a finding

A comment must not cite a `plans/*.md` path, nor a plan's internal labels — `Task 3`, `Phase 2c`, `Defect B`, `P2 Task 6`, "the plan's Decisions", a post-audit finding number. Plans are deleted when their feature ships, so every such reference has a scheduled expiry. Cut it and keep the fact, or repoint to `docs/<file>.md "<section>"` after verifying that section exists.

This holds even for a plan only recoverable from git: a reader cannot tell a git-only pointer from a live one. Provenance belongs in the commit message, which is permanent and is where `git log` already looks.

When a **`docs/*.md`** citation breaks, run `git log --oneline -- <deleted-path>`. If that content moved into another named document, **repoint** rather than cut — dropping it loses a live cross-reference.

**Never regex-sweep plan labels.** `Task` is a BCL type (`async Task`, `Task.Run`) and `phase` is a domain word in some codebases (`zero-phase`, `minimum-phase`); a mechanical substitution corrupts both, per `wf-blanket-rename-safety`. Judge per site. Expect false positives from any detector: `docs/x.md "Phase 4b — provenance" (Task 4)` has a legitimate section name and one real violation on the same line.

## Notes

- Path scope is your lever for risk control — start narrow, expand once confidence is established. `--dry-run` on a single partition is the safest first validation.
- If agents repeatedly cut something you wanted kept, add a `cq-comments-track-code` clause naming the pattern rather than fighting it per-file.
