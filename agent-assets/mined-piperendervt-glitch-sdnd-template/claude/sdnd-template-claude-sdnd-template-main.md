# {プロジェクト名}

## 概要
このプロジェクトは SDND（Spec-Driven Novel Development）フレームワークを使った長編小説制作プロジェクトです。
仕様駆動で物語の整合性を保ちながら、エピソード単位で執筆・検査・正史登録を行います。

## 現在のフェーズ
{現在の執筆フェーズ。例: Arc 1 執筆中（EP-001〜）}

## 参照すべきドキュメント

### 常時読み込み（TIER 1）
- specs/core/invariants.md — 不変ルール（INV-*）
- specs/core/characters_state.md — キャラ現在状態
- canon/quick_ref.md — Canon最新状態スナップショット

### エピソード実行時（TIER 2）
- canon/active/*.md — 直近N話のCANONエントリ
- meta/open_loops.md — オープンループ一覧

### 参照時のみ（TIER 3）
- specs/reference/world.md — 世界設定
- specs/reference/system.md — {コアシステム}体系
- specs/reference/characters_detail.md — キャラ詳細設定
- canon/archive/*.md — 過去CANONエントリ

### ガイド・ポリシー
- docs/ARCHITECTURE.md — プロジェクト構成ガイド
- specs/_index.md — スペック読み込み階層ガイド
- canon/README.md — Canon運用ルール
- meta/phase_plan.md — フェーズ計画

### テンプレート
- canon/active/CANON-TEMPLATE.md — CANONエントリテンプレート

### ツール
- tools/ — 自動化スクリプト

## 設計方針
- canon は3層分離構造（quick_ref + active + archive）
- Specs は TIER 1（必須）/ TIER 2（実行時）/ TIER 3（参照時）に階層化
- open_loops.md は canon 確定のブロッキングゲートで同期を強制
- active ウィンドウのサイズは sdnd-config.yaml の canon.active_window で設定

## Git 運用ルール
- commit とブランチ操作は自動で実行してよい
- main/master への merge は、実行前に必ずユーザーに確認を求めること
- commit メッセージは [story], [spec], [canon], [qa], [chore] のprefixを付けること

## サブエージェント運用ルール

本プロジェクトでは3つのサブエージェントを使い分ける。

| エージェント | 役割 | 起動タイミング |
|-------------|------|--------------|
| writer | EP本文と canon-proposal の執筆 | 「EP-NNN を書いて」 |
| qa | QAレポートの作成 | 「EP-NNN をQAして」 |
| editor | Canon登録・仕様更新 | 「Canon登録して」「仕様を修正して」 |

### ファイル変更権限
- writer: story/ のみ書き込み可。specs/ は読み取りのみ
- qa: qa/reports/ のみ書き込み可。story/ specs/ は読み取りのみ
- editor: specs/ meta/ canon/ のみ書き込み可

### ワークフロー
1. メインセッション（PM）が writer を呼び出し → EP本文が生成される
2. メインセッション（PM）が qa を呼び出し → QAレポートが生成される
3. QA PASS なら editor を呼び出し → Canon登録・仕様更新
4. QA に指摘があれば writer を再度呼び出し → 修正
