---
name: seo-image-prompt
description: 基于 SEO 内容理解自动生成配图 Prompt。先读懂页面语义再决定画什么，为每个模块（intro/pain/usecase/highlight）生成高质量配图 prompt 和 SEO 元数据。
agent_created: true
---

# SEO配图Prompt引擎

> 功能定位：读懂 SEO 页面内容 → 为每个模块生成配图 Prompt → 输出完整的图片 SEO 元数据。

---

## 启动前置问答

**执行任务前，必须先向用户确认以下信息。**

### Q1. 品牌视觉信息
请提供：
- 品牌主色调：
- 品牌次色调（如有）：
- 视觉风格偏好：（例如：写实摄影 / 3D 渲染 / 扁平插画 / 科技风）
- 需要避免的视觉元素：（例如：不用蓝色光效、不用机器人手、不用全息 UI）

### Q2. 页面内容
请提供需要配图的页面信息：
- 页面 Title：
- 页面 H1：
- 所有 H2 标题及其对应正文：（或直接提供完整 Markdown 文件）
- 核心关键词：
- 目标用户（至少 2 类）：

### Q3. 图片规格
- [ ] 图片尺寸是否有特殊要求？（默认 intro/pain/highlight=1:1, usecase=16:9）
- [ ] 是否需要指定生图模型？
- [ ] 是否需要下载图片到本地？还是只输出 URL？
- [ ] 每张图是否需要同时输出 alt text / filename / caption？

### Q4. 已配图的页面（防止风格碰撞）
最近配图过的页面是什么？它们的视觉风格和色彩基调是怎样的？我需要确保新配图与之统一。

---

**收到以上信息后，开始执行配图 Prompt 生成。**

---

## 核心思路：先读懂页面，再决定画什么

不是根据"模块标签"决定画什么——而是先解析页面内容，理解语义后再出图。

每张图生成前必须先回答四问：

```
Who:    目标用户是谁？（从页面内容提取，不只从关键词猜）
Problem: 用户遇到什么痛点？（从 H2 正文提取）
Action:  工具做了什么？
Result:  用户得到什么？
```

---

## 工作流

```
Step 1: 解析页面内容
  输入：页面的 title + h1 + 所有 h2 及其正文
  输出：Page Understanding（关键词 / 搜索意图 / 目标用户 / 核心功能）

Step 2: 为每个模块写 Image Intent Statement
  Who + Problem + Action + Result，必须引用具体 H2 内容

Step 3: 从 Intent Statement 延展为 Prompt

Step 4: QA 评分
  内容匹配度检查（能否溯源到具体 H2 文案？）
  图片质量检查（是否泛化、是否与其他页撞图？）
```

---

## 模块配图策略

| 模块 | 生图? | 目的 | 默认构图 |
|------|:---:|------|---------|
| intro | ✅ | 回答 "What is [keyword]?" | 见下方 intro 选项 |
| pain | ✅ | 回答 "Why change?" | split_screen（Before vs After） |
| usecase | ✅ | 回答 "Who uses it? Why?" | 见下方 usecase 模式 |
| highlight | ✅ | 回答 "What can it do?" | feature_proof（功能证据） |
| howto | ❌ | 操作流程 | 真机截图，不走 AI |
| review | ❌ | 用户评价 | 暂不配图 |
| cta | ❌ | 行动引导 | 暂不配图 |
| faq | ❌ | 长尾关键词 | 暂不配图 |

### Intro 四种构图选项

根据产品类型选择：

| 选项 | 适用场景 | 构图 |
|------|---------|------|
| transformation | 有明确 input→output 的工具（如去背、增强） | 左 input → 中 AI → 右 output |
| analysis | 分析/检测类工具 | 原图 + 标注/报告叠加 |
| capability | 生成类工具，成品说明一切 | 全幅最佳结果 + AI badge |
| scenario | 强调使用场景 | 人物在真实环境中使用/享受结果 |

### Usecase 四种区分模式

| 模式 | 适用 | 3 张图按什么区分 |
|------|------|----------------|
| persona | 用户身份差异明显 | 3 种用户身份 + 环境 |
| scenario | 使用场景差异明显 | 3 种使用场景 |
| industry | 跨行业应用 | 3 种行业/垂直领域 |
| before-after | 核心价值是对比 | 3 组不同素材的 before/after |

---

## Prompt 写作铁律

