---
name: asana-workflow
description: Asana MCPを使ったタスク取得・更新・進捗管理のワークフロー。ブランチ名やPR番号からAsanaタスクを引き当て、実装完了後にコメント・ステータスを更新するパターン。「Asanaのタスク」「このチケット」「Asanaで確認」といった文脈で参照する。mcp__asanaとmcp__claude_ai_Asanaの2種類があり、どちらも同じAsana APIを叩く。
---

# asana-workflow

この skill の詳細手順は `~/.agents/references/asana-workflow.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
