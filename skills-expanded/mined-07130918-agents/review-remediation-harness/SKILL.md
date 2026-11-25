---
name: review-remediation-harness
description: |
  独立した最終レビューを含む修正・検証を、既存workflowと確認記録につないで自律的に進める。
  Use when: user explicitly asks for a review-remediation harness, reviewer/implementer separation across a fix workflow, or a review/fix/verify/re-review loop with an independent final reviewer.
  For Issue URLs, issue-to-pr owns intake and initial implementation before handing over the candidate. Does not trigger on: review-only requests, PR creation only, ordinary Issue implementation without a Harness request, or evaluation/updates of this Harness itself.
---

# review-remediation-harness

この skill の詳細手順は `~/.agents/references/review-remediation-harness.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中のCLIに対応する手順・チェックリスト・注意事項に従ってください。
