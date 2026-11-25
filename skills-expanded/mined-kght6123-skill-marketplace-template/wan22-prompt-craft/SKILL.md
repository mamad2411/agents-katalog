---
name: wan22-prompt-craft
description: Wan2.2（Alibaba製オープンソース動画/画像生成モデル）向けのプロンプトを新規作成・修正・改善するスキル。ユーザーが「Wan2.2のプロンプトを書いて」「動画生成プロンプトを作って」「Wan2.2用に直して」「カメラワークを追加して」「プロンプトが短すぎる」「Wan2.2のプロンプトを改善して」「Wan 2.2」「Wan prompt」などと言った場合に使用する。動画生成AIのプロンプトエンジニアリング全般、ComfyUIでのWan2.2利用、Text-to-Video / Image-to-Video プロンプト、カメラワーク指示、ライティング・カラーグレーディング指定に関する質問や依頼にも積極的に使う。
---

# Wan2.2 プロンプトクラフト

Wan2.2の動画/画像生成プロンプトを作成・修正するためのスキル。FluxやStable Diffusionとは異なるWan2.2固有のプロンプト構造・語彙・ベストプラクティスに基づいて高品質なプロンプトを出力する。

## Wan2.2プロンプトの鉄則

以下の5つのルールは常に守る。

1. **80〜120単語を目指す** — 短すぎるとモデルが不足分を独自に補完してランダムな結果になりやすい（MoE構成の A14B 系モデルはこの傾向がより強い）。逆に長すぎても効果は薄い
2. **カメラワークを明確に指定する** — Pan / Tilt / Dolly / Orbital / Crane / Tracking など。Wan2.2の最大の差別化ポイント
3. **ライティングとカラーグレーディングを含める** — volumetric dusk, teal-and-orange, kodak portra など具体的なスタイルワード
4. **モーションの質感を記述する** — slow-motion, whip-pan, smooth glide, handheld tremor などスピード・深度表現
5. **短いクリップに収める想定で書く** — フレーム数は `4n+1`（61, 81, 97, 121 など）である必要がある。実用上は **81フレーム（16fpsで約5秒）** か **121フレーム（24fpsで約5秒）** の2択を基本にする。Wan2.2はこの長さで最も高品質

## プロンプト構造テンプレート

プロンプトは以下の4パートで構成する。すべてのパートを含める必要はないが、最低でも①②④は含めること。

```
① Opening Scene（シーン設定）
② Camera Movement（カメラワーク）
③ Motion Details（動き・アクションの詳細）
④ Visual Style & Color Grade（映像スタイル・ライティング・カラーグレード・レンズ効果）
```

### パート別の書き方

**① Opening Scene** — 「誰が」「どこで」「何をしている」を簡潔に。スタイルキーワード（cinematic, documentary style, anime style など）を冒頭に置くと効果的。

**② Camera Movement** — カメラワーク語彙表（後述）から選ぶ。方向と速度を明記する。複合カメラワーク（パンしながらドリーインなど）も可。

**③ Motion Details** — 被写体の動き、環境の動き（風、水、煙など）、前景/中景/背景の動きの差を記述すると立体感が出る。

**④ Visual Style & Color Grade** — ライティング（volumetric dusk など）、色調（teal-and-orange, bleach-bypass など）、レンズ効果、フィルムスタイル、HDR設定、フィルムグレインなどをまとめて記述する。

## カメラワーク語彙表

| カメラワーク | プロンプト表現 | 説明 |
|---|---|---|
| パン（左右） | `Camera pans left/right` | 水平方向の移動 |
| チルト（上下） | `Camera tilts up/down` | 垂直方向の移動 |
| ドリー（前後） | `Camera dollies in/out` | 被写体に近づく/離れる |
| オービタル | `Slow 360° orbital shot` | 被写体を中心に回転 |
| クレーン | `Crane shot rising above...` | 上空へ上昇/下降 |
| トラッキング | `Steadily tracking forward` | 被写体を追跡移動 |
| ウィップパン | `Aggressive whip-pan` | 高速パン（モーションブラー） |
| 手持ち | `Handheld tremor` | 揺れによるリアリティ |
| 滑らか移動 | `Smooth glide` | 安定した滑らかな移動 |

カメラワークが指示と逆方向に動くことがある。その場合は表現を強化する：
- 弱い: `Camera pans left`
- 強い: `Camera performs a deliberate, smooth pan left across the scene, moving from right to left steadily`

## ライティング・カラー語彙表

**ライティング:**
- `volumetric dusk` — ボリューメトリックな夕暮れ
- `harsh noon sun` — 強い正午の太陽
- `neon rim light` — ネオンのリムライト
- `soft backlight` — 柔らかい逆光
- `god rays` — 光芒
- `studio key light` — スタジオのキーライト

**カラーグレーディング:**
- `teal-and-orange` — 映画的なティール&オレンジ
- `bleach-bypass` — 彩度低下のブリーチバイパス
- `kodak portra` — 暖色系フィルム風
- `cinemagraphic HDR` — シネマグラフィックHDR
- `desaturated` — 低彩度

