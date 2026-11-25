---
name: thesis-figures
description: >-
  本论文统一画图入口 skill——收编本论文 CLAUDE.md "数据可视化配图规范"全部铁律，
  并吸收 scipilot-figure-skill 与既有画图实践的方法论精华。定位是"可视化顾问 + 路由器"：先判断该不该画、画什么图、
  走哪条技术路线（R/ggplot2 数据图 | TikZ 流程架构图 | mac-editable 可编辑改造），再执行
  并强制走"真实数据核对 → 黑白灰度优先 → 双格式导出 → FIGURES.md 登记 → 目视 PNG 验收"
  闭环。触发词：画图、配图、出图、论文图表、可视化、帕累托、鱼骨图、雷达图、甘特图、
  流程图、架构图、技术路线图、TikZ、ggplot、图转SVG、可编辑图、重渲图、改图、figure。
  只可视化论文已有表格的真实数据，严禁编造任何统计量/坐标。
---

# thesis-figures — 本论文统一画图入口

> **定位**：本论文统一画图入口，thesis-analyze / thesis-defense 等图表需求均路由到此。
> **适用范围**：本 MEM 论文（浙大 zjuthesis，黑白打印送审）的全部插图工作——新建、修改、重渲、改造为可编辑格式。
> **既有基础设施（必须复用，不另起炉灶）**：`zjuthesis/figures/FIGURES.md`（图↔源↔数据对照清单）、`figures/rebuild_all.sh`（一键重建）、`figures/src/`（全部图源）、`figures/src/crop.py`（TikZ 裁切）。

---

## 0. 第一问：这张图要论证什么？（吸收自 scipilot 第 0 步）

**任何画图请求，先回答两个问题再动手**：

1. **这张图要支撑正文哪个结论？** 同一批数据，论点不同图型就不同（对比改进前后→斜率图/成对柱；占比结构→帕累托/横向柱；趋势→折线；权重结构→雷达/树）。用户没说清就问一句，或从章节上下文推断并明确说出你的假设。
2. **数据在正文哪张表？** 本论文铁律：**只可视化论文已有表格的真实数据**。没有对应表格/正文数字的图一律不画；聚类没有原始点坐标就不画散点。这一条同时替代了 scipilot 的 `profile_data.py` 数据剖析步——本论文的"数据剖析"就是**打开对应正文表格逐个核对数字**，并查 `FIGURES.md` 确认依赖关系。

**一图一论点**（scipilot P12）：一张图塞不下就拆图，不硬塞。

---

## 1. 适用判断树（三条技术路线）

```
用户要画/改一张图
│
├─ ① 数据图表（柱/折线/散点/帕累托/雷达/甘特/回归系数CI/LDA占比…）
│     → R/ggplot2 路线（§2）。执行后端 = 全局 nature-figure skill
│       (~/ai-skills/nature-skills/skills/nature-figure/，选 backend=r)，
│       本 skill 提供论文级约束与验收闭环。**若未装 nature-figure**，直接用本 skill 附带
│       scripts/templates/*.R 骨架(自带黑白主题+跨平台中文字体+双导出，零外部依赖)。
│       现有实例：fig_pareto / fig_kano / fig_regression / fig_perf_progress /
│       fig_gantt / fig_lda / fig_scheme（源在 figures/src/*.R）
│
├─ ② 流程图/架构图/示意图（鱼骨/KJ亲和/技术路线/指标体系树/前后对比示意/趋势标注图）
│     → LaTeX TikZ 路线（§3）。standalone 编译 + crop.py 裁切。
│       现有实例：fig_fishbone / fig_kj / fig_beforeafter / fig_trend / fig_radar
│       （源在 figures/src/*.tex）；技术路线图/指标树为章节内联 TikZ，随正文编译。
│       scipilot 明确不做这类图（"不做示意图、流程图、架构图"）——此路线是本
│       skill 相对 scipilot 的独有覆盖。
│
└─ ③ 需要"可编辑成品"（放进 PPT 手工改 / 把外部位图·PDF 变矢量 / Figma·Inkscape 编辑）
      → mac-editable-figure 路线（§4）。直接调用 S/mac-editable-figure，
        本 skill 只做路由：
        - 已有矢量 PDF → pdf2svg 无损转 SVG（首选）
        - 位图/截图/AI图 → LLM 视觉重建为 SVG/TikZ/Mermaid（结构图最准）
          或 vtracer 自动矢量化（色块最准）
        - 改完 rsvg-convert 导回 PDF(LaTeX)/PNG 300dpi(DOCX/PPT)
```

**路线选择速判**：图里的核心是"数值→几何映射"（轴/刻度/图例）→ ①；核心是"框和箭头+文字"→ ②；输入已是成品图、目的是"让它可改"→ ③。答辩 PPT 要用论文里的图：直接用现成 `figures/*.png`（300dpi）即可，只有需要在 PPT 里改文字/配色时才走 ③。

---

## 2. R/ggplot2 数据图路线

### 2.1 环境（本机已踩坑验证，照抄勿改）

- 安装：`HOMEBREW_NO_AUTO_UPDATE=1 brew install r`（清华镜像 auto-update 会卡死十几分钟；已卡死则 `pkill -f "mirrors.tuna"` 再装）。
- Homebrew R 是源码版：`install.packages` **不带** `type="binary"`（报 not supported），走源码编译约 2 分钟。
- 包：`ggplot2 patchwork showtext sysfonts`，CRAN 镜像 `https://mirrors.tuna.tsinghua.edu.cn/CRAN/`。
- 中文字体固定为：`font_add("cn","/System/Library/Fonts/STHeiti Medium.ttc"); showtext_auto()`。**不采用** scipilot 的 Noto/SimHei 优先级链——本论文全部既有图用 STHeiti，换字体会造成图间不一致。跨平台复用见 `scripts/templates/_common.R` 的 `cn_font()` 自动探测（macOS STHeiti / Linux Noto·文泉驿，`WENQU_CN_FONT` 可覆盖；同一论文内字体保持一致即可）。
- 导出：`cairo_pdf`（LaTeX 用）+ `ggsave(..., dpi=300)` PNG（DOCX 用）。

### 2.2 选图速查（吸收自 scipilot chart_selection，按本论文场景裁剪）

| 数据形态（本论文典型） | 首选 | 不该用 |
|---|---|---|
| 分类占比/主次排序（缺陷分类、LDA 主题） | 横向/纵向柱按值降序；主次分析用帕累托（柱+累计线） | 饼图（人眼判角度差长度 3 倍） |
| 改进前后对照（多指标） | 成对柱/斜率图/雷达（≤8 维） | 3D 柱 |
| 月度趋势 | 折线（不同指标靠线型+标记区分） | 堆叠面积 |
| 回归系数 | 系数点 + 95%CI 横线（横向排布更易读） | 只给表不给图 |
| 时间计划 | 甘特 | — |
| x 是分类 | 点/柱 | 折线连均值（暗示不存在的连续关系，scipilot P6） |

### 2.3 主动拦截清单（吸收自 scipilot"顾问职责"，先说明再给替代，不默默照做）

| 触发 | 问题 | 替代 |
|---|---|---|
| 双 Y 轴放两个无关变量 | 视觉相关是作图者捏造的 | 拆上下子图共享 x；或标准化共轴。**例外**：fig_trend 已有左右轴（率% vs 时延），保留但必须双侧轴标签+图注注明口径 |
| 比例/率的 Y 轴不从 0 起 | 小差异被放大误导 | 从 0 起；确需截断则明示断裂标记并在图注说明 |
| 饼图/3D 图 | 感知失真 | 横向柱按值排序 |
| rainbow/jet 连续色图 | 感知不均匀、灰度打印全糊 | 灰度渐变或 viridis（并过 §5 灰度验收） |
| 图里出现正文/表格里找不到的数字 | **编造数据，零容忍** | 停手，回正文找表；找不到就不画 |
| 一图多论点、分组组合过多 | 没论点 | 拆图 |

**不采纳** scipilot 的"n<10 均值柱→箱线+stripplot"拦截为强制项：本论文数据是系统埋点全量指标与已汇总表格值，不是原始样本点，无 stripplot 可叠；该条降级为"若未来出现小样本原始数据图再启用"。

### 2.4 误差/统计交代（吸收自 scipilot 原则 5，适配本论文）

凡带 CI/误差棒的图（如 fig_regression 的 β±95%CI），图注必须写清：区间类型（95%CI）、N、来源表号；统计量一律取自 `stats/` 脚本派生值（如 regression_stats.py），**禁止为画图手算或补造 SE/CI**。

---

## 3. TikZ 流程/架构图路线

（本节收编 mgmt-paper-diagrams 的核心独有价值）

- **standalone 紧裁模板**（避免大画布反模式）：

  ```latex
  \documentclass[border=6pt]{standalone}
  \usepackage{ctex}\usepackage{tikz}
  \begin{document}\begin{tikzpicture} ... \end{tikzpicture}\end{document}
  ```

  不要用 `geometry paperwidth=40cm` 大画布——图占一角，`\includegraphics` 整块缩小四周留白。诊断：`pdfinfo fig.pdf | grep 'Page size'`。
- **裁切降级链**：`pdfcrop` → `gs -sDEVICE=bbox` → PyMuPDF 像素级兜底。本项目已固化为 `figures/src/crop.py`，直接用它，不重写。
- **风格与图 1.1 技术路线图统一**：黑白、矩形无填充、虚线分组、不用间隔号 `·`（AI 痕迹清单 A 类）；框内只放通用概念词，不放具体数字/算法名/统计名。
- 内联 TikZ（技术路线图、指标体系树、Ch4 流程图）源码在章节 `.tex` 里，改章节即改图，无需单独重渲。
- 草图阶段可用 Mermaid 快速对结构（mgmt-paper-diagrams 的"先 Mermaid 草图→定稿改 TikZ"两段法），但**定稿必须是 TikZ**（与正文字体一致、矢量、可进 rebuild_all.sh）。

---

## 4. 可编辑改造路线（→ mac-editable-figure，保留不收编）

该 skill 有本 skill 不重复的独立工具链（pdf2svg / vtracer / potrace / rsvg-convert / LLM 视觉重建 + `scripts/figtool.sh` + 独立 venv），涉及 PPT 可编辑、外部图矢量化时**直接调用 S/mac-editable-figure**。其重建铁律与本 skill 一致：只复刻可见结构与文字，不臆造数据。

---

## 5. 论文铁律（全收编，任何路线都必须过）

1. **真实数据**：只可视化论文已有表格的真实数据，严禁为画图编造任何统计量/坐标。改图先对表，对不上先改正文或停手。
2. **黑白/灰度打印优先（硬约束）**：学位论文按黑白打印送审，**默认黑白灰 + 明度/线型/标记/填充纹理区分**，与图 1.1 黑白路线图风格统一。**彩色仅在确认最终打印/提交方式支持彩色后才允许使用**，且启用彩色时仍须通过灰度预览验收（转灰后各系列可分）。灰度预览做法（吸收自 scipilot `grayscale_preview` 思路，本地实现）：`magick fig_x.png -colorspace Gray fig_x_gray.png` 后 Read 目视。色盲友好性由"灰度可分"自然覆盖，不单独引入 Okabe-Ito 彩板为默认。

**灰度分离度定量验收（比目视更早抓"打印糊"）**：`python3 scripts/print_check.py`（PIL+numpy，扫 `zjuthesis/figures/*.png`）。判据三条：①**相邻填充灰阶明度差 ≥51/255（20%）安全**，38–51 偏近、<38 半调打印易糊——屏幕发光能分的灰，激光打印机靠网点抖动模拟灰度，明度差太小会糊成一团；②**大面积中灰（80–180）占比 >18% 报网点颗粒**（打印/复印发麻，装饰性瑕疵）；③**残余彩色扫描**（防"两条不同色但明度相近的线，转黑白塌成同一个灰"）。**关键认知**：灰度≠打印不糊，"是不是彩色"（饱和度扫描）和"灰阶够不够分得开"（本脚本）是两件事；**线条图靠形状/位置/线型区分、不受明度差限**（脚本报 999=检不到填充灰阶即线条图），填充类图才重点看明度差与网点面积。全部图源改灰度后必跑一次。
3. **双格式导出**：每图必出 `figures/fig_*.pdf`（LaTeX `\includegraphics`）+ `figures/fig_*.png`（DOCX/PPT，300dpi）。矢量优先，绝不 JPEG（scipilot 原则 2，与本地实践一致）。
4. **中文渲染**：R 用 `showtext` + STHeiti；TikZ 用 `ctex`。出图后目视确认无方框缺字。
5. **图源可复现 + FIGURES.md 登记**：新图必须有源脚本入 `figures/src/`（R 或 TikZ），并在 `figures/FIGURES.md` 增行（图名/源/类型/关键数据/依赖表/重渲命令），接入 `rebuild_all.sh`。**不得手改成品 pdf/png**。改正文数字→查 FIGURES.md→重渲受影响图→`grep 旧值` 清零（对应记忆铁律"改数字先查 FIGURES.md 重渲图"）。
6. **目视 PNG 验收（视觉自检闭环）**：出图后必须用 Read 读 PNG 逐项核对，发现问题回改源脚本重渲，直到通过。核对清单（本地"必目视"实践 + scipilot visual_review 8 项合并）：
   - 无缺字/乱码方框（含负号）；
   - 文字无越界裁切、刻度标签无重叠（历史真实案例：帕累托首柱标签被累计点遮挡、鱼骨图肋骨文字重叠——编译无报错、肉眼可见）；
   - 图例不压数据；多面板对齐；
   - 灰度下各系列可分（见铁律 2）；
   - 图中每个数字与正文/表格同值。
7. **按最终尺寸出图，不二次缩放**（scipilot 原则 1，采纳）：R 图 `ggsave` 直接设论文实际宽度（正文满栏约 15cm/6in），字号按最终尺寸可读（标签≥8pt 观感）；TikZ 图 `\resizebox{\textwidth}{!}` 仅用于本就按比例设计的路线图，数据图不得靠 LaTeX 大幅缩放补救。
8. **图注规范**（收编自 mgmt-paper-publication-figures）：图题中文置于图下、表题置于表上；需要说明口径/来源时以"注："另起；率与时延双轴等特殊口径必须注明（如率/时延双轴须加口径注）。
9. **AI 痕迹**：图内文字同样过 AI 痕迹清单——不用间隔号 `·`、不用破折号插语、中文标点统一。
10. **题注中英双语 + 一致性机制**（若学校规范要求图题/表题双语）：**只题注双语、图表内部文字保持中文**（规范要的是"图题/表题双语"，非图内文字）。唯一合法写法 `\caption[中文标题]{中文标题 \\ English Title}`——可选参数 `[中文]` 进目录（只中文），主参数"中文 `\\` 英文"正文双行。英文 Title-Case 名词短语无句点、术语与英文摘要一致、数学记号原样保留。**一致性铁律（中文为唯一事实源）**：改题注必须在同一个 `\caption` 里中英一起改；改完跑 `scripts/check_captions.py`（设 `THESIS_ROOT` 为论文编译根）——纯 grep+hash、零 LLM key、只诊断不误改手工润色的英文，报"缺英文/目录参数不符/中文改了英文可能过时"（靠 `figures/CAPTIONS.md` 中文 hash 比对），补齐后 `--update` 刷新基准。

---

## 6. scipilot-figure-skill 采纳/不采清单

**来源**：GitHub Haojae/scipilot-figure-skill v2.1（SKILL.md + README，仅吸收方法论，不下载执行其代码）。

### 采纳（已折入上文对应小节）

