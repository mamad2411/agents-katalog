---
name: gws-cli
description: |
  Google Workspace（Calendar / Drive / Docs / Meet）の CLI 操作スキル。
  発火条件: 文脈に「Drive」「ドライブ」「マイドライブ」「GDrive」「Docs」「Meet」「Calendar」「Workspace」のいずれかが含まれ、以下のいずれかに該当するとき。口語・短縮・カタカナ／英語混在（up / DL / アップ / 落として / 投げて / 放り込んで / 置いて / あげて / 保存して）も全て対象。
  - マイドライブへのローカルファイルアップロード（例:「Drive に上げて」「マイドライブに保存」「PDF をアップ」「Drive に up しといて」「成果物を Drive に投げて」）
  - Agent 生成物（提案書・PPTX・PDF・議事録 Markdown 等）の Drive 保存
  - Drive からローカルへのダウンロード（例:「Drive から落として」「PPTX を DL」「Doc を docx で保存」「最新版に差し替え」）
  - Meet 文字起こし／議事録元データの取得
  - Calendar イベント添付ファイル／説明欄の Drive リンク抽出
  - 期間・キーワードによる Calendar イベント検索、自分のカレンダー一覧
  - Google Docs 本文のテキスト取得
  - Meet 会議内容の要約・分析の前段階としての元データ取得
allowed-tools:
  - "Bash(gws-cli:*)"
---

# gws-cli: Google Workspace CLI

Google Workspace のリソースを読み書きする CLI ツール。Calendar / Docs / Drive を 1 つのコマンドラインから扱える。

- 読み取り: Calendar イベント (添付 + 説明文の Drive リンク抽出含む) / Calendar 一覧 / Google Docs テキスト / Drive ファイルダウンロード
- 書き込み: ローカルファイルをマイドライブへアップロード（Agent 生成物の保存など）

## 前提条件

- リポジトリ: `github.com/sakai-classmethod/gws-cli`
- ADC 認証済み（`calendar.readonly` + `drive.readonly` + `drive.file` スコープ）
- `uv tool install` 済み（`gws-cli` コマンドが PATH で使用可能）

## コマンド一覧

### Calendar イベント取得（単発）

```bash
gws-cli calendar event get <event-id> [--calendar-id <calendar-id>]
```

- `event-id`: Google Calendar のイベント ID
- `--calendar-id`: カレンダー ID（デフォルト: `primary`）
- 出力: Calendar API events.get の生レスポンス JSON に、追加フィールドとして必ず以下を付与
  - `attachments`: API の `attachments` 配列（API 上は省略され得るが本コマンドは常に空配列以上を返す）
  - `links`: 後述の Drive リンクスキーマ（dedup 済み）

### Calendar イベント検索（範囲）

```bash
gws-cli calendar event list \
  [--calendar-id <id>] \
  [--time-min <iso8601>] [--time-max <iso8601>] \
  [--q <query>] [--event-type <type>]... \
  [--order-by startTime|updated] \
  [--page-size <n>] [--page-token <token>] \
  [--time-zone <iana-tz>] \
  [--show-deleted] \
  [--all-pages]
```

- 出力: `{"items": [...], "nextPageToken"?: "...", "nextSyncToken"?: "..."}` の envelope JSON
- 各 `items[i]` は events.list の生 event に `attachments` と `links` を加えたもの（`event get` と同形式）
- `--all-pages` 指定時は内部でページを連結し、`items` に全件集約。`nextPageToken` は省略
- `--all-pages` には `--time-min` と `--time-max` の両方が必須（未指定なら exit 2 で拒否、長期レンジ全件取得の事故防止）
- `singleEvents=true` 相当で動作（繰り返しイベントは個別インスタンスに展開済み）。recurring master を見たい場合は本 CLI ではなく Drive UI または別 API を使う

### links フィールドのスキーマ

Calendar イベント (`event get` / `event list` の各 item) に付与される `links` は以下の形:

