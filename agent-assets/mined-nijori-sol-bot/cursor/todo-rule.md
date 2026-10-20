---
description: 
globs: 
alwaysApply: true
---
1. フォルダ & ファイル構成

repo-root/
 └── .todo/
      ├──  backlog.mdc    # 未着手タスク (inbox)
      ├──  sprint.mdc     # 今スプリントの WIP/Done
      └──  archive.mdc    # 完了 3 ヵ月後にここへ移動

運用サイクル:
Backlog にインプット → 週次スクラムで Sprint へ選別 → 完了タスクは ~~打消し~~ にして 3 か月後 Archive へ。

重要★
作成するbotの要件は適宜C:\Users\nijor\Dev\SOL_bot\SOLUSDT_Algo_Strategy_Designを参照
またTodoの更新はC:\Users\nijor\Dev\SOL_bot\.todo\todo-format.mdも参照
git周りはC:\Users\nijor\Dev\SOL_bot\.github\workflowsを参照
将来的な開発はC:\Users\nijor\Dev\SOL_bot\plan.mdに記載あり

大重要★
以前大事故が起こりました。もう同じ事故を起こさないために。下記を守って下さい。
習慣/具体例
基本的に破壊的操作は必ずブランチで/git switch -c codemod/import-js　など
ツールは Dry-Run で	/ npx jscodeshift … --dry
コミット間隔を細かく / こまめに git add -p → git commit -m "logical unit"
自動化スクリプトを使う際は--dry-runモードやコミット前 hook と組み合わせると安心度が上がる

2. タスク行フォーマット

- [ ] TASK‑ID: <短いタイトル>  ← 1 行目は見出し
      - 📅 Due        : YYYY‑MM‑DD
      - 👤 Owner      : <GitHub ユーザー or @slack>
      - 🔗 Depends-on : TASK‑ID1, TASK‑ID2 ...
      - 🏷️  Label      : bug / feat / doc / infra / 研究
      - 🩺 Health     : ⏳ / ⚠️ / 🚑 / ✅
      - 📊 Progress   : 0% / 25% / 50% / 75% / 100%
      - ✎ Notes      : (自由メモ 120 字以内)


＞記号意味
フィールド例：TASK‑ID
説明例：DAT‑001
説明：3 文字カテゴリ + 3 桁通番

フィールド例：DAT‑001
説明例：⏳=WIP, ⚠️=遅延気味, 🚑=要救援, ✅=完了

＞チェックボックス [ ] / [x] は GitHub diff で完了判定をするため "小文字 x" を推奨。


3. カテゴリ接頭辞 一覧

略号/意味

DAT/データ収集・ETL

ALG/売買ロジック／バックテスト

OMS/発注・OMS 実装

INF/インフラ・CI/CD

DOC/ドキュメント

PERF/パフォーマンス最適化

SEC/セキュリティ関連

CICD/CI/CD関連

4. ライフサイクル・ルール
 1. **新規作成**: backlog.mdc に追加。Health = ⏳
 2. **スプリント移動**: 週次で優先タスクを sprint.mdc へコピー
 3. **状態更新**: コミット時に [ ]→[x] & Health✅
 4. **アーカイブ移行**: 
    - 完了タスクは3ヵ月経過で sprint.mdc から archive.mdc へ移動
    - 完了したがスキップまたは置き換えられたタスクも archive.mdc に移動し、Notes に置き換え理由や関連タスク（例: 「TST-012 に置き換えられました」）を明記
 5. **トレーサビリティの確保**:
    - タスクがマージや再編成される場合、元のタスクを削除する前に archive.mdc に移動
    - 関連タスクとの紐付けを Notes に明記（例: 「TST-012として再実装」「ALG-040に機能統合」など）
    - スプリントから直接削除せず、必ず archive.mdc へのトレース情報を残す
    - アーカイブするべき前スプリントのタスクをコメントアウトするような形で先頭に「.」を追加、これによりタスクID重複検出の対象から除外

5. サンプル sprint.mdc

## 🗓 2025‑W22 Sprint

- [ ] DAT‑001: 1h 足データ取り込みジョブ
      - 📅 Due        : 2025‑06‑03
      - 👤 Owner      : @koshi
      - 🔗 Depends-on : INF‑002
      - 🏷️  Label      : feat
      - 🩺 Health     : ⏳
      - 📊 Progress   : 25%
      - ✎ Notes      : Dagster or Airflow どちら使うか決める

- [x] INF‑002: S3 バケット権限設定
      - 📅 Due        : 2025‑05‑25
      - 👤 Owner      : @assistant
      - 🏷️  Label      : infra
      - 🩺 Health     : ✅
      - 📊 Progress   : 100%
      - ✎ Notes      : ServerSideEncryption = AES256

6. Git 運用 Tips

PR テンプレに Fixes TASK‑ID を必ず入れて紐付け。

PRタイトルに「XXX-000: 変更内容」の形式でタスクIDを含める。

GitHub Actionsによる自動化:
- PRマージ時にTodoタスクを自動的に完了([x])に更新
- Todoフォーマット検証で必須項目の漏れをチェック
- PRテンプレートでタスクIDを明示するよう強制

7. CI/CD連携

- PRマージ時のTodoタスク自動更新: PRタイトルまたは本文のタスクIDを識別し、対応するタスクを自動的に完了状態に更新
- Todoファイル形式チェック: ラベル、進捗、ヘルスステータスなどの必須フィールドが正しく設定されているか自動検証
- PRテンプレートとの連携: 「Fixes: XXX-000」形式でタスクIDを明示的に参照するよう促進

8. データ処理関連機能

MultiTimeframeDataFetcher: 複数時間足(1m, 15m, 1h, 1d)のデータを自動的に取得・保存
ParquetDataStore: 高効率なParquet形式でのデータ永続化と検索
スケジュール実行: node-cronを使用した定期的なデータ取得ジョブ

9. 今後の改善アイデア

GitHub Actions で Slack 通知: Due ‑ 2 日で DM。

Mermaid ガント を自動生成し進捗を可視化。

.todo/metrics.yaml にコミット履歴を集計しベロシティ可視化。



Todoタスク分析ダッシュボード: 遅延タスク、依存関係、リスク状況を可視化