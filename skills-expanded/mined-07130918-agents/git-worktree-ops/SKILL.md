---
name: git-worktree-ops
description: Git worktreeを安全に作成・確認・整理する。「新しいworktreeで作業」「別PRへ変更を混ぜない」「worktreeを切って」「merge後にworktreeとbranchを削除」と依頼されたときに使う。通常のbranch作成だけ、PR作成だけ、未コミット変更の移植だけには使わない。
argument-hint: "[create|status|cleanup] [branch-or-pr]"
allowed-tools: Read Glob Grep Bash(git status *) Bash(git branch *) Bash(git worktree *) Bash(git fetch *) Bash(git pull *) Bash(git rev-parse *) Bash(git symbolic-ref *) Bash(git merge-base *) Bash(git log *) Bash(git show-ref *) Bash(git push *) Bash(gh pr view *) Bash(test *) Bash(mkdir *)
---

# git-worktree-ops

この skill の詳細手順は `~/.agents/references/git-worktree-ops.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
