---
name: image-prompt-craft
description: 专业文生图提示词工程——把分镜写成电影级写实、欧美真实中产质感的图像提示词,并跨镜锁死角色身份、场景、人物走位。写关键帧/验证图/任何 image prompt 前必读。Triggers 文生图, image prompt, 提示词, keyframe, 关键帧, 人物一致, character consistency, 场景一致, 走位, staging, blocking, 欧美, photoreal, 中产.
---

# 文生图提示词工程:电影级写实 + 跨镜锁定

一张好图 = 具体 + 一致。业余提示词有两个通病:①一次一次重描主角("a young man"),模型每镜画一个**不同的人**;②只写"发生什么",不写"谁站哪、看哪",同一场景人物**位置乱跳**。这份 skill 就治这两条,并把画面拉到**欧美真实中产、电影写实**的高端质感——不是廉价 stock、不是塑料 AI 脸。

配合 `storyboard-craft`(故事/衔接)、`filmmaker`(镜头语言/180°轴线)、`emotional-narrative`(情绪)一起用:那三个管"拍什么",这份管"提示词怎么写才专业、才一致"。

## 铁律一:先建 Character Sheet,再逐镜**原样粘贴**(治身份漂移)

动任何镜头前,给**每个出场角色**写一段**锁定身份块(identity block)**,一次写死、之后每一镜出现该角色就**逐字复制**进提示词,只改动作/表情/机位。这是 prompt-only(z_image)做人物一致性的**唯一**办法(真正训练级一致要上 element/soul 参考,见 nolan-board 参考图铁律;但即便有参考,identity block 也要一起写)。

身份块必须具体到"选角卡"级别——**年龄段 + 族裔/肤色 + 身形 + 脸型五官 + 发型发色 + 精确服饰(单品+材质+颜色)**,并带一个**固定 seed 词**(如角色名当锚)。写进 `write_storyboard` 的版本 `meta.cast`,每镜 image_prompt 里再粘一次。

模板:
```
[NAME], a [age] [ethnicity] [gender], [build/height];
[hair: length/color/style], [face: features], [skin texture];
wearing [top: cut+material+exact color] + [bottom] + [shoes] + [accessories].
```

欧美中产范例(直接可用,B7《The Reservation》):
- **EVAN** — Evan, a early-30s white American man, lean athletic build, 180cm; short dark-brown hair neatly cropped, light stubble, warm hazel eyes, natural skin with faint texture; wearing an unstructured oatmeal wool blazer over a white cotton tee, charcoal tapered trousers, brown leather derby shoes, a thin steel watch.
- **MIA** — Mia, a late-20s Korean-American woman, slim, 165cm; shoulder-length glossy black hair with a middle part, soft natural makeup, warm brown eyes; wearing a camel ribbed-knit sweater, high-waist dark denim, gold hoop earrings, tan leather crossbody bag.

**只要 Evan 出现,这一整段 EVAN 原样进 prompt;Mia 同理。** 多人同框就两段都粘,并在动作里点名("Evan on the left…, Mia on the right…")。**一镜里同一角色只出现一次**(别让模型画出双胞胎)。

## 铁律二:建 Location Sheet,同样锁死

场景也写一段一次、逐镜复用——地点 + 时段 + 光态 + 关键陈设 + 色世界。同一场景的相邻镜必须共用这一段,只换机位/景别。

范例:
- **RESTAURANT** — an intimate hard-to-book American neighborhood bistro, evening; warm low candlelight + amber tungsten, walnut wood, small marble two-top by a window, muted olive-and-cream palette, other diners softly out of focus in the background.

## 铁律三:走位与轴线(治"人物位置混乱")

同一场景连续镜,**机位可以变,人物的相对位置不能乱**。每镜在提示词里写清三件事:

1. **屏幕位置**:谁在画面 left / right / center,前景还是背景("Mia seated camera-left, Evan camera-right across the marble table")。
2. **视线 (eyeline)**:各自看哪("Evan looking down at the menu", "Mia looking at Evan")——视线是剪辑衔接的锚。
3. **180° 轴线**:整场戏两人的左右关系**全程不翻**(Mia 一直在左、Evan 一直在右)。要越轴必须是有意的过轴镜。见 `filmmaker` 的轴线条目。

一句话:**身份块锁"是谁",走位块锁"在哪、看哪"**。两个都写,同场景才连得起来。

## 提示词骨架(按此顺序填槽,自然语言成句,别堆标签)

