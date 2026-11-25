---
name: commit-triage
description: Classify uncommitted changes into commit-ready, failure-archive, and ambiguous buckets, then produce clean grouped commits with no co-author attribution. Use when the user asks to commit, tidy up `git status`, prepare a PR, archive failed experiments to a `failure/` folder, separate research artifacts from code before a commit, or clean up a noisy working tree at the end of a session.
---

# Commit Triage

Use this skill at the end of a working session, or any time `git status` has become noisy, to produce **clean grouped commits** while archiving failed experiments and pausing on anything ambiguous.

This skill exists because committing after long research sessions is the single most common flashpoint for unwanted autonomous actions — stray Co-Authored-By tags, accidentally committed scratch directories, or failed experiments mixed into a feature commit. The triage step is the guardrail.

## Core rules (non-negotiable)

- **NEVER** add `Co-Authored-By: Claude` (or any co-author attribution) to commit messages, unless the user explicitly asks for it.
- **NEVER** use `git add .` or `git add -A`. Always stage named paths so nothing sneaks in.
- **NEVER** `git push` unless the user explicitly asked. Approval of the commit plan does not authorize push or PR creation; stop after commit verification unless that further action was explicitly requested and its applicable approval requirements are satisfied.
- **NEVER** delete files. Move failed experiments into `failure/` with `git mv` so they remain recoverable from git history.
- Pause and ask on anything that looks destructive, ambiguous, or unfamiliar (new top-level directories, renames, submodule changes, lock-file bumps, large generated artifacts).

## Inputs to confirm

Ask only for what is missing:
- target repository (default: current working directory)
- any stated preference for a single commit or multiple logical commits (otherwise propose grouping in step 3)
- any directories or patterns the user wants to always treat as failure or always skip (e.g. `write/`, `scratch/`, `_gen/`)

If the user just says "commit" without context, run the full triage workflow below. Do not shortcut to `git commit -am`.

## Workflow

### 1. Observe — collect the full state first

Run these in parallel, read-only:

```bash
git status                         # no -uall flag; large repos choke
git diff --stat                    # size of each modified path
git diff --stat --cached           # anything already staged
git log --oneline -5               # recent commit style
```

Do not stage or modify anything yet.

### 2. Classify — put every path into exactly one bucket

For each changed path, assign one of three buckets using `references/classification.md`:

- **COMMIT** — research-relevant, code, docs, or artifacts the user clearly wants preserved in history
- **FAILURE** — runs, logs, or outputs from experiments that did not work out and belong in `failure/`
- **ASK** — anything where the classification is not obvious (new top-level dirs, `write/`, `scratch/`, large artifacts, files the user did not mention)

Default stance when in doubt: **ASK**. It is cheap to confirm and expensive to commit noise or delete work.

### 3. Present — show the categorization before touching anything

Produce a compact table grouped by bucket, with a one-line reason per path. Include every path's proposed classification, exact failure-move destinations and diagnosis-note paths, commit grouping, and draft commit messages in this initial approval presentation. Resolve any single-versus-multiple-commit choice here. Example path table:

```text
COMMIT
  src/model.py                     new activation-scale variant (matches current task)
  tests/test_model.py              new tests for above
  report.md                        updated results section

FAILURE
  outputs/run_2026-04-15_psi/      crashed at epoch 12 (OOM), no useful metrics

ASK
  write/                           new top-level dir, unclear if intended
  data/normalization_v3.bin        large binary, regenerated? to track or ignore?
```

Wait for explicit approval of the path classifications and complete plan before touching anything. If the user corrects a row or leaves a choice unresolved, revise the affected plan and obtain approval. Execute only the approved paths, moves, grouping, and messages in steps 4–6; ask again only if that plan changes, not merely because the next step begins.

### 4. Archive failures — move, do not delete

Create the approved dated slug under `failure/` and move only approved FAILURE paths with `git mv` to their approved destinations. See `references/failure-layout.md` for the directory convention and the short diagnosis note included in the approved plan.

```bash
mkdir -p failure/2026-04-18-oom-psi-run
git mv outputs/run_2026-04-15_psi failure/2026-04-18-oom-psi-run/
```

Write the approved `failure/<slug>/NOTES.md` summarizing *what was attempted*, *what failed*, and *what was learned* — enough so a later skim tells you whether to revisit.

### 5. Stage — named paths only, grouped logically

Stage only the paths and logical groupings approved in step 3 (including approved failure moves and notes). Always use named paths:

```bash
git add src/model.py tests/test_model.py
```

Do not introduce an automatic second grouping gate. If the grouping or path scope must change, present that change for approval before staging it.

### 6. Commit — use the approved messages

Follow the repo's existing commit style from `git log` when drafting messages for step 3. Commit only with the message approved for that grouping; a changed message requires renewed approval. Use a HEREDOC for multi-line bodies.

```bash
git commit -m "$(cat <<'EOF'
Short imperative subject under 70 chars

- bullet explaining the why
- bullet for any non-obvious choice
EOF
)"
```

**Do not** include `Co-Authored-By`, `Generated with Claude`, or any attribution. If the user's global config or project template adds it automatically, flag that to the user rather than silently leaving it in.

### 7. Verify — show the result, stop

Run `git status` and `git log --oneline -3` and show the output. For a commit-only request, stop here. Push or PR creation requires an explicit user request and any applicable approval; never infer that authority from approval of the commit plan.

## Edge cases

- **Pre-commit hook fails**: the commit did not happen. Fix the underlying issue, re-stage, create a **new** commit. Never use `--amend` to sidestep the hook, and never pass `--no-verify`.
- **Merge conflicts in the working tree**: abort the triage, surface the conflict, and ask the user how to proceed.
- **Detached HEAD or rebase in progress**: do not commit. Report the state and wait.
- **Submodule changes**: always ASK. Submodule bumps are almost never casual.
- **Very large diffs** (hundreds of files): triage by directory rather than per-path, and propose the grouping before enumerating.

## Resources

- `references/classification.md` — heuristics for deciding COMMIT vs FAILURE vs ASK.
- `references/failure-layout.md` — `failure/<slug>/` convention and the `NOTES.md` template.
- Pairs naturally with `research-log` for recording the decision behind a failure, and with `research-report` when the commit closes a reportable experiment.
