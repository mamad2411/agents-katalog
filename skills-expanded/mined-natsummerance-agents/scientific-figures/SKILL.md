---
name: scientific-figures
description: |
  学术论文出版级插图规范：用 matplotlib 按 figures4papers 的 house style 制作投稿级静态图表——
  分组柱状对比、趋势线、热图、多面板网格、雷达与概念示意图，语义色板（蓝=提出方法、绿=改进、红=基线）、
  Helvetica/Arial 字体层级、去顶右边框、dpi300/600 与 png+pdf 双格式矢量导出。
  当用户要为论文/期刊/学术幻灯定稿插图，说「出版质量」「publication-ready」「分组柱状图导出 PDF」
  「和仓库里图风格一致」时使用。
  不适用于：交互式 dashboard 或网页可视化（Plotly/Bokeh）、扁平商业 HTML 图表（转 lieflat-charts）。
source_project: ChenLiu-1996/figures4papers
tags: [scientific-figures, matplotlib, publication, 学术出版, 论文插图, 蒸馏技能]
---

# Scientific Figures · 学术论文出版级插图规范

## R (Reading) — 上游原文

> "The dominant house style is minimalist, high-contrast, and publication-oriented: Primary `font.family = 'helvetica'`; Large-panel bar/comparison figures: `font.size = 24`, `axes.linewidth = 3`; Paper subfigures: `font.size = 15-16`, `axes.linewidth = 2`; `axes.spines.right = False`, `axes.spines.top = False`; finalize with `fig.tight_layout(pad=2)` and export at `dpi=300` (or `600` for dense bar panels)."
>
> — 上游 scientific-figure-making/references/design-theory.md（ChenLiu-1996__figures4papers）

上游 README.md 说明这些图的出处：「This is a centralized repository of my own Python scripts for high-quality figures. These figures are published at top venues, including Nature Machine Intelligence, ICML, NeurIPS, ECCV.」SKILL.md 同时划定边界：「Do not use for interactive dashboards or web viz (Plotly, Altair, Bokeh), exploratory-only plots without a publication target…」

api.md 补充工程约定：「In batch or headless runs, set a non-interactive backend before `import matplotlib.pyplot` (for example `matplotlib.use("Agg")`).」「When comparisons, panel count, color roles, resolution, or data layout are underspecified in a way that would change the figure, confirm with the user before finalizing.」

## I (Interpretation) — 方法论骨架

1. **先问发表目标再动手**：本 skill 的存在前提是「有 publication target」；纯探索性画图 seaborn/pandas 足够，不必上出版规范。目标决定字号档位（大面板柱状 24pt / 紧凑子图 15–16pt）与线宽（3 vs 2）。
2. **rcParams 预置一次成型**：调 `apply_publication_style(FigureStyle(...))` 统一设置——字体族 Arial/Helvetica/DejaVu Sans 回退栈、去顶/右边框、无框 legend、`svg.fonttype='none'` 保矢量可编辑文本；数学密集标签才开 `text.usetex=True`。
3. **语义色板是跨图契约**：PALETTE 固定角色——蓝 #0F4D92/#3775BA = 提出的方法或关键结果，绿三阶 #DDF3DE/#AADCA9/#8BCF8B = 改进与正向变体，红三阶至 #B64342 = 基线与对照，中性灰 = 背景/参考类目，金色 #FFD700 只给唯一 callout；全篇论文内「提出 vs 基线」的颜色含义不得漂移。
4. **布局三件套**：多指标对比用超宽画布（figsize (45,12) 或 (28,6)，宽高比 3–4:1 从左往右叙事）；复杂多系列把 legend 放进独立 `ax.set_axis_off()` 子图面板；类目抽象化时隐藏 x 刻度（set_xticks([])）靠 legend/标题识别方法名。
5. **柱编码策略**：数值直接标注在柱顶（ax.text 大字号），黑色描边 linewidth 1.5–3 保证灰度打印可分；消融实验用同主色不同 alpha（0.2→1.0 表达完整度）；必要时加 hatch（///\\\..）做打印安全的子类区分；y 轴手动收紧到相关区间（如 min−std）突出差异而非从 0 铺满。
6. **趋势线纪律**：每轴 2–4 条主线、线宽 2–3、可控 alpha、不确定度用 fill_between；网格极简或省略。雷达图沿用同一线宽与标签纪律（范例在 figure_VIGIL）。
7. **导出政策是硬规则**：`finalize_figure(fig, path, formats=['png','pdf'], dpi=300, pad≈0.05–0.06)` 收尾——默认 dpi300、超密柱状面板 dpi600、tight_layout(pad=2)（紧凑多面板 pad=1）、自动建目录；批处理/无头环境先 `matplotlib.use("Agg")` 再 import pyplot。
8. **helpers 复用而非重写**：make_grouped_bar / annotate_bars / make_trend / make_heatmap / make_scatter / make_sphere_illustration 已内置长度校验与 numpy 转换；参数不足以定稿（比较对象、面板数、颜色角色、分辨率会改变图形）时先向用户确认。
9. **按需加载 references，不预读全集**：SKILL.md 是入口索引——tutorials.md 管端到端流程、api.md 管函数签名与校验、common-patterns.md 管布局模式、design-theory.md 管风格理据、demos.md 管真实 figure_* 脚本链接；用到哪层开哪层，保持上下文精瘦。

## A1 (Past Application) — 源项目典型应用

### 案例: 多数据集上的方法对比柱状图
- **输入**: ImmunoStruct 在 IEDB/CEDAR 两套基准上与多个基线方法的性能数值
- **做法**: apply_publication_style(font_size=24, axes_linewidth=3) → make_grouped_bar + 黑描边 + 柱顶大字标注 → dpi=600 导出应对超高密度柱面板
- **结果**: 发表于 Nature Machine Intelligence 的分组对比图，灰度打印下各方法仍清晰可辨

### 案例: 训练过程多曲线趋势图
- **输入**: VIGIL 训练前后多个指标随 epoch 变化的序列
- **做法**: make_trend 限 2–4 条线、线宽 2–3、fill_between 画不确定带；y 轴收紧到有效区间放大差异
- **结果**: 一眼读出 post-training 增益的趋势图，配色沿用「蓝=本文方法」语义不漂移

### 案例: 组成分解与概念示意
- **输入**: Brainteaser 数据集的类别构成占比；Dispersion 需要三维球体概念图
- **做法**: 构成分解用堆叠/分组柱（brute_force.png 式）；概念图用 make_sphere_illustration 画带光影的 2D 圆盘伪装 3D 球体，去轴刻度
- **结果**: NeurIPS 论文的组成图与 ICML 论文的概念插图，风格与本库其余图一致

### 案例: 临床回顾研究的月度趋势
- **输入**: 眼科综述项目的按月病例数据（figure_ophthal_review）
- **做法**: plot_trend.py 画月度趋势线，plot_composition.py 画病种构成；同一项目内共享字号、线宽与色板角色
- **结果**: 综述配图在多面板间保持视觉一致性，直接用于出版排版

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 论文/期刊投稿前定稿实验图表：分组柱状对比、消融、趋势、热图、多面板拼图
2. 学术幻灯或海报复用论文图，要求与已发表图视觉完全一致（同一 house style）
3. 明确点名「publication-ready / 出版质量 / 和 figures4papers 里那张图一个风格」

### 语言信号
- "帮我把消融实验画成出版质量的分组柱状图，导出 PDF"
- "这张图要投 Nature 子刊，字体和线宽按学术规范来"
- "做一个和我仓库 figure_* 项目里风格一致的 heatmap"
- "论文 final 版插图，png 加 pdf 双格式，dpi 300"
- "这张雷达图要放 ECCV 海报上，线条和标签按仓库纪律来"

