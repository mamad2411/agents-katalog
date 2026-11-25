---
name: design-extractor
description: |
  任意のURLから動的レンダリング済みのHTML/CSS/JSを取得し、
  アニメーション情報を含むデザイン仕様（VANILLA.md と INTERPRETED.md の 2 段階）を自動生成するスキル。
  VANILLA.md は推測なしの生抽出、INTERPRETED.md は VANILLA を唯一の入力とした意味付け解釈。

  以下の状況で使用:
  - 「このURL抽出して」「このサイトの仕様取ってきて」
  - 「このサイトのデザイン情報取ってきて」
  - 「このURLからアニメーション情報抜き出して」
  - 「design-extractorで解析して」
  - URLと「抽出」「解析」「VANILLA」「INTERPRETED」等のキーワードが同時に来たとき

  以下には使用しない:
  - 「既存ファイルを編集したい」
  - 「このデザインを実装して」（実装タスク）
  - 「アニメーションを作って」（生成タスク）
---

# design-extractor

URL を入力に **VANILLA.md（生抽出）と INTERPRETED.md（意味付け解釈）の 2 段階成果物**を自動生成するスキル。
取得は Playwright（fetch.js）が担当し、解釈・生成は Claude 自身が行う。

**注**: 出力ファイル名は `VANILLA.md` / `INTERPRETED.md` であり `DESIGN.md` ではない。design-creator の出力する `DESIGN.md` とはセクション構成が同系統（Colors/Typography/Spacing/Components/Animations/Constraints は共通）だが、先頭セクションは VANILLA は `Meta`、DESIGN は `Intent` で異なる。

---

## 初回チェック: 推奨権限

セッション内で本スキルを **初めて呼ぶ時のみ** 実施します（2 回目以降はスキップ）。

```bash
grep -q "python3 -m http.server" ~/.claude/settings.json 2>/dev/null && echo INSTALLED || echo MISSING
```

`INSTALLED` ならスキップして「前提確認」へ進みます。

`MISSING` の場合、ユーザーに **1 度だけ** 以下を提案します（`lang=en` 指定時は英語で提示）:

```
本スキル群は mkdir / cp / npm install / npx playwright install / python3 -m http.server などを
自動で実行します。そのままだと毎回 "Do you want to proceed?" 確認が表示されます。

リポジトリ同梱の settings.recommended.json を ~/.claude/settings.json の permissions.allow に
マージすると、これらの安全なコマンドのみ確認なしで通るようになります。

マージしますか？ (yes / no / 後で)
- yes: 自動でマージして以降のプロンプトを抑制します
- no:  以降このセッションでは再提案しません
- 後で: 今回はスキップし、次回セッションで再度確認します
```

`yes` の場合、後述の **設定ファイルの解決手順** に従ってリポジトリの `settings.recommended.json` を読み込み、`~/.claude/settings.json` の `permissions.allow` 配列に **未登録の項目だけ** 追記します（重複させない）。`~/.claude/settings.json` が存在しない・JSON として不正な場合は手動マージを案内し、スキルは停止しません。

`no` / `後で`: 即座に「前提確認」へ進みます。settings 操作はしません。

### 設定ファイルの解決手順

`settings.recommended.json` の場所はインストール形態（symlink / 直接配置 / 移設後）で変わるため、以下を上から順に試して **最初に見つかったもの** を採用します。

```
1. 環境変数 $ADVANCED_DESIGN_MD_DIR が設定されていれば $ADVANCED_DESIGN_MD_DIR/settings.recommended.json
2. このスキル本体の実体パス（symlink ならその参照先）から `../../settings.recommended.json`
   - 解決例: `readlink -f ~/.claude/skills/design-extractor` → `/home/user/advanced-design-md/skills/design-extractor`
   - その親の親 = `/home/user/advanced-design-md/`
3. ホーム直下の慣例パス: `~/advanced-design-md/settings.recommended.json`
4. カレントディレクトリ: `./settings.recommended.json` および `./advanced-design-md/settings.recommended.json`
```

いずれにも見つからない場合は手動マージを案内します。