| scipilot 内容 | 进入本 skill | 采纳理由 |
|---|---|---|
| 第 0 步"这张图要论证什么"+ 不默认用户知道自己要什么 | §0 | 通用且成本为零；本论文改稿常见"为画而画"，此问能拦住 |
| 顾问式主动拦截（双Y轴/饼图/Y轴截断/rainbow/分类连折线/一图多论点，先劝阻留记录再执行） | §2.3 | 与盲审专家视角一致，全部适用中文学位论文 |
| 视觉自检闭环：渲 PNG→程序/AI 读图→回改→重渲直到通过 | §5.6 | 本地"必目视 PNG"铁律的系统化版本；其 8 项清单（图例压数据/子图对齐/灰度可分）比本地散条更全，合并采纳。程序自检脚本（visual_qa.audit_layout）不下载，用"Read 读 PNG"人工/多模态核对达到同效 |
| 灰度预览（grayscale_preview） | §5.2 | 与"黑白打印友好"铁律天然契合；本地用 ImageMagick 实现思路，不引其脚本 |
| 按最终尺寸出图不二次缩放（figsize 定死、字号绝对单位） | §5.7 | Word/LaTeX 缩放后字号糊是本论文 DOCX 交付的真实风险 |
| 矢量优先、绝不 JPEG | §5.3 | 与本地双格式实践一致，补充"禁 JPEG"底线 |
| 误差必有交代（区间类型+N+来源） | §2.4 | fig_regression 类图直接适用；并叠加本论文"统计量必须脚本派生"铁律 |
| 选图速查表 + 一图一论点 | §0、§2.2 | 裁剪为本论文实际图型子集 |

### 不采纳（及原因）

| scipilot 内容 | 不采原因 |
|---|---|
| matplotlib + seaborn + SciencePlots + plotly 技术栈 | 本论文既有 12 图全部为 R/ggplot2 + TikZ，FIGURES.md/rebuild_all.sh 可复现体系已建成；换栈=全部重画+图间风格断裂。plotly 交互图对打印论文无意义 |
| `profile_data.py` EDA 数据剖析步 | 本论文无原始 CSV 探索场景——数据全部来自正文已定稿表格，"剖析"退化为§0 的对表核对；且任务约束不执行外部代码 |
| 期刊规范查询（Nature/IEEE 栏宽、投稿 DPI 矩阵） | 目标载体固定为浙大 zjuthesis 模板（正文满栏）+ DOCX，不存在"选期刊"分支；仅保留其"按最终尺寸出图"的底层原则 |
| Okabe-Ito 色盲安全彩板为默认配色 | 与"黑白灰度优先"硬约束冲突——学位论文默认根本不上彩；灰度可分已覆盖色盲可分。彩色被确认允许时可参考，但不是默认 |
| CJK 字体优先级链（Noto Sans CJK > Source Han > SimHei） | 本论文字体已锁定 STHeiti（R/showtext）与 ctex 默认（TikZ），换链会造成新旧图字体不一致 |
| n<10 均值柱→箱线+stripplot 强制拦截 | 本论文图的输入是汇总表值/全量埋点指标，非原始样本点，无点可叠；降级为备用规则（§2.3 末注） |
| 显著性标注桥（statannotations） | 本论文统计规范：埋点全量指标只做描述性统计不做检验；t 检验结果以表呈现，无组间显著性桥需求 |
| 中文期刊"宋体+Times New Roman 数字"混排（serif_for_zh） | 本论文既有图统一 STHeiti 黑体系，中途换衬线混排破坏一致性；zjuthesis 对图内字体无宋体强制 |

---

## 7. 标准作业流（SOP 摘要）

1. 明确论点 + 定位正文数据表（§0）→ 2. 判断路线①②③（§1）→ 3. 按路线画：R（§2，nature-figure backend=r + 本地环境§2.1）或 TikZ（§3，standalone + crop.py）或转 mac-editable-figure（§4）→ 4. 双格式导出到 `figures/`（§5.3）→ 5. FIGURES.md 增行 + 接入 rebuild_all.sh（§5.5）→ 6. Read 读 PNG 过验收清单，含灰度检查（§5.6）→ 7. 正文 `\includegraphics` 挂接 + 编译 `grep undefined` 清零 → 8. 若改的是既有数字：先查 FIGURES.md 反查受影响图，重渲后 `grep 旧值` 清零。
