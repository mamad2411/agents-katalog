---
name: address-claude-pr-comments
description: GitHub PR番号またはURLを受け取り、Claudeの未解決レビューコメントを確認して対応する。修正が必要なら実装・検証・push後に返信してresolveし、不要なら理由を返信してresolveする。「Claudeレビュー対応」「claudeのコメント対応」「PRコメントをresolve」と言われたときに使う。
argument-hint: <pr-number-or-url>
allowed-tools: Read Edit Glob Grep Bash(git *) Bash(gh *) Bash(npm *) Bash(make *) Bash(uv *) Bash(rg *) Bash(jq *) Bash(sed *) Bash(cat *)
---

# address-claude-pr-comments

この skill の詳細手順は `~/.agents/references/address-claude-pr-comments.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