```json
{
  "url": "https://docs.google.com/document/d/.../edit",
  "fileId": "1aBcD...",
  "mimeType": "application/vnd.google-apps.document",
  "title": "Gemini によるメモ",
  "sources": ["event.attachments", "event.description"],
  "sourceUrls": ["https://docs.google.com/document/d/.../edit"]
}
```

挙動:

- `fileId` で dedup する。`event.attachments` と `event.description` の両方に同じ Doc が現れた場合は 1 件にまとめ、`sources` に両方を記録
- `sourceUrls` は同じ Doc に対する URL バリエーション (`/edit?usp=meet` と `/edit` 等) を全て保持
- `title` は attachment 由来ならその `title`、description 由来は anchor タグのテキスト（URL と同一なら `null`）
- `mimeType` は attachment 由来ならその値、URL のみ由来なら URL prefix から推定
  - `docs.google.com/{document,spreadsheets,presentation,forms,drawings}/d/...` → 各 native MIME
  - `drive.google.com/drive/folders/...` → `application/vnd.google-apps.folder`
  - `drive.google.com/file/d/...` → `null`（URL からは MIME を確定できない）
- 削除済み Drive 参照（`fileId` を Drive で引くと 404）も `links` に含める。Calendar 上に残っている事実を保持する仕様で、Drive の生死検証はしない
- description は HTML / 平文のどちらにも耐性あり: anchor タグ抽出 + `html.unescape()` 済みテキストの URL regex 抽出 の二段構え

### Calendar 一覧

```bash
gws-cli calendar calendars
```

- 出力: `{"items": [...]}` envelope。`items[i]` は CalendarList resource（`id`, `summary`, `accessRole` など）
- `event get` / `event list` の `--calendar-id` に渡す ID をここで調べられる

### Calendar 添付ファイル取得 (deprecated)

```bash
gws-cli calendar attachments <event-id> [--calendar-id <id>]
```

- 互換維持のために残しているが deprecated。実行時 stderr に警告を出力する
- 次メジャーで削除予定。新規利用は `gws-cli calendar event get` に統一する

### Docs テキスト取得

```bash
gws-cli docs get <doc-id> [--format plain|md] [--section transcript|notes]
```

- `doc-id`: Google Docs のドキュメント ID（`event get` / `event list` の `links[].fileId` を渡す）
- `--format`: 出力形式（デフォルト: `plain`、`md` で Markdown 変換）
- `--section`: セクション抽出（`transcript` で文字起こしのみ、`notes` でメモのみ）

挙動:

- `--format` と `--section` は独立に適用される（先に format 変換 → 後からセクション抽出）。両方同時に指定可能
- `doc-id` は Google Docs 形式（`mimeType: application/vnd.google-apps.document`）のファイルに限定。PDF / スプレッドシート / スライド等は `files.export` が失敗しエラー終了
- `--section transcript`: `📖 文字起こし` マーカー（含む）から本文末尾までを返す。後続に `📝 メモ` が続く場合もそれを含めて末尾まで返す
- `--section notes`: `📝 メモ` マーカー（含む）から、本文中に `📖 文字起こし` が現れる場合はその直前まで、現れない場合は本文末尾まで返す（Meet ドキュメントはメモ → 文字起こしの順で生成される想定）
- `--section transcript|notes` 指定時、対応するマーカーが本文に含まれない場合は全文を返す（silent fallback。エラーにはならず exit 0 / stderr への警告もなし）。fallback を呼び出し側で検知するには、出力本文の先頭 1 行目が該当マーカー（`📖 文字起こし` / `📝 メモ`）で始まるかを確認する（マーカー自体は出力に含まれる仕様のため、含まれていなければ fallback 発生）。fallback が発生した場合は「該当セクションが本当に存在しない（録画/Gemini メモ未生成）」「マーカー無しの旧フォーマット」「Docs を手動編集してマーカーが消えた」のいずれかであり、CLI 側で区別する手段はない。ユーザーに状況確認するのが安全

### Drive ダウンロード

```bash
gws-cli drive download <file-id> [<dest>] [--export <format>] [--overwrite]
```

