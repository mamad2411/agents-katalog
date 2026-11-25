---
name: nsfc-nssfc-grant-writing
description: >-
  帮助申请人撰写自己的【国家社会科学基金（国社科/NSSFC）】与【国家自然科学基金（国自然/NSFC）】项目申请书/标书/本子的完整辅导
  skill。覆盖选题与申请代码归口、立项依据与研究现状述评、研究内容/研究目标/关键科学问题凝练、研究方案与技术路线、创新点、研究
  基础与队伍、经费预算、预期成果、年度计划、活页匿名、评审打分逻辑与被毙原因、科研诚信红线与生成式AI使用规范、申报流程时间线，
  并内置【图表制作】工具一键生成技术路线图/研究框架图/机制模型图/甘特图（matplotlib，导出可印刷的 PNG/PDF/SVG）。
  Use this whenever the user mentions 国社科/国家社会科学基金/社科基金/国自然/国家自然科学基金/自科基金/基金申请书/标书/本子/
  活页/课题论证/立项依据/技术路线图/申报书/面上项目/青年基金/重大项目/重点项目/中华学术外译/后期资助，或说"写基金/改本子/
  润色立项依据/做技术路线图/凝练科学问题/基金申报/课题申报/申请书怎么写/评审会不会中"。这是写"自己的"申请书的辅助工具，
  不代写、不买卖申请书。NOT for 期刊论文写作/毕业论文/开题报告（用 thesis 相关 skill）、纯文献综述、或与基金申报无关的写作。
---

# 国社科 / 国自然 基金申请书写作辅导

帮**申请人本人**把一个研究想法，写成一份**逻辑严密、评审友好、合规**的国家级基金申请书，
并能一键生成本子里该有的图表。两套基金体系都覆盖，按需路由。

## 🔴 红线声明（每次都先读，先守住再开工）

本 skill 只做一件事：**帮你把"你自己的"研究写清楚、查严实、画明白。**

- ✅ 可以：梳理结构、打磨论证与语言、凝练科学问题/创新点、润色现状述评、生成图表、对照清单做合规与形式自检、用评审视角挑毛病。
- ❌ 不可以：**代写/代投/买卖申请书**、**伪造或夸大研究基础与预实验**、**编造文献或数据**、冒名或不当署名。
- 这些是 **NSFC《国家自然科学基金条例》及科研不端处理办法、国社科科研诚信规定** 的绝对红线，触碰可致撤项、追回经费、多年禁申、记入科研失信记录。
- **生成式 AI 的边界**：可辅助检索、文献整理、语言润色、结构梳理、图表草拟；**核心创新与研究方案必须出自申请人本人**，AI 生成内容须人工核实、按当年要求声明标识，**不得用 AI 直接生成申请书**。详见 [compliance-redlines.md](references/compliance-redlines.md) 与声明模板 [checklists.md](assets/templates/checklists.md)。

如果用户来意是"帮我把整本本子写出来交差"，温和地把它转成正路：**让用户先给出自己的研究想法/材料，你来做结构化、论证打磨、图表与合规自检。**

---

## 第一步：先分清你在写哪一种（两套体系完全不同，别混）

| 维度 | **国自然（NSFC）** | **国社科（NSSFC）** |
|---|---|---|
| 学科 | 自然科学/工程/医学 | 哲学社会科学 |
| 主管·平台 | 国家自然科学基金委员会 · ISIS（grants.nsfc.gov.cn） | 全国哲学社会科学工作办公室 · nopss.gov.cn |
| 核心文本 | 报告正文（**不匿名**） | 《课题论证》**活页（严格匿名，一票否决）** |
| 招牌术语 | 关键科学问题、技术路线、研究属性、申请代码 | 选题依据、研究现状述评、研究思路、学科归口 |
| 类型 | 面上/青年A·B·C/地区/重点/重大… | 年度（重点/一般/青年）/重大招标/后期资助/外译/西部… |

> 用户没说清就先问一句"国自然还是国社科、申报哪个类型"。两边的结构模块、参数、红线都不一样。

---

## 工作流（按这个顺序帮用户推进，每步都有对应模块可深读）

1. **定位与选题** — 确认基金/类型、把研究想法收敛成一个能被评审看懂的题目；选**申请代码/学科归口**（选错=送错专家/不受理）。→ [code-selection.md](references/code-selection.md)
2. **搭骨架** — 列研究内容→研究目标→关键科学问题（国自然）/ 选题依据→研究内容→思路方法（国社科），三者一一对应不错位。→ [nsfc-structure.md](references/nsfc-structure.md)、[nssfc-structure.md](references/nssfc-structure.md)、模板 [assets/templates/](assets/templates/)
3. **写论证** — 立项依据叙事弧线、研究现状"述评"而非罗列、创新点具体可证伪、语言去模板腔。→ [writing-craft.md](references/writing-craft.md)
4. **画图表** — 技术路线图/研究框架图/机制模型/甘特图，用内置工具生成（见下"图表制作"）。→ [figures-guide.md](references/figures-guide.md)、[assets/figures/SPEC.md](assets/figures/SPEC.md)
5. **补支撑** — 研究方案与可行性、研究基础与工作条件、研究队伍、经费预算、预期成果（这些都是评审打分项，别轻视）。→ [supporting-sections.md](references/supporting-sections.md)、[budget-guide.md](references/budget-guide.md)
6. **看类型差异** — 重大招标/后期资助/外译/地区/重点等有专门写法。→ [project-types.md](references/project-types.md)
7. **评审视角自检** — 用打分逻辑和高频被毙原因反向挑毛病；该答辩的准备答辩。→ [review-criteria.md](references/review-criteria.md)、[defense-lifecycle.md](references/defense-lifecycle.md)
8. **合规与形审终检** — 匿名、限项、AI 声明、形式审查清单逐条过；核对当年参数。→ [checklists.md](assets/templates/checklists.md)、[compliance-redlines.md](references/compliance-redlines.md)、[key-parameters.md](references/key-parameters.md)、[process-timeline.md](references/process-timeline.md)