```
settings.recommended.json の場所を自動検出できませんでした。
リポジトリの settings.recommended.json を手動で開き、permissions.allow を
~/.claude/settings.json にマージしてください。

または、$ADVANCED_DESIGN_MD_DIR にリポジトリのパスを設定すると次回から自動検出されます:
export ADVANCED_DESIGN_MD_DIR="$HOME/advanced-design-md"
```

---

## 前提確認

実行前に以下を順にチェックします。未インストールの場合は **ユーザーに通知 → 自動セットアップ実行** までを 1 セットで実施します（毎回ユーザー確認を取らない）。

### 1. Node.js バージョン

```bash
node --version   # >= 18 が必要
```

18 未満の場合は停止し、`references/troubleshooting.md` を案内します。

### 2. 依存パッケージの有無

```bash
test -d <スキルディレクトリ>/node_modules/playwright && echo OK || echo MISSING
```

`MISSING` の場合、ユーザーに以下のように 1 行で通知してから **自動で実行します**（追加の確認プロンプトは取らない）:

```
初回セットアップが未実施です。npm install + playwright install chromium を実行します（数分かかります）。
```

```bash
cd <スキルディレクトリ>
npm install
npx playwright install chromium
```

完了したら Step 1 へ進みます。失敗した場合は停止し、`references/troubleshooting.md` を案内します。

> **Note**: この自動実行は `Bash(npm install)` `Bash(npx playwright install:*)` の権限を必要とします。配布リポジトリ同梱の `settings.recommended.json` を `~/.claude/settings.json` にマージしておくと、プロンプトが出ずに実行されます。

---

## Step 0: 保存先 + スラグ決定

### 保存先（output base）

スキル呼び出し時に `output=<path>` が指定された場合はそれを採用します。
省略時は環境変数 `DESIGN_LIBRARY_DIR` を確認し、未設定なら以下のフォールバック順で解決します:

```
1. output= パラメータ
2. $DESIGN_LIBRARY_DIR
3. ~/design-library/sites/    (ホーム直下の慣例パス)
4. ./design-library/sites/    (カレントディレクトリ配下)
```

### スラグ確認

実行前にユーザーへスラグを確認します。

```
サイトのスラグ（フォルダ名）を指定してください。
例: acme-fantasy-game / nova-corp-top / atlas-portfolio
```

- 形式: 英数字・ハイフンのみ（スペース禁止・kebab-case）
- `<output base>/{slug}/` に全成果物を保存します

スラグが決まったら以下の変数として扱います:

```
SLUG = <ユーザーが入力した値>
SITE_DIR = <output base>/{SLUG}
```

---

## Step 1: ソース取得

### 実行前の初期化

```bash
mkdir -p {SITE_DIR}/raw/styles {SITE_DIR}/raw/scripts
```

### fetch.js の実行

```bash
node scripts/fetch.js <URL> {SITE_DIR}/raw
```

実行後、以下のファイルが生成される:

```
{SITE_DIR}/raw/
  dom.html                # レンダリング後のHTML（インラインstyle属性含む）
  styles/                 # CSS分割保存
    001-inline.css
    002-https___...css
  styles-manifest.json    # CSS取得元・順序・種別・media query情報
  scripts/                # シグネチャ判定済みJSファイル群
  behavior-log.json       # 動的挙動観測ログ
```

stderr に ERROR が出力された場合はユーザーに通知してスキルを停止します。
詰まった場合は `references/troubleshooting.md` を参照してください。

---

## Step 2: ソース解析

以下の順番でファイルを読みます。順序を守ってください（DOM 構造の把握が先）。

```bash
cat {SITE_DIR}/raw/dom.html
cat {SITE_DIR}/raw/styles-manifest.json
cat {SITE_DIR}/raw/styles/*.css
cat {SITE_DIR}/raw/scripts/*.js
cat {SITE_DIR}/raw/behavior-log.json
```

### 解析時の注意

読み込んだソースから以下を抽出します:

**Colors / Typography / Spacing / Components**
- CSSの変数・クラス定義から読み取る
- JSで動的に設定される値は`[動的: JS制御]`と明記