```
[STYLE 前缀,全片统一] — [SHOT SIZE + ANGLE] of [CHARACTER identity block(s)],
[action/pose + eyeline + screen position], in [LOCATION sheet],
[composition: foreground/background, negative space], [lighting state],
[mood]; [camera: lens/movement]. [负向尾缀]
```

- **STYLE 前缀**全片一个、逐字复用(如 `cinematic photoreal film still, 35mm, natural soft lighting, muted color grade, shallow depth of field —`)。
- **景别/角度**明确:ECU/CU/MCU/MS/WIDE + eye-level/low/high/over-the-shoulder。
- **镜头/焦段**:z_image、seedream、flux 认焦段与景深(24mm 广、35mm 记录感、85mm 人像压缩)——写。**注意 Nano Banana Pro 会忽略 mm/f 数**,给它就写景别与构图词。
- **自然成句**,不是 "man, office, warm, 4k" 这种 tag soup。

## 欧美真实中产质感(避开廉价 AI 感)

要"高端但不炫富、真实但不邋遢"。写进去:
- **film 质感**:`shot on 35mm film, subtle grain, natural color science, gentle highlight rolloff`;避免 `hyperreal, 8k, octane, HDR, overprocessed`(一写就塑料)。
- **真实皮肤**:`natural skin texture, faint pores and freckles, no retouching`;避免 `flawless/glossy/airbrushed`。
- **中产实景**:真实有生活痕迹的空间——`lived-in modern apartment, a few real objects on the counter, imperfect natural styling`;避免 `luxury mansion, showroom, pristine`。
- **穿搭**:`quality unbranded wardrobe, natural fabrics (wool, cotton, denim, leather)`,不写任何品牌 logo(会花屏+侵权)。
- **光**:`natural window light / practical lamps / candlelight`,`soft, motivated, slightly underexposed`;避免 `studio softbox, ring light`。
- **选角**:`authentic casting, relatable, early-30s`;避免 `supermodel, perfect, magazine`。

## 负向 & 质量尾缀(每条 prompt 结尾固定)

沿用 storyboard-craft 的单场景无分格尾缀,再补画质负向:
```
— single frame, one continuous scene, no split screen, no collage, no grid, no panels,
no storyboard layout, clean frame, no text, no caption, no watermark, no logo,
no plastic skin, no oversaturation, no distorted hands, no extra fingers, no warped faces
```
文字/UI/账单金额一律**后期叠加**,画面里留干净区域,绝不写进 prompt(见 nolan-board 干净画面铁律)。

## 落库

- 版本 `meta.cast` = 每个角色的完整 identity block(文档"人物"区靠它,出图靠它)。
- 版本 `meta.locations`(或写进 brief)= 每个 Location sheet。
- 每镜 `image_prompt` = STYLE 前缀 + 粘贴的 identity block(们)+ 走位 + Location + 机位 + 光 + 负向尾缀。
- `description` 写中文剧情(给人读),`image_prompt` 写英文(给模型)。

## 改写示范(把用户那版 S4 从业余改成专业)

**业余(身份/走位全缺)**:
> …the young couple entering together, she is visibly excited, he is smiling at her…

**专业(锁身份+走位+实景+质感)**:
> `cinematic photoreal film still, 35mm, natural soft lighting, muted color grade, shallow depth of field —` MS tracking from behind and slightly camera-left of the couple: EVAN [粘贴 EVAN 完整 identity block] on the right, one hand on the door; MIA [粘贴 MIA identity block] on the left, half a step ahead, looking back at him with genuine excitement — entering RESTAURANT [粘贴 Location sheet], warm amber interior spilling onto the wet evening sidewalk, other diners soft in the background; shot on 35mm film, subtle grain, natural skin texture, motivated candlelight; a gentle handheld follow. `— single frame, one continuous scene, … no plastic skin, no warped faces`

差别:同一个 Evan/Mia 会**跨镜长一个样**,Mia 全程在左、Evan 在右不乱,餐厅是同一间,质感是真实中产不是 stock。

## 验收(出图前自查)

1. 每个出场角色都粘了**完整 identity block**吗?(不是"the man")
2. 同场景相邻镜**左右位置、视线一致、不越轴**吗?
3. Location sheet 复用了吗?
4. 有没有 film/真实皮肤/实景/自然光这些**去 AI 感**词?
5. 负向尾缀 + 干净画面(文字后期叠加)守住了吗?