> 不必每次走满 8 步——用户问哪步做哪步。但**红线、匿名（国社科）、限项、当年参数**这几关任何时候都要守。

---

## 图表制作（本 skill 的硬能力，📌 几乎每本都要）

用内置 matplotlib 引擎，从一份 JSON 规格一键生成**评审友好、灰度打印安全**的矢量图，
导出 **PNG(300dpi)+PDF+SVG**，可直接插进 Word/LaTeX。无需浏览器、无需 graphviz。

```bash
python scripts/grant_figures.py 你的spec.json          # 同名输出 .png/.pdf/.svg
python scripts/grant_figures.py spec.json -o out/图1 -f png,pdf --dpi 300
```

| 图类型（spec 的 `type`） | 用途 |
|---|---|
| `tech_roadmap` | **技术路线图**（国自然几乎必备） |
| `framework` | 研究框架/理论框架（国社科常用） |
| `mechanism` / `model` | 机制图/假设模型（H1/H2…、中介调节） |
| `gantt` | 研究进度甘特图（含里程碑菱形） |

**怎么用**：复制 [assets/figures/examples/](assets/figures/examples/) 里对应的 `*.json`，把里面的文字换成用户研究的内容，再跑脚本。
字段细节见 [assets/figures/SPEC.md](assets/figures/SPEC.md)；设计规范（配色不超3色、字号下限、与正文一一对应、别太花）见 [figures-guide.md](references/figures-guide.md)。
拿不准配色就用 `"palette":"gray"`（本子常黑白印刷，灰度最稳）。

---

## 参考模块地图（按需读，别一次全读）

| 文件 | 何时读 |
|---|---|
| [key-parameters.md](references/key-parameters.md) | **任何涉及数字（钱/日期/字数/限项/资助率）时——唯一权威口径** |
| [nsfc-structure.md](references/nsfc-structure.md) | 写国自然报告正文（含 2026 三段式改版说明） |
| [nssfc-structure.md](references/nssfc-structure.md) | 写国社科活页/申请书 |
| [writing-craft.md](references/writing-craft.md) | 打磨立项依据/现状述评/科学问题/创新点/语言 |
| [figures-guide.md](references/figures-guide.md) | 画任何图前看设计规范 |
| [code-selection.md](references/code-selection.md) | 选申请代码/学科归口 |
| [budget-guide.md](references/budget-guide.md) | 编经费预算 |
| [supporting-sections.md](references/supporting-sections.md) | 写研究队伍/研究基础/预期成果 |
| [project-types.md](references/project-types.md) | 申报面上/年度一般以外的类型 |
| [review-criteria.md](references/review-criteria.md) | 自检、理解评审怎么打分、为何被毙 |
| [defense-lifecycle.md](references/defense-lifecycle.md) | 准备上会答辩、了解结题/全周期承诺 |
| [compliance-redlines.md](references/compliance-redlines.md) | 诚信红线、AI 使用规范（动笔即应知） |
| [process-timeline.md](references/process-timeline.md) | 申报流程、系统填报、倒排时间表 |

模板（复制即填）：`assets/templates/` —— [nsfc_zhengwen_outline.md](assets/templates/nsfc_zhengwen_outline.md)、[nssfc_huoye_outline.md](assets/templates/nssfc_huoye_outline.md)、[checklists.md](assets/templates/checklists.md)。

---

## 给 Claude 的执行提示

- **先要材料再动手**：让用户给出研究想法、已有基础、初稿或片段。空手"替用户想研究内容"既不合规也不会中。
- **当年参数必现查**：本 skill 的数字是 2025–2026 快照，凡涉及钱/日期/字数/限项，引用 [key-parameters.md](references/key-parameters.md) 并提醒"以当年官方公告/指南为准"。
- **绝不编造**：不杜撰文献、数据、预实验结果、他人成果。缺什么就标注"待补"，让用户提供。
- **国社科先查匿名**：任何国社科活页内容，输出前先过匿名自检（姓名/单位/导师/自引/PDF属性）。
- **改写给对照**：润色时给"差→好"对照并说明为什么改，让用户学会、也便于自己把控。
- **图表与正文锁定**：图里出现的模块/阶段必须和正文研究内容一一对应，别各说各话。
