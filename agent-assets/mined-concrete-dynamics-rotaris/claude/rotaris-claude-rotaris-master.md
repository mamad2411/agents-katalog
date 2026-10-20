# CLAUDE.md

Before touching code, read
[AGENTS.md § Workflow](AGENTS.md#workflow--worktree-merge): it
decides whether the work belongs in a worktree, on a branch in the main
checkout, or straight on `master`, and it sets the order — **fast gate, merge
into `master` unasked**. Nothing there waits for a human.

## Worktrees in Claude Code sessions

AGENTS.md makes a worktree the default workspace for a feature. Claude Code owns
`.claude/worktrees/` and reaches it through session tools; the other harnesses
have their own areas and never write into this one.

- **Ask for your base first.** `uv run python devtools/milestone.py branch-for
  SWR-<n>` prints `master` or the milestone branch this requirement's work
  belongs on. It decides which of the two entry forms below applies, and it is
  the merge target in AGENTS.md § 4.
- **Enter (base `master`)** with `EnterWorktree`, passing an explicit `name` in
  branch form (`feat/swr-2608-verifier-visibility`) — never the generated random
  one, since the branch follows from the name. It branches off `origin/master`,
  creates `.claude/worktrees/<name>`, and moves the session there.
- **Enter (base a milestone branch)** by cutting the worktree yourself and
  entering it by `path`. `EnterWorktree` takes no base ref — its base comes from
  the `worktree.baseRef` setting, which is unset here and so always means
  `origin/master`. Passing `name` would silently branch off the wrong base:

  ```bash
  git fetch origin milestone/m1-event-store
  git worktree add .claude/worktrees/feat/swr-2901-event-store \
      -b feat/swr-2901-event-store origin/milestone/m1-event-store
  ```

  then `EnterWorktree` with `path: .claude/worktrees/feat/swr-2901-event-store`.
- **Then** run `uv sync --all-packages` once — AGENTS.md § 1 says why that
  step is what makes a worktree trustworthy.
- **Leave** with `ExitWorktree` action `keep`, once the branch is committed and
  your base is merged into it. Never `remove`: it deletes the branch, and at that
  point the merge has not happened yet. (A worktree entered by `path` is never
  removed by `ExitWorktree` anyway — `keep` is the only correct action for it.)
- **Merge into your base.** `ExitWorktree` puts the session back in the main
  checkout; that tree is on `master`, so it is where AGENTS.md § 4's merge runs
  when your base *is* `master`. When your base is a milestone branch, merge in
  that branch's own integration worktree instead — the main checkout must never
  leave `master`, or a second tree can grab it.
- **Only then** clean up: `git branch -d <branch>` and
  `git worktree remove .claude/worktrees/<name>`.
- **Background `Agent` calls** take `isolation: "worktree"` instead; they get
  their own tree and cannot use the session tools.
- Not every session can switch directory (a hook-driven or non-interactive run).
  Those fall back to the plain `git worktree add .tmp_wt/<name>` form in
  AGENTS.md § 1.