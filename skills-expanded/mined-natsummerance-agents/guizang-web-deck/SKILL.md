---
name: guizang-web-deck
description: |
  生成单文件 HTML 网页版幻灯片：杂志编辑风（衬线+暖色）或瑞士国际主义风（无衬线+高饱和功能色），
  带 WebGL 颗粒/渐变质感、放映模式与演讲备注。当用户要「网页 PPT」「杂志感 slides」
  「Swiss Style 演示」「horizontal swipe deck」，且交付形态是浏览器放映而非 .pptx 文件时使用。
  不适用于：需要 PowerPoint 继续编辑的原生文件（改用 ppt-master-native）。
source_project: op7418/guizang-ppt-skill
tags: [guizang-web-deck, html-slides, web-ppt, 演示设计, 蒸馏技能]
---

# 网页幻灯片引擎 · 杂志/Swiss 双风格

## R (Reading) — 源项目核心设计

> "这是一个**单文件 HTML** 的横滑页 PPT……提供两种可选视觉方向：方案 A「独立杂志 · 微博墨水」（衬线 + 米白背景 + 暖色调）与方案 B「瑞士网格海报」（无衬线 + 极简背景 + IKB/朱红黄/森林绿/安全橙高饱和功能色）。"
>
> — 上游 SKILL.md（op7418/guizang-ppt-skill）

上游把「视觉风格选择」前置为第一决策：风格决定加载哪套 template/themes/layouts 资产，而不是先写内容再套壳。

## I (Interpretation) — 方法论骨架

1. **风格即架构**：A 方案=编辑部美学（Noto Serif SC + Playfair Display，Monocle 式留白，适合人文叙事/行业观察）；B 方案=网格系统（Inter/Helvetica，信息密度控制，IKB 单色强调，适合科技产品/数据汇报）。选错风格的返工成本远高于补内容。
2. **七问开工清单**：写任何 slide 之前必须问齐——①A 还是 B？②观众是谁？③时长定页数（15min≈10 页）；④有无原始素材；⑤截图/图片处理偏好；⑥主色选择（A 五色/B 四色任一）；⑦硬性约束。缺答案就先问，不猜测开写。
3. **单文件交付纪律**：所有 CSS/WebGL 动效（motion.min.js）、Lucide 图标内联进一个 HTML；CDN 双备份防断网；ESC 进缩略图、P 进演讲者模式是交互契约的一部分。
4. **内容密度红线**：每页只承载一个论点；数据用 B 方案的 Data Hero 版式，照片叙事用 A 方案的图片大版式——版式跟随内容类型，不混用。

## A1 (Past Application) — 源项目典型应用

### 案例: AI 产品发布 demo day
- **输入**: 产品介绍文稿 + 一组界面截图
- **做法**: 判定为科技发布 → B 方案 Swiss 风；截图统一 CleanShot X 式描边处理；数据页走 Data Hero 网格
- **结果**: 单 HTML 文件即可全屏放映，动效入场，无需 PowerPoint

### 案例: 人文行业观察长文改编
- **输入**: 数千字行业评论文章
- **做法**: A 方案杂志风；章节标题做跨页大字；引文用衬线斜体块
- **结果**: 「一本会翻的杂志」式观感，适配私享会慢讲场景

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 「帮我做个能直接在浏览器里放的 PPT，要有设计感」
2. 发布会/demo day/内部汇报，且明确说不要 .pptx 或强调网页形式
3. 提到「杂志感」「瑞士风」「Swiss Style」「横滑 deck」「Monocle 那种感觉」

### 语言信号

- "做一个网页版的 slides"
- "要有杂志那种排版质感"
- "Helvetica / 瑞士风格 / 高级感的演示"

### 与相邻 skill 的区分

- 与 `ppt-master-native` 的区别: 本 skill 产出**单文件 HTML 网页放映件**，视觉动效强但不可在 PowerPoint 中编辑；后者产出**原生可编辑 PPTX**（母版/DrawingML/原生图表），适合后续要改的正式交付。用户说「发我一份 ppt 文件」「要在公司模板里继续改」→ 转 ppt-master-native。

## E (Execution) — 可执行步骤

1. **风格判定** — 完成标准: 从用户措辞/场合映射出 A 或 B；两可时给出推荐并等确认
2. **七问清单采集** — 完成标准: 时长/受众/素材/主色/约束七项全部有明确答案或用户明示跳过
3. **大纲映射页数** — 完成标准: 每页一个论点的页级大纲获用户确认（15min≈10 页基准）
4. **资产装配** — 完成标准: 选定的 template.html 或 template-swiss.html + 对应 themes/layouts 参考已读取并确定配色 token
5. **逐页编写** — 完成标准: 全部页面写入单个 HTML，图片完成定位/描边/占位处理，图标用 Lucide 内联
6. **放映自检** — 完成标准: 浏览器打开验证翻页/ESC 缩略图/P 演讲者模式/断网可用（无未回退的 CDN 依赖）
7. **交付说明** — 完成标准: 附一句「如何放映 + 如何改字」的使用说明

## B (Boundary) — 边界

### 不适用场景
- 需要 .pptx 文件、公司模板套用、他人协作编辑 → `ppt-master-native`
- 培训课件等需打印讲义、信息密度极高的场景（网页单文件不利于打印分发）
- 无浏览器的纯离线投影环境且不允许携带 HTML 文件

### 已知局限 / 失败模式
- WebGL 质感在低端办公机上可能掉帧，需降级为纯 CSS 渐变
- 上游维护方声明本 skill 只负责生成 HTML/PPT 内容，不承担所生成材料的版权审查

## 相关 skills

- contrasts-with: ppt-master-native（网页放映件 vs 原生可编辑 PPTX）
- composes-with: ppt-master-native（先用本 skill 出视觉稿，再转原生管线落地的情况）

---

## 审计信息

- **验证**: V1 ✓（SKILL.md/README 多处互证） / V2 ✓（可回答「该选哪套模板」新问题） / V3 ✓（风格即架构+七问前置是非常识工作流）
- **蒸馏时间**: 2026-08-25
- **来源**: vendor/op7418__guizang-ppt-skill/{SKILL.md, README.md, assets/, references/}
