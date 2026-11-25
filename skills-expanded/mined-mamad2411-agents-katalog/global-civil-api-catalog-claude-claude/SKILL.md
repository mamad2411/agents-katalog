# ClaudeOS v9.0 — プロジェクト設定（要点版 / スタブ）

> 📌 本ファイルの全文ポリシーは、毎ターン自動ロードされる固定コンテキストを軽量化するため退避しました。
>
> - 🗂️ v9.0 全文: `.claude/claudeos/policy/claudeos-v9.0-full.md`
> - 🗂️ **運用の正本（要点）: ルート `CLAUDE.md`（要点版）**
> - 🗂️ カーネル文書: `.claude/claudeos/`（`system/` `loops/` `ci/` `executive/` `evolution/` ...）

## 📌 方針

本プロジェクトの運用方針は **ルート `CLAUDE.md`（要点版）を正本** とする。
以下はルート要点版に集約済み。詳細手順が必要なときだけ全文版・カーネル文書を参照する。

- 🈁 言語: 日本語（コード内コメントは英語可）
- 🎨 出力: アイコン多用（ルート `CLAUDE.md` §1 準拠）
- 🎯 Goal 駆動 + Supervisor/CTO 全権委任（§2）
- 🔒 Human Final Decision Boundary（§3・厳守）
- ✅ STABLE 判定 / Release Guard（§4）
- ⏱ 5 時間セッション制約・Token 管理・終了処理（§5）
- 🔧 Git/GitHub・Codex/CodeRabbit レビュー（§6）
- 👥 Agent Teams・`/workflows`（§10）

> 🧭 矛盾時の優先順位: **現在のユーザー指示 > ルート要点版 > 全文版 > モデル推測**。
