---
name: design-taste-jp
description: taste-skill(design-taste-frontend ほかデザイン系スキル群)を日本語運用に適応させる統治層。デザイン(LP・ポートフォリオ・redesign・UI)の依頼を日本語で受けたとき、Design Read と全ユーザー向け出力を日本語で行い、訳すと壊れる固有名詞を英語のまま保ち、和文タイポグラフィ固有の配慮(和文フォント・行間・禁則・和欧混植)を上乗せする。日本語プロダクト/日本語話者向けの画面を作るとき最初に使う。
origin: user
---

# design-taste-jp (デザインスキルの日本語運用)

taste-skill 系(`design-taste-frontend` 他)は優秀だがラテン文字前提。これは**それらを土台に、日本語運用と和文タイポの配慮を足す薄い統治層**。スキル本体は訳さない(ジャーゴンは訳すと壊れる)——運用のルールだけ日本語で定める。

## いつ使うか
- 日本語プロダクト / 日本語話者向けの LP・ポートフォリオ・redesign・UI を作るとき。
- taste 系スキルを日本語の依頼で回すとき。

## 土台にするスキル(登録名=ディレクトリ名で呼ぶ)
| 方向性 | 使うスキル(登録名) |
|---|---|
| 総合(アンチスロップ) | `taste-skill`(旗艦・内部名 design-taste-frontend)/ `gpt-tasteskill` |
| ミニマル / エディトリアル | `minimalist-skill` |
| 高級・エージェンシー質感 | `soft-skill` |
| ブルータリスト | `brutalist-skill` |
| 既存改修 | `redesign-skill` |
| 画像から実装 / 参考画像生成 | `image-to-code-skill` / `imagegen-frontend-web` / `imagegen-frontend-mobile` |
| ブランド / デザインシステム | `brandkit` / `stitch-skill` |
| 完全出力(省略禁止) | `output-skill` |

まず土台スキルの Design Read で方向性を決め、その上に下の日本語ルールを重ねる。

## ルール1: 出力言語
- **Design Read と全ユーザー向け出力は日本語**で書く。旗艦の「Reading this as: …」は日本語で:
  - 例:「これは **技術購買者向けの B2B SaaS ランディング**、**Linear 系のミニマル**言語、**Tailwind + Geist + 抑えたモーション**寄りと読みました。」
  - 例:「これは **採用担当向けの個人デザイナーポートフォリオ**、**エディトリアル/キネティックタイポ**言語、**native CSS + スクロール駆動アニメ**寄りと読みました。」
- 曖昧なら**1問だけ**日本語で聞く(taste-skill の作法を継承。多問ダンプ禁止)。

## ルール2: 訳さない固有名詞(英語のまま保つ)
- フォント名: Geist / Inter / Noto Sans JP など
- フレームワーク・技術: Tailwind / GSAP / CSS プロパティ名 / フレームワーク名
- 美意識ジャーゴン: Awwwards / Linear-style / bento / brutalist / glassmorphism / editorial
- コード・クラス名・変数
- → これらを無理に和訳しない([[anti-hallucination]]:訳語の捏造をしない)。

## ルール3: 和文タイポグラフィ(taste-skill に無い追加知見=本スキルの改良点)
日本語 UI はラテン文字と別物。以下を必ず考慮する。

- **和文フォント選定**: 本文=Noto Sans JP / Hiragino Kaku Gothic / Yu Gothic / Zen Kaku Gothic。見出しに明朝(Noto Serif JP)でコントラスト。Web フォントは**サブセット化**(和文は重い)。
- **行間(line-height)**: 和文は広め。本文 **1.7〜2.0**(ラテンの 1.4〜1.6 より大きく)。詰めると可読性が落ちる。
- **字間・約物**: `font-feature-settings: "palt"` で仮名の詰め。約物(、。「」())の空きに注意。全角/半角の混在を統一。
- **禁則処理**: 行頭に `。、` を置かない。CSS `line-break: strict;` `word-break: normal;` `overflow-wrap: anywhere` を用途で使い分け。
- **和欧混植**: `font-family` で欧文フォント → 和文フォントの順に指定し、英数字と日本語のベースライン/サイズ差を調整。数字は等幅 or tabular が要る箇所に注意。
- **改行の意味**: 日本語は分かち書きしないので、`<br>` や `<wbr>`・`word-break` で意図した位置に折る。6行折り返しの禁(gpt-tasteskill のルール)は和文でも有効=1文を長く垂れ流さない。
- **字面の圧**: 漢字は密度が高い。ラテン向けの VISUAL_DENSITY をそのまま使うと日本語は詰まって見える → **密度ダイヤルを1〜2下げる**か余白を増やす。

## ルール4: 品質ゲート(既存規則と接続)
- あなたの web/design-quality.md の**アンチテンプレ方針**(AI紫グラデ/中央寄せhero/等幅3カード等の禁止)を必ず適用。
- [[fable]] Phase 0 で完了条件(「どの画面が・どのブレークポイントで・何を満たせば完成か」)を先に固定。Phase 4 で実機確認(320/375/768/1024/1440、和文の折り返し崩れ・フォント落ちを実際に見る)。

## やってはいけない
- 13スキルを丸ごと和訳する(ジャーゴン破壊・誤訳リスク)。本スキルは**運用ルールの上乗せ**に留める。
- ラテン前提の行間・密度のまま日本語を流し込む(詰まって安っぽく見える)。
- Design Read を英語で出す。

## 関連
- 土台: `taste-skill` ほか taste 系(`~/.claude/skills/`、manifest=`.taste-skills-manifest.txt`)。
- [[fable]] / [[anti-hallucination]] — 完了条件と固有名詞の扱い。
- 既存デザイン資産(frontend-design / ui-ux-pro-max / design-system)と重複するときは、より具体的な方(taste の美意識別スキル)を土台に、本スキルで日本語運用を被せる。
