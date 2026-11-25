---
name: create-pr
description: |
  このユーザーglobal構成のPR提出を一貫して扱う正本。現在branchの変更を品質gate後に意味のある単位でcommitし、pushして日本語のPRを作成する。
  Use when: user asks to commit and create a PR, push and open a pull request, submit current changes, create a PR, or run /create-pr.
  Does not trigger on: commit only without a PR, issue investigation or implementation (defer to issue-to-pr), or diff inspection only (defer to git-diff).
  Accepts args: none.
---

# create-pr

この skill の詳細手順は `~/.agents/references/create-pr.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
