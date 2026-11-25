---
name: issue-to-pr
description: |
  GitHub issue を起点に、issue 精読から実装計画・実装・品質ゲート・レビュー・PR 提出までを一気通貫で進める。
  明確なブロッカーがない限り、計画提示やブランチ作成だけで止めず PR 作成まで継続する。
  Use when: user gives an issue URL/number with a request like "このissueに対応して", "issueをよく読み実装して", "issueから実装計画を立ててPRまで", or runs /issue-to-pr.
  Does not trigger on: a bare bug report or question without an issue reference (defer to bug-investigation).
  Accepts args: issue number or URL.
---

# issue-to-pr

この skill の詳細手順は `~/.agents/references/issue-to-pr.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
