---
name: ppt-master-native
description: |
  从主题或素材生成**原生可编辑 PPTX**：SVG 中间管线 → DrawingML 母版/原生形状/数据图表，
  支持四路由（生成/建模板/填充已有PPTX/增强已有PPTX）与 Default/Quick 双运行时。
  当用户要「一份 ppt 文件」「能在 PowerPoint 里继续改」「套公司模板」「美化现有 PPT」时使用。
  不适用于：浏览器放映的网页幻灯片（改用 guizang-web-deck）。
source_project: hugohe3/ppt-master
tags: [ppt-master-native, pptx, native-powerpoint, 演示设计, 蒸馏技能]
---

# 原生 PPTX 生成引擎 · 四路由管线

## R (Reading) — 源项目核心设计

> "Editable is already table stakes — what sets PPT Master apart is native depth. It hands you a real PowerPoint: slide masters, native shapes, data-backed charts and tables — not flat text boxes, and not a filled-in template."
>
> — 上游 README.md（hugohe3/ppt-master）

上游核心纪律：**先论证后设计**（Strategist 把叙事结构定稿再进视觉执行），且四条顶层路由互斥——生成新 PPTX / 创建模板工作区 / 用模板填充新材料 / 对成品 PPTX 做 OOXML 直补增强，禁止互相串线。

## I (Interpretation) — 方法论骨架

1. **路由先行**：接到任务第一问是「产物是什么」——新演示→Generate；要从品牌/旧稿提炼可复用版式→Create Template；旧模板+新材料→Template Fill；只改现有 PPTX 的视觉→Native Enhance。路由错了整条管线白跑。
2. **双运行时取舍**：Default=Strategist 出叙事规格 → 用户确认沟通契约与模板选择 → Executor 执行（质量优先，交互多）；Quick=跳过策略与确认直接产出（速度优先）。用户说"快速出个草稿"走 Quick，说"重要汇报"必须 Default。
3. **SVG 是中间态不是终点**：页面以受约束的 SVG 编写（共享视觉规范+效果库），经质量检查器验证后导出为原生 PPTX 元素；任何"直接往成品 PPTX 里加母版结构"的操作都被上游明令禁止——必须回到模板工作区重新生成。
4. **素材入池纪律**：事实不足先跑 topic-research；图片经分析入运行时图池，检索失败才允许拉取一个网页作补充源且仅入选页进入图池；图标从内置库选取并 sync 校验缺名。

## A1 (Past Application) — 源项目典型应用

### 案例: PDF 报告转可编辑汇报
- **输入**: 一份 30 页 PDF 行业报告 + "下周要用 PPT 讲"
- **做法**: source_to_md 转换素材 → Default 运行时，Stage1 确认叙事契约 → SVG 分页 → svg_quality_checker 通过后导出原生 PPTX
- **结果**: 母版、原生图表可在 PowerPoint 中逐元素修改

### 案例: 成品 PPTX 视觉翻新
- **输入**: 客户旧 PPTX + "内容别动，变好看"
- **做法**: 判定为 Native Enhance 路由（OOXML 直补），不进入 SVG 再生成
- **结果**: 内容零改动、样式整体升级

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 「给我一份 pptx / PowerPoint 文件」，交付后还要自己编辑
2. 有公司模板/旧 PPT 要套用或美化
3. 重要正式汇报（答辩/客户提案），要求母版级别的规范性

### 语言信号

- "发我一份 ppt 文件"
- "按我们公司模板来做"
- "把这个 PPT 美化一下，内容不要动"

### 与相邻 skill 的区分

- 与 `guizang-web-deck` 的区别: 本 skill 产出**原生 .pptx 可编辑文件**（PowerPoint 工作流）；后者是**单 HTML 网页放映件**（浏览器工作流）。用户要"看着酷、网页里放"→ 转 guizang-web-deck。

## E (Execution) — 可执行步骤

1. **路由判定** — 完成标准: 在 Generate / Create Template / Template Fill / Native Enhance 四路由中明确唯一选择并向用户复述
2. **运行时选择** — 完成标准: 依"正式度×时间压力"确定 Default 或 Quick，说明取舍
3. **素材入池** — 完成标准: 源材料完成转换（source_to_md），图片/图标/音效资产就位且缺名校验通过
4. **规格确认**（仅 Default）— 完成标准: 叙事大纲+沟通契约+模板候选获用户确认后才动工
5. **分页编写** — 完成标准: 全部页面按共享 SVG 规范完成并通过 svg_quality_checker 零错误
6. **导出与校验** — 完成标准: project_manager validate 通过，PPTX 打开无占位符残留，图表为可编辑原生对象
7. **交付** — 完成标准: 附项目目录路径与后续修改指引（改哪层母版/页面）

## B (Boundary) — 边界

### 不适用场景
- 网页放映/强动效展示 → `guizang-web-deck`
- 只想要文字大纲还没到做片阶段（先回对话层面梳理）
- 需要在 Google Slides / Keynote 为主力工具的协作环境（原生深度以 PowerPoint 为准）

### 已知局限 / 失败模式
- 依赖本地 Python 脚本链与图像生成 API 配置，环境缺失时 Quick 路线也会中断
- 上游明确：原始 PPTX 不能当 Generate 模板工作区直接吃，必须先 create-template——绕行会产生损坏结构

## 相关 skills

- contrasts-with: guizang-web-deck（可编辑 PPTX vs 网页放映件）
- composes-with: guizang-web-deck（网页版定视觉方向后再落原生管线的接力用法）

---

## 审计信息

- **验证**: V1 ✓（README/AGENTS.md/workflows 多处互证） / V2 ✓（可回答「该走哪条路由」新问题） / V3 ✓（路由互斥+SVG中间态纪律是非常识工程约束）
- **蒸馏时间**: 2026-08-25
- **来源**: vendor/hugohe3__ppt-master/{README.md, AGENTS.md, skills/ppt-master/workflows/routing.md 结构}