### 与同 agent 兄弟 skill 的区分
- 与 `lieflat-charts` 的区别一句话：本 skill 产出**matplotlib 出版级静态学术插图**（矢量 PDF/SVG 进论文排版、LaTeX 数学标注、灰度打印安全），lieflat-charts 产出**浏览器阅读的扁平化商业 HTML 图表**（动效、公众号/汇报场合）。

## E (Execution) — 可执行步骤

1. **确认发表语境与规格** — 完成标准: 已明确目标载体（期刊/会议/幻灯）、单双栏对应的目标宽度、所需输出格式与 dpi；规格不足且会影响构图时向用户提问
2. **选 helpers 与面板结构** — 完成标准: 图型映射到具体 helper（grouped_bar/trend/heatmap/scatter 等）与 figsize；多指标对比采用宽高比 ≥3:1 或声明为何不用
3. **应用 rcParams 与语义色板** — 完成标准: apply_publication_style 已调用且字号/线宽匹配面板类型；每个颜色都能说出 PALETTE 角色，「提出方法=蓝、基线=红」全程未漂移
4. **实现编码细节** — 完成标准: 柱有黑描边与柱顶标注（如适用）、legend 不遮挡数据（独立面板或框外）、y 轴范围收紧有依据、需要灰度安全的组间用了 hatch/edge
5. **校验数据契约** — 完成标准: 序列已转 numpy 且长度校验通过（categories 数 == series 列数、每条 series 与 x 等长）
6. **导出与收尾** — 完成标准: finalize_figure 以 png+pdf（或用户指定格式）落盘、dpi 达标（常规 300/密集柱面 600）、tight_layout(pad=2) 已过、无头环境用 Agg 后端、文件可在查看器中打开核对

## B (Boundary) — 边界

### 不适用场景
- Plotly/Altair/Bokeh 等交互式或网页优先的可视化；持续更新的 dashboard → 转 lieflat-charts（若需扁平 HTML 风格）
- 没有发表目标的纯探索性数据分析（seaborn/pandas 快速出图即可，不值得背上出版规范）
- 以 3D/GIS 为主体的可视化工作流，以及 Illustrator/Figma 为主的手工信息图排版
- 非matplotlib 工具链的绘图请求（R/ggplot2、D3 等）

### 已知局限 / 失败模式
- LaTeX 渲染依赖本地 TeX 环境，未安装时 use_tex=True 会直接失败；应回退 mathtext 并告知用户
- 上游风格是从 figure_* 脚本反推的约定（design-theory.md 自述 "inferred"），个别历史脚本存在 sans-serif/helvetica 混用等不一致，遇到冲突以 references/api.md 的正式契约为准
- PDF 内字体嵌入依赖本机安装的 Helvetica/Arial；目标环境缺字体时回退 DejaVu Sans，视觉宽度略有差异，投稿前应在最终排版环境中复核

## 相关 skills

- contrasts-with: lieflat-charts（学术出版级 matplotlib 静态插图 vs 扁平商业 HTML 图表）
- composes-with: lieflat-charts（同一研究成果：论文里用本 skill，传播端用兄弟 skill 重绘）

---

## 审计信息

- **验证**: V1 ✓（README.md、SKILL.md 与 references/design-theory.md、api.md 在字体层级、色板角色、导出 dpi 上多处互证）/ V2 ✓（可回答「这组对比该用什么布局」「为什么 y 轴不从 0 开始」「hatch 何时必要」等新问题）/ V3 ✓（语义色板角色制、独立 legend 面板、alpha 编码消融完整度是非常识性工作流）
- **蒸馏时间**: 2026-08-25
- **来源文件清单**: vendor/ChenLiu-1996__figures4papers/{README.md, scientific-figure-making/SKILL.md, scientific-figure-making/references/design-theory.md, scientific-figure-making/references/api.md, scientific-figure-making/references/common-patterns.md}
