---
name: moc-skill
description: >-
  FIWARE Orion Context Broker (NGSIv2) からエンティティ情報を読み取り専用で取得する。
  データ連携基盤・都市OS・スマートシティ基盤・センサーデータ・IoTプラットフォームへの
  GET クエリ、エンティティ一覧・件数確認、NGSIv2 API 調査が必要なときに能動的に使う。
  Orion / NGSIv2 / Context Broker / エンティティ取得 / q クエリ /
  地理空間クエリ / Fiware-Service ヘッダー付き基盤アクセスの依頼で発火する。
license: MIT
---

# FIWARE Orion 読み取り専用クエリ

FIWARE Orion Context Broker (NGSIv2) に対して、**認証不要の GET のみ**でエンティティ情報を取得するスキルです。書き込み・Subscription・Registration は実装していません。

## インストール

[skills CLI](https://github.com/vercel-labs/skills) でインストールします（OpenCode / Claude Code / Cursor 等に対応）。

```bash
npx skills add kzkski/moc-skill -a opencode -y
.agents/skills/moc-skill/scripts/setup-opencode.sh
```

`setup-opencode.sh` は OpenCode のツール実行詳細（bash 出力など）を**デフォルトで非表示**にします。一般ユーザー向けの静かな UI 用です。詳細を見たいときは OpenCode で `/details` を実行してください。

ローカルパスから試す場合:

```bash
npx skills add ./path/to/moc-skill --list
npx skills add ./path/to/moc-skill -a opencode -y
.agents/skills/moc-skill/scripts/setup-opencode.sh
```

## 重要: アクセス経路

**必ず `scripts/orion.sh` 経由でアクセスすること。** カタログ外 URL へ直接 `curl` しないでください。対象基盤は `endpoints.json` に登録された名前だけを使います。

`npx skills add` 後、`moc-skill` スキル配下の `scripts/orion.sh` を絶対パスで実行します。代表パス:

- `.agents/skills/moc-skill/scripts/orion.sh`（OpenCode / Cursor 等）
- `.claude/skills/moc-skill/scripts/orion.sh`（Claude Code）
- `~/.config/opencode/skills/moc-skill/scripts/orion.sh`（OpenCode グローバル）

エージェントは `**/moc-skill/scripts/orion.sh` を探索し、見つかったパスを `ORION` として使ってください。`orion.sh` は同ディレクトリ隣の `endpoints.json` を自動解決します。

```bash
ORION="/path/to/moc-skill/scripts/orion.sh"
```

環境変数 `ORION_ENDPOINTS_FILE` でカタログパスを上書きできます（未設定時はスキル同梱の `endpoints.json`）。

## 回答フォーマット

最終回答は**一般ユーザーが読みやすい要約**にすること。`orion.sh` の取得結果をそのまま貼り付けない。

- 一覧・比較・属性値は**表**または**箇条書き**で要約する
- 件数・基盤名・型名・主要属性など、依頼に答える情報だけを含める
- 実行したコマンド、curl、生 JSON、HTTP ヘッダーなどの**技術的な詳細は最終回答に含めない**
- ユーザーが「生 JSON を見せて」「コマンドも教えて」「デバッグ用に全文」などと**明示したときだけ**技術的な出力を含める

## 推奨ワークフロー

`endpoints.json` に登録された makeour.city 系 Orion では **`types` を呼ばない**（`GET /v2/types` は 401 Unauthorized）。無駄なリトライを避け、次の順で探索します。

1. **endpoints** — 基盤名・Fiware-Service 一覧（各 `note`）を確認
2. **entities / count** — `service=`（複数サービス時）と `type=` で直接取得・件数確認
3. **entity** — 特定 ID の詳細取得

型名の手がかりは `endpoints` のサービス `note`、ユーザーの依頼文、または `entities` の試行結果から得ます。

```bash
"${ORION}" endpoints
"${ORION}" entities sagacity service=moc_sagacity limit=10
"${ORION}" count sagacity service=sagacity_topita type=TopitaPointUser
"${ORION}" entities yokosuka type=WeatherForecast limit=5
"${ORION}" entity yokosuka "forecast-001" attrs=location
```

## コマンドリファレンス

| コマンド | 説明 |
|----------|------|
| `endpoints` | カタログに登録された基盤名・URL・Fiware-Service 一覧・説明を表示 |
| `types <ep> [service=NAME]` | `GET /v2/types?options=count`（**makeour.city では 401 のため使用しない**） |
| `entities <ep> [k=v ...]` | `GET /v2/entities`（未指定時 `options=keyValues` `limit=20` を付与） |
| `entity <ep> <id> [k=v ...]` | `GET /v2/entities/{id}`（同上デフォルト付与） |
| `count <ep> [k=v ...]` | `limit=1&options=count` で `Fiware-Total-Count` ヘッダーのみ返す |
| `raw <ep> <path?query> [service=NAME]` | `/v2/` 配下に限定した任意 GET |

`<ep>` は `endpoints.json` のキー名（例: `Sandbox`, `sagacity`, `yokosuka`）。

**複数 Fiware-Service**: 1 エントリに配列で複数サービスを登録できます。クエリ時は `service=NAME` を指定してください（Orion へのクエリパラメータではなく、ヘッダー選択用の予約キー）。単一サービスのエントリでは `service=` は不要です。

### デバッグ

`ORION_DRY_RUN=1` を設定すると curl コマンドを表示するだけで実行しません。

```bash
ORION_DRY_RUN=1 "${ORION}" entities yokosuka type=WeatherForecast
```

## NGSIv2 クエリパラメータ早見表

`entities` / `entity` / `count` / `raw` の `[k=v ...]` または `raw` のクエリ文字列に指定します。

| パラメータ | 用途 |
|------------|------|
| `type` | Entity Type でフィルタ（例: `type=Device`） |
| `q` | 属性条件（例: `q=temperature>25`） |
| `attrs` | 返却属性の限定（例: `attrs=location,temperature`） |
| `idPattern` | エンティティ ID の正規表現（例: `idPattern=^sensor-.*`） |
| `limit` | 最大取得件数（`entities`/`entity` デフォルト 20） |
| `offset` | ページング開始位置 |
| `orderBy` | ソート（例: `orderBy=!dateObserved`） |
| `georel` + `geometry` + `coords` | 地理空間クエリ（例: `georel=near;maxDistance:1000` `geometry=Point` `coords=-3.7,40.4`） |
| `options` | レスポンス形式（`keyValues`, `count`, `values` など） |

## 注意点

- **types は使わない**: 登録基盤では `/v2/types` が 401。型探索は `entities` + `type=` / `count` で行う
- **読み取り専用**: POST / PATCH / DELETE / Subscription / Registration は行わない
- **カタログ必須**: 未定義のエンドポイント名は拒否される
- **raw は /v2/ のみ**: `/v2/` 以外へのパスはエラー
- **Entity ID**: `[A-Za-z0-9._:~-]+` のみ許可（パストラバーサル対策）
- **Fiware ヘッダー**: `endpoints.json` の `Fiware-Service` / `Fiware-ServicePath` が空でなければ自動付与。`Fiware-Service` が配列の場合は `service=` で選択
- **依存**: `curl`, `jq` が PATH に必要

## カタログ形式 (`endpoints.json`)

```json
{
  "endpoints": {
    "<名前>": {
      "base_url": "https://orion.<自治体>.makeour.city",
      "Fiware-Service": "単一ヘッダー値",
      "Fiware-ServicePath": "ヘッダー値(不要なら空文字)",
      "note": "説明"
    },
    "sagacity": {
      "base_url": "https://orion.sagacity.makeour.city",
      "Fiware-Service": [
        { "value": "moc_sagacity", "note": "MoC 佐賀" },
        { "value": "sagacity_topita", "note": "Topita" },
        { "value": "sagacity_ikunowa", "note": "保育園データ" }
      ],
      "Fiware-ServicePath": "",
      "note": "複数サービスを1エントリで管理"
    }
  }
}
```

`Fiware-Service` は **文字列**（単一）または **配列**（複数）を指定できます。配列要素は文字列、または `value` / `Fiware-ServicePath` / `note` を持つオブジェクトにできます。エントリ共通の `Fiware-ServicePath` は、オブジェクト側で未指定の場合のデフォルトになります。

新しい基盤を追加するときは、運用者が提供する Orion URL と Fiware ヘッダー値をこの形式で追記してください。
