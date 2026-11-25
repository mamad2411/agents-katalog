---
name: sdxl-original-character-prompt-craft
description: 特定のオリジナルキャラクター（ピンク髪・ハート目・全年齢エロ可愛い）向けにSDXL用プロンプト（ポジティブ＋ネガティブ）を生成・改良するスキル。ユーザーが「SDXLのプロンプトを作って」「○○のテーマでSDXLのプロンプトを書いて」「SDXL用に直して」「SDXLのプロンプトを改善して」「SDXLプロンプト」「Stable Diffusion XL prompt」などと言ったら必ず使う。固定のキャラクターテンプレートを基盤に、テーマ・シチュエーション・衣装・構図を改変してコピペ可能な完成プロンプトを出力する。SDXLのText-to-Image生成・LoRA指定・カメラワーク・ライティング指示の話題が出たときも積極的に使う。
---

# SDXL Prompt Craft（オリジナルキャラクター用）

特定のオリジナルキャラクター向けに、SDXLのText-to-Imageプロンプトを生成・改良するスキル。

## このスキルの基本方針

- **キャラクターの一貫性は維持する**：基本属性（ピンク髪、ハート目、全年齢エロ可愛い）は固定
- **年齢表現は成人**：このキャラクターは成人女性として扱う。学生服・学校を想起させる設定は避ける
- **テーマに応じて変える**：シチュエーション、衣装、ポーズ、背景、ライティング、LoRA重みなど
- **コピペ可能な形で出す**：ポジティブとネガティブを別々のコードブロックで出力
- **「映え」を狙う**：バズり狙いの構図・配色・ポーズを優先

---

## 出力フォーマット

必ず以下の形式で出力する（説明文は最小限、コピペしやすさ最優先）：

````
## ポジティブプロンプト

```
（ここにポジティブプロンプト）
```

## ネガティブプロンプト

```
（ここにネガティブプロンプト）
```
````

---

## ベースプロンプト構造（ポジティブ）

ポジティブプロンプトは以下の順序で構築する。各ブロックの間は空行で区切ると人間が読みやすい：

1. **品質タグ**（固定）
   `masterpiece, best quality, very aesthetic, ultra-detailed, beautiful detailed eyes, beautiful detailed face,`

2. **シーン・ライティング**（テーマに応じて変える）
   背景、時間帯、光の演出、エフェクト（光の粒子、ボケ、レンズフレアなど）

3. **画風指定**（基本固定、テーマで微調整）
   `soft anime illustration, pastel color palette, vibrant pastel tones, dreamy atmosphere, cinematic lighting,`

4. **キャラクター基本情報**（固定）
   `1girl, solo, mature female, balanced proportions, large breasts,`

5. **ポーズ・ハンドジェスチャー**（テーマに応じて変える）
   ポーズ、手の動作、表情。**ハート目は必須**：`heart-shaped pupils, heart in eyes, sparkling eyes,`

6. **表情**
   `smiling, happy expression, open mouth smile, pink eyes,` をベースに、テーマで微調整

7. **衣装**（テーマに応じて変える）
   トップス、ボトムス、靴、小物、帽子。スカートのなびきや髪のなびきがあると映える

8. **立ち位置・立ち方**（テーマに応じて変える）
   足元の状態、立っている場所

9. **髪・顔のディテール**（基本固定）
   `long light pink hair, flowing hair strands, hair fluttering in the wind,` ＋ テーマに応じたヘアアクセ
   `light eyebrows, slightly pink cheeks, soft blush,`

10. **線画・シェーディング**（固定）
    `no lineart, soft cel shading, subtle gradient shading, glossy highlights,`

11. **ライティング詳細**（テーマで微調整）
    `soft lighting, diffused light, light bloom, rim light, backlight, god rays,`

12. **カメラ・構図**（テーマに応じて変える、**ダイナミックを優先**）
    視線、角度、ショットサイズ、背景の詳細さ、被写界深度

13. **ムード**（テーマに応じて変える）
    全体の感情・空気感のキーワード

14. **LoRAとトリガーワード**（環境依存、要差し替え）
    以下は構成の一例。**LoRAのファイル名・トリガーワードは生成環境ごとに異なるため、このまま使っても存在しないLoRA名としてエラーになるか無視される**。自分の環境にあるLoRA（ディテール強化系・画風系など）とそのトリガーワードに置き換えて使うこと。

    ```
    <lora:ディテール強化系LoRA:1.5> <lora:キャラクター/画風LoRA:1>,
    <lora:和風/洋風の画風LoRA:0.7>, [トリガーワード],
    ```
    - ディテール強化系LoRA：基本1.5、ディテール重視のテーマでは1.7まで上げてOK
    - キャラクター/画風LoRAの重みは、そのLoRAの推奨値に従う
    - 和風/洋風の傾向を出すLoRAがあれば、和風テーマで0.8〜0.9、洋風・モダン系で0.5〜0.6程度から調整する
    - トリガーワードが必要なLoRAを使う場合は、生成のたびに必ず維持する

---

## ベースプロンプト構造（ネガティブ）

ネガティブプロンプトはほぼ固定。テーマに応じて末尾の構図関連だけ微調整する：

1. **品質除外**（固定）：`worst quality, low quality, normal quality, jpeg artifacts, blurry, out of focus,`
2. **解剖学エラー除外**（固定）：`bad anatomy, bad hands, extra digits, missing fingers, malformed limbs, deformed,`
3. **目のエラー除外**（固定、ハート目を維持するため重要）：`asymmetric eyes, cross-eyed, deformed pupils, half-closed eyes,`（ポジに `half-lidded eyes` を使うときは、ここから `half-closed eyes` を抜く。NG集参照）
4. **ポーズ除外**（基本固定、ただしテーマで意図的に座らせたい場合などは `sitting` を抜く）：`stiff pose, standing straight facing front, sitting,`
5. **画風除外**（固定）：`thick lineart, sketchy lines, flat shading only, monochrome,`
6. **ライティング除外**（固定）：`harsh shadows, strong contrast, dramatic dark lighting, gloomy,`
7. **写実除外**（固定）：`photorealistic, realistic skin texture, 3d render,`
8. **背景・構図除外**（固定）：`busy background, cluttered background, multiple girls,`
9. **表情除外**（固定）：`expressionless, angry expression, crying,`
10. **メタ情報除外**（固定）：`text, watermark, logo, signature,`
11. **NSFW除外**（固定、全年齢のため）：`nsfw, nude, cleavage, exposed breasts, unbuttoned, see-through skin, transparent clothes showing body, wet clothes clinging to nude body,`
    - ここでの `see-through` / `wet clothes` は「肌や下着が透けて見える」表現を指す。Tips集の `sheer stockings`（生地の質感）や `wet hair`（濡れた髪の艶）程度の演出はこれに抵触しない
12. **ショットサイズ除外**（テーマに応じて変える）：基本は `full body, wide shot, long shot, small face, cowboy shot, thigh-up shot,` を入れて顔・上半身が映えるショットを維持する。全身を見せたいテーマのときは、この項目自体を外すか望むショットだけ削る

---

## NG集（やってはいけないこと）

このスキルを使うときに必ず守るルール。指摘されたら追記して自己改善する。

