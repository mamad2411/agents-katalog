---
name: git-path-run
description: 'Move or remove project paths while preserving Git history and local work, via the git-aware helper. Use for authorized file or directory relocation where tracked and untracked work coexist. RU: перенос файлов, переместить, удалить путь.'
---

# Git-aware moves and removal

Use for an authorized path move or removal when tracked and untracked work may coexist. Inspect the actual source, destination, repository status and ownership first. Git infers renames by comparing content; a plain filesystem move does not inherently destroy history, but it leaves staging to a separate operation. This helper uses `git mv` or `git rm` for tracked paths and filesystem operations for untracked paths, so tracked operations change the index. It does not commit.

Resolve the plugin root through the current runtime's supported interface:

```bash
"$PLUGIN_ROOT"/skills/git-path-run/git-path-run.sh <source> <destination>
"$PLUGIN_ROOT"/skills/git-path-run/git-path-run.sh --rm <explicit-file>
"$PLUGIN_ROOT"/skills/git-path-run/git-path-run.sh --rm --recursive <untracked-directory>
```

Examples of moves include `.agents/kanban/grooming/card.md` to `.agents/kanban/todo/card.md` when the board's own lifecycle rules authorize the transition. Prefer the board's canonical lifecycle helper when it maintains status, approval gates or allocation state.

The helper refuses an existing destination, overlapping removal paths, the current directory or an ancestor, and a tracked directory containing untracked, ignored or empty entries. Deleting an untracked directory requires the explicit `--recursive` flag. It validates every requested removal before starting; native Git safety checks still apply. These checks do not make a multi-path operation atomic or protect against concurrent writers. The implementation currently requires GNU `realpath` and `mv`; macOS/BSD compatibility is unverified. Do not use it to delete anything without the user's applicable authorization, and do not bypass hooks or Git safety checks.

Afterward verify actual filesystem paths, staged and unstaged changes, and preserved unrelated work. Follow `git-repo-run` for any separately authorized commit.
