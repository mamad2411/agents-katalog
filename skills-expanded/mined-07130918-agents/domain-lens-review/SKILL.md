---
name: domain-lens-review
description: ドメイン固有の観点リストを指定してコードを多角レビューする読み取り専用 workflow。「〜の観点でレビュー」「infra/security/test の観点で多角レビュー」「観点を列挙してレビュー」「N観点で」など、観点リストが明示されたレビュー依頼で使う。観点指定がない汎用レビューは pr-risk-reviewer agent / principle-of-programming-reviewer skill を使う。
argument-hint: "[観点1,観点2,... (省略時は diff から提案)]"
allowed-tools: Read Glob Grep Bash(git diff *) Bash(git log *) Bash(git status *) Bash(git ls-files *) Bash(find *) Bash(wc *) mcp__context7__*
---

# domain-lens-review

この skill の詳細手順は `~/.agents/references/domain-lens-review.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
