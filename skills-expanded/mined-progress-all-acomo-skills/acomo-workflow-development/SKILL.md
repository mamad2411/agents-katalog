---
name: acomo-workflow-development
description: >
  acomo をバックエンドとした業務ワークフローシステムを、開発者でも非開発者でも AI エージェントとの対話だけで
  開発・検証・改善できるようにするための開発ループ（ヒアリング → 設計 → 静的検証 → 登録 → ウォークスルー → 改善）の正本。
  モデル draft の静的検証ハーネスとウォークスルー計画ジェネレーターを同梱する。
  acomo 標準 UI / CLI での運用に加えて、acomo をエンジンとして裏に置くカスタムフロントエンド開発
  （画面設計 → @acomo/client / 公開 API 実装 → 認証統合 → E2E）までを A1〜A4 トラックでカバーする。
  「acomo でワークフローシステムを作りたい」という依頼全般の入口として使い、
  設計対話は acomo-workflow-modeling、CLI 操作は acomo、画面操作は acomo-ui の各スキルへ委譲する。
---

# acomo ワークフローシステム開発ループ（スキルセット入口）

このスキルは、**acomo をバックエンドとした業務ワークフローシステムを AI エージェントと対話的に開発する**ための
**開発ループとハーネスの正本**である。ユーザーが開発者かどうかを問わず、「業務の説明 → 動くワークフロー」までを
エージェント主導で反復できるようにする。

> **ユーザー向け回答の作法**はリポジトリ共通ルール（`AGENTS.md`「ユーザー向け回答（全スキル共通）」）に従う。
> スキル名・参照ファイルパス・取得過程をエンドユーザー向けの説明文に出さない。

## このパッケージが提供するもの

| 提供物 | 場所 | 役割 |
|--------|------|------|
| 開発ループの正本 | [references/loop-guide.md](references/loop-guide.md) | フェーズ定義・停止条件・非開発者/開発者モードの分岐 |
| 静的検証ハーネス | `scripts/validate-model.mjs` | draft（definition / dataSchema / policy）のスキーマ準拠 + グラフ・整合性検証 |
| ウォークスルー計画 | `scripts/walkthrough-plan.mjs` | モデル JSON から経路列挙 + CLI / UI テスト手順 + サンプルデータを生成 |
| ハーネスの使い方 | [references/harness-guide.md](references/harness-guide.md) | コマンド・オプション・エラーコード対応表 |
| ウォークスルー手順 | [references/walkthrough-testing.md](references/walkthrough-testing.md) | 公開後の実走テスト（CLI 経路 / UI 経路・複数アクター） |
| カスタムアプリトラック | [references/custom-app-guide.md](references/custom-app-guide.md) | カスタムフロントエンド開発（A1〜A4）の正本・アーキテクチャ選定・スキャフォールドレシピ |
| 画面設計の写像規則 | [references/screen-design.md](references/screen-design.md) | モデル → 画面・フォーム・操作への写像と設計書テンプレート（A1） |
| 最小 SPA スキャフォールド | [references/spa-scaffold-minimal.md](references/spa-scaffold-minimal.md) | (a) SPA 直呼び構成の最小 3 ファイル（Vite + dev proxy + SuperTokens）（A2） |
| クライアント実装ガイド | [references/client-integration.md](references/client-integration.md) | `@acomo/client` / 公開 API の検証済み呼び出しパターン（A2） |
| 認証統合ガイド | [references/auth-integration.md](references/auth-integration.md) | セッション透過 / Client Credentials / ローカル開発の非対話認証（A2） |
| カスタム UI の E2E | [references/custom-app-e2e.md](references/custom-app-e2e.md) | walkthrough JSON を正本にした経路網羅テスト（A3） |
| 動作サンプル | `fixtures/sample-*.json` / `fixtures/broken-model.json` | 実走確認済みのお手本モデル（基本承認 / 条件分岐 / 並列審査 / 差し戻しループ — 一覧は harness-guide.md）とエラーカタログ |

## スキルセット構成（ルーティング）

このスキルは**オーケストレーター**であり、各作業は既存スキルへ委譲する。該当スキルを必ず読み込んでから作業する。

