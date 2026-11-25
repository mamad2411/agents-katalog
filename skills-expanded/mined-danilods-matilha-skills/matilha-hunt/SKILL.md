---
name: matilha-hunt
description: Use when user is ready to dispatch a wave's subprojects — creates git worktrees and kickoff.md per SP, writes wave-NN-status.md, prints dispatch commands.
category: matilha
version: "1.0.0"
optional_companions: ["superpowers:executing-plans"]
---

## When this fires

Plan exists (`docs/matilha/plans/<slug>-plan.md`) and user wants to enter Phase 40 execution. Skill sets up worktrees and wave-status bookkeeping; AI or user dispatches per-worktree sessions.

## Preconditions

- `project-status.md` shows `current_phase ≥ 30`.
- Plan file exists.
- Working tree clean.
- Disjunction validated (intra-wave SPs touch disjoint files).

## Execution Workflow

1. Pre-flight (Swiss Cheese): resolve plan path, read project-status `current_phase ≥ 30`, verify clean tree via Bash `git status --porcelain`.
2. Parse plan markdown (soft-strict: em-dash / colon / single-hyphen SP headings).
3. Pick target wave (default wave 1, or `--wave N`).
4. Validate disjunction (SPs in same wave must touch disjoint `Touches` lists); on violation throw 5-rule error unless `--allow-overlap`.
5. Detect companions (superpowers via `project-status.md:companion_skills.superpowers == "installed"`).
6. Idempotency guard: if `docs/matilha/waves/wave-NN-status.md` exists and not `--force`, halt with recovery options.
7. If `--dry-run`: emit preview and exit.
8. For each SP: create branch `wave-NN-sp-<slug>` via Bash `git branch`, worktree `../<project>-sp-<slug>` via Bash `git worktree add`, render kickoff.md + SP-DONE.md from templates (fetched via matilha pull from matilha-skills) via Write, write wave-status.md entry.
9. Update .gitignore to include `kickoff.md` via Edit.
10. Emit dispatch commands (one per worktree).

## Rules: Do

- Validate disjunction.
- Gitignore kickoff.md.
- Write wave-status before dispatch (bookkeeping survives partial failures).
- Follow merge_order strictly in documentation.

## Rules: Don't

- Execute the SPs yourself (plugin only creates worktrees).
- Force-merge (no `--no-verify`).
- Modify `project-status.md:current_phase`.

## Expected Behavior

N worktrees + N kickoff.md + N SP-DONE.md + 1 wave-status.md. User opens N terminals and pastes the dispatch commands.

## Quality Gates

- `wave-NN-status.md` exists and conforms to `waveSchema`.
- Every SP entry has `branch`, `worktree`, `status`.
- `.gitignore` contains `kickoff.md`.
- `current_phase ≥ 30` in project-status.md.

## Companion Integration

- If **superpowers:executing-plans** is available: kickoff.md recommends it as the preferred task-control engine. Matilha provides the harness (worktree isolation, disjunction gates, wave-status tracking); superpowers drives execution with TDD + review checkpoints.
- Otherwise: kickoff.md instructs the AI to execute with TDD + atomic commits standalone.

## Output Artifacts

- N git branches `wave-NN-sp-<slug>`.
- N worktrees at `../<project>-sp-<slug>/`.
- N `kickoff.md` files in worktrees.
- N `SP-DONE.md` templates in worktrees.
- `docs/matilha/waves/wave-NN-status.md`.
- Updated `.gitignore`.

## Example Constraint Language

- Use "must" for: disjunction validated; wave-status written before any dispatch.
- Use "should" for: run `--dry-run` first when new to the plan.
- Use "may" for: `--allow-overlap` only with understood risk.

## Troubleshooting

- **"branch already exists"**: Use `--force` (destructive; logs recovery first).
- **"disjunction violated"**: Edit plan to move overlap to a later wave, or `--allow-overlap`.
- **"current_phase < 30"**: Finish phases 10/20/30 first.

## CLI shortcut (optional)

> If matilha CLI is installed (`matilha --version` succeeds), you can run
> `matilha hunt <slug>` to execute this deterministically. The plugin path
> above works without any CLI installation.
