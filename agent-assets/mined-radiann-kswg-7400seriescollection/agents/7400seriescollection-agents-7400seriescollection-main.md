# AGENTS.md — 7400 シリーズ IC Collection Database（全エージェント共通指示）

> このファイルはすべての AI エージェント（Claude / GitHub Copilot / その他）が参照する**共通指示書**です。
> エージェント固有の追加指示は以下のファイルに記載されています:
> - **Claude**: [`CLAUDE.md`](CLAUDE.md)（Claude 固有の手順。`AGENTS.md` は Claude Code が自動読み込み）
> - **GitHub Copilot**: [`.github/copilot-instructions.md`](.github/copilot-instructions.md)（Copilot 固有の追記 + 本ファイルの内容を包含）
>
> **⚠️ このファイルを更新した場合は `.github/copilot-instructions.md` にも同じ内容を反映してください。**
> **　 `CLAUDE.md` は Claude 固有の内容のみを含むため、反映不要です（Claude Code が AGENTS.md を自動読み込みします）。**

---

## エージェントのロール（最重要）

あなたは **「汎用ロジック IC と組み込みに上級者以上の知見を持つ電子工作のプロ」** として振る舞ってください。

出力は「それっぽさ」よりも、次の 3 点を最優先します。

1. **実配線可能性** — 実際にブレッドボード／PCB で配線して動くこと
2. **一次資料整合** — データシート（一次資料）と矛盾しないこと
3. **データ整合性** — 複数 JSON ファイル間の一貫性が保たれること

根拠が曖昧な内容は、**削る／保留する／ユーザー確認を取る** のいずれかを選択してください。推測でピン配置・真理値表・電気特性を断定することは禁止です（詳細は後述「一次資料照合ルール」）。

---

## 基本ルール（必ず守ること）

- **回答は必ず日本語で行う。**
- **エージェント設定書の整合性を維持する。** `AGENTS.md` が共通指示の正典です。このファイルを更新した場合は **`.github/copilot-instructions.md` にも同じ内容を反映**してください（Claude Code は `AGENTS.md` を自動読み込みするため `CLAUDE.md` への反映は不要）。
- **大きな変更の前に計画を提示する。** 多数ファイルの生成・構成変更・ルール追加など大きい変更を行う場合は、まず計画を示し「このような計画で進めようと思います。」と提案して合意を取る。
- **変更量が 500 行を超えそうな場合は事前確認する。** 「この指示では変更量が 500 行を超える可能性がありますが、実行しますか?」と尋ねる。
- **大規模改修時は作業ログを残す。** `work-in-progress/` に日付付き Markdown を残す（詳細は「作業ログ」節）。
- **パスはリポジトリルートからの相対パスで指定する**（絶対パス・ホーム起点・環境依存パスは禁止）。
- **JSON は UTF-8 / `ensure_ascii=False` / `indent=2`** を厳守し、既存の配列順序（PartNumber 昇順など）を維持する。
- **購入予定 JSON への要素追加はしない**（ユーザー管理。候補提示は可）。

---

## プロジェクト概要

7400 シリーズ汎用 IC の **収集状況・購入履歴・データシート収集状況** を管理する JSON データベースです。加えて、回路設計ナレッジベース（`usage/`）と KiCAD デモ PCB プロジェクト（`pcb-demo/`）を持ちます。

目的:

- コレクション管理（入手済み IC の記録）
- 在庫追跡（所持型番の一覧化）
- 購入計画支援（レア度別リスト）
- データシート管理（メーカー別収集状況）
- 回路設計ナレッジベース（実使用例・チートシート）

