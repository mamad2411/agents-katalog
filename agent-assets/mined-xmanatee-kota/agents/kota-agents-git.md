# Git Module

This directory owns the `git` capability pack — version control operations with safety guardrails.

- The single `git` tool handles status, diff, log, show, add, commit, branch, and push.
- Each operation parses a strict argument grammar before invoking Git. Read
  operations reject file-writing and execution-capable flags, and local paths
  used by any operation must resolve inside the active scope, including
  through symlinks.
- Non-lease force-pushes to `main`/`master` are blocked by parsed destination,
  including command-line and configured refspecs, configured push remotes,
  upstream defaults, and cross-branch pushes. Unsupported or abbreviated long
  push options fail closed. Pushes are external-network writes; forced,
  config-selected, and remote-destructive forms are dangerous.
  Deletion of protected local branches is blocked. Large diffs are auto-truncated.
- Tools and tests live here; no tool logic belongs in `src/core/tools/`.
- Invocation effects distinguish local reads, local mutations and pushes.
  Git subprocesses disable optional locks and diff's automatic index refresh;
  required writes still execute for authorized mutation operations.
  Mutation destinations remain unknown for every operation: configured helpers
  such as fsmonitor and clean filters can write during reads, and pushes can
  update local refs/configuration. Bounded filesystem policies therefore deny
  Git calls; optional-lock suppression alone does not establish mutation freedom.
## Boundaries

- Does not own GitHub API operations (those belong in `github/`).
- Does not own file-read or shell execution (those belong in `filesystem/` and `execution/`).