- ❌ **強調括弧 `(word:1.3)` や `((word))` を使わない**：色が真っ黒になる原因。重みの調整はLoRA側で行う
- ❌ **静的な棒立ち構図にしない**：「ダイナミックな構図」を優先。動きのあるポーズ、風になびく髪・スカート、低めのアングルや見上げ構図を積極的に使う
- ❌ **ハート目を外さない**：`heart-shaped pupils, heart in eyes` は必須。テーマが落ち着いた雰囲気でも入れる
- ❌ **全年齢の範囲を外さない**：エロ可愛さは「ちらり」「ふわり」「生地の透け感」「ちょっとしたポーズ」で表現。肌が透けて見えるほどの表現や露出はNG
- ❌ **「無難で安全」な構図を選ばない**：バズり・SNS映え狙いを優先。ありきたりな正面立ち絵は避ける
- ⚠️ **「可愛い」だけで単調にしない**：テーマに合うなら、色気の要素も検討する（必須ではない。全年齢の範囲で、テーマに合わないなら無理に入れない）
- ⚠️ **半目系の重複に注意**：`half-lidded eyes`（誘うような半目）をポジに入れたいときは、ネガから `half-closed eyes` を抜く。両方残すと衝突する。代替表現として `seductive eyes, bedroom eyes` も使える
- ❌ **全身を見せたいテーマでもないのに、ショットサイズ除外（§ネガティブ12）を理由なく削らない**：基本は顔・上半身が映えるショットサイズを維持する

---

## Tips集（映え＆可愛さを上げるコツ）

良いプロンプトを作るためのヒント。新しい発見があったら追記して自己改善する。

### 構図・カメラワーク（ダイナミックさを出す）
- **ローアングル見上げ**：`from below, looking up at viewer, dynamic angle` で躍動感
- **ダッチアングル**：`dutch angle, tilted camera` で動きを出す
- **動きのあるポーズ**：走る、ジャンプ、振り返り、髪をかきあげる、スカートを押さえる
- **風の演出**：`wind blowing, hair fluttering, skirt fluttering, petals flying` でレイヤーを増やす
- **手前ボケ前景**：`foreground blur, foreground bokeh, out of focus foreground elements` で奥行き

### 「映え」を出す要素
- **光の演出を盛る**：`god rays, light particles, lens flare, light bloom, sparkles, glitter` を組み合わせる
- **色対比**：パステルベースに1色だけ強い色（夕焼けのオレンジ、ネオンのピンクなど）を入れる
- **シーズン要素**：桜、紫陽花、向日葵、紅葉、雪、イルミネーションなど季節感のある背景
- **マジックアワー**：`golden hour, blue hour, magic hour` は鉄板で映える

### 「可愛さ」を盛る要素
- **小物**：リボン、フリル、レース、ぬいぐるみ、お菓子、花、ハートの装飾
- **ハンドジェスチャー**：ハート、ピース、頬に手、口元に指、両手で何か持つ
- **頬の赤み**：`soft blush, pink cheeks, slightly flushed cheeks`
- **目のキラキラ**：`sparkling eyes, starry eyes, shiny pupils, glossy eyes`

### シチュエーション別の鉄板テク

**和装（浴衣・着物・巫女）系の色気**
- うなじを露出する構図が最強：`exposed nape of neck, lifting hair off nape, hair tied up, hair pulled back`
- 振り返り構図と相性◎：`looking back over shoulder, three-quarter back view emphasizing nape and shoulder line`
- 着崩れ感（NSFWラインを越えない範囲）：`slightly loosened obi sash, off-shoulder yukata slip, one shoulder exposed, yukata hem hiked up by movement, exposed ankle, glimpse of inner thigh through yukata slit`
- 後れ毛：`loose hair tendrils on neck, stray hair strands on neck`
- 浴衣の場合、ネガに `unbuttoned yukata, fully open yukata` を追加して着崩れすぎを防ぐ

**夏・暑い季節の色気（汗・光反射）**
- `sweat drops on cheek and neck, sheen of sweat on shoulder and collarbone, slight perspiration on chest`
- `sweat-damp hair clinging to skin, dewy glistening skin, glossy skin`
- `light reflecting off sweat` を入れると光と組み合わさって質感が映える
- 夜＋光源（花火・提灯・ネオン）と組み合わせると、`fireworks light illuminating body from above, multiple fireworks reflected on skin` のような肌に光が映る描写が強い

