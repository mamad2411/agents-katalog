---
name: design-md-generator
description: URL・画像・テキスト要件からAIコーディングエージェント向けのDESIGN.mdを生成するスキル。「example.comをDESIGN.md化して」「このサムネをDESIGN.md化して」「クールでポップなLP用のDESIGN.mdを作って」といったリクエストで使用する。Claude Code / Cursor / Stitch に渡せば一貫したUIを生成できる、getdesign.md / awesome-design-md 準拠の9セクション構成のデザイン仕様書を出力する。CSS解析・画像目視抽出・要件生成の3パターンに対応。
license: MIT
author: shohei
version: 1.0.0
---

# DESIGN.md Generator

任意のサイトURL・参考画像・テキスト要件から、AIコーディングエージェント（Claude Code / Cursor / v0 等）向けの **DESIGN.md** を生成するスキル。

## DESIGN.md とは

AIコーディングエージェント向けのデザイン仕様書フォーマット。プレーンテキスト（Markdown）でカラー・タイポグラフィ・コンポーネント・余白・トーンを記述する。プロジェクトルートに置いて `@DESIGN.md` で参照すると、AIが一貫したUIを生成できる。

本スキルは [getdesign.md](https://getdesign.md/) / [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) で広く使われている9セクション構成に準拠して出力する。

## 入力の3パターン

### 1. URL → DESIGN.md（CSS解析ベース）

サイトURLを受け取って、CSS から色・フォント・角丸・シャドウを抽出して DESIGN.md にまとめる。

**ユーザー指示例:**
- 「<https://neverjp.com/> を DESIGN.md にして」
- 「example.com の DESIGN.md を作って」

**手順:**

```bash
python {SKILL_DIR}/scripts/extract_css.py <URL>
```

スクリプトが返す JSON（カラー頻度・フォント・角丸・シャドウ・ブレークポイント）を Claude が `references/template.md` に当てはめて DESIGN.md を組み立てる。出力先はユーザー指定 or `./DESIGN.md`。

### 2. 画像 → DESIGN.md（目視抽出）

サムネ・スクショ・モックなどの画像を受け取って、Claude が vision で目視抽出して DESIGN.md にする。

**ユーザー指示例:**
- 「このサムネを DESIGN.md 化して」（画像添付）
- 「このスクショと同じトーンの DESIGN.md を作って」

**手順:**

1. 画像を Claude に直接読ませる（Read ツールで画像パスを開く）
2. `references/template.md` の9セクションに沿って、画像から読み取れる要素を埋める
3. CSSが取れない要素（HEX値など）は近似値を提案し、`要確認` マークを付ける
4. 出力先はユーザー指定 or `./DESIGN.md`

### 3. テキスト要件 → DESIGN.md（要件から生成）

「クールでポップな LP」「和モダンなコーポレート」など、テキスト要件から DESIGN.md を生成する。

**ユーザー指示例:**
- 「クールでポップな LP 用の DESIGN.md を作って」
- 「和モダンな士業サイト用の DESIGN.md が欲しい」

**手順:**

1. ユーザーの要件を以下に分解する:
   - 雰囲気・業界・ターゲット
   - 求めるトーン（ポップ／高級／フラット／レトロ等）
   - 必須要素（カラー指定や使いたいフォントの希望）
2. `references/template.md` の9セクションを要件に合わせて埋める
3. カラーパレット・フォント・角丸方針は要件と整合する組み合わせを提案する
4. 出力先はユーザー指定 or `./DESIGN.md`

## 出力する DESIGN.md の9セクション

`references/template.md` を参照。getdesign.md / awesome-design-md 準拠の9セクション構成。すべての出力で以下の章順・章名を厳守する:

### 必須セクション

1. **Visual Theme & Atmosphere** — Mood / density / aesthetic philosophy（Brand Voice もここに集約）
2. **Color Palette & Roles** — Descriptive Name + Hex + Functional Role（Primary / Surface / Text / Accent でグループ化）
3. **Typography Rules** — Font Family + Hierarchy table + Principles
4. **Component Stylings** — Buttons / Cards / Inputs / Navigation / Image・Iconography / Microinteractions
5. **Layout Principles** — Spacing / Container / Grid / Whitespace philosophy
7. **Do's and Don'ts** — 守るべきルール・禁止事項（**必須**: AIの脱線を防ぐ最重要セクション）

### 推奨セクション（入力情報がある場合は必ず埋める）

6. **Depth & Elevation** — Shadow Scale + Border Radius Scale + Shadow philosophy
8. **Responsive Behavior** — Breakpoints / Touch Targets / Collapsing Strategy
9. **Agent Prompt Guide** — Quick Reference + Component Prompts 例 + Iteration Guide

章番号は 1〜9 の順序を維持する（必須/推奨の区分は章順を変えない）。情報が不足して埋められない章は省略せず、`(要確認)` マークを付けて空欄を残すこと。

## Tips

- **入力タイプの判定**: ユーザーの指示にURL（http/httpsで始まる文字列）が含まれていたらURLモード、画像パス（.png/.jpg/.webp等）が含まれていたら画像モード、それ以外はテキスト要件モードとして扱う
- **複数入力の混合**: URL + 「ポップな雰囲気を加えて」のような混合指示は、URLモードでDESIGN.mdを生成してから、テキスト要件で調整する2段階処理にする
- **推測値には注釈を付ける**: 画像モードや要件モードで推測値（HEX値・rem値など）を出すときは「(推定値・要確認)」を末尾に付ける
- **出力の最後に Source 行**: どの入力から生成したかを末尾に明記する（例: `**Source**: https://example.com/ (CSS解析, 2026-04時点)`）

## 必要な依存

- Python 3.9+
- `requests`（CSS取得用）

```bash
pip install requests
```
