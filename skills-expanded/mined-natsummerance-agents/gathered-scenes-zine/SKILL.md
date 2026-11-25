---
name: gathered-scenes-zine
description: |
  将用户提供的实景照片转化为竖向 3:5 拾景拼贴海报：真实摄影锚定在宽敞的源衍生插画场域内，密集细节（树叶/枝条/人群）压缩为少数大型安静块面（省略 85-95% 微观细节），以一个高饱和色相作为构图结构而非装饰，保留可见的手撕纤维纸边作为摄影与纸面的过渡。触发场景：用户要求实景拼贴、拾景风格、手撕纸质感艺术海报或自然场景的插画化再创作。边界：不篡改照片、不做满铺描摹式插画、单一添加色相必须通过"移除测试"。
source_project: Zeejay0/gathered-scenes-zine-skill
tags: [zine, collage, photography, illustration-field, torn-paper]
related_skills: ["photo-relic-editorial", "photo-abstract-editorial", "minimal-zine-poster"]
---

# Gathered Scenes Zine — 实景拼贴海报

## R (Reading) — 源项目核心设计

> 签名公式："**真景为锚、插画成场、色彩成结构、撕纸成界、纸面会呼吸**。" 复杂度法则："Complexity in the photograph is a reason to simplify more, not a reason to print more." 密度标尺：插画场域占海报 45-70%，其中 55-75% 保持安静；叶dominant 场景省略约 85-95% 的单片叶片。

（来源：vendor/Zeejay0__gathered-scenes-zine-skill/skills/scenes-gathered-zine-v1-3/SKILL.md）

## I (Interpretation) — 方法论骨架

**决策优先级（冲突时依序裁决）**：1 保留场景身份与关键空间关系 → 2 摄影部分保真 → 3 复杂细节压缩为少数大块面 → 4 插画成为大型设计场域而非字面复写 → 5 摄影/插画/色相共享同一源生骨架 → 6 高饱和色相须改变平衡/运动/图地关系 → 7 插画内外保留充足安静空间 → 8 手撕纤维边为默认过渡 → 9 一条克制微文本不削弱层级。先关系后细节，先删减后装饰。

**Scene Card 内部档案**：核心主体（1-2）/支撑元素（2-3）/空间不变量/主导手势/视觉权重图/原生色彩氛围/源形状候选（1-2 个可跨三媒介延续的形）/天然安静区/语义最小集。

**抽象引擎**：默认中等抽象——保留主体+主导手势+一处关键空间关系，去除约 60-80% 小细节；对每个区域做 Retain/Merge/Omit/Transform/Expose 五判；插画语法五选一：silhouette-led / contour-led / field-led / rhythm-led / cut-paper-led（主语法一个+至多一个辅助）。

## A1 (Past Application) — 源项目的典型应用

### 案例: 松林雪景照的叶dominant 压缩
- **输入**: 一张针叶密林的冬日照片。
- **做法**: Scene Card 判定叶dominant → 选 silhouette-led 主语法：一主树冠体量 + 1-3 条方向性枝势 ≤2 个次级簇 + 一处稀疏纹理采样；单片松针省略 85-95%；钴蓝以 selective replacement 模式替换一段真实阴影区（占全幅约 4%）过移除测试；主过渡带做 35-70% 周长的手撕纤维边。
- **结果**: 缩略图下仍是"那片松林雪坡"，近看是安静的剪纸块面与呼吸纸面——复杂度转化为体量而非细节。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 实景转拼贴："把这张风景/街景照做成拾景拼贴海报。"
2. 手撕纸质感："要那种撕纸边缘的手作 zine 质感。"
3. 插画场域扩容："照片小一点没关系，周围用插画把氛围延展开。"

### 语言信号
- "拾景 / 拼贴海报 / collage"
- "手撕纸 / 撕纸边 / torn paper"
- "插画场域 / 把画面延展出去"
- "zine 质感 / 纸面呼吸感"