| 作業 | 委譲先スキル |
|------|-------------|
| 業務ヒアリング・モデル設計対話（draft 生成・逆質問） | `acomo-workflow-modeling`（[SKILL.md](../acomo-workflow-modeling/SKILL.md)） |
| モデルの型・パターン・設計原則 | 同上の [philosophy.md](../acomo-workflow-modeling/philosophy.md) / [patterns.md](../acomo-workflow-modeling/patterns.md) |
| CLI / 公開 API の呼び出し（登録・公開・プロセス操作） | `acomo`（[SKILL.md](../acomo/SKILL.md)。モノレポでは外部スキル — 無ければ `npm run skills:install`。配布リポジトリでは併設済み） |
| ユーザーに画面操作を案内する（非開発者の確認・受入） | `acomo-ui`（[SKILL.md](../acomo-ui/SKILL.md)） |
| 検証・テスト・改善ループの回し方 | **本スキル**（references/） |
| カスタムフロントエンドの設計・実装・E2E | **本スキル**（[custom-app-guide.md](references/custom-app-guide.md) から辿る） |

acomo-ui は **acomo 標準画面**の案内スキル。カスタムアプリの画面はアプリ自身の言葉で案内する（A4）。

## 2 つの利用モード

最初にユーザーの環境と役割を把握し、モードを決める（途中で切り替えてよい）。

| | **同伴モード（非開発者向け）** | **開発者モード** |
|---|---|---|
| 想定ユーザー | 業務担当者・管理者。コードやターミナルは使わない | acomo をバックエンドに使う開発者 |
| モデルの登録・公開 | エージェントが CLI で代行 | ユーザー自身 or エージェントが CLI |
| 検証ハーネス | エージェントが実行し、結果を業務の言葉で説明 | ユーザーも直接実行できる |
| ウォークスルー | ユーザーはブラウザ画面で操作・確認（acomo-ui の言葉で案内）。エージェントは CLI で並走確認 | CLI / 画面のどちらでも |
| 受入判断 | ユーザーが画面上の動きを見て判断 | ユーザーがテスト結果と画面で判断 |

**どちらのモードでも、業務の意思決定（承認段数・権限・分岐条件など）はユーザーに確認する。**
技術的な検証・修正はエージェントが自律的に回す。

## 開発ループ（概要）

正本は [references/loop-guide.md](references/loop-guide.md)。各フェーズには入口条件・出口条件（DoD）がある。

```
Phase 0 環境準備      … 接続先（ローカル or 本番テナント）と認証を確立し、疎通を確認する
Phase 1 ヒアリング設計 … acomo-workflow-modeling に従い draft（definition/dataSchema/policy）を対話生成
Phase 2 静的検証      … validate-model.mjs でエラー 0 になるまで draft を修正（エージェント自律ループ）
Phase 3 登録          … createWorkflowModel でドラフト登録し、モデル ID を控える
Phase 4 ウォークスルー … walkthrough-plan.mjs の計画に沿って公開 → 全結末経路を実走 → 証跡を残す
Phase 5 改善          … ユーザーのフィードバックを差分で draft に反映し、Phase 2 へ戻る
Phase 6 引き渡し      … 運用手順（画面操作ベース）をユーザーに説明して完了
```

**カスタムフロントエンドが要る場合**は、Phase 4 green を入口条件に **A1〜A4 トラック**
（画面設計 → 実装 → E2E → 引き渡し。正本: [references/custom-app-guide.md](references/custom-app-guide.md)）へ続ける。
操作面が acomo 標準 UI / CLI で足りるなら Phase 6 で完了。

**ループ停止条件（このスキルの DoD）**

1. `validate-model.mjs` がエラー 0（警告は個別に妥当性を説明済み）
2. ウォークスルー計画の全経路（承認・却下など全結末）を実走し、期待した終了ノードに到達した
3. ユーザーが画面上（または CLI 出力）で業務どおり動くことを確認し、受け入れた
4. （カスタムアプリを作る場合）A3 の DoD — 全結末経路がカスタム UI 経由でも到達し、権限外ケースを確認済み

## エージェント実行レール（迷ったらこの順）