**Animations**
- `references/animation-patterns.md`を参照してライブラリを特定する
- `@keyframes`・`animation`・`transition`プロパティを抽出
- `behavior-log.json`の`eventListeners`・`observers`からScroll/Hover挙動を読み取る
- jQueryサイトの場合: `fadeIn`/`fadeOut`/`animate({`/`scrollTop`の呼び出しパターンを確認
- `missingReasons`がある場合はDESIGN.mdの該当箇所に`[未取得: <理由>]`と明記

**フィルタリング基準（keyframesが大量の場合）**
- `animation-duration`が0.1s以上のもの
- body / main / セクションレベルの要素に適用されているものを優先
- 同じeasing・durationのパターンはまとめて記述

---

## Step 3: VANILLA.md 生成

`references/design-md-format.md` の Part A（VANILLA.md フォーマット）と A-3 のチェックリストを参照しながら直接生成します。

出力先: `{SITE_DIR}/VANILLA.md`

### 出力前チェック

- [ ] 必須見出し7つが全て存在するか（Meta/Colors/Typography/Spacing/Components/Animations/Constraints）
- [ ] Animationsの5サブセクションのうち2つ以上が空でないか
- [ ] 空欄がないか（未取得は`[未取得]`または`[未取得: <理由>]`で明記）
- [ ] 推測補完していないか
- [ ] カラー値が`#RRGGBB`形式か
- [ ] durationが`ms`または`s`で統一されているか
- [ ] セクション順序が規約通りか

---

## Step 4: INTERPRETED.md 生成

`{SITE_DIR}/VANILLA.md` を唯一の入力として、意味付けと解釈を行います。
書式の詳細は `references/design-md-format.md` の Part B を参照してください。

**絶対ルール: VANILLA に存在しない値は一切書かないこと。補完・推測・創作は禁止です。**

出力先: `{SITE_DIR}/INTERPRETED.md`

### 命名

各要素（色・アニメーション・コンポーネント）に以下の形式で名前を付与します。

```yaml
name: fade-blur-in          # 英語（CSSクラス名と共通）
ja: フェードブラーイン        # 日本語（人間用補助）
```

### アニメーション要素の解釈

VANILLA の Animations セクションにある各 keyframe・transition に対して付与します。

```yaml
name: fade-blur-in
ja: フェードブラーイン
source: ".ani → .ani.active"           # VANILLA の source をそのまま引用
spec: filter blur(15px)→0 + opacity 0→1, 1.5s ease   # VANILLA の値そのまま
tone: [霧が晴れる, 静かな浮かび上がり]   # 印象・感覚（リスト形式）
effect: スクロール入場時のコンテンツ出現演出   # 機能（何をするか）
strength: ファーストビューの印象形成に向く
weakness: 繰り返し使うと間延びする
good-for:
  concrete: [hero-title, section-heading]   # parts-naming.md の確定部品名のみ
  abstract: []                                # 命名体系外の用途は abstract 側
avoid:
  concrete: [nav-link]
  abstract: []
```

**good-for / avoid のルール**
- `concrete` には `references/parts-naming.md` の確定済み部品名のみを使用します
- 命名体系外の用語は `abstract` 側、または `weakness` / `note` 等の自由文フィールドに記述します
- 該当なしの場合は `[]` と記述します
- フィールドの完全な書式は `references/design-md-format.md` の Part B を参照してください

### コンポーネントの解釈

コンポーネントには `states` セクションで状態ごとのアニメーションを紐付けます。
全フィールドの完全仕様は `references/design-md-format.md` の Part B を真の出典とし、本セクションは要約に過ぎません。乖離があれば design-md-format.md 側を優先してください。

```yaml
name: character-card
ja: キャラクターカード
tone: 静的な存在感・並列的な提示
strength: グリッドでの一覧表示に向く
weakness: 高さ固定のため縦長コンテンツには不向き
states:
  enter:
    preferred: fade-blur-in     # 第一選択
    trigger: scroll-reveal      # 発火トリガー（あれば）
    alternative: rise-in        # 代替（VANILLAに存在する場合のみ書く）
  hover:
    preferred: ghost-fade
```

**states のルール**
- 状態名の例: `enter` / `hover` / `hover-on` / `hover-off` / `open` / `close` / `active`
- `preferred` は必須です。`alternative` と `trigger` は VANILLA に根拠がある場合のみ記述してください

### 色・タイポグラフィの解釈

VANILLA の色値に意味のある名前を付与します。