### 与同 agent 兄弟 skill 的区分（互设诱饵）
- 与 photo-relic-editorial：对方下半部是小面积遗存墨迹+大量留白、无撕纸无高饱和结构色；本 skill 插画是大场域且必有撕纸边与结构色相。要大面积插画延展来这里。
- 与 photo-abstract-editorial：对方是均匀象牙底板上的空间关系抽象、无插画语法无撕纸；本 skill 有明确版画/剪纸插画语言。
- 与 minimal-zine-poster：对方焦点事件小而孤立（占 8-25%）、可纯主题起稿；本 skill 必须有实景照片且插画影响近半画面。

## E (Execution) — 可执行步骤

1. **审读建卡** — 构建 Scene Card 九字段并确定语义最小集（仍能认出此场景的最小形式组合）。完成标准: 核心主体/不变量/源形状候选三项成文且可追溯照片。
2. **选布局与注意力几何** — 从五种布局范围（transformative seam/underprint overlay/photo anchor+expansive field/directional split/irregular fragments）按主导手势选型，定焦区、眼路、安静区。完成标准: 摄影占比落在对应区间且由视觉权重校正过。
3. **建抽象地图** — 对每个插画区做 Retain/Merge/Omit/Transform/Expose 判定，选一个主插画语法；叶dominant 场景执行压缩铁律。完成标准: 每区的取舍清单齐备且安静占比达标（55-75%）。
4. **定色彩结构与撕纸边** — 选一种整合模式（source continuation/selective replacement/underprint passage/counterform/directional rhythm），定精确色相与占比，跑"移除测试"；在主交接带构建不规则撕纸轮廓与 1-4% 纤维带。完成标准: 色相通过移除测试（拿掉它构图确会塌），撕边周长覆盖 35-70% 摄影边界。
5. **微文本与 prompt 编译** — 默认英文 ≤5 词（单词/关键词序列/超短语三选一，用户提供则逐字使用），中文 ≤8 字仅限用户要求；按四段式（画布几何→场景保真→插画/色彩/撕边/文本→复刻氛围与 hard avoids）编译。完成标准: prompt 只含可渲染像素指令，文本长度合规。
6. **生成与质检** — 以原照片为参考生成，全图+缩略图双档检查质量门清单（场景可辨/摄影真实/插画非描摹/单语法/负空间充足/撕边可读/单色相过测/文本安静）；失败则对照 targeted correction 清单定向重生成一次。完成标准: 质检项逐条通过或定向修正后通过。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- **篡改照片内容**（换脸/移除人物/改天换地） → 拒绝：摄影锚区必须保真。
- 数据可视化、UI 设计、商业广告物料 → 不属本 skill；广告层级/CTA/logo 在 hard avoids 中明令禁止。
- 无照片的凭空场景拼贴 → 本 skill 以实景照片为事实源。

### 已知局限 / 失效模式（≥1条）
- 最常见漂移是"过度勤勉"：模型倾向把每片叶子都画出来变成植物学铜版画，或把添加色相做成漂浮装饰块——分别靠压缩铁律与移除测试拦截；4K 大图会放大这两类失败。

### 结构红线
- 添加色相不是装饰：通不过"结构性移除测试"的色块必须重设计为源生形状的延续/替换/底印/负形/节奏；撕纸边不得退化成均匀装饰框或数字抠图白边。

## 相关 skills
- contrasts-with: photo-relic-editorial（大场域撕纸 vs 小遗存留白）、photo-abstract-editorial（版画插画语言 vs 关系抽象面板）、minimal-zine-poster(实景锚定 vs 主题隐喻)

---

## 审计信息
- **验证**: V1 ✓（本地 upstream 已核） / V2 ✓（RIA++ 六段齐备） / V3 ✓（darwin 用例 7 条推演全过）
- **蒸馏时间**: 2026-08-25；**来源**: upstream `D:\outcome\self\vendor/Zeejay0__gathered-scenes-zine-skill\skills\scenes-gathered-zine-v1-3\SKILL.md`，在既有 39 行半成品上扩写，保留签名公式、决策优先级与 Scene Card 骨架等原有正确内容