モデル 1 本を作って引き渡すまでの機械的な最短手順。**各行のゲートを満たすまで次の行に進まない**。
詳細・例外は [references/loop-guide.md](references/loop-guide.md)。JSON の形で迷ったら
`fixtures/sample-*.json` を正とする（文中の断片より fixtures 優先）。

| # | やること（コマンド） | 進んでよい条件（ゲート） |
|---|---------------------|--------------------------|
| 1 | `acomo --version`（モノレポでは `acomo-cli/package.json` と突合）→ `acomo getCurrentUser` | 認証・テナント・モードが確定 |
| 2 | acomo-workflow-modeling で draft を対話生成し、**`/tmp/<モデル名>-draft.json` に保存**（以降このファイルが正本） | ユーザーがフロー・項目・権限に合意 |
| 3 | `npm run workflow:validate -- /tmp/<モデル名>-draft.json` | **エラー 0**（警告は説明・合意済み） |
| 4 | `acomo createWorkflowModel '<draft の中身>'`（改善時は `saveWorkflowModel`） | modelId を取得 |
| 5 | `npm run workflow:walkthrough -- /tmp/<モデル名>-draft.json` → **アクター表を先に全部埋める** → `acomo publishWorkflowModel --modelId <ID>` → 全経路を実走 | 全結末経路が期待した終了ノードに到達 + 権限外 1 ケース確認 |
| 6 | フィードバックは draft ファイルを差分更新して行 3 に戻る。受入後に引き渡し（カスタム UI が要るなら A1〜A4 へ） | ユーザー受入 |

## ハーネス早見

モノレポ内ではルート npm script を使う（実体は本スキル `scripts/` 配下・依存ゼロの Node スクリプト）。

```bash
# draft の静的検証（fenced ブロック付きテキストも直接渡せる）
npm run workflow:validate -- path/to/draft.json
npm run workflow:validate -- path/to/draft.json --json   # 機械可読

# ウォークスルー計画の生成（Markdown。--json で機械可読）
npm run workflow:walkthrough -- path/to/draft.json
```

モノレポ外（スタンドアロン配布時）は `node scripts/validate-model.mjs <file>` で直接実行できる。
詳細・エラーコード対応表: [references/harness-guide.md](references/harness-guide.md)

## モノレポ外での利用（配布）