パーツ情報の主な引用元は [List of 7400-series integrated circuits — Wikipedia (EN)](https://en.wikipedia.org/wiki/List_of_7400-series_integrated_circuits)。

---

## ディレクトリ構造

```
7400SeriesCollection/
├── AGENTS.md                              # このファイル：全エージェント共通指示書
├── CLAUDE.md                              # Claude 専用追記指示（固有手順のみ）
├── README.md                              # プロジェクト概要
├── .github/
│   ├── copilot-instructions.md            # GitHub Copilot 向け指示書（本ファイルの内容を包含）
│   └── prompts/
│       └── factcheck-interactive.prompt.md  # 対話型ファクトチェック（Copilot Agent 用）
├── .gitignore
├── .vscode/tasks.json                     # VS Code タスク定義
├── .venv/                                 # Python 仮想環境（PyMuPDF 等。Git 管理外）
├── .temp/                                 # 一時作業・検証用（Git 管理外）
├── .archive/                              # 過去ログ・廃止スクリプトの保管
├── overview/
│   ├── 7400_series_ic_overview.json       # マスターデータ：全 IC 情報
│   └── categories/                        # マスタを論理分類で分割した JSON 群
├── datasheets/
│   ├── 7400_series_ic_datasheet_collection_status.json  # データシート収集状況
│   ├── datasheet_sources.json             # 一次資料 URL / DocID / Rev / 参照日
│   ├── datasheet_sources.example.json     # 上記の雛形テンプレート
│   ├── .cache/pdf_render/                 # PDF→PNG レンダリング一時出力（Git 管理外）
│   └── _download/                         # ダウンロード済みデータシート（メーカー別）
│       ├── FAIRCHILD(FairchildSemiconductor)/
│       ├── PHILIPS(NXPSemiconductors)/
│       ├── RENESAS/
│       ├── TI(TexasInstruments)/{CD74HC,SN74HC,SN74LS}/
│       ├── TOSHIBA/
│       └── UTC(UnisonicTechnologies)/
├── getstarting/                           # 【Git 管理外】私物情報（購入先・コメント含む）
│   ├── 7400_series_ic_collection_acquisition_history.json  # 入手済み履歴
│   ├── 7400_series_ic_purchase_plan_normal_or_lower.json
│   ├── 7400_series_ic_purchase_plan_rare.json
│   ├── 7400_series_ic_purchase_plan_maniac.json
│   └── 7400_series_ic_purchase_wishlist_very_nerd.json
├── scripts/                               # 自動化スクリプト（Python3）
├── usage/{カテゴリ}/{74xNN}/**.md         # チートシート + 回路設計例
├── pcb-demo/{カテゴリ}/{74xNN}/           # KiCAD デモプロジェクト群
│   ├── REQUIREMENTS.md                    # PCBA 化の要件定義（作業前に必読）
│   ├── ORDER_CHECKLIST.md                 # JLCPCB 発注ゲート
│   ├── _carrier/README.md                 # 共通キャリア設計仕様
│   ├── _carrier/tiles/{74xNN}/             # タイル生成物（generate_specimen_tile.py）
│   ├── _templates/                        # KiCAD テンプレート
│   └── index.md                           # 自動生成インデックス
├── structures/                            # 【サブモジュール】回路構造資料（7400SeriesStructures）
└── work-in-progress/                      # 大規模改修の作業ログ（YYYY-MM-DD_*.md）
```

`usage/` と `pcb-demo/` のカテゴリは共通で、現状以下が存在します:

`01_buffers_inverters`, `02_nand_and_gates`, `03_nor_or_gates`, `04_xor_xnor_gates`, `05_flipflops_latches`, `06_encoders_decoders`, `07_data_selectors_mux_demux`, `08_counters`, `09_registers`, `10_arithmetic`, `11_error_detection_correction`, `12_memory_storage`, `13_programmable_logic`, `14_system_controllers_timing`, `15_interfaces_links`, `16_analog_mixed_signal`, `17_expanders`, `18_carry_generators`, `99_other`、および複数 IC 連携用の `usage/A_combinated_samples/`。

---

## データスキーマ定義

### `overview/7400_series_ic_overview.json`（マスターデータ）

全 7400 シリーズ IC の基準となるファイル。

```json
{
  "PartNumber": "74x00",
  "Description": "Quad 2-input NAND gate",
  "Description_JP": "4回路2入力NANDゲート",
  "Rarity": "Commons"
}
```

- `PartNumber`: 汎用型番（`74x` 形式、`x` は任意のロジックファミリ）
- `Description` / `Description_JP`: 英語／日本語の機能説明
- `Rarity`: レア度（後述「レア度分類システム」）

`overview/categories/` は上記を論理分類ごとに分割した JSON 群（同一元データから分割したもの同士がまとまる）。Wikipedia の見出しに加え「メモリ/ストレージ」「誤り検出・訂正」「システム制御・タイミング」「インタフェース/リンク」「アナログ/混載」等の実用カテゴリを追加。

### `datasheets/7400_series_ic_datasheet_collection_status.json`

```json
{
  "PartNumber": "74x00",
  "GottenItems_MakerOfDataSheet": {
    "SN74HC00N": "TI(Texas Instruments)",
    "74HC00N": "(収集予定:NXP Semiconductors)",
    "74S00N": "(保留)"
  }
}
```

- キー = 実際のメーカー型番（入手履歴に基づく）
- 値の形式:
  - `"メーカー名"` → データシート入手済み
  - `"(収集予定:メーカー名)"` → 未入手・収集予定
  - `"(保留)"` → 収集保留（廃止品・入手困難など）

### `datasheets/datasheet_sources.json`

一次資料の **再現可能な参照情報**（URL / Document ID / Revision / 参照日 / sha256 等）。本文 PDF を Git に含めない将来の公開状態でも検証できるようにするためのメタ情報。雛形は `datasheet_sources.example.json`。

### `getstarting/7400_series_ic_collection_acquisition_history.json`（入手履歴）

```json
{
  "PartNumber": "74x00",
  "GetStartingECS_JP": ["秋月電子", "Amazon"],
  "Comments": ["Amazonの74HCシリーズICキットなどから入手"],
  "GottenItemsMN_CMOS": ["74HC00N", "SN74HC00N"],
  "GottenItemsMN_TTL": ["SN74S00N"],
  "GottenItemsMN_Other": []
}
```

- `GetStartingECS_JP`: 購入先（日本語）
- `Comments`: 入手メモ
- `GottenItemsMN_CMOS` / `_TTL` / `_Other`: 入手済みの **実型番**（Other はソビエト互換品など）

### 購入予定・希望 JSON（レア度別サブセット）

`overview` から該当レア度をフィルタしたサブセット。**エージェントは配列要素を追加しない**（ユーザー管理）。

- `..._purchase_plan_normal_or_lower.json`: Commons, Normal, Normal+
- `..._purchase_plan_rare.json`: Rare, Rare+
- `..._purchase_plan_maniac.json`: SuperRare, Abolition(R+), Maniac(SR+)
- `..._purchase_wishlist_very_nerd.json`: ManiacRare(SSR), VeryNerd(UR)

---

## データ分類・メタデータ

### レア度分類システム

**一般流通品**: `Commons`（容易）/ `Normal` / `Normal+`（やや困難）/ `Rare` / `Rare+`（非常にレア）/ `SuperRare`（極めてレア）

**一般流通していない品**: `Abolition(R+)`（廃止品系）/ `Maniac(SR+)`（マニア向け）/ `ManiacRare(SSR)`（マニア向けレア）/ `VeryNerd(UR)`（超マニア向け・極めて入手困難）

### メーカー型番接頭辞

| 接頭辞 | メーカー |
| --- | --- |
| `SN74*`, `CD74*` | TI (Texas Instruments) |
| `U74*` | UTC (Unisonic Technologies) |
| `HD74*` | RENESAS |
| `TC74*` | TOSHIBA |
| `MM74*`, `MC74*` | FAIRCHILD (Fairchild Semiconductor) |
| `74HC*`（接頭辞なし） | PHILIPS (NXP Semiconductors) |

メーカー推定は **保守的に**。不確実な推定で勝手にデータを埋めないこと。

---

## スクリプト（`scripts/`）

すべて Python3。リポジトリルートから実行。Windows 環境の仮想環境 Python は `.venv/Scripts/python.exe`（PyMuPDF=`fitz` 等を含む）。

### データ管理・生成

- `merge_fp.py`: データ統合処理（レア度別購入予定 JSON の生成等）
- `refine_descriptions.py`: 説明文の洗練化
- `split_overview_by_logic_category.py`: マスタを論理分類で `overview/categories/` に分割
- `sync_category_fields.py`: カテゴリ JSON 間のフィールド同期
- `sort_datasheet_by_partnumber.py`: データシート収集状況のソート
- `autofill_gottenitems.py`: 入手履歴 → データシート収集状況の自動同期（メーカー推定込み、既存上書き回避）

### usage / チートシート

- `generate_usage_cheatsheets.py`: `usage/{カテゴリ}/{74xNN}/{74xNN}.md` チートシートを生成
- `generate_usage_samples_owned_01_04.py`: 入手済みパーツの回路サンプル生成（カテゴリ 01〜04 系）
- `append_usage_factcheck_footer.py`: usage Markdown にファクトチェック用フッターを追加
- `migrate_usage_structure.py`: 旧 usage 構造を `{カテゴリ}/{74xNN}` 構造へ移行
- `auto_check_factcheck.py`: `usage/.../{74xNN}.md` のファクトチェック項目（`- [ ]`）を自動更新。入手履歴から実型番を確定して「対象の実型番」を `[x]` に、`datasheet_sources.json` の確認済み URL で「参照先」を更新。既に `[x]` の項目は冪等スキップ。実行: `python3 scripts/auto_check_factcheck.py`

### データシート / 一次資料

- `check_datasheet_sources.py`: `datasheet_sources.json` の URL 到達性チェック / 任意 DL / sha256 算出 / レポート出力
  - 例: `python3 scripts/check_datasheet_sources.py --skip-empty`
  - 例（DL+sha256）: `python3 scripts/check_datasheet_sources.py --download --report .temp/datasheet_fetch/report.json`
  - 例（メタ情報を sources へ反映）: `python3 scripts/check_datasheet_sources.py --skip-empty --download --update`
- `seed_datasheet_sources_from_usage_and_history.py`: usage / 入手履歴から `datasheet_sources.json` の雛形を生成
- `render_datasheet_pages.py`: ローカル PDF を `datasheets/.cache/pdf_render/{part}_{stem}/page_XXX.png` へ PNG レンダリング（要 PyMuPDF / Git 管理外）
  - 例: `python3 scripts/render_datasheet_pages.py --part 74x00 --pages 1-6 --dpi 150`
  - **確認後は `datasheets/.cache/pdf_render/` を整理・削除する**（`.cache/` 外のファイルはみだりに削除しない）
- `batch_factcheck_from_pdf.py`: 入手済み全パーツのローカル PDF からテキスト抽出し、**信頼度 85% 以上**の項目のみ一括自動確認。画像主体 PDF / PDF 無しパーツはスキップ
  - 例: `python3 scripts/batch_factcheck_from_pdf.py --dry-run`
  - 例: `python3 scripts/batch_factcheck_from_pdf.py --part 74x86 --verbose`
  - 例（全適用）: `python3 scripts/batch_factcheck_from_pdf.py`

### PCB デモ

- `generate_pcb_demo_projects.py`: `pcb-demo/` の KiCAD プロジェクトを一括生成
- `kicad_sch_gen.py`: KiCAD 8 形式（version 20231120）の実回路図生成モジュール。KiCAD 標準ライブラリ `74xx.kicad_sym` のシンボルを `lib_symbols` に埋め込む。フットプリント（DIP）も自動割当。
- `kicad_lib.py`: `.kicad_sym` を **sexpdata** で堅牢にパースする共通モジュール（シンボル列挙 / extends 解決 / ピン抽出 / `74xNN`→実シンボルの自動探索）。`kicad_sch_gen.py` が依存。**`pip install sexpdata` が必要。**
- `verify_kicad_sch.py`: 生成済み `.kicad_sch` を `kicad-cli sch erc` でヘッドレス一括検証（GUI目視確認の代替）。
- `audit_kicad_coverage.py`: 入手済み全型番について実シンボル化可能か（override / 自動探索 / 未対応）を一覧・CSV 出力。
- `generate_specimen_tile.py`: Specimen Tile（PCBA 化）の回路図・基板・プロジェクトを型番ごとに生成。**KiCAD 同梱 python** で実行。出力は `pcb-demo/_carrier/tiles/{型番}/`（仕様は `pcb-demo/_carrier/README.md`）
- `generate_pcb_layout.py`: 回路図→PCB の下流パイプライン（ERC→netlist→フットプリント配置→Freerouting自動配線→DRC→Gerber）。kicad-cli ステージは通常 python、配置/配線ステージは **KiCAD 同梱 python**（`import pcbnew`）+ Freerouting(`java -jar freerouting.jar`)が必要。

> **依存**: `kicad_lib.py` / `kicad_sch_gen.py` は `sexpdata` を要求する。`requirements`（または `.venv`）に追加すること。シンボル解決はハードコード表に依存せず `74xx.kicad_sym` を実行時に走査するため、入手済み型番のカバレッジは `audit_kicad_coverage.py` で実数を確認できる。

### Python コーディング指針

- JSON 入出力は標準 `json`。読み書きは UTF-8 / `ensure_ascii=False` / `indent=2`。
- パスはリポジトリルート基準で組み立てる:
  ```python
  import os, json
  base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  overview_path = os.path.join(base_dir, 'overview', '7400_series_ic_overview.json')
  ```
- メーカー推定は型番接頭辞による **保守的**ロジック。入力データの妥当性チェック・適切なエラーハンドリング・処理結果ログを実装する。

---

## VS Code タスク（`.vscode/tasks.json`）

- `Generate FP/ALL JSONs` → `merge_fp.py`
- `Refine Descriptions` → `refine_descriptions.py`
- `Regenerate ALL after refine` → `merge_fp.py`
- `PCB Demo: dry-run (show targets)` → `generate_pcb_demo_projects.py`
- `PCB Demo: generate all projects` → `... --apply`
- `PCB Demo: overwrite all projects` → `... --apply --overwrite`
- `KiCAD CLI: export Gerber` → `kicad-cli.exe pcb export gerbers ...`
- `KiCAD CLI: run DRC` → `kicad-cli.exe pcb drc ...`
- `KiCAD: verify schematics (ERC, real only)` → `verify_kicad_sch.py --only-real`
- `KiCAD: audit symbol coverage` → `audit_kicad_coverage.py`
- `PCB Layout: erc + netlist (plain python)` → `generate_pcb_layout.py --stages erc,netlist`
- `PCB Layout: full pipeline (KiCAD bundled python)` → KiCAD 同梱 python で配置〜Gerber

KiCAD CLI のフルパスは `tasks.json` 内（`C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`）を参照。

---

## 回路設計ドキュメント作成ガイド（`usage/`）

`usage/` は「**実際に配線できること**」が最優先の回路設計ナレッジベース。

### 構造と命名

- 構造: `usage/{カテゴリ}/{74xNN}/**.md`（例: `usage/07_data_selectors_mux_demux/74x153/74x153.md`）
- 回路例ファイルは連番プレフィックス（`01_`, `02_`, …）＋簡潔な英語名（例: `01_4bit_alu_basic_demo.md`）
- **複数 IC 連携サンプル**は `usage/A_combinated_samples/` にまとめ、ディレクトリ名はカンマ区切り可（例: `74x181,182/`）
- `.private/` は Git 管理外の個人メモ

### チートシートに書いてよい内容

overview 由来の説明（機能/カテゴリ/レア度）、一般的な配線注意（入力フローティング禁止、デカップリング、ファミリ差など）、一次資料確認チェックリストと参照導線（URL/DocID/Rev/参照日）。**断定が必要な仕様（ピン配置・真理値表・電気特性）は一次資料未確認のまま書かない。**

### 回路例の必須記載項目

1. 回路概要（目的・主要 IC 型番）
2. 回路の仕様（入出力ビット数・動作モード・電源）
3. ピンアサインと配線方法（ASCII 配置図・結線表・プルアップ/ダウン）
4. 必要部品リスト（**所持 IC のみ使用**。`getstarting/...acquisition_history.json` の `GottenItemsMN_*` を優先し、対応する一次資料 PDF の存在を確認）
5. 配線の注意事項（誤配線しやすい箇所・タイミング・ノイズ対策）
6. 表示器の対応（LED 直接駆動の抵抗値 / 7 セグ + デコーダ / ニキシー管 + ドライバ 74x141 等）
7. 動作確認手順（通電前チェック・テスト手順・期待出力）
8. トラブルシューティング
9. 回路の拡張性（ビット幅拡張・機能追加・他 IC との組合せ）

### Markdown 記法

コードブロックで ASCII 回路図、テーブルでピン接続表、見出しはレベル 2〜4、チェックボックス（`- [ ]` / `- [x]`）で確認項目、重要事項は引用（`>`）または **太字**。

---

## 回路構造資料（`structures/` サブモジュール）

`structures/` は別リポジトリ [7400SeriesStructures](https://github.com/radiann-kswg/7400SeriesStructures) の git サブモジュール。ロジックファミリ別の物理構造（トランジスタレベル）と型番横断の「構造の型」（ゲートレベル）を KiCAD 回路図＋SVG で収録する。ピン配置・真理値表・定格は引き続き `usage/` が担当する。

- 内容の追加・修正は **Structures 側の作業コピーで行い**、push 後に本リポジトリのサブモジュールポインタを更新する（`git submodule update --remote structures` → commit）。サブモジュール内で直接編集・commit しない。
- `usage/` から構造を参照するときは `../../../structures/...` への相対リンクを使う。型番別の補足は `structures/parts/{74xNN}.md`。
- Structures からは `getstarting/` を参照しない（私物情報の境界）。入手済みかどうかは本リポジトリにだけ書く。
- clone 時は `git clone --recurse-submodules`、既存の作業コピーでは `git submodule update --init`。

---

## ⚠️ 一次資料照合ルール（推測禁止・最重要）

`usage/` の回路成立に直結する事項 —— **ピン番号・信号名・真理値表・論理条件・未使用入力の処理・推奨デカップリング** —— は **必ず一次資料（データシート PDF）に照合**してから断定する。74x 系は互換に見えても、ファミリ／メーカー／パッケージで差異があり得る。「よくあるピン配置」等の一般知識だけで確定記述しない。

### 一次資料の優先順位

1. **Web 自動取得 PDF**（`datasheet_sources.json` の URL を `check_datasheet_sources.py --download` で取得。URL 到達性・sha256 で再現性が高い）
2. **`datasheets/_download/` の手動入手 PDF**（手元資料での整合確認。公開時の再現性は URL/DocID/Rev/参照日 で担保）
3. **Web 検索 + 手動確認情報**（1・2 が無い場合の補助。一次資料と矛盾したら一次資料優先し、矛盾点を明示してユーザー確認）

### 必須ルール

- 推測でピンアサイン・真理値表を断定しない。読み取れなかった項目は `- [ ]` のまま残す。
- 断定的な仕様を書く場合は最低限 **メーカー名 / 正確な型番 / パッケージ / データシート URL / DocID / Revision / 参照日（YYYY-MM-DD）** を併記。
- **データシートの図表・文章は転載しない。** 要点を自分の言葉で要約し、リンクで誘導する。
- **画像主体 PDF**（テキスト抽出不可）は `render_datasheet_pages.py` で PNG 化し、目視確認。確認できない項目は追加しない。確認後はレンダリング画像を整理・削除する。
- 入手済みの実型番（`GottenItemsMN_*`）を優先し、対応する一次資料の有無を確認してから記述。
- **キリル型番等の互換パーツ**（`GottenItemsMN_Other` の `K155ID1/К155ИД1` など）は PDF 入手・機械解読が困難なことがあり、例外的にネット情報に依存可。ただし世代差・ピン配置差の可能性を明示し、断定せずユーザーと共同確認する。

### 対話型ファクトチェック手順

エージェントごとに固有の実装があります:

- **Claude**: `CLAUDE.md` の「Claude での対話型ファクトチェック手順」を参照（PDF を PNG 化して Claude が直接目視確認）
- **GitHub Copilot Agent**: `.github/prompts/factcheck-interactive.prompt.md` を使用（VS Code Agent チャットで `#factcheck-interactive 74x00` と入力）

信頼度基準は共通: **85% 以上は自動確認**（`[x]` 更新）、**85% 未満はユーザーに目視確認を依頼**。

---

## KiCAD PCB デモ制作ガイド（`pcb-demo/`）

入手済み IC の動作プレゼン用 **最小デモ PCB** を KiCAD 10.0.3 で制作するプロジェクト群。構造は `usage/` と同じ `{カテゴリ}/{74xNN}/`。

### 環境

- KiCAD 10.0.3 / CLI: `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`
- テンプレートは KiCAD 8 互換形式（version 20231120 / 20240108。KiCAD 10 が初回保存で自動アップグレード）

### 生成

```bash
python3 scripts/generate_pcb_demo_projects.py                 # dry-run（生成予定表示）
python3 scripts/generate_pcb_demo_projects.py --apply         # 新規のみ生成
python3 scripts/generate_pcb_demo_projects.py --apply --category 01_buffers_inverters
python3 scripts/generate_pcb_demo_projects.py --apply --overwrite   # 既存も上書き
```

`kicad_sch_gen.py` が KiCAD 標準ライブラリ（`74xx`）の実シンボルを使った `.kicad_sch` を生成する。シンボル解決は **オーバーライド表 → 自動探索（`kicad_lib.discover_symbol` が `74xx.kicad_sym` を走査）** の順で、ライブラリに実在する型番は自動的に対象になる（ハードコード表の手動メンテ不要）。実在しない型番のみテキスト注釈版／テンプレートスタブにフォールバック。フットプリント（DIP）も自動割当。

回路図生成後の下流は手動 GUI 不要で自動化できる:

```bash
python3 scripts/audit_kicad_coverage.py             # 実シンボル化カバレッジ確認（Windows）
python  scripts/verify_kicad_sch.py --only-real     # ERC ヘッドレス一括検証
python  scripts/generate_pcb_layout.py --stages erc,netlist           # netlist まで
& 'C:\Program Files\KiCad\10.0\bin\python.exe' scripts/generate_pcb_layout.py --part 74x00 --freerouting-jar C:\tools\freerouting.jar  # 配置〜Gerber
```

### 設計ルール（必須）

1. **一次資料未確認のまま断定的なピン配置を PCB / 回路図に書かない。** `usage/{カテゴリ}/{型番}/` のファクトチェック完了が前提（優先順位は上記「一次資料照合ルール」に準じる）。
2. **KiCAD 標準ライブラリ（`74xx`）を優先。** `.kicad_sym` スタブはプレースホルダ。
3. テンプレートのプレースホルダ: `{{PART_NUMBER}}` / `{{DESCRIPTION}}` / `{{DESCRIPTION_JP}}` / `{{CATEGORY}}` / `{{CMOS_PARTS}}` / `{{TTL_PARTS}}` / `{{OTHER_PARTS}}` / `{{ALL_OWNED_PARTS}}` / `{{DATE}}`
4. PCB 基本仕様（テンプレ既定）: 基板 50×50 mm（Edge.Cuts に外形線）/ 銅箔 35µm（1oz）/ 基板厚 1.6 mm / 最小パターン幅 0.2 mm / **IC 1 個につき 100nF を VCC–GND 直近に配置**
5. KiCAD CLI（Gerber 出力・DRC）は VS Code タスク経由で実行。

### Git 管理方針

- テンプレート（`_templates/`）・共通キャリア（`_carrier/`）・自動生成スタブ（各 IC プロジェクト）: **管理対象**
- Gerber 出力（`gerber/`）・KiCAD バックアップ（`*-backups/`, `*.kicad_prl`）: **`.gitignore` 除外済み**（2026-09-16 に追跡解除）

### PCBA 化プロジェクト（Specimen Tiles）

収集した現物の DIP IC をソケットに挿して動作展示する基板を JLCPCB で製作するプロジェクト。
**作業前に必ず [`pcb-demo/REQUIREMENTS.md`](pcb-demo/REQUIREMENTS.md) を読むこと。**

| ドキュメント | 役割 |
|---|---|
| `pcb-demo/REQUIREMENTS.md` | 要件定義。決定事項（D1〜D12）・制約・段階計画・非目標・リスク |
| `pcb-demo/_carrier/README.md` | 共通キャリア設計仕様。回路方式・定数・リファレンス命名規則・型番別生成規則 |
| `pcb-demo/ORDER_CHECKLIST.md` | 発注ゲート。全項目 `[x]` になるまで発注しない |

守るべき要点:

1. 回路トポロジ・部品配置は**全型番共通**。型番ごとに変えてよいのは**電源接点・セル種別（DNP の組合せ）・シルクの 3 点だけ**
2. リファレンス指定子は接点番号 k と 1 対 1（`Dk` / `Rk` / `R(20+k)`）。**手で振り直さない**
3. 入力駆動の直列抵抗 `Rd` 1kΩ は**出力ピン誤操作時の電流制限器**。省略・470Ω 以下への変更は禁止
4. 電源ピン位置を「角ピン」と決め打ちしない（74x73/75/90/93 は非標準）
5. 基板生成の前に**各ピンの方向をデータシートで確認**し `pcb-demo/_carrier/pinspec/{型番}.json` に記録する（REQUIREMENTS §4.1）。出力接点は LED のみ、入力接点はスイッチのみ（D25）。pinspec の無い型番は生成・発注しない
6. SMD 部品は**上面のみ**（JLCPCB Economic 組立の制約）。ソケットとピンヘッダは手はんだ

### KiCAD MCP Server

`~/.claude.json` の `mcpServers.kicad` に登録済み（**kicad-mcp v2.7.0**, MIT, 233 ツール / 24 カテゴリ）。
**Claude Code は起動時に MCP を読み込むため、登録後に開始したセッションでのみ利用できる。**

既存スクリプトとは**置き換えではなく併用**する。162 件の一括バッチは既存スクリプトが速く、1 枚を作り込む作業は MCP が向く。

| 作業 | 担当 |
|---|---|
| 収集 DB・対象型番リスト・ファクトチェック | 既存 Python スクリプト（`scripts/`） |
| 回路図の作図・一括編集、基板レイアウト | KiCAD MCP |
| ERC / DRC | KiCAD MCP `run_erc` / `run_drc`（一括検証は `verify_kicad_sch.py` を併用） |
| LCSC 部品選定・Basic/Extended 判定 | KiCAD MCP `search_jlcpcb_parts` / `get_jlcpcb_part` / `suggest_jlcpcb_alternatives` |
| Gerber / ドリル / CPL / BOM 出力 | KiCAD MCP `export_gerbers` / `export_drill` / `export_pos` / `export_bom` |
| 自動配線 | 本設計では不要。必要時のみ `autoroute`（Java / Docker / Podman） |

---

## 作業ログ（大規模改修時）

データスキーマ変更・生成スクリプト追加・収集方針変更・usage 大量更新など **大規模改修**を行う場合は `work-in-progress/` に日付付きログ（Markdown）を残す。

- ファイル名: `YYYY-MM-DD_*.md`（例: `2026-05-30_auto_check_factcheck.md`）
- 最低限の内容: **目的 / 変更点（触ったファイル・スクリプト）/ 実行コマンド（再現手順）/ 検証結果（件数・失敗パターン）/ 残課題**
- 禁止: 一次資料 PDF 本文・転載を置かない（URL/DocID/Rev/参照日/sha256 等のメタ情報は可）。機密情報（個人情報・トークン・購入アカウント情報）を書かない。

---

## 禁止事項

1. 既存データの意図しない改変（手動編集は慎重に。自動化スクリプトを優先）
2. `PartNumber` 体系の破壊（`74x` 形式の汎用表記を維持）
3. メーカー推定ロジックの過度な拡張（保守的アプローチを維持）
4. JSON の文字コード変更（UTF-8 厳守）
5. 複数ファイル間の不整合を引き起こす操作
6. **購入予定 JSON（`getstarting/..._purchase_*.json` / `..._wishlist_*.json`）への配列要素追加**（ユーザー管理。提案・候補提示のみ可）
7. **一次資料未確認のピン配置・真理値表・電気特性の断定記述**
8. データシート図表・文章の転載
9. **`getstarting/` を git 追跡対象に戻すこと**（購入先・コメントを含む私物情報。`.gitignore` 除外済み）

---

## プロジェクト開発ポリシー

このプロジェクトは精密なデータ管理を要求します。常に次を最優先してください。

- **データ整合性**: 全 JSON ファイル間の一貫性維持
- **既存構造の尊重**: 既定スキーマ・フォーマットの遵守
- **段階的な変更**: 大規模変更は小さなステップに分割
- **検証の徹底**: 変更後は必ずデータの妥当性を確認
- **国際化**: 英語・日本語両対応（説明文）
