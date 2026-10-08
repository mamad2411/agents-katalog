---
name: autotrade_skill_ui_mock_generation_v0_1
description: 要件追跡可能なクリック可能UIモックを、固定ダミーデータとローカル品質確認を前提に生成する。
---

# autotrade_skill_ui_mock_generation_v0_1

## 目的

運用者が「何ができ、どう操作し、どの状態になるか」を確認できるクリック可能なUIモックを、要件・ユースケース・画面・状態・テストIDと結び付けて生成する。対象は仕様確認用のローカルUIであり、本番の自動売買処理ではない。

## 入力

- `phase_id`、`step_id`、`output_root`、`log_root`、`artifact_index`
- `detail_boundary`、`human_gate_policy`、`unknown_policy`
- 要件ID、ユースケースID、画面ID、UI状態ID、テストIDの追跡表
- 画面一覧、操作フロー、状態遷移、受入条件、レビュー済みの安全境界
- 固定Seed、固定基準日時、ダミーデータ版、PC/スマートフォンのviewport方針
- 承認済みのFrontend基盤とコンポーネント方針

## 出力

- クリック可能なUIモックのソース、画面・部品カタログ、Storybookのstories
- 要件IDから画面操作・状態・テストIDへ辿れる追跡表の差分
- 固定ダミーデータの定義と再現手順
- キーボード操作、focus、フォーム、Dialog、Tableを含むcomponent testの骨格
- 未確定事項、生成できなかった操作、後続Human Gateへの引き継ぎ

## 実施規約

1. まず追跡表と画面状態を読み、画面を追加する理由と対応するIDを確認する。
2. 生成時は同じSeed・基準日時・ダミーデータ版を使い、画面に「例」「未接続」「未承認」を表示する。
3. 重要操作には、可視のラベル、キーボード到達性、focus表示、成功・失敗・停止後の表示を用意する。
4. 単一Backtest、網羅検証、Forward/Shadow/Paper/Live候補、Human Gate、安全停止を別状態として扱う。
5. Storybookとcomponent testで再現できる最小状態を残し、正式HTML・追跡表・テスト証跡の正本を混同しない。

## 禁止事項・境界

- Broker、実市場データ、実口座、Secret、外部API、外部AIサービス、実注文へ接続しない。
- 固定ダミー値を、後続Gateで決める実数値・実銘柄条件・性能基準として確定しない。
- 認証・ユーザー管理・権限管理を勝手に追加しない。単一運用者・認証不要の要件を変更しない。
- UIソースだけを正式要件・合否証跡に昇格させない。UnknownをPassにしない。
- 外部CDNや無承認のnpmパッケージを追加しない。

## 品質チェック

- 要件・ユースケース・画面・状態・テストIDの欠落、重複、孤立リンクがない。
- PC幅とスマートフォン幅で主要操作が同じ意味を保つ。
- ボタンの無効化、取消、停止、復旧、未入力、データなし、未承認が文字で説明される。
- `@playwright/test`、Storybook、Vitest/axeの正式入口へ渡せる再現手順がある。
- Critical/High、Secret、外部接続、Look-ahead、実注文に関する指摘を残したままPassにしない。

## Phase依存パラメータ

- `phase_id`
- `step_id`
- `output_root`
- `log_root`
- `artifact_index`
- `detail_boundary`
- `human_gate_policy`
- `unknown_policy`
- `traceability_matrix`
- `seed_policy`
- `viewport_policy`

## 参照成果物

- `doc/ai_foundation/03_プロジェクト汎用Skill仕様.html`
- `doc/ai_foundation/07_AI部品作成ルール.html`
- `plan/requirements_update/RQU-UI_要件UIテスト追跡マトリクス_2026-08-11.md`
- `doc/requirements/01_自動トレードシステム要件定義書.html`