| # | 原则 | 做法 |
|---|------|------|
| 1 | **说物品不说标签** | ❌ `luxury aesthetic` → ✅ `cream cashmere coat with visible weave texture` |
| 2 | **说光源不说氛围** | ❌ `warm atmosphere` → ✅ `late afternoon sun through tall windows` |
| 3 | **说材质不说风格** | ❌ `Vogue editorial` → ✅ `matte black turtleneck against raw concrete` |
| 4 | **限色调不堆色** | 限定 1-2 主导色 + 1 中性色。`cream, charcoal, camel — no bright colors` |
| 5 | **不教 AI 排版** | 不要 `top half empty for text`，排版是 CSS 的事 |
| 6 | **否定词必加** | 每张图末尾追加否定词，例如：`No text, no words, no watermarks, no logos, no unnatural poses, no oversaturated colors`（可根据实际需要增减） |

### 人物描述公式

```
[性别] + [2个面部特征] + [发型/发色] + [穿着—说材质颜色不说品牌] + [姿势—说关节不说形容词] + [表情—说五官部位不说情绪词]
```

示例：

| ❌ 模糊 | ✅ 具体 |
|---------|--------|
| beautiful smiling woman | woman with high cheekbones and slight gap between front teeth, mid-length ash blonde hair tucked behind one ear, lips parted in half-smile |
| confident male model | man with defined jawline and faint crow's feet, dark hair swept back, weight shifted onto right hip, eyes narrowed as if listening |

### 场景描述公式

```
[地点—具体物体] + [光源—方向+颜色+软硬] + [前景/背景材质] + [色调约束]
```

### 常见出图问题与修正

| 问题 | 原因 | 修正 |
|------|------|------|
| 人物过于完美/对称 | prompt 用了 beautiful/perfect 等词 | 给不对称特征：gap teeth, crooked smile, one eyebrow slightly raised |
| 光照不自然（全局均匀柔光） | 没指定光源 | 指定光源方向 + 阴影落点 |
| 皮肤质感差（像塑料或 CG） | 没描述皮肤质地 | 加 `visible pores, fine lines at eye corners, natural skin texture` |
| 颜色过于饱和 | AI 默认高饱和 | 限色调：用具体色名 + muted palette |
| 手指/关节变形 | AI 通病 | 否定词：`natural hands, relaxed fingers` |

---

## 泛化图片禁令

以下类型图片容易沦为"可套用到任何产品页的模板图"，应尽量避免：
- 无具体身份、无具体场景的"通用人物"
- 与产品功能无关的 lifestyle 场景
- 过于抽象、无法识别产品用途的装饰图

**每张图必须能溯源到页面中的具体一句 H2 文案。** 如果画出来的人和场景可以套用到任何其他同类产品页面上 → 这张图是泛化的，重做。

---

## Prompt 组装模板

```
[画面内容：谁+穿什么+在哪+做什么]
+ [光源：方向+颜色+阴影]
+ [材质：2-3个具体表面描述]
+ [色调约束：限定2-3色]
+ [否定词清单]
```

完整示例：

```
A man in a charcoal wool overcoat with visible herringbone weave, 
standing on wet cobblestones at blue hour, one hand in pocket, 
looking slightly past the camera with a faint asymmetrical smile. 
A single streetlamp casts warm amber light from above-left, 
leaving the right side of his face in cool shadow. 
Rain reflections on the stones. 
Entire image in charcoal, navy blue, and muted amber — no other colors.
No text, no words, no watermarks, no unnatural poses.
```

---

## QA 评分

### 图片质量评分

每张图从以下维度评估（0-5 分），综合评分偏低时应重新设计 Prompt：

- Intent Match：是否匹配搜索意图？
- Entity Recognition：能否一眼识别产品/功能？
- Commercial Value：是否增强转化意愿？
- Visual Clarity：画面是否清晰无歧义？
- Image Search Potential：在 Google Image 中有竞争力吗？

### 内容匹配度

每张图自我检查以下四问，任意一项不通过则回到 Step 2 重写 Intent Statement：

- 这张图能不能让用户不用看文字就知道它属于哪个 section？
- 是否可视化了一句具体 H2 文案？
- 是否展示了用户搜索这个词时想看到的问题/结果？
- 单独放到 Google Image 搜索结果里，用户会点吗？

---

## SEO 元数据输出

每张图需同时输出：

```
filename: [keyword]-[role]-[brief].jpg
alt text: ≤125 chars，含 keyword + 图片功能描述
caption: ≤200 chars，简短图注
placement: 放在哪个 section 或 h2 下方
keyword_target: 对应的 primary keyword
```

---

## 配置项（需替换为你产品的值）

| 配置 | 说明 |
|------|------|
| 品牌色 | 你的品牌主色，用于需要品牌识别的场景 |
| 默认尺寸 | intro/pain/highlight 默认 1:1，usecase 默认 16:9（可根据需要调整） |
| 默认模型 | 生图 API 的默认模型 |
| 否定词 | 根据你的产品追加特定否定词 |
