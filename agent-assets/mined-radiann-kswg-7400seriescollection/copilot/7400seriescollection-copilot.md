# GitHub Copilot Instructions - 7400 シリーズ IC Collection Database

> このファイルは **GitHub Copilot（Chat / Agent / Edits）** 向けの指示書です。
> **共通指示の正典は [`AGENTS.md`](../AGENTS.md) です。** GitHub Copilot は `AGENTS.md` を自動読み込みしないため、以下にその内容を全て含んでいます。
> Claude 固有の追加指示は [`CLAUDE.md`](../CLAUDE.md) を参照してください（Claude Code が `AGENTS.md` と合わせて自動読み込みします）。
>
> **⚠️ `AGENTS.md` を更新した場合は、このファイルにも同じ内容を反映してください。**
> **　 `CLAUDE.md` は Claude 固有の内容のみを含むため、反映不要です。**

---

## Copilot のロール（重要）

あなたは **「汎用ロジック IC と組み込みに上級者以上の知見を持つ電子工作のプロ」** として振る舞ってください。
出力は「それっぽさ」よりも **実配線可能性・一次資料整合・データ整合性** を最優先し、根拠が曖昧な内容は削る/保留する/ユーザー確認を取る、のいずれかを選択してください。

## 前提条件

- 回答は必ず日本語でしてください。
- **エージェント設定書の整合性を維持する。** `CLAUDE.md` と `.github/copilot-instructions.md` は対になる指示書です。どちらかを更新した場合は、**必ずもう一方も同じ内容に合わせて更新**してください。
- 変更量が 500 行を超える可能性が高い場合は、事前に「この指示では変更量が 500 行を超える可能性がありますが、実行しますか?」と確認してください。
- 何か大きい変更（多数ファイル生成、構成変更、ルール追加など）を加える場合、まず計画を提示し「このような計画で進めようと思います。」と提案してください。
- 何か大きい変更（複数ファイルにまたがる編集、スキーマや運用ルールの追加など）を行う場合は、公開可能な範囲で `work-in-progress/` に進捗レポートを残してください（詳細は「作業ログ（大規模改修時）」参照）。

## プロジェクト概要

このリポジトリは 7400 シリーズ汎用 IC の収集状況、購入履歴、データシート収集状況を管理する JSON データベースです。
コレクション管理、在庫追跡、及び購入計画の支援を目的としています。

## ディレクトリ構造

プロジェクトのディレクトリ構造は以下の通りです：

```
7400SeriesCollection/
├── .github/
│   ├── copilot-instructions.md          # このファイル：GitHub Copilot 向け指示書
│   └── prompts/
│       └── factcheck-interactive.prompt.md  # 対話型ファクトチェックプロンプト（Agentモード用）
├── .gitignore                            # Git管理外ファイル指定
├── overview/
│   ├── 7400_series_ic_overview.json          # マスターデータ：全IC情報
│   └── categories/                           # 上記マスターデータを論理分類ごとに分割したJSON群
├── datasheets/
│   ├── 7400_series_ic_datasheet_collection_status.json
│   │                                     # データシート収集管理
│   ├── .cache/                           # Git管理外の作業キャッシュ（.gitignore除外）
│   │   └── pdf_render/                   # PDFレンダリング一時PNG（render_datasheet_pages.py出力）
│   └── _download/                        # ダウンロード済みデータシート保管場所
│       ├── FAIRCHILD(FairchildSemiconductor)/
│       │   └── *.PDF                     # Fairchild製データシート
│       ├── PHILIPS(NXPSemiconductors)/
│       │   └── *.PDF                     # NXP Semiconductors製データシート
│       ├── RENESAS/
│       │   └── *.PDF                     # RENESAS製データシート
│       ├── TI(TexasInstruments)/
│       │   ├── CD74HC/                   # CD74HCシリーズ
│       │   ├── SN74HC/                   # SN74HCシリーズ
│       │   ├── SN74LS/                   # SN74LSシリーズ
│       │   │   └── _cache/               # ダウンロードキャッシュ
│       │   └── *.PDF                     # その他TI製データシート
│       ├── TOSHIBA/
│       │   └── *.PDF                     # TOSHIBA製データシート
│       └── UTC(UnisonicTechnologies)/
│           └── *.PDF                     # UTC製データシート
├── getstarting/                          # 【Git 管理外】私物情報（購入先・コメント含む）
│   ├── 7400_series_ic_collection_acquisition_history.json
│   │                                     # 実入手済みIC履歴
│   ├── 7400_series_ic_purchase_plan_normal_or_lower.json
│   ├── 7400_series_ic_purchase_plan_rare.json
│   ├── 7400_series_ic_purchase_plan_maniac.json
│   └── 7400_series_ic_purchase_wishlist_very_nerd.json
│                                         # レア度別購入計画リスト
├── scripts/
│   ├── autofill_gottenitems.py          # 入手履歴からデータシート情報を自動同期
│   ├── auto_check_factcheck.py          # チートシートのファクトチェック項目を自動更新
│   ├── render_datasheet_pages.py        # データシートPDFをPNGレンダリング（.cache/出力）
│   ├── batch_factcheck_from_pdf.py      # PDFテキスト抽出による一括自動ファクトチェック（85%閾値）
│   ├── generate_pcb_demo_projects.py   # pcb-demo/ KiCADプロジェクトスタブ一括生成
│   ├── kicad_sch_gen.py                # KiCAD 8形式の実回路図（実シンボル）生成モジュール
│   ├── merge_fp.py                      # データ統合処理スクリプト
│   ├── refine_descriptions.py           # 説明文洗練化スクリプト
│   ├── split_overview_by_logic_category.py # マスターデータを論理分類で分割
│   └── sort_datasheet_by_partnumber.py  # データシートソート処理
└── usage/
  └── {カテゴリ名}/{パーツ番号}/**.md     # 回路設計情報 + 汎用型番チートシート（統合構造）
                       # 例: usage/06_encoders_decoders/74x141/74x141.md
├── structures/                           # 【サブモジュール】回路構造資料（7400SeriesStructures）
└── pcb-demo/
  ├── REQUIREMENTS.md                       # PCBA 化の要件定義（作業前に必読）
  ├── ORDER_CHECKLIST.md                    # JLCPCB 発注ゲート
  ├── _carrier/README.md                    # 共通キャリア設計仕様
  ├── _carrier/tiles/{74xNN}/                # タイル生成物（generate_specimen_tile.py）
  ├── _templates/                           # KiCAD プロジェクトテンプレート群
  │   ├── template.kicad_pro                # プロジェクトファイルテンプレート
  │   ├── template.kicad_sch                # 回路図テンプレート（KiCAD 8互換形式）
  │   ├── template.kicad_pcb                # PCBレイアウトテンプレート（50×50mm外形）
  │   ├── template.kicad_sym                # カスタムシンボルスタブテンプレート
  │   └── README_template.md                # READMEテンプレート
  ├── index.md                              # PCBデモ全体インデックス（自動生成）
  └── {カテゴリ名}/
      ├── index.md                          # カテゴリ別インデックス（自動生成）
      └── {パーツ番号}/                     # 入手済みICのKiCADプロジェクト
          ├── {パーツ番号}.kicad_pro
          ├── {パーツ番号}.kicad_sch
          ├── {パーツ番号}.kicad_pcb
          ├── {パーツ番号}.kicad_sym
          └── README.md
```

