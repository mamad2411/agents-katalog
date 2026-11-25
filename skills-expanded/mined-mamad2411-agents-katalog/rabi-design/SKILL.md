---
name: rabi-design
description: >-
  Rabi のブランドスタイル（色・フォント・余白・角丸・影・深さ・トーン）を適用する。
  Rabi 名義の UI・LP・ドキュメント・図を作るとき、
  または「Rabi スタイルで」と言われたときに使う。
  デザイントークンと適用の規則を含む。
---

# rabi-design

## 読む順

1. [`references/DESIGN.md`](references/DESIGN.md) —— 仕様の全文
2. [`assets/rabi-tokens.css`](assets/rabi-tokens.css) —— front matter から生成した `--rabi-*` とテーマ指定
3. [`assets/rabi-head.html`](assets/rabi-head.html) —— front matter から生成した webfont の `<link>`

SSOT は 1。front matter がトークンの値、本文が適用の規則。2 と 3 は写しで、**手で直さない**。

## 展開する順

CSS を書く媒体では `assets/rabi-tokens.css` を先頭にインライン展開する。

`<head>` を持つ媒体では `assets/rabi-head.html` の `<link>` を入れる。入れなくても OS のフォントへ落ちる。

部品の CSS は配らない。`references/DESIGN.md` の「Components」の規則から、その媒体に要る分だけを書く。

色・余白・角丸・影・書体・丈・時間は `--rabi-*` を引く。**例外はトークンが無い値だけ** —— front matter の component が持つ literal と、本文が定める値。それはその値をそのまま書く。

図を描くライブラリ・アイコンのデータ・テーマ切替の JS も**配らない**。同じく規則から組み立てる。

CSS を持たない媒体（docx・スライド）では front matter の値を直に当てる。テーマは light の値だけを使う。

組んだあとに「Do's and Don'ts」で当たりを取る。

## 値を変えるとき

トークンの値は front matter を直し、写しを作り直す。

```bash
bun <skills root>/rabi-design/scripts/gen-css.ts
```

**path は skill 側の実体を指す。**

front matter に無い値は本文が持つ。**本文を直しても生成物は変わらない**。

写しが front matter と食い違っていないかは `--check` で見る。食い違ったら非ゼロで終わる。

```bash
bun <skills root>/rabi-design/scripts/gen-css.ts --check
```

CSS の関数（`light-dark()` / `color-mix()` / `clamp()`）を front matter に**書かない**。組み立ては `scripts/gen-css.ts` と、可変の見出しは `references/DESIGN.md` の「Typography」。

## 射程

対象は Rabi 名義の面 —— 製品 UI・LP・ドキュメント・図。

ブランドの照合元は製品側のカタログと、カタログが読むトークン・共通部品・文書の CSS。この skill の SSOT は `references/DESIGN.md`。食い違いはカタログの実表示と CSS を確認し、front matter と本文を更新する。

共有するのはブランドの値と適用規則。製品固有のルート・class API・テーマの起動処理は**取り込まない**。生成 CSS は単独の媒体向けで、製品の CSS と全トークン・テーマ属性が一致するとは扱わない。

**カタログの在処はここに書かない**（この repo は public）。人に聞く。