**洋装（カフェ・室内）系の色気**
- 体のラインを出す：`tight fitting clothes, body-hugging fabric, oversized shirt with body line visible`
- 小さな露出：`off-shoulder, bare shoulders, exposed collarbone, crop top showing navel`
- 絶対領域：`thigh highs, zettai ryouiki visible, lace trim stockings`
- アクセントに `black ribbon choker, neck ribbon, gold chain necklace`

**変身・ファンタジー系の色気**
- 衣装が形成される瞬間の演出：`light ribbons partially covering skin in transformation, ribbons trailing across body`
- 浮遊・反らせ：`floating mid-air, weightless pose, pronounced back arch, hips tilted`
- 肌のツヤ強調：`glowing skin, light sheen on shoulders and thighs`

### 「全年齢エロ可愛い」のさじ加減（**テーマに合えば色気も検討する**）

**方針**：可愛さだけでも成立するが、テーマ次第では全年齢の範囲内で色気・セクシーさの要素を足すと「映え」につながりやすい。無理に毎回入れる必要はなく、テーマに合わないときは入れない。

**ポーズ・しぐさで色気を出す（推奨）**
- `slight back arch, arched back, gentle curve of the back` 軽く反らせる
- `legs slightly crossed, knees touching, inner thighs visible` 内ももをチラ見せ
- `hand on hip, hand on waist, hand brushing hair behind ear` 手の動きで艶っぽさ
- `bending forward slightly, leaning forward, looking back over shoulder` 振り返り・前傾
- `licking lips, biting lower lip, finger near lips, finger on chin` 口元の演出
- `arms behind back, both hands behind head, stretching pose` 胸のラインを強調
- `looking down at viewer, half-lidded eyes, seductive gaze, sultry expression` 目線で誘う
- `playing with hair, lifting hair, hair tucked behind ear` 髪をいじる仕草

**衣装で色気を出す（推奨）**
- `oversized shirt, off-shoulder, bare shoulders, exposed shoulders` 肩・鎖骨を出す
- `tight fitting clothes, form-fitting outfit, body-hugging fabric` 体のラインを出す
- `crop top, short top, bare midriff, exposed belly button, navel visible` お腹チラ見せ
- `mini skirt, micro skirt, short skirt, skirt lift by wind` ミニスカ＋風
- `thigh highs, over-knee socks, garter belt visible, zettai ryouiki` 絶対領域
- `choker, ribbon collar, neck ribbon` 首元アクセで視線誘導
- `sheer stockings, lace details, frilly underskirt peeking` 透け感・レース（肌が透けて見えるほどにはしない）
- `wet hair, glistening skin, sweat drops, dewy skin` 濡れ感・汗
- `loose ribbon, untied ribbon, slightly disheveled` アクセサリー・後れ毛程度の着崩れ感（服がはだけて肌が露出するのはNGライン）
- `swimsuit, bikini, one-piece swimsuit` 水着系（露出ではなく可愛さで。谷間や下着ラインの強調は避ける）

**身体表現の演出（推奨）**
- `soft skin, smooth skin, glossy skin, shiny skin` 肌の質感
- `flushed cheeks, deeper blush, embarrassed expression` 赤面強め
- `hot breath, slight pant, parted lips, glossy lips` 息遣い・口元
- `arched eyebrows, slight tearful eyes, watery eyes` 困り顔・潤んだ目

**OKライン（全年齢内）**
- うなじ、肩、鎖骨、二の腕、お腹のちょっとした露出
- 内もも、絶対領域、足首、ふくらはぎ
- 胸のライン（服の上からのシルエット）
- 下着のひも・キャミソールの肩紐がチラッと見える
- 体に密着した衣装、肌が透けない程度の生地の濡れ感（艶・光沢の演出であって、肌が透けて見える表現ではない）
- お風呂上がり・湯気・タオル巻き（タオルはしっかり巻く）

**NGライン（必ず避ける）**
- 胸の谷間 `cleavage` の直接的な強調
- 下着そのものが見える `panties visible, underwear visible`
- 肌の過度な露出（`exposed breasts, nude, topless`）
- はだけた服（アクセサリーの緩み程度を超えるもの）`unbuttoned shirt, open shirt exposing chest`
- 透けて中身が見える `see-through, transparent clothes`