- `file-id`: Drive のファイル ID（必須）
- `dest`: 保存先（省略時はカレントディレクトリ、`-` で stdout）。判定ルールは次の通り:
  - 末尾が `/` で終わる → ディレクトリ扱い。ディレクトリが存在しない場合はエラー（自動作成しない）。配下に Drive 名+拡張子で保存
  - 既存ディレクトリのパス → ディレクトリ扱い。配下に Drive 名+拡張子で保存
  - 上記以外 → ファイル名扱い。親ディレクトリは自動作成される（`mkdir -p` 相当を CLI 内部で実施）
- `--export`: Google native（Docs/Sheets/Slides/Drawings）のエクスポート形式
  - shortcut: `pdf`, `docx`, `xlsx`, `pptx`, `png`, `jpeg`, `csv`, `txt`, `rtf`, `odt`, `ods`, `epub`, `tsv`
  - MIME 直指定可（例: `--export application/pdf`）
  - 既定: Docs→docx / Sheets→xlsx / Slides→pptx / Drawings→png
- `--overwrite`: 既存 **ローカルファイル** があれば上書き（Drive 側には影響しない。`drive upload --overwrite` の Drive 上 revision 上書きとは意味が異なる点に注意）
- 出力: ファイル保存時は JSON を stdout、`-` の場合は bytes を stdout / JSON を stderr

挙動:

- Google native は `files.export` 経由でエクスポート、それ以外は `files.get_media` で chunked 取得
- 共有ドライブ上のファイルにも対応（読み取りのみ）
- 拒否される mimeType: フォルダ / shortcut / form / site / `audio/*` / `video/*`
- `files.export` の 10MB 出力上限に該当する場合は専用エラーで Drive UI / Takeout を案内
- 書き込みは temp ファイル → atomic replace（途中失敗時に半端ファイルを残さない）

`docs get` との使い分け:

- Meet 議事録の `📖 文字起こし` / `📝 メモ` を section 抽出 / md 変換したい → `docs get`
- Google Docs / Sheets / Slides を docx/xlsx/pptx などのバイナリで保存したい → `drive download --export ...`
- PDF / PPTX / 画像など Drive 上のバイナリをそのまま取得したい → `drive download`

### Drive アップロード

```bash
gws-cli drive upload <local-path> [--folder-id <folder-id>] [--name <drive-name>] [--overwrite] [--keep-forever]
```

- `local-path`: アップロードするローカルファイル（必須）
- `--folder-id`: マイドライブのフォルダ ID（デフォルト: マイドライブ直下）。環境変数 `GWS_CLI_DEFAULT_FOLDER_ID` でも指定可
- `--name`: Drive 上の表示名（デフォルト: ローカルファイルの basename）
- `--overwrite`: 同名ファイルが 1 件だけある場合に **Drive 上の revision を破壊的に上書き**（`drive download --overwrite` のローカル上書きとは別物。誤付与すると既存ファイルを書き換える）
- `--keep-forever`: 作成した revision に `keepRevisionForever` を付与し、30 日 / 100 件の自動削除上限から除外する（**revision 履歴の保護限定**。ファイル本体の削除防止や共有制御は対象外で、それらが必要なら Drive UI で別途設定）
- 出力: JSON（`fileId`, `name`, `mimeType`, `webViewLink`, `action`）。`action` は `created` または `updated`

挙動:

- 同名 0 件: 新規作成（`--overwrite` を付けても害はない。新規作成パスに進み `action: created`。gws-cli が作成したファイルになるため、以後 `--overwrite` による revision 上書きが可能）
- 同名 1 件 + `--overwrite`: revision 上書き（stderr に `previousRevisionId` を表示）
- 同名 1 件 + `--overwrite` なし: エラー終了
- 同名 2 件以上: エラー終了（`--overwrite` 有無にかかわらず）
- 共有ドライブ配下のフォルダ指定: エラー終了（マイドライブ限定）
- `--keep-forever` は `action` が `created`（新規作成の初回 revision）でも `updated`（上書き後の最新 revision）でも付与される

`--overwrite` の運用指針:

