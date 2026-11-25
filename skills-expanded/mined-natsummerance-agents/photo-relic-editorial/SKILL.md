---
name: photo-relic-editorial
description: |
  将用户提供的照片转化为竖向编辑艺术作品：上半部分保留真实照片，下半部分创建"照片遗存"——从照片压缩出的几笔精确墨迹记忆（暖象牙底板+深蓝墨黑灰绿+一个暖色信号）。触发场景：用户要求把照片转为极简艺术、摄影遗存海报、纸上记忆版画、抽象编辑摄影或画廊风格系列封面。边界：照片区域不可重绘/美化/加滤镜；不做数据可视化与凭空虚构摄影；输出须通过缩略图可辨认性与来源色板质检门。
source_project: wnby/photo-relic-editorial
tags: [photography, relic-print, editorial-art, memory-compression]
related_skills: ["photo-abstract-editorial", "gathered-scenes-zine", "minimal-zine-poster"]
---

# Photo Relic Editorial — 照片遗存版画

## R (Reading) — 源项目核心设计

> "Real photograph above. Memory print below. The lower relic should look as if **time pressed the photo into a few ink marks on warm paper**." 且明令："Preserve the photograph's content and truth. Do not redraw, beautify, repaint, expand, hallucinate, or stylize the original photographic area." 遗存必须 thumbnail 可辨认但不沦为普通插画。

（来源：vendor/wnby__photo-relic-editorial/SKILL.md）

## I (Interpretation) — 方法论骨架

**核心思想**：时间将照片压入暖纸上的几笔墨迹——不是插画，不是装饰，是压缩的视觉记忆。

**五步工作流**：
1. 审读照片 → 提取 3-5 个源线索
2. 选择遗存配方（布局节奏 × 遗存语法 × 标记重量 × 标题模式 × 动效种子）
3. 读 references/afterimage-editorial-prompt.md 后编译生成 prompt
4. 生成一张完成的竖向作品
5. 通过质量门检查；单项重大失败则带更紧约束定向重生成一次

**签名特征**：暖象牙/暖白底板；深蓝/墨黑/灰绿/石灰+一个暖信号色；一种主要形态+少量支撑标记不填满画面；标题小而诗意如标签；现代版画语言（平涂墨块/软化边缘/负空间切口）。

## A1 (Past Application) — 源项目的典型应用

### 案例: 城市天际线照的 Architectural Seal 处理
- **输入**: 一张黄昏角楼照片。
- **做法**: 提取源线索（暮色静默的情绪内核、朱红信号色候选、左来光向、屋顶层叠结构）；选 horizon-cover 布局 + ink-seal 语法 + quiet ink 重量 + 小英文标题；prompt 中明确禁止改写照片区。
- **结果**: 上半真实照片原样保留，下半以堆叠弧线与基线封印建筑身份，一个朱红短杠作签名；缩略图下仍可辨认，系列感稳定可复制成组。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 记忆版画："把这张照片做成安静的纸上记忆版画/艺术海报"——有情感温度的场景。
2. 系列封面："给账号做一组画廊风格的摄影艺术封面，要能连成一个系列。"
3. 社媒动效潜力："做成抖音能用的竖版封面，主体轮廓可以动画化。"→ 加 Motion Cover Seed 配方。

### 语言信号
- "记忆版画 / 遗存 / relic / 时间压进纸里"
- "极简艺术海报 / 画廊风格 / 编辑摄影"
- "安静 / 克制 / 东方留白"
- "照片上面保留，下面做抽象"

### 与同 agent 兄弟 skill 的区分（互设诱饵）
- 与 photo-abstract-editorial：本 skill 的下半部是**有主形态的墨迹记忆**（一种主要形态+支撑标记），对方是**无主形态的空间关系重建**；有明确情绪温度选这里，强调空间构成选那里。
- 与 gathered-scenes-zine：对方插画占大场域且有手撕纤维边与高饱和结构色；本 skill 遗存克制留白多、无撕纸元素。
- 与 minimal-zine-poster：对方可无照片纯主题起稿；本 skill 必须有真实照片为源。

## E (Execution) — 可执行步骤

1. **审读源照片** — 记录主体身份关系、情绪内核短语、主导色+信号色候选、光影方向、结构线索五类源线索。完成标准: 3-5 条源线索成文，每条可追溯到照片可见事实。
2. **定遗存配方** — 从布局节奏（photo-over-paper/deep-paper/axis-diptych/horizon-cover/social-cover）、遗存语法、标记重量、标题模式各选一项；近期输出雷同则换配方但保持系列身份。完成标准: 五轴取值齐备且与照片特征匹配（如对称建筑配 axis-diptych）。
3. **编译 prompt** — 包含：照片区保真禁令、竖版系列构图、仅源自照片的可辨认主遗存、暖纸底板、现代版画语言、克制的单一小标题、对照片区的精确禁止清单；不泄露内部分析词汇。完成标准: prompt 全部为可渲染的生产语言且含照片保真禁令句。
4. **生成** — 以用户照片为参考图调用图像生成工具产出一张竖向作品。完成标准: 得到完整图像文件而非仅文字描述。
5. **过质量门** — 十项检查：照片区真实未动/遗存缩略图可辨/保留完整主体关系非装饰碎片/像记忆印刷不像普通插画/标记少而准源自照片/系列签名稳定/移动端可读/排版极小/色板来自照片/无 UI 水印贴纸杂物。完成标准: 清单逐项通过；单项重大失败定向重生成一次并复检。
6. **交付** — 返回成品图与一句创作说明；用户追问时才给构图笔记。完成标准: 输出含图像+简短说明，未主动倾倒 prompt 细节。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- **修改/替换/美化照片内容本身**（P 掉旧楼换新楼、瘦脸、加滤镜） → 硬约束拒绝：照片区域不可篡改是本 skill 根基。
- 数据可视化、信息图、UI 设计 → 不属视觉转译范畴。
- 凭空虚构一张"看起来像实拍"的照片再做成遗存 → 无真实照片即停止并索要。

### 已知局限 / 失效模式（≥1条）
- 图像模型可能把遗存画成普通插画或填满画面、给照片区偷偷加滤镜；需靠质量门十项拦截后带更短更严的 prompt 定向重生成一次，二次仍败则如实说明局限交付较优结果。

### 质量红线
- 照片区域不可被重绘、美化或加滤镜；遗存的一切形态与色彩必须源自照片本身，不得引入照片中不存在的装饰几何或无关符号。

## 相关 skills
- contrasts-with: photo-abstract-editorial（墨迹主形态 vs 关系重建）、gathered-scenes-zine（克制留白 vs 场域拼贴）、minimal-zine-poster(必须有照片 vs 可纯主题)

---

## 审计信息
- **验证**: V1 ✓（本地 upstream 已核） / V2 ✓（RIA++ 六段齐备） / V3 ✓（darwin 用例 7 条推演全过）
- **蒸馏时间**: 2026-08-25；**来源**: upstream `D:\outcome\self\vendor/wnby__photo-relic-editorial`（SKILL.md + references/afterimage-editorial-prompt.md），在既有 48 行半成品上扩写，保留五构图模式表与质量红线等原有正确内容