**レンズ・撮影スタイル:**
- `anamorphic bokeh` — アナモルフィックボケ
- `16mm grain` — 16mmフィルムグレイン
- `shallow depth of field` — 浅い被写界深度
- `lens flare` — レンズフレア
- `wide-angle distortion` — 広角歪み

## アニメ風プロンプトのコツ

Wan2.2は実写シネマティック系が強みだが、アニメ風の映像も生成できる。ただしFluxやSDXLのようなタグベースではなく、映像演出の言葉で指示するのがポイント。

### スタイル指定キーワード

冒頭に以下のいずれかを置いてアニメ風であることを明示する：
- `Anime-style cinematic scene` — 汎用的なアニメ映像
- `In the style of Japanese animation` — ジブリ〜京アニ的な方向
- `Cel-shaded animation style` — セルシェーディング強調
- `2D animated sequence` — 2Dアニメ感を強調
- `Anime key visual style` — キービジュアル的な一枚絵（frames=1向け）

### アニメ特有の演出語彙

| 表現 | プロンプト | 効果 |
|---|---|---|
| 髪・服のなびき | `hair flowing dramatically in the wind` | アニメ的な動きの誇張 |
| 光の粒子 | `sparkling light particles floating in the air` | 幻想的な演出 |
| 速度線 | `dynamic speed lines in the background` | アクションの躍動感 |
| 桜・花びら | `cherry blossom petals drifting across the frame` | 日本アニメの定番演出 |
| 夕焼けグラデ | `dramatic sunset gradient sky in warm orange and purple` | アニメの印象的な空 |
| レンズフレア | `bright anime-style lens flare` | 光の演出 |
| 感情エフェクト | `soft glow surrounding the character` | キャラクターの存在感強調 |

### アニメ風で避けるべきこと

- `photorealistic` や `RAW photo` など実写系のキーワードは競合するので使わない
- `16mm grain` や `kodak portra` などフィルム系も合わない
- 代わりに `vibrant colors`, `clean lines`, `smooth shading` など絵的な語彙を使う

### アニメ×カメラワークの相性

アニメでもカメラワーク指示は有効。特に以下が効果的：
- **ドリーイン** — キャラクターの感情を強調するクローズアップへの移動
- **パン** — 背景美術を見せる横移動
- **チルトアップ** — 巨大な存在やスケール感の演出
- **スローモーション** — アクションの決めポーズ、感情の高まり

## モーション表現

**スピード:**
- `slow-motion` — スローモーション
- `whip-pan` — 高速パン
- `time-lapse` — タイムラプス
- `handheld tremor` — 手持ちの揺れ
- `smooth glide` — 滑らかな移動

**深度（立体感の演出）:**
前景・中景・背景の動きの差を書く。例: `Foreground grass sways gently while mountains remain still in the background`

## タスク別の対応手順

### 新規プロンプト作成

1. ユーザーからシーンのアイデア（被写体、場所、雰囲気、用途）を確認する
2. T2V（テキストから動画）か I2V（画像から動画）か、または画像生成（frames=1）かを確認する
3. テンプレート構造に従って80〜120単語のプロンプトを作成する
4. 完成したプロンプトを英語で提示する（Wan2.2は英語プロンプトが最も安定）
5. 必要に応じてネガティブプロンプトも提示する（基本は軽量な推奨ネガティブで十分）

### 既存プロンプトの修正・改善

1. ユーザーのプロンプトを受け取る
2. 以下のチェックリストで診断する：
   - [ ] 単語数は80〜120語の範囲か？（短すぎるのが最も多い問題）
   - [ ] カメラワーク指示が含まれているか？
   - [ ] ライティング/カラー指示が具体的か？
   - [ ] モーション表現（速度・深度）があるか？
   - [ ] 前景/背景の記述で立体感が出ているか？
3. 不足しているパートを追加し、改善版を提示する
4. 変更点を箇条書きで説明する

### 画像生成モード（frames=1）

動画モデルなので静止画でも「動画の1フレーム」のように見えることがある。カメラワーク指示は削除または最小限にしたうえで、以下を追加する：
- **実写・シネマティック系**：`photorealistic, natural depth, layered composition, cinematic still frame`
- **アニメ風**（アニメ風プロンプトのコツを参照）：`photorealistic` は使わず、代わりに `anime key visual style, layered composition, natural depth, cinematic still frame` を使う。`16mm grain` や `kodak portra` などフィルム系語彙も避ける

## ネガティブプロンプト

特殊な要件がなければ、以下の軽量なネガティブプロンプトで十分:
```
blurry, ugly, low quality, distorted, deformed
```
中国語版: `模糊，丑陋，低质量，变形，扭曲`

## 出力形式

プロンプトは常に以下の形式で提示する：

```
**Prompt:**
[英語プロンプト本文]

**Negative prompt:**
blurry, ugly, low quality, distorted, deformed

**推奨設定:**
- Mode: T2V / I2V / Image (frames=1)
- Length: [フレーム数、`4n+1` を満たす値] ([秒数])
- Size: [解像度]
```

プロンプト提示後、日本語で各パートの意図や狙いを簡潔に説明する。

## 実践例

詳細な実践例とモデルバリエーションの選び方は `references/examples.md` を参照。カメラワークの組み合わせ例や、ジャンル別テンプレート（アクション、風景、ポートレート、サイバーパンク等）が含まれている。