- ユーザーが「上書き」「最新版に差し替え」「アップデート」と明示したとき: 初回から `--overwrite` を付ける
- ユーザーが「新規アップロード」「保存して」と依頼したとき: `--overwrite` を付けない。同名 1 件で `already exists` エラーが返ったら、既存ファイルを壊す変更になるためユーザーに確認してから `--overwrite` を付けて再実行する
- `--overwrite` は「同名 1 件に対する破壊的な revision 更新」であり、予防的・思考停止で付けるのは避ける

## 典型的なワークフロー

### ワークフロー A: Meet の文字起こしを取得（gws-cli 完結）

#### Step 1: イベントを検索して ID を特定

```bash
gws-cli calendar event list \
  --time-min 2026-04-15T00:00:00+09:00 \
  --time-max 2026-04-15T23:59:59+09:00 \
  --time-zone Asia/Tokyo \
  --q '会議名キーワード'
```

レスポンスの `items[].id` がイベント ID。target が見つからない場合は `--q` を外して期間内全件を確認する。複数候補が出たら `summary` / `start` をユーザーに確認する。

#### Step 2: イベント詳細と Doc リンクを取得

```bash
gws-cli calendar event get <event-id>
```

`links` フィールドに Drive 由来のリンクが dedup 済みで並ぶ。Meet の Gemini メモ Doc は通常以下の特徴を持つ:

- `mimeType: application/vnd.google-apps.document`
- `title: "Gemini によるメモ"` または `title: "メモ - 「<会議名>」"`
- `sources: ["event.attachments"]`

複数候補があるとき (例: Recording mp4 + メモ Doc + 議題 Doc) は `mimeType` で絞り、`title` / `sources` で判別する。`mimeType` が `application/vnd.google-apps.document` 以外（PDF, video/mp4 等）は `docs get` には渡せないので除外する。

`links: []`（0 件）の場合は以下の可能性をユーザーに確認する: (1) Meet の録画・文字起こし設定が有効でなかった、(2) 会議直後で Gemini のメモ生成がまだ完了していない（数分〜十数分のラグあり）、(3) 別カレンダーのイベントだった（その場合は `gws-cli calendar calendars` で別カレンダー ID を調べ、`--calendar-id` を指定して再実行）。

#### Step 3: 文字起こしテキストを取得

```bash
# 文字起こしのみ抽出（トークン節約）
gws-cli docs get <fileId> --section transcript

# メモ（Gemini 要約）のみ
gws-cli docs get <fileId> --section notes

# 全文
gws-cli docs get <fileId>

# Markdown 形式で取得
gws-cli docs get <fileId> --format md --section transcript
```

### ワークフロー B': Drive のファイルをローカルへ取得

```bash
# バイナリ（PDF / PPTX / 画像など）はそのままダウンロード
gws-cli drive download <fileId>
gws-cli drive download <fileId> ./out/
gws-cli drive download <fileId> ./report.pdf

# Google Docs を docx で保存（既定）
gws-cli drive download <docId>

# Google Docs を PDF で保存
gws-cli drive download <docId> --export pdf

# Sheets を CSV で stdout に流す
gws-cli drive download <sheetId> - --export csv

# 既存ローカルファイルを Drive 上の最新版で上書き（ローカル側の上書き。Drive には影響しない）
gws-cli drive download <fileId> ./out/proposal.pptx --overwrite
```

`fileId` は `calendar event get` の `links[].fileId` や Drive UI の URL から取得できる。

### ワークフロー B: Agent の生成物をマイドライブへアップロード

提案書・スライド・PDF などをローカルで生成した後に Drive へ保存する。

```bash
# 新規アップロード（マイドライブ直下）
gws-cli drive upload ./proposal.pptx

# 指定フォルダに任意の名前で保存
gws-cli drive upload ./report.pdf --folder-id <folder-id> --name "2026Q2 レポート.pdf"

# 既存ファイルを revision として上書き（ファイル名一致が 1 件のみの場合）
gws-cli drive upload ./proposal.pptx --overwrite

# 長期保存（30日 / 100 revision の自動削除対象から除外）
gws-cli drive upload ./proposal.pptx --overwrite --keep-forever
```