本スキルは acomo モノレポを持たない**利用者・カスタムアプリ開発者**にも配布される
（配布チャネル: [acomo-skills リポジトリ](https://github.com/progress-all/acomo-skills)。公開手順はモノレポの `docs/skills-distribution.md`）。
配布レイアウトでも次が成り立つように書かれている。

- 依存スキル（`acomo` / `acomo-workflow-modeling` / `acomo-ui`）は**同じ親ディレクトリに併設**される前提。
  相対リンク（`../acomo/SKILL.md` 等）はそのまま解決する。
- ハーネスは依存ゼロの Node スクリプト（Node 20+）。`node <このスキル>/scripts/validate-model.mjs <file>` で動く。
  スキーマ検証層は併設の `acomo-workflow-modeling/schemas/` を自動解決する（無ければ `--schemas-dir` か
  環境変数 `ACOMO_MODEL_SCHEMAS_DIR` で指定。未指定時はスキーマ層のみスキップし警告を出す）。
- `npm run workflow:validate` / `workflow:walkthrough` / `npm run skills:install` は**モノレポ内専用**の入口。
  配布環境では上記のスタンドアロン実行を使う。
- ローカル開発スタック（`dev:up` / seed ユーザー等）に触れる記述はモノレポ内でのみ有効。配布先では
  対象テナントの実値（URL・authTenantId・ユーザー）に読み替える。

## 進め方の原則（ループエンジニアリング）

- **draft を早く見せ、検証を挟んでから登録する。** ヒアリングだけを続けない（acomo-workflow-modeling の段階生成プロトコルに従う）。
- **静的検証はエージェントの自律ループ。** validate のエラーはユーザーに逐一報告せず、直してから結果だけ伝える。警告は「業務判断が要るもの」だけユーザーに確認する。
- **ウォークスルーは必ず全結末を通す。** 承認で終わる経路だけでなく、却下・差し戻し・分岐の各経路を通し、期待した終了ノード名に到達したことを確認する。
- **改善は差分で回す。** フィードバックのたびに全作り直しせず、definition / dataSchema / policy のどこに効くかを説明してから draft を更新し、Phase 2（静的検証）から再走する。
- **証跡を残す。** 各ウォークスルーの実行コマンド・プロセス ID・到達ノードを記録し、受入時にユーザーへ提示する。

## Known failure modes

- **エッジ `type` に `revert` を書く** — モデル JSON の `FlowType` に `revert` は存在しない（差し戻しはノードの `canRevert` とランタイム API の担当）。validate が `E_EDGE_TYPE` で検出する。
- **条件式を文字列 1 本で書く** — `conditions[].expression` / `actionPolicies[].allow` は必ず `{operator, expression1, expression2}` のオブジェクト形式（`"$token.approveCount >= $token.childTokenLength"` のような文字列はスキーマ違反で `E_SCHEMA_DEFINITION` になる）。**正しい形の正本は `fixtures/sample-*.json`** — 文中の JSON 断片と食い違ったら fixtures を正とする。
- **policy のノード ID をノード名や別 ID で書く** — definition の `id` と完全一致が必要。`E_POLICY_NODE` で検出する。
- **dataSchema プロパティの `_order` 欠落** — バックエンドの AJV は `_order` / `_acomoType` を必須とする。スキーマ検証（`E_SCHEMA`）で検出する。
- **却下経路の実走漏れ** — 承認経路だけ試して完成と報告してしまう。walkthrough-plan が列挙する全経路を通すこと。
- **ローカル検証で `acomo login` の恒久トークンを前提にする** — ローカル開発スタックでは SuperTokens のセッションアクセストークンを `ACOMO_ACCESS_TOKEN` に使う（短命）。手順は [references/walkthrough-testing.md](references/walkthrough-testing.md)。
- **プロセスデータを `{"data":{...}}` で包んで送る** — engine 系 API（submit / approve / reject / save）の body は dataSchema のキーをトップレベルに持つ**フラットな JSON**（ローカル実走で確認済み）。包んで送ると dataSchema 外のキーとして無視される。
- **完了後にプロセスデータが見えないのをバグと報告する** — 終了イベントに read の policy がないと完了後の取得で data が `{}` になる仕様。完了後閲覧が要る業務は終了イベントに read を並べる。
- **`@acomo/client` の高レベル生成メソッドでプロセスを受け取る** — engine 系・プロセス取得系は `*Raw` + `raw.json()` を使う（高レベル版は `token.childProcessTokens` の FromJSON マッパーで落ちる。ローカル実走で確認済み。正本: [references/client-integration.md](references/client-integration.md)）。
- **`Engine:execute` ロールなしのユーザーで engine API を叩いて 403 を actionPolicies のせいにする** — engine 系はロールの SystemActionPolicies `Engine:execute` が前提（実測。エラーメッセージに `Engine:execute が必要` と出る）。カスタムアプリ利用者・E2E テストユーザーに該当ロールを割り当てる。
- **カスタムアプリでボタン活性をロール名・status 文字列で自作判定する** — `getProcessWithNodeActions` の `nodeActions`（サーバー側の actionPolicies 評価結果）を使う。
- **`@acomo/client` のクラス名を operationId から推測する / 一般ユーザーのアプリで `getWorkflowModel` を呼ぶ** — 生成クラスは OpenAPI tag ごと（`getMyModel` は `MyModelApi`）。`/models`・`/processes` 系は `Model:read` 等が要る管理者向けで一般業務ユーザーは 403 — アプリは `/my/...`（`MyModelApi` / `MyProcessApi`）で組む。対応表: [references/client-integration.md](references/client-integration.md)。
- **カスタム SPA から業務 API をブラウザ直呼びして CORS で落ちる** — CORS の許可ヘッダに `x-tenant-id` が含まれない（実測）。認証 API は直呼びできるが、業務 API は同一オリジン化（プロキシ / BFF）する。正本: [references/auth-integration.md](references/auth-integration.md)。