```yaml
name: cursed-blue
ja: 呪力ブルー
value: "#2da6e3"   # VANILLAの値をそのまま使う
role: インタラクション全般のアクセント
```

### meta.yaml の生成

INTERPRETED.md 生成後、以下の内容で `{SITE_DIR}/meta.yaml` を作成します。

```yaml
slug: {SLUG}
url: <取得元URL>
extracted: <YYYY-MM-DD>
tags: []      # ユーザーが後から追記
notes: ""     # ユーザーが後から追記
```

---

### 出力前チェック

- [ ] 全ての値が VANILLA（`{SITE_DIR}/VANILLA.md`）に存在するか
- [ ] 新しい色値・数値・フォント名・アニメ名を追加していないか
- [ ] `name` は英語の kebab-case か
- [ ] `ja` は日本語で併記されているか
- [ ] VANILLA に記載のないアニメーションを追加していないか
- [ ] `good-for.concrete` / `avoid.concrete` が `references/parts-naming.md` の確定部品名で構成されているか
- [ ] 命名体系外の語が `concrete` ではなく `abstract` 側に振られているか
- [ ] `tone` がリスト形式になっているか
- [ ] `effect` フィールドが全アニメーションに存在するか

---

## 成功条件

| 種別 | 条件 |
|------|------|
| 定量 | VANILLA.md に必須セクション7つが全て存在する |
| 定量 | Animationsにライブラリ名1件以上、keyframesまたはtransitions1件以上 |
| 定量 | Animationsサブセクション5つのうち2つ以上が空でない |
| 定量 | `[未取得]`比率が全項目の30%以下（後述の根拠参照） |
| 定量 | INTERPRETED.md の各要素に name / ja / role(or tone) が揃っている |
| 定性 | 推測補完・誤記がない |

### `[未取得]` 30% の根拠

通常の静的サイト・標準的な SPA であれば fetch.js が CSS / DOM / JS をフルに取れ、`[未取得]` は 10% 前後に収まる。
30% を超えるのは典型的に以下のケース:

- 動的レンダリングが Playwright のレンダリング待ちより長く、CSS / JS の一部が取りこぼされている
- CDN / iframe 越しに本体スタイルが配信されており fetch 範囲外
- カスタムフォントのライセンス保護で CSS が暗号化されている

つまり 30% 超 = 「fetch ロジックの限界 or サイト固有の保護」のシグナル。`references/troubleshooting.md` で対処法を確認する。

---

## 呼び出し形式

```
/design-extractor [パラメータ]
```

スキル名と同名のスラッシュコマンドです。会話文脈に「このサイト抽出して」「この URL からデザイン情報取って」等が含まれる場合は、明示コマンドなしでも発動します。

| パラメータ | 説明 | 例 |
|---|---|---|
| `url=` | 抽出対象 URL（明示指定） | `url=https://example.com` |
| `slug=` | 保存フォルダ名（kebab-case） | `slug=acme-fantasy-game` |
| `output=` | 出力先 base ディレクトリ | `output=~/my-library/sites/` |

すべて省略可能です。url / slug が省略された場合は、ステップ進行中に確認します。

---

## アンチパターン

- ❌ Playwright のセットアップを確認せず fetch.js を実行する — node_modules 不在で即落ちます。前提確認セクションを必ず通してください
- ❌ VANILLA.md にない値を INTERPRETED.md に書く — INTERPRETED は VANILLA を唯一の入力とする原則違反です
- ❌ INTERPRETED.md の good-for / avoid に命名体系外の名前を書く — `references/parts-naming.md` の確定部品名のみを使用してください
- ❌ DESIGN.md という名前のファイルを生成する — 本スキルの出力は VANILLA.md と INTERPRETED.md の 2 ファイルです。DESIGN.md は design-creator の出力名です

---

## Reference Files

- `references/design-md-format.md` — VANILLA.md フォーマット規約・チェックリスト
- `references/animation-patterns.md` — ライブラリ別シグネチャ・パターン集
- `references/troubleshooting.md` — エラー・取得失敗時の対処手順
- `references/parts-naming.md` — 部品名・アニメーション分類の命名体系（INTERPRETED.md の good-for/avoid で使用）