レスポンス例:
```json
{
  "fileId": "1AbC...",
  "name": "proposal.pptx",
  "mimeType": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  "webViewLink": "https://drive.google.com/file/d/.../view",
  "action": "created"
}
```

### ワークフロー C: イベントから Drive リンクを一括収集

説明欄に Drive フォルダや Doc を貼り込む運用 (定例の議事録置き場リンクなど) のイベントから、参照ファイルを構造化して取り出す。

```bash
gws-cli calendar event get <event-id> | \
  uv run python -c "
import json, sys
event = json.load(sys.stdin)
for link in event['links']:
    print(link['fileId'], link['mimeType'] or '', '|', link.get('title') or link['url'])
"
```

`links` の各エントリは `sources` でどこから拾われたか (attachment / description) を確認できる。Drive で削除済みのファイルも残るので、404 を許容する側で実体取得を試みる必要がある。

## 注意事項

- Meet の文字起こしと Gemini メモは同一ドキュメント内の別セクションに格納されている（「Docs テキスト取得」節の挙動を参照）
- トークン節約目的なら `--section transcript` / `--section notes` を使い、必要なセクションだけ抽出する
- フォーマット選択: ユーザーが Markdown を明示的に要求したら `--format md` を優先する。明示要求がなく Agent 内部処理のみで使う場合は `--format plain`（デフォルト）がコンパクトでトークン効率が良い
- エラー時は stderr にメッセージ + exit 1（`event list --all-pages` の引数不足は exit 2）
- `uv tool install` でインストール済みのためどの作業ディレクトリからでも実行可能
- `drive upload` はマイドライブ専用（共有ドライブは未対応）
- 同じフォルダ・同じ名前の対象に並行アップロードを走らせるとレース条件で重複作成になるため、Agent ワークフローでは逐次実行すること
- バイナリファイル（PPTX/PDF など）の revision は標準で 30 日 / 100 件の早い方が上限。長期保存が必要なら `--keep-forever` を付ける
- `--overwrite` は `drive.file` スコープの仕様上、この CLI で作成したファイルにのみ有効。Drive UI 等で手動作成された同名ファイルは検出はされるが `files.update` が 403 を返すため、別名で新規作成するか Drive UI で削除してから再実行する
  - `drive.file` スコープ: OAuth スコープの一種で、このアプリが作成したファイルにのみ書き込み権限を与える（他アプリ / Drive UI 作成ファイルは読み取り専用になる）。`drive.readonly` が同名検出のためのメタデータ参照、`drive.file` が create / update 実行、という役割分担

## エラー対処

- 403 Forbidden: 主に 2 系統ある。切り分けは「同じ ADC で別コマンド（例: `gws-cli calendar calendars`）が通るか」で判定
  - 読み取り系コマンドも 403 → ADC のスコープ不足。`gcloud auth application-default login --scopes=...` を再実行
  - 読み取り系は通るが `drive upload --overwrite` のみ 403 → `drive.file` スコープ制約（下記の `--overwrite` 実行時 403 を参照）
- 404 Not Found: イベント ID / ドキュメント ID / フォルダ ID が不正、または `--calendar-id` を間違えている
- `event list --all-pages` で exit 2: `--time-min` と `--time-max` の両方を指定する。長期レンジ全件取得の事故防止のための仕様
- `File '...' already exists`: 同名ファイルが既存。`--overwrite` を付けるか `--name` で別名に変更
- `Multiple files named '...' exist`: 同名ファイルが 2 件以上。Drive UI で整理してから再実行
- `Folder ... is on a shared drive`: 共有ドライブのフォルダは未対応。マイドライブのフォルダ ID を指定
- `--overwrite` 実行時に 403 Forbidden: 対象ファイルがこの CLI 以外（Drive UI 等）で作成されている可能性が高い。`drive.file` スコープは他ツール作成ファイルを更新できない。`--name` で別名にして新規作成するか Drive UI で削除してから再実行
- `'calendar attachments' is deprecated` warning: 新コマンド `gws-cli calendar event get` に切り替える。挙動はほぼ上位互換 (event 全体 + `links` フィールド付き)
