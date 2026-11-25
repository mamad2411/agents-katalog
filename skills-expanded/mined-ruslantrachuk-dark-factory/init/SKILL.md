---
name: init
description: Set up the dark-factory solo kit in the current project — the operating contract in CLAUDE.md, scripts/merge-feature.sh, .claude/fences.env (solo), a minimal pre-push test gate and the plugin entry in .claude/settings.json. Dry run first, never overwrites, writes only after the human's yes. Invoked by the human as /dark-factory:init.
argument-hint: "[test command, e.g. 'python3 -m pytest -q']"
disable-model-invocation: true
---

# /dark-factory:init — the solo kit

The plugin's hooks (the guard, the quota guard, git-hook repair) are already running; this command opts the
project in and adds the few files a solo developer needs. The mechanics are one script,
`${CLAUDE_PLUGIN_ROOT}/scripts/init_kit.py`; this skill is the questions and the "yes".

## Rules

1. **Dry run first, then write.** Show the dry-run output to the human; write only after an explicit "yes".
2. **Never overwrite.** The script skips existing files, appends the CLAUDE.md block once, and adds only missing
   keys to `.claude/settings.json`. Show every SKIP to the human; do not "fix" a skipped file by hand.
3. **Nothing leaves the machine.** No commit, push or PR here — the human decides how the kit gets committed.

## Steps

1. Work out the answers, then confirm them with the human in one message:
   - **main branch** — the script detects it from `origin/HEAD`, else an existing `main` or `master`, else the current branch; when the dry run prints an `AMBIGUOUS` note, ask the human;
   - **merge strategy** — `merge` (default; squash breaks ancestry and branch cleanup), `squash` or `rebase`;
   - **test command** for the pre-push gate — the argument of this command if given; otherwise propose one from the
     project (`pyproject.toml`/`pytest.ini` → `python3 -m pytest -q`, `package.json` with a `test` script →
     `npm test`, `go.mod` → `go test ./...`, `Cargo.toml` → `cargo test`); none — leave it empty (the hook then
     only prints a hint);
   - **marketplace** collaborators are offered — the script copies how this machine added the dark-factory
     marketplace when that is GitHub; otherwise (a local folder means nothing to others) it writes the published
     repository `ruslantrachuk/dark-factory`. For a fork, ask for its GitHub `owner/repo` and pass
     `--marketplace-repo owner/repo`.
2. Dry run:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/init_kit.py" --main-branch <main> --merge-flag <merge|squash|rebase> [--test-cmd '<cmd>']
   ```
   Show the output and the CLAUDE.md block (`${CLAUDE_PLUGIN_ROOT}/templates/solo/CLAUDE.md`). Say that `FENCE_LEVEL=solo`
   fences only destructive things, and that `standard` and `team` exist (`.claude/fences.env` explains them).
   If the output has a `WARNING` that `core.hooksPath` points elsewhere, the pre-push test gate is not active: tell the
   human and offer to chain `.githooks/pre-push` from their existing hook (do not rewrite their hooks unasked).
3. After "yes": the same command with `--apply`.
4. Report what was written, then the next steps:
   - commit `.claude/fences.env`, `.claude/settings.json`, `.githooks/` and `scripts/merge-feature.sh` (with
     `CLAUDE.md`) soon: an untracked fence file can be removed by `git clean`/`git stash -u`, and the copy on the
     main branch is the floor the guard reads — once it is there, the level cannot be lowered without a merge;
   - commit the kit on a branch, give its PR a description with `## Done`, `## Decisions` and `## Open questions`
     (the script refuses without them), and merge it with
     `scripts/merge-feature.sh <branch> "Add the dark-factory solo kit"`, or the human pushes
     it to the main branch themselves (the guard denies the agent a push to the main branch);
   - turn on GitHub branch protection for the main branch (block force pushes, require a pull request) — the backstop
     a hook cannot be;
   - collaborators who open the project are offered the plugin through `.claude/settings.json`.

## Not this command

The full harness (beads queue, OpenSpec, CI tiers, test pyramid, skills) is the `base` template of this plugin,
installed with `/dark-factory:add base`; it builds on what this command wrote.
