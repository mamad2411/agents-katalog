---
name: memory-extract
description: 未処理セッションの要約から、長期的に有効な意味記憶だけを抽出して Vault に保存する。セッションから学習、記憶を抽出、memory extract、/memory-extract の依頼で使う。
---

# Memory Extract

セッション履歴を安定した意味記憶へ変換する専用ワークフロー。通常の記憶の読み書きは `shared-memory` を使う。

## 手順

1. `list_unextracted(limit=10)` で未処理セッションを取得し、各セッションの `id`、`user_id`、`project_id` を保持する
2. summary から、ユーザーの好み、環境・ツール設定、プロジェクトのルール・決定、繰り返すワークフロー、コミュニケーションの好みを抽出候補にする
3. 一時的な作業内容、セッション固有の事情、未検証の推測、既存記憶と重複する内容は候補から除外する
4. `search` / `get_context` で現行記憶との重複・矛盾を確認する
5. `list_tags` で既存タグを確認し、抽出候補にタグを付ける場合は同義タグを増やさず可能な限り再利用する
6. 保存する候補を `write_memory` に渡す。抽出では元セッションの `session_id` を必ず指定し、project 記憶は元の `project_id` と一致させる
7. すべての保存結果を確認した後、元の `session_id` で `mark_extracted` を呼ぶ。保存に失敗したセッションは処理済みにしない
8. `search` と `get_context` で保存結果を確認する

## 保存の分類

- `profile`: ユーザーの静的な好み・環境
- `feedback`: 協働や応答に関する確認済みの好み
- `reference`: プロジェクトの決定事項・参照情報

confidence は確認の確かさに合わせ、未検証の推測には付けない。抽出すべき内容がない場合も、確認後に `mark_extracted` を実行する。

## MCP が使えない場合

`memory/README.md` の同じ明示設定を確認したうえで、`list-unextracted` → `write-memory --session-id` → `mark-extracted --session-id` の順に CLI を使う。設定エラーや権限エラーを別 Vault で回避しない。部分失敗の調査は `memory` スキルへ委譲する。
