---
name: claude-review
description: Codex から Claude Code CLI を介して現在の作業ブランチを厳格にコードレビューする。コードの正確性・ベストプラクティス・セキュリティ観点で分析する。`/claude-review` または `/clr` で呼び出される。
argument-hint: [base-branch]
allowed-tools: Bash(git *), Bash(command -v claude), Bash(claude *), Bash(mktemp *), Bash(cat *), Bash(printf *), Bash(wc *), Bash(rm *)
---

# claude-review

この skill の詳細手順は `~/.agents/references/claude-review.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
