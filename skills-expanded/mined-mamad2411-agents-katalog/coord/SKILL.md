---
name: coord
description: Claims board for parallel Claude sessions on one repo. Use before starting a roadmap item, PR or release another session might own, or when a command is refused with "held by another live session".
---

# coord

Each session on this box sees one board per GitHub repo. A claim is a key, such as
`Z0`, `branch:feat/x` or `release`, held by one session until that session ends,
releases it, or goes silent for 3 hours.

```bash
C=~/.claude/skills/coord/bin/coord.mjs
node $C list                                  # this repo's board; --all-repos for every repo
node $C claim Z0 --note "token eval rerun"    # exit 2: another live session holds it
node $C release Z0                            # or --all; --force frees someone else's
```

The mod does the rest without being asked:
- The first prompt carries the board for the session's repo.
- Creating a branch, pushing, tagging `v*`, `gh release create`, `npm version` and
  `npm publish` claim the branch or `release`. If another live session holds it, the
  Bash call is refused with the owner's session, folder and note.
- `gh pr merge` is checked against the PR's head branch.
- A `release` claim lapses after 2 hours by itself.

When refused: run ListAgents, find the owner by its folder, and SendMessage it. Do not
`--force` a claim whose owner is active unless Keith says so.

Limits: claims live in `~/.claude/coord-state/` on this box only. Work on the other box
shows up through `~/.claude/scripts/inflight.sh <repo>` and open PRs.
