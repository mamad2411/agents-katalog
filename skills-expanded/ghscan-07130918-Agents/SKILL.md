---
name: session-retrospective
description: セッション完了後の振り返りを行い、AI CLI 設定に残すべき学びを分類する。長い実装・バグ調査・PR 後に、AGENTS.md、CLAUDE.md、skill、reference、次回タスクへの反映候補を整理し、ユーザーが明示した範囲だけ更新する。
argument-hint: current-session | branch | pr-number
allowed-tools: Read Write Edit Glob Grep Bash(git *) Bash(find *) Bash(wc *)
---

# session-retrospective

この skill の詳細手順は `~/.agents/references/session-retrospective.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