**実装のコツ**
- 色気の要素を入れるときは、ポーズ1つ＋衣装1つ、など組み合わせると効果的
- 「ハート目」「キラキラ」「可愛さ」と**両立**させる（あくまでエロ可愛い、エロだけにしない）
- 色気を盛るときも、ネガティブプロンプトのNSFW除外はそのまま維持する

### 衣装のバリエーション例
- 春：ニットカーディガン、シフォンブラウス、プリーツスカート、麦わら帽子
- 夏：白ワンピース、リネンシャツ、ショートパンツ、サンダル、ストローハット
- 秋：ベレー帽、ロングカーディガン、チェックスカート、ローファー
- 冬：ダッフルコート、マフラー、ベレー帽、ニーハイブーツ、手袋
- イベント：浴衣、サンタコスチューム、ハロウィンコス、メイド服

### LoRA重みの調整指針
- ディテール重視（顔のアップ、衣装の質感）：ディテール強化系LoRAを1.7程度まで上げる
- 和風（着物、和室、神社、桜、紅葉）：和風LoRAがあれば0.8〜0.9程度
- 洋風・モダン（カフェ、街、室内、洋装）：和風LoRAは0.5〜0.6程度に抑える
- ファンタジー（魔法少女、衣装大盛り）：ディテール強化系LoRAを1.7程度まで上げる

---

## 改造ワークフロー

ユーザーから「○○のテーマでプロンプトを作って」と言われたら：

1. **テーマを分解する**
   - シーン（場所・時間・季節）
   - ムード（明るい/しっとり/ダイナミック など）
   - 衣装の方向性
   - ポーズ・表情のニュアンス

2. **ダイナミック寄りに振る**
   - 棒立ちにせず、動きのある構図を選ぶ
   - 風・光・粒子のレイヤーを必ず1つ以上入れる
   - カメラアングルに変化をつける（真正面以外を優先）

3. **「映え＆可愛さ」を意識、テーマに合えば色気もプラス**
   - Tips集の要素を最低2〜3個取り入れる
   - 色対比 or 光演出 or 小物 のいずれかは必ず
   - テーマに合うなら、色気の要素も1〜2個検討する（ポーズ系＋衣装系の組み合わせ推奨。必須ではない）

4. **ハート目は維持**

5. **LoRA重みをテーマに合わせて微調整**

6. **NG集に違反していないかチェック**
   - 強調括弧使ってない？
   - 棒立ちじゃない？
   - ハート目入ってる？
   - テーマに合う場合、色気の要素も検討したか？
   - 露出多すぎない？（NSFWラインを越えてない？）
   - ショット指定が顔・上半身寄りになってる？

7. **出力**：上の「出力フォーマット」通りにポジ/ネガをコードブロックで出す。説明は最小限に。

---

## 自己改善

このSKILL.mdはマーケットプレイスの配布物であり、直接編集しない。プラグインが更新されるたびに上書きされ、更新を受け取れなくなるため。

ユーザーから出力に対する指摘があった場合、このスキルを親とする**子スキル**に追記する。

- 子スキルの場所：`~/.claude/skills/sdxl-original-character-prompt-craft-updates/SKILL.md`（無ければ新規作成する）
- 子スキルのフロントマター例：
  ```
  ---
  name: sdxl-original-character-prompt-craft-updates
  description: sdxl-original-character-prompt-craft スキルの追加NG集・Tips集を保持する子スキル。sdxl-original-character-prompt-craft を使う際は必ず一緒に参照する。
  ---
  ```
- 「○○がダメ」「△△の方が良い」と言われたら → 子スキルの **NG集** に追記
- 「□□すると映える」「◇◇が可愛い」と言われたら → 子スキルの **Tips集** に追記
- 追記後、子スキルの「NG集/Tips集に追記しました」と一言伝える