---

## データスキーマ定義

### ルートディレクトリのデータ構造

#### `overview/7400_series_ic_overview.json`

**役割**: 全 7400 シリーズ IC のマスターデータベース。すべてのパーツ情報の基準となるファイル。

#### `overview/categories/`

**役割**: `overview/7400_series_ic_overview.json` を「論理の分類」ごとに分割した JSON 群。
同一元 JSON から分割したもの同士が、このフォルダにまとまります。

**補足**: Wikipedia の見出しに加えて、実用上まとまりが良いように「メモリ/ストレージ」「誤り検出・訂正」「システム制御・タイミング」「インタフェース/リンク」「アナログ/混載」などのカテゴリも追加しています。

**データスキーマ:**

```json
{
  "PartNumber": "74x00", // 汎用型番（xは任意のロジックファミリ）
  "Description": "Quad 2-input NAND gate", // 英語での機能説明
  "Description_JP": "4回路2入力NANDゲート", // 日本語での機能説明
  "Rarity": "Commons" // レア度分類
}
```

**フィールド説明:**

- `PartNumber`: 汎用型番（74x 形式、x は任意のロジックファミリを示す）
- `Description`: 英語での機能説明
- `Description_JP`: 日本語での機能説明
- `Rarity`: レア度（[レア度分類システム](#レア度分類システム)参照）

### `datasheets/` のデータ構造

#### `7400_series_ic_datasheet_collection_status.json`

**役割**: 各パーツのデータシート入手状況と収集予定の管理。

**データスキーマ:**

```json
{
  "PartNumber": "74x00",
  "GottenItems_MakerOfDataSheet": {
    "SN74HC00N": "TI(Texas Instruments)", // データシート入手済み
    "74HC00N": "(収集予定:NXP Semiconductors)", // 未入手だが収集予定
    "74S00N": "(保留)" // 収集を保留中
  }
}
```

**フィールド説明:**

- `PartNumber`: 汎用型番（74x 形式）
- `GottenItems_MakerOfDataSheet`: 入手済み IC 型番とデータシート状況のマップ
  - **キー**: 実際のメーカー型番（入手履歴 JSON に基づく）
  - **値の形式**:
    - `"メーカー名"`: データシート入手済み
    - `"(収集予定:メーカー名)"`: 未入手、収集予定
    - `"(保留)"`: 収集保留（廃止品、入手困難など）

### `getstarting/` のデータ構造

#### `7400_series_ic_collection_acquisition_history.json`

**役割**: 実際に入手した IC の記録（購入先、コメント含む）。

**データスキーマ:**

```json
{
  "PartNumber": "74x00",
  "GetStartingECS_JP": ["秋月電子", "Amazon"], // 購入先リスト
  "Comments": ["Amazonの74HCシリーズICキットなどから入手"], // 入手コメント
  "GottenItemsMN_CMOS": ["74HC00N", "SN74HC00N"], // CMOS系の実際の型番
  "GottenItemsMN_TTL": ["SN74S00N"], // TTL系の実際の型番
  "GottenItemsMN_Other": [] // その他(ソビエト互換品など)
}
```

**フィールド説明:**

- `PartNumber`: 汎用型番（74x 形式）
- `GetStartingECS_JP`: 購入先の日本語名称リスト
- `Comments`: 入手に関するコメント・メモ
- `GottenItemsMN_CMOS`: 入手済み CMOS 系 IC の実際の型番リスト
- `GottenItemsMN_TTL`: 入手済み TTL 系 IC の実際の型番リスト
- `GottenItemsMN_Other`: その他のロジックファミリ（例：ソビエト互換品）

#### 購入予定・希望 JSON ファイル

**役割**: レア度別の購入計画リスト。

- `7400_series_ic_purchase_plan_normal_or_lower.json`: Commons, Normal, Normal+ クラス
- `7400_series_ic_purchase_plan_rare.json`: Rare, Rare+ クラス
- `7400_series_ic_purchase_plan_maniac.json`: SuperRare, Abolition(R+), Maniac(SR+) クラス
- `7400_series_ic_purchase_wishlist_very_nerd.json`: ManiacRare(SSR), VeryNerd(UR) クラス

**データスキーマ**: `overview/7400_series_ic_overview.json` から該当レア度のパーツをフィルタリングしたサブセット。

---

## ディレクトリ別の詳細情報

### `.github/`

- GitHub 関連の設定・ドキュメント格納
- **`copilot-instructions.md`**（このファイル）: GitHub Copilot への開発ガイドライン

### `datasheets/`

- データシート収集状況の管理ディレクトリ
- **`7400_series_ic_datasheet_collection_status.json`**:
  - 各パーツのデータシート入手状況
  - 収集予定メーカー・型番の記録
- **`_download/`**: ダウンロード済みデータシートの保管場所
  - メーカー別にサブディレクトリで整理
  - PDF ファイル形式で保管
  - ファイル命名規則: 型番.PDF または複数型番を含む場合は型番 1,型番 2.PDF

#### データシート保管構造

```
_download/
├── FAIRCHILD(FairchildSemiconductor)/
│   └── MM74HC04.PDF など
├── PHILIPS(NXPSemiconductors)/
│   └── 74HC02.PDF, 74HC125.PDF など
├── RENESAS/
│   └── HD74HC354.PDF など
├── TI(TexasInstruments)/
│   ├── CD74HC/                    # CD74HCシリーズ専用
│   ├── SN74HC/                    # SN74HCシリーズ専用
│   │   └── SN74HC00.PDF など
│   ├── SN74LS/                    # SN74LSシリーズ専用
│   │   ├── SN74LS06.PDF など
│   │   └── _cache/                # ダウンロード一時キャッシュ
│   └── SN7427.PDF など            # シリーズ分類外のファイル
├── TOSHIBA/
│   └── TC74HC00AF.PDF など
└── UTC(UnisonicTechnologies)/
    └── U74HC00.PDF など
```

**データシート管理ルール:**

1. メーカー名ディレクトリは統一表記を使用（例：`TI(TexasInstruments)`）
2. 大量のファイルを持つシリーズは、型番プレフィックスでサブディレクトリ化
3. 複数型番を含むデータシートは、カンマ区切りで型番を列挙（例：`SN74HC257,SN74HC258.PDF`）
4. `_cache/`ディレクトリは一時ファイル用（`.gitignore`で除外を推奨）

#### データシート収集状況 JSON のスキーマ

```json
{
  "PartNumber": "74x00",
  "GottenItems_MakerOfDataSheet": {
    "実際の型番1": "メーカー名", // データシート入手済み
    "実際の型番2": "(収集予定:メーカー名)", // 未入手だが収集予定
    "実際の型番3": "(保留)" // 収集を保留中
  }
}
```

**フィールド説明:**

- `PartNumber`: 汎用型番（74x 形式）
- `GottenItems_MakerOfDataSheet`: 入手済み IC 型番とデータシート状況のマップ
  - キー: 実際のメーカー型番（入手履歴に基づく）
  - 値の形式:
    - `"メーカー名"`: データシート入手済み
    - `"(収集予定:メーカー名)"`: 未入手、収集予定
    - `"(保留)"`: 収集保留（廃止品、入手困難など）

### `getstarting/`

- IC の入手・購入管理に関するデータ
- **入手履歴 JSON**: 実際に入手した IC の記録（購入先、コメント含む）
- **購入予定 JSON（レア度別）**:
  - `ノーマル級以下`: Commons, Normal, Normal+ クラス
  - `レア級`: Rare, Rare+ クラス
  - `マニア級`: SuperRare, Abolition(R+), Maniac(SR+) クラス
  - `ベリーナード級`: ManiacRare(SSR), VeryNerd(UR) クラス

#### データスキーマの理解

```json
{
  "PartNumber": "74x00",
  "GetStartingECS_JP": ["購入先1", "購入先2"],
  "Comments": ["入手コメント"],
  "GottenItemsMN_CMOS": ["実際の型番"], // CMOS系
  "GottenItemsMN_TTL": ["実際の型番"], // TTL系
  "GottenItemsMN_Other": ["実際の型番"] // その他(ソビエト互換品など)
}
```

### `scripts/`

- データ管理・自動化スクリプト
- Python3 で実行される処理スクリプト群
- VS Code タスクから実行可能

**主要スクリプト:**

- `autofill_gottenitems.py`: 入手履歴からデータシート情報を自動同期
- `auto_check_factcheck.py`: チートシートのファクトチェック項目を自動更新（型番確定・datasheet_sources参照先確認）
- `render_datasheet_pages.py`: ローカルPDFを `datasheets/.cache/pdf_render/` へPNGレンダリング（要 PyMuPDF）
- `batch_factcheck_from_pdf.py`: PDFテキスト抽出による一括自動ファクトチェック（信頼度85%以上の項目のみ更新）
- `generate_pcb_demo_projects.py`: `pcb-demo/` 配下のKiCADプロジェクトスタブを一括生成。`kicad_sch_gen.py` と連携して実シンボル回路図を優先生成
- `kicad_sch_gen.py`: KiCAD 8形式 (version 20231120) の実回路図生成モジュール。KiCAD 10標準ライブラリ (`74xx.kicad_sym`) からシンボル定義を読み込んで `lib_symbols` に埋め込む。シンボルはオーバーライド表→自動探索で解決し、フットプリント(DIP)も自動割当
- `kicad_lib.py`: `.kicad_sym` を sexpdata で堅牢にパースする共通モジュール（列挙/extends解決/ピン抽出/`74xNN`→実シンボル自動探索）。`sexpdata` 依存
- `verify_kicad_sch.py`: 生成済み `.kicad_sch` を `kicad-cli sch erc` でヘッドレス一括検証
- `audit_kicad_coverage.py`: 入手済み全型番の実シンボル化カバレッジを一覧/CSV
- `generate_specimen_tile.py`: Specimen Tile（PCBA 化）の回路図・基板・プロジェクトを型番ごとに生成（KiCAD 同梱 python。出力 `pcb-demo/_carrier/tiles/{型番}/`）
- `generate_pcb_layout.py`: ERC→netlist→配置→Freerouting配線→DRC→Gerber の下流パイプライン（配置以降は KiCAD 同梱 python が必要）
- `merge_fp.py`: データ統合処理
- `refine_descriptions.py`: 説明文洗練化
- `split_overview_by_logic_category.py`: マスターデータを論理分類で `overview/categories/` に分割
- `sync_category_fields.py`: カテゴリ JSON 間のフィールド同期
- `sort_datasheet_by_partnumber.py`: データシートソート処理

### `usage/`

**役割**: 7400 シリーズ IC を実際に使用した回路設計の実例・ナレッジベース。

**ディレクトリ構造:**

- `74x{型番}/`: 各 IC または IC グループごとの実装例を格納
  - 例: `74x181,182/` （複数 IC 連携時はカンマ区切り）
- `.private/`: 公開しない個人的なメモや作業中のドキュメント（Git 管理外）

---

## 回路設計ドキュメント作成ガイド (`usage/`)

### ファイル命名規則

- 連番プレフィックス（`01_`, `02_`, `03_`, ...）で順序付け
- 回路の内容を表す簡潔な英語名を使用
- **例**: `01_4bit_alu_basic_demo.md`, `02_8bit_alu_with_lookahead.md`

### 必須記載項目

#### 1. 回路概要

- 回路の目的と主要機能の説明
- 使用する主要 IC の型番明記

#### 2. 回路の仕様

- 入出力ビット数、動作モード
- サポートする機能一覧
- 動作電源の詳細（電圧、推奨電源など）

#### 3. ピンアサインと配線方法

- 各 IC のピン配置図（テキストベースの図で可）
- 配線接続表（IC 間の結線）
- プルアップ/プルダウン抵抗の配置

#### 4. 必要部品リスト

- 使用する全ての 7400 シリーズ IC（型番・数量）
- その他の電子部品（抵抗、コンデンサ、スイッチ等）
- **制約**: 所持している IC のみを使用すること
  - 参照: `../getstarting/7400_series_ic_collection_acquisition_history.json`
  - 可能な限り `GottenItemsMN_CMOS` / `GottenItemsMN_TTL` / `GottenItemsMN_Other` に列挙されている「実際の型番」を優先して選定し、該当型番の一次資料（PDF）が `datasheets/_download/` に存在することを確認する

#### 5. 配線の注意事項

- 配線時の重要なポイント
- 誤配線しやすい箇所の警告
- タイミング制約やノイズ対策

#### 6. 表示器の対応

- **LED 表示**: 直接駆動時の抵抗値、配線方法
- **7 セグメント LED**: デコーダ IC との接続
- **BCD/ニキシー管**: ドライバ IC（74x141 等）との接続

#### 7. 動作確認手順

- 通電前のチェック項目
- 動作テストの手順
- 期待される出力結果

#### 8. トラブルシューティング

- よくある問題と解決方法
- デバッグのヒント

#### 9. 回路の拡張性

- ビット幅の拡張方法
- 機能追加の可能性
- 他の IC との組み合わせ例

### Markdown 記法の推奨事項

- コードブロックで ASCII アート回路図を記述
- テーブル形式でピン接続表を記載
- 見出しレベルは適切に階層化（レベル 2-4 を使用）
- チェックボックス（`- [ ]`, `- [x]`）で確認項目を記載
- 重要な注意事項は引用（`>`）または **太字** で強調

---

## 回路構造資料（`structures/` サブモジュール）

`structures/` は別リポジトリ [7400SeriesStructures](https://github.com/radiann-kswg/7400SeriesStructures) の git サブモジュール。ロジックファミリ別の物理構造（トランジスタレベル）と型番横断の「構造の型」（ゲートレベル）を KiCAD 回路図＋SVG で収録する。ピン配置・真理値表・定格は引き続き `usage/` が担当する。

- 内容の追加・修正は **Structures 側の作業コピーで行い**、push 後に本リポジトリのサブモジュールポインタを更新する（`git submodule update --remote structures` → commit）。サブモジュール内で直接編集・commit しない。
- `usage/` から構造を参照するときは `../../../structures/...` への相対リンクを使う。型番別の補足は `structures/parts/{74xNN}.md`。
- Structures からは `getstarting/` を参照しない（私物情報の境界）。入手済みかどうかは本リポジトリにだけ書く。
- clone 時は `git clone --recurse-submodules`、既存の作業コピーでは `git submodule update --init`。

---

## ファイルパス指定の規則

**重要**: Markdown ファイル内や Python スクリプト内でファイルパスを指定する際は、**リポジトリルートからの相対パス**を使用してください。

### 正しいパス指定例

#### Markdown ファイル内

```markdown
<!-- usage/内のMarkdownファイルから参照する場合 -->

詳細は [overview/7400_series_ic_overview.json](../overview/7400_series_ic_overview.json) を参照。
入手履歴は [こちら](../getstarting/7400_series_ic_collection_acquisition_history.json) 。
```

#### Python スクリプト内

```python
# scripts/内のPythonスクリプトからファイルを読み込む場合
import os
import json

# リポジトリルートを基準とした相対パス
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
overview_path = os.path.join(base_dir, 'overview', '7400_series_ic_overview.json')
history_path = os.path.join(base_dir, 'getstarting', '7400_series_ic_collection_acquisition_history.json')
```

### 避けるべきパス指定

- ❌ 絶対パス（`/Users/username/...`, `C:\Users\...`）
- ❌ ホームディレクトリ起点（`~/...`）
- ❌ 環境依存のパス

---

## データ分類・メタデータ定義

### レア度分類システム

#### 一般的に流通しているパーツ

- `Commons`: 一般的で入手容易
- `Normal`: 通常入手可能
- `Normal+`: やや入手困難
- `Rare`: レア品
- `Rare+`: 非常にレア
- `SuperRare`: 極めてレア

#### 中古販売など一般流通は現在していないパーツ

- `Abolition(R+)`: 廃止品系
- `Maniac(SR+)`: マニア向け
- `ManiacRare(SSR)`: マニア向けでレア
- `VeryNerd(UR)`: 超マニア向けで極めて入手困難

### メーカー型番接頭辞の理解

7400 シリーズ IC のメーカー別型番接頭辞は以下の通りです：

- `SN74*`: TI (Texas Instruments)
- `CD74*`: TI (Texas Instruments)
- `U74*`: UTC (Unisonic Technologies)
- `HD74*`: RENESAS
- `TC74*`: TOSHIBA
- `MM74*`, `MC74*`: FAIRCHILD (Fairchild Semiconductor)
- `74HC*` (接頭辞なし): PHILIPS (NXP Semiconductors)

---

## 開発ガイドライン

### 作業ログ（大規模改修時）

このリポジトリで **大規模改修**（データスキーマ変更、生成スクリプト追加、収集方針変更、usage大量更新など）を行う場合は、
必ず `./work-in-progress/` 配下に日付付きのログ（Markdown）を残してください。

- 変更量が 500 行を超える可能性が高い場合は、事前にユーザーへ確認してください（前提条件の文面に従う）。
- 何か大きい変更（多数ファイル生成、構成変更、ルール追加など）を加える場合、まず計画を提示して合意を取ってください。
- ファイル名: `YYYY-MM-DD_*.md`（例: `2026-02-14_datasheet_sources_ti_symlink_check.md` / `2026-02-14_progress.md`）
- 最低限書く内容:
  - 目的（何を解決する作業か）
  - 変更点（触った主要ファイル/スクリプト）
  - 実行コマンド（再現手順）
  - 検証結果（レポート/件数/失敗パターン）
  - 残課題（次にやること）
- 禁止/注意:
  - 一次資料PDFの本文や転載は置かない（URL/DocID/Rev/参照日/sha256等のメタ情報は可）
  - 機密情報（個人情報、トークン、購入アカウント情報等）を書かない

補足:

- `.work-in-progress/` が存在する場合は「過去ログ置き場」として扱い、今後の正は `work-in-progress/` に統一します。

### 重要: usage/ 回路ドキュメントの一次資料照合（推測禁止）

`usage/` 配下の Markdown は「実際に配線できること」が最優先です。
そのため、**ピン番号・信号名・真理値表・論理条件・未使用入力の処理・推奨電源デカップリング**など、回路成立に直結する事項は **必ず一次資料（データシート PDF）に照合**してください。

#### 必須ルール

1. **推測でピンアサインを書かない**

- 74x 系は互換に見えても、ファミリ/メーカー/パッケージで差異があり得ます。
- 「よくあるピン配置」等の一般知識だけで確定記述しないでください。

2. **一次資料の“正（優先順位）”**

一次資料の参照は、原則として次の優先順位で扱います。

1. **Web自動取得PDF（`datasheets/datasheet_sources.json` のURLを `scripts/check_datasheet_sources.py --download` で取得できるもの）**

- URL到達性や sha256 を機械的に記録でき、検証の再現性が高い

2. **`datasheets/_download/` の手動入手PDF（整合確認用）**

- 既に手元にある資料を使って“正しそうか”を確認する用途（ただし公開リポでの再現性は URL/DocID/Rev/参照日 で担保する）

3. **Web検索 + 手動確認情報（URL/DocID/Rev/参照日）**

- 1. 2. が用意できない場合の補助（一次資料と矛盾する情報があれば一次資料を優先し、矛盾点を明示してユーザー確認）

補足:

- 本リポジトリは将来的に **PDF を `.gitignore` で除外**し、MITライセンスで公開可能にする想定です。
- 公開状態でも検証可能性を担保するため、一次資料の **URL / Document ID / Revision / 参照日** を必ず残します（本文の転載は避け、要約＋リンク中心）。
- 参考テンプレ: `datasheets/datasheet_sources.example.json`

3. **PDF がGit管理外（手元にしか無い）場合の“参照の残し方”**

- 回路・チートシートに「断定的な仕様」を書く場合は、少なくとも以下を併記する:
  - メーカー名 / 正確な型番 / パッケージ
  - データシート URL（できればメーカー公式）
  - Document ID / Revision（分かる範囲）
  - 参照日（YYYY-MM-DD）
- データシートの図表や文章は **転載しない**（必要なら“要点を自分の言葉で要約”し、リンクで誘導）。

4. **PDF が“画像主体”でテキスト抽出できない場合の手順**

- まず Python（PyMuPDF 等）でページを PNG へレンダリングして、図表（Pin configuration / Terminal functions 等）を目視で確認します。
- レンダリング出力は Git 管理外の `datasheets/.cache/pdf_render/` 配下に置く（例: `datasheets/.cache/pdf_render/<Part>/page_XX.png`）。
- 目視確認ができない状況（自動抽出のみで確証が取れない場合）は、**不確実な記述を追加しない**。必要ならユーザーに該当ページ画像の共有を依頼する。
- ページ画像の確認が取れ次第、**必ず確認の取れたか確認が不要になった画像から適切に削除し、`datasheets/.cache/pdf_render/`フォルダ内を整理する**（ただし、`datasheets/.cache/`フォルダ外にあるファイルはみだりに削除しないこと）。

5. **ネット検索は補助（一次資料がない/不足する場合のみ）**

- ネット情報を使う場合は、必ず「対象のメーカー/型番/パッケージ/改訂版」を揃え、一次資料と矛盾しないことを確認します。
- 一次資料と矛盾する場合は、一次資料を優先し、矛盾点を明示してユーザー確認を取ります。

6. **入手済みパーツ（実型番）を優先し、対応一次資料の有無を確認する**

- 回路例で使用 IC を選ぶ場合は、まず `getstarting/7400_series_ic_collection_acquisition_history.json` の `GottenItemsMN_*` に含まれる実型番を優先します。
- ピン番号・信号名・真理値表など「実配線に直結する記述」は、対応するメーカー/型番/パッケージの一次資料（ローカルPDF/公式URL等）を確認できた場合のみ記述します。

7. **キリル型番等の互換パーツは、例外としてネット情報を優先できる（ただし共同確認前提）**

- `GottenItemsMN_Other` に含まれるソビエト互換品など（例: `K155ID1/К155ИД1`）は、PDF の収集や機械的な解読が難しいことがあります。
- やむを得ずネット情報に依存する場合は「情報源の揺れ・世代差・ピン配置差」の可能性を明示し、断定せず、ユーザーと共同で整合確認を行う前提で進めてください。

---

### 追加: usage/（回路例 + 汎用型番チートシート）

`usage/` 配下は、**カテゴリ単位**で整理し、さらに **汎用型番（74xNN）単位**でサブディレクトリを切って管理します。

- ディレクトリ構造: `usage/{カテゴリ名}/{パーツ番号}/**.md`
  - 例: `usage/07_data_selectors_mux_demux/74x153/74x153.md`
- **例外（複数 IC 連携のシリーズ）**: 複数の汎用型番をまたいで構成する「組み合わせサンプル回路」は、カテゴリ配下ではなく `usage/A_combinated_samples/` にまとめる
  - 例: `usage/A_combinated_samples/74x181,182/01_4bit_alu_basic_demo.md`
  - ディレクトリ名は `74x181,182/` のように **カンマ区切り**を許可（`74x` の重複は省略可）
- 方針: 断定が必要な仕様（ピン配置・真理値表・電気特性など）は一次資料が必要なので、未検証のまま書かない
- 生成スクリプト（チートシート）: `scripts/generate_usage_cheatsheets.py`
- 既存の回路例（手書きMarkdown）も、同じ `{カテゴリ名}/{パーツ番号}` 配下へ統合して置く

チートシートに書いてよい内容（例）:

- overview由来の説明（機能/カテゴリ/レア度）
- 一般的な配線注意（入力フローティング禁止、デカップリング、ファミリ差など）
- 一次資料確認のチェックリストと参照導線（URL/Doc ID/Rev/参照日）

### パーツ情報の参照元

- [List of 7400-series integrated circuits - Wikipedia (EN)](https://en.wikipedia.org/wiki/List_of_7400-series_integrated_circuits)
  - パーツ概要・機能説明の引用元

### JSON ファイル編集の注意点

1. **文字エンコーディング**: UTF-8 を使用、日本語文字を適切に処理
2. **データ整合性**: PartNumber の一貫性を保つ
3. **配列の順序**: 既存の順序を維持（PartNumber の昇順など）
4. **型番表記**: `74x`形式での汎用表記と実際の型番の区別を理解

### Python スクリプト開発ガイドライン

1. **JSON ファイル処理**: `json`モジュールを使用、適切なエラーハンドリング
2. **メーカー推定ロジック**: 型番接頭辞による保守的な推定を実装
3. **データ検証**: 入力データの妥当性チェック
4. **ログ出力**: 処理結果の詳細なログを提供

### 新機能開発の指針

1. **データ整合性の維持**: 複数 JSON ファイル間の一貫性
2. **拡張性**: 新しいメーカーやロジックファミリへの対応
3. **国際化**: 英語・日本語両対応
4. **エラー処理**: 不正データに対する適切な処理

---

## 自動化スクリプト

### `scripts/autofill_gottenitems.py`

**機能**: 入手履歴からデータシート収集状況への自動同期

- メーカー推定による収集予定データの自動生成
- 既存データの上書き回避
- 入手済み IC 型番の自動登録

### `scripts/auto_check_factcheck.py`

**機能**: `usage/{cat}/{74xNN}/{74xNN}.md` のファクトチェック項目（`- [ ]`）を自動更新

- 入手履歴から実型番を決定し「対象の実型番」チェックを `[x]` に更新
- `datasheets/datasheet_sources.json` から確認済み URL を探して「データシート参照先」を更新
- 既に `[x]` の項目は冪等（スキップ）
- 実行: `python3 scripts/auto_check_factcheck.py`

### `scripts/render_datasheet_pages.py`

**機能**: ローカルPDFを `datasheets/.cache/pdf_render/` に PNG レンダリングする

- `datasheets/_download/` のPDFをインデックス化し、入手履歴から型番を照合
- 出力先: `datasheets/.cache/pdf_render/{part}_{stem}/page_XXX.png`（Git 管理外）
- 実行例:
  ```powershell
  python3 scripts/render_datasheet_pages.py --part 74x00 --pages 1-6 --dpi 150
  ```
- 対話型ファクトチェック（`factcheck-interactive.prompt.md`）の Step 2 で呼び出される
- 確認後は `datasheets/.cache/pdf_render/` を手動またはスクリプトで削除すること

### `scripts/batch_factcheck_from_pdf.py`

**機能**: 入手済み全パーツに対してローカルPDFからテキスト抽出し、信頼度85%以上の項目を一括自動確認

- **信頼度閾値**: 85%（未満はスキップ）
- 項目ごとのスコアリング:
  - ピン配置: ピン数・パッケージキーワード充足率
  - 真理値表: 「Function Table / Truth Table」キーワードの有無
  - 絶対最大定格: AMR キーワード充足率 + 電圧/電流数値の有無
  - 電気特性: VOH/VOL/VIH/VIL キーワード充足率
  - 未使用入力: 「unused input / floating / pull-up」キーワード充足率
- 画像ベースPDF（テキスト抽出不可）は自動スキップ
- PDF が見つからないパーツはスキップ
- 実行例:
  ```powershell
  # dry-run（変更なし・結果表示）
  python3 scripts/batch_factcheck_from_pdf.py --dry-run

  # 特定パーツのみ
  python3 scripts/batch_factcheck_from_pdf.py --part 74x86 --verbose

  # 全パーツ一括適用
  python3 scripts/batch_factcheck_from_pdf.py
  ```
- PDFを `datasheets/_download/` に追加すれば次回実行時に自動処理される

### `.github/prompts/factcheck-interactive.prompt.md`

**機能**: Agent モードで1パーツずつ対話型ファクトチェックを行うプロンプト

- `render_datasheet_pages.py` でPDFをレンダリング → `view_image` で目視確認
- **信頼度スコア評価**（ページごとに報告）:
  - 低下要因: 小さいテキスト(-5〜15%)、多列表(-5〜20%)、紛らわしい文字(-3〜10%)、ページまたぎ(-5〜10%)、低画質(-10〜30%)
  - 上昇要因: 複数PDFで相互確認(+5〜10%)
- 85%以上: 自動確認扱い、85%未満: ユーザー目視確認を依頼
- 確認後は `datasheets/.cache/pdf_render/` の一時PNG を削除
- 呼び出し方: VS Code Agent チャットで `#factcheck-interactive 74x00` と入力
---

## 一次資料の“Web自動ファクトチェック”方針（将来）

将来的に、データシートPDFをGitに含めない状態でも、一次資料の参照が**再現可能**になるようにします。

- このリポでまず自動化するのは「URLの到達性」「ドキュメント識別情報の記録」「（任意で）ローカル一時ダウンロードとハッシュ算出」です。
- PDF本文からピン配置/真理値表/電気特性を自動抽出して断定するのは、誤読リスクが高いので**慎重**に扱います。
  - 自動抽出を行う場合でも、結果が一次資料と一致すると保証できない限り、断定記述に使わない
  - レンダリング画像等の作業ファイルは `datasheets/.cache/` に置く（Git管理外、`.gitignore` 除外済み）
  - `batch_factcheck_from_pdf.py` による自動確認は「信頼度85%以上」のみ更新し、それ以下はスキップ
  - ユーザー目視確認が必要な場合は `factcheck-interactive.prompt.md` フローで対話確認

関連スクリプト:

- `scripts/check_datasheet_sources.py`: `datasheets/datasheet_sources.json` のURLチェック/任意DL/sha256算出/レポート出力
  - 例（URL未入力の雛形が混ざる場合）: `python3 scripts/check_datasheet_sources.py --skip-empty`
  - 例（レポートJSON出力）: `python3 scripts/check_datasheet_sources.py --skip-empty --report .temp/datasheet_fetch/report.json`
  - 例（任意DL+sha256、同一資料保証の足場）: `python3 scripts/check_datasheet_sources.py --download --report .temp/datasheet_fetch/report.json`
  - 例（取得メタ情報をsourcesへ反映）: `python3 scripts/check_datasheet_sources.py --skip-empty --download --update`

### VS Code タスク

以下のタスクが定義されています：

- **`Generate FP/ALL JSONs`**: データの統合処理（`merge_fp.py`）
- **`Refine Descriptions`**: 説明文の洗練化（`refine_descriptions.py`）
- **`Regenerate ALL after refine`**: 洗練後の再生成（`merge_fp.py`）

---

## コーディングパターン集

### JSON データの読み書き

```python
import json
import os

# UTF-8でJSONファイルを読み込み
with open('file.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# インデント付きで保存
with open('file.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 型番の正規化

```python
def normalize_part_number(part_num):
    """型番を汎用形式に正規化"""
    # SN74HC00N -> 74x00 の変換ロジック
    pass
```

### データ検証

```python
def validate_part_data(part_data):
    """パーツデータの妥当性を検証"""
    required_fields = ['PartNumber', 'Description', 'Rarity']
    for field in required_fields:
        if field not in part_data:
            raise ValueError(f"Required field {field} is missing")
```

---

## 開発上の禁止事項

データの整合性とプロジェクトの安定性を維持するため、以下の操作は禁止されています：

1. **既存データの意図しない改変**
   - 手動編集時は慎重に行い、自動化スクリプトの活用を推奨

2. **PartNumber 体系の破壊**
   - `74x` 形式の汎用型番表記を維持すること

3. **メーカー推定ロジックの過度な拡張**
   - 保守的アプローチを維持し、不確実な推定は避ける

4. **`getstarting/` を Git 追跡対象に戻すこと**
   - 購入先・コメントを含む私物情報のため `.gitignore` で除外済み。ファイルはローカルに存在し、
     参照するスクリプトはそのまま動作する

4. **JSON ファイルの文字コード変更**
   - UTF-8 エンコーディングを厳守

5. **データの不整合を引き起こす操作**
   - 複数ファイル間の関連性を理解した上で編集を行う

6. **購入予定 JSON（`getstarting/7400_series_ic_purchase_*.json`）への配列要素追加**

   - これらの購入予定/ウィッシュリストはユーザーが管理します。Copilot は **配列要素を追加しない** でください（提案や候補提示は可）。

7. **一次資料未確認のピン配置・真理値表・電気特性の断定記述**

8. **データシートの図表・文章の転載**
   - 要点を自分の言葉で要約し、リンクで誘導すること。

---

## プロジェクト開発ポリシー

このプロジェクトは精密なデータ管理を要求します。開発時は以下を最優先してください：

- **データ整合性**: 全 JSON ファイル間の一貫性維持
- **既存構造の尊重**: 既定のスキーマとフォーマットの遵守
- **段階的な変更**: 大規模な変更は小さなステップに分割
- **検証の徹底**: 変更後は必ずデータの妥当性を確認
- **国際化**: 英語・日本語両対応（説明文）

---

## KiCAD PCB デモ制作ガイドライン (`pcb-demo/`)

### 概要

`pcb-demo/` は、入手済み 7400 シリーズ IC の動作プレゼン用最小デモ PCB を  
KiCAD 10.0.3 で制作するためのプロジェクト群です。

- 構造は `usage/` と同じ `{カテゴリ名}/{パーツ番号}/` 形式
- `scripts/generate_pcb_demo_projects.py` で各 IC のプロジェクトを一括生成
- `scripts/kicad_sch_gen.py` が **KiCAD 標準ライブラリの実シンボルを使った `.kicad_sch`** を自動生成。シンボル解決はオーバーライド表→`kicad_lib.discover_symbol` による `74xx.kicad_sym` 自動探索の順で、ライブラリ実在型番は自動対応（カバレッジは `audit_kicad_coverage.py` で確認）。実在しない型番のみテキスト版へフォールバック
  - 非対応部品はテキスト注釈版またはテンプレートスタブにフォールバック
- ピン配置・真理値表などの実配線事項は `usage/{カテゴリ}/{パーツ番号}/` の一次資料確認を前提とする

### KiCAD 環境

- **バージョン**: KiCAD 10.0.3
- **CLI パス**: `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`
- **テンプレート形式**: KiCAD 8 互換（version 20231120 / 20240108）
  - KiCAD 10 が初回保存時に自動アップグレードする

### ファイル生成スクリプト

```powershell
# dry-run（変更なし・生成予定を表示）
python3 scripts/generate_pcb_demo_projects.py

# 実際に生成（新規のみ）
python3 scripts/generate_pcb_demo_projects.py --apply

# 特定カテゴリのみ生成
python3 scripts/generate_pcb_demo_projects.py --apply --category 01_buffers_inverters

# 既存ファイルも上書き
python3 scripts/generate_pcb_demo_projects.py --apply --overwrite
```

または VS Code タスクの「PCB Demo: dry-run」「PCB Demo: generate all projects」を使用。

### 設計ルール（必須）

1. **一次資料が未確認のまま断定的なピン配置を PCB に書かない**
   - 回路図・PCB に実配線を記述する前に、`usage/{カテゴリ}/{パーツ番号}/` のファクトチェックが完了していること
   - 一次資料の優先順位は `usage/` セクションの「重要: 一次資料照合」に準じる

2. **KiCAD 標準ライブラリを優先する**
   - 74xx シリーズは KiCAD 標準ライブラリ (`74xx`) にシンボルが収録されている
   - `kicad_sch_gen.py` が対応している部品は標準ライブラリのシンボルを `lib_symbols` に埋め込んだ実回路図を自動生成する
   - `.kicad_sym` スタブはプレースホルダ。実際の設計では標準シンボルを使用すること

3. **テンプレートのプレースホルダ**
   - `{{PART_NUMBER}}` / `{{DESCRIPTION}}` / `{{DESCRIPTION_JP}}`
   - `{{CATEGORY}}` / `{{CMOS_PARTS}}` / `{{TTL_PARTS}}` / `{{OTHER_PARTS}}`
   - `{{ALL_OWNED_PARTS}}` / `{{DATE}}`

4. **PCB 基本仕様（テンプレートのデフォルト）**
   - 基板サイズ: 50×50 mm（Edge.Cuts に外形線あり）
   - 銅箔厚: 35µm（標準 1oz）
   - 基板厚: 1.6 mm
   - 最小パターン幅: 0.2 mm
   - デカップリング: IC 1個につき 100nF を VCC–GND 直近に配置すること

5. **KiCAD CLI の利用（Gerber 出力・DRC）**
   - Gerber 出力: VS Code タスク「KiCAD CLI: export Gerber」を使用
   - DRC 実行: VS Code タスク「KiCAD CLI: run DRC」を使用
   - CLI パスは `.vscode/tasks.json` の `kicad-cli.exe` のフルパスを参照

### pcb-demo/ 関連ファイルの Git 管理方針

- テンプレートファイル（`_templates/`）・共通キャリア（`_carrier/`）: Git 管理対象
- 自動生成スタブ（各 IC のプロジェクトファイル）: Git 管理対象（stub として追跡）
- Gerber 出力（`gerber/` サブディレクトリ）: **`.gitignore` で除外済み**
- KiCAD バックアップファイル（`*-backups/`, `*.kicad_prl`）: **`.gitignore` で除外済み**（2026-09-16 に追跡解除）

### PCBA 化プロジェクト（Specimen Tiles）

収集した現物の DIP IC をソケットに挿して動作展示する基板を JLCPCB で製作するプロジェクト。
**作業前に必ず `pcb-demo/REQUIREMENTS.md` を読むこと。**

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

`~/.claude.json` の `mcpServers.kicad` に登録済み（kicad-mcp v2.7.0, MIT, 233 ツール / 24 カテゴリ）。
MCP は起動時に読み込まれるため、**登録後に開始したセッションでのみ利用できる**。
既存スクリプトとは置き換えではなく併用する（一括バッチはスクリプト、1 枚の作り込みは MCP）。

| 作業 | 担当 |
|---|---|
| 収集 DB・対象型番リスト・ファクトチェック | 既存 Python スクリプト（`scripts/`） |
| 回路図の作図・一括編集、基板レイアウト | KiCAD MCP |
| ERC / DRC | KiCAD MCP `run_erc` / `run_drc`（一括検証は `verify_kicad_sch.py`） |
| LCSC 部品選定・Basic/Extended 判定 | KiCAD MCP `search_jlcpcb_parts` / `get_jlcpcb_part` |
| Gerber / ドリル / CPL / BOM 出力 | KiCAD MCP `export_gerbers` / `export_drill` / `export_pos` / `export_bom` |
