---
name: autoppt
description: AutoPPT（AI备课神器）——只需一句话的课程主题（或一份教学大纲），先了解老师的课程需求，再一键生成一整周精美、可交互的 HTML 教学课件（两节理论课 + 一节实践课，各约 45 分钟）：完整讲稿、浏览器里真实计算的互动、可直接运行的实践代码与 Notebook、学生版、教师指南与出处页；三种风格（学术刊物 / 黑底舞台 / 几何色块）任选。Use when a teacher asks to design / build / 做 / 设计 course slides or 课件, a weekly design doc (设计文档), lecture decks from a syllabus, or says "开干" after a design doc.
---

# AutoPPT（AI备课神器）：一周三节课的交互式 HTML 课件

你要交付的是**一整周可以直接上课的课件**：理论一、理论二、实践课三套 Reveal.js 幻灯片（1920×1080，离线可用），每页有完整讲稿，互动在浏览器里真实计算，实践课代码真实运行并生成 Notebook，另有学生版、教师指南、学生指南、事实出处与图片来源。

参考实现：仓库里的 `examples/week01/`（《人工智能基础》第 1 周，含设计文档）。动手前至少打开它的 `lecture1.html` 和 `第一周 设计文档.md` 看一遍。

## 什么时候用
- 老师第一次来、要做一门课 → 先 ⓪ 需求访谈、① 课程内容设计，老师确认后再做第 1 周。
- 一句话：“帮我做一节 / 一周关于 X 的课件” → **快速模式**：只问学生是谁和风格，其余用默认值，写设计文档并完整实现。
- “设计 / 做第 N 周的课件” → 写设计文档 **并完整实现**。
- “设计第 N 周的课程内容 / 设计文档” → **只写设计文档**；教师说“开干”再实现。
- “根据大纲做课件”“把这门课做成 HTML 课件” → 先建课程大纲与制作约定，再从第 1 周开始。

## 流程（详见 references/workflow.md）
**先了解老师的课，再做课件。** 前两步（⓪①）每门课只做一次，结果要老师确认。

⓪ **了解课程（需求访谈）**——`references/intake.md`、`templates/课程需求表.md`：先读老师给的大纲 / 教材目录 / 旧课件，再用选择题一轮最多 4 问补齐：学生是谁（会不会编程）、几周几节、每周讲什么、实践课做什么（编程 / 案例 / 实验 / 习题 / 写作）、配图政策（能否搜开放图库、能否 AI 生成、是否公开发布）、课件风格。快速模式（老师只说一句）只问学生和风格，其余用默认值并标“假设”。

① **课程内容设计**——产出 `课程大纲.md`（周次表：每周主题、三节课各讲什么、实践课形式、项目里程碑、每周主线、素材计划），**交老师修改确认**；同时建立《课件制作约定》。

**选风格**（在 ⓪ 中一并问）：给用户看 `styles/styles.jpg`，三选一（有选择题工具就用它，否则列编号选项）：
   - **A 学术刊物** `academic`（默认）：暖纸底 · 宋体大标题 · 整句标题 + 图证据
   - **B 黑底舞台** `stage`：深色封面与章节页 · 巨型年份 · 大字金句；内容页冷灰底
   - **C 几何色块** `blocks`：深蓝大色块 · 橙色圆点 · 网格信息；无衬线粗标题
   选定后写进《课件制作约定》，同一门课各周保持一致。

然后每一周：
1. **读**：课程大纲、`课件制作约定.md`、上一周的设计文档与结果、旧课件里**内容**对应的部分。
2. **设计文档**：按 `templates/周设计文档模板.md` 写《第 N 周 设计文档.md》——一句主线、逐页表、新组件、数据与计算、事实核查清单（联网核对）、验收标准、需要教师确认的事。教师修改后以修改版为准。
3. **生成骨架**：
   ```bash
   python3 <本 skill>/scripts/new_week.py --dest <课程文件夹> --week N --style academic --course "课程名" \
       --teacher "教师" --school "学校" --term "学期" --topic "本周主题" --l1 "理论一" --l2 "理论二" --lab "实践课"
   ```
   得到 `weekNN/`（风格写在 `src/styles/theme.css`；换风格 = 把 `src/styles/themes/` 里另一个文件复制过去）：页型样板（每种版式一页）、首页、学生指南、教师指南模板、`build.py`、`start.py`、`tools/run_lab.py`、`week.json`。上一周首页会自动加“第 N 周 →”。
4. **数据先行**：先写并跑通 `tools/toyN.py`（理论课互动的数据与对照值）；实践课是编程时，再写 `tools/run_lab.py`（真实运行 + assert 自检）。页面和讲稿里的数字一律来自这里。实践课不是编程时（案例研讨、实验、史料研读……），把 lab1.html 的代码页换成材料页、任务单、讨论题与评分要点，删掉 run_lab.py。
5. **配图**（`references/images.md`）：按“自绘 SVG → 脚本计算 → 老师素材 → 开放许可图库 → AI 生成示意”的顺序为每一页找图。非 AI 类课程（历史、医学、生物、地理、艺术……）常需要真实图片：用 `scripts/find_images.py search "<英文关键词>"` 搜 Wikimedia Commons 与 Openverse，看过候选再 `get` 下载并自动登记作者、许可、链接；AI 生成的图标“AI 生成示意”，不生成真实人物与需要真实的科学图。
6. **组件**：新互动写进 `src/components/`，用 `W1.reg(name, {init, reset})`；浏览器计算与 Python 逐项对照（references/components.md）。
7. **写三节课**：把样板页替换成设计文档里的每一页（references/authoring.md）。每页一个核心观点、整句标题、完整讲稿（【建议用时】【本页目标】【讲述建议】…【转场】）。
8. **配套页**：`index.html`、`student-setup.html`、`sources.html`、`src/teacher-guide.tpl.html`、`README.md`、`TESTING.md`；第三方图片登记到 `week.json` 的 `images`。
9. **构建与检查**：
   ```bash
   cd weekNN && python3 build.py
   bash <本 skill>/scripts/check_week.sh weekNN    # 冒烟测试 + 版式检查 + 逐页截图与总览图
   ```
   **逐张看总览图**并修到满意；写 TESTING.md。
10. **交付**：写进课程文件夹；把新学到的规矩、示例数据的已知结果追加到 `课件制作约定.md`；给教师一段简短总结 + 需要确认的事。

## 硬性要求
- **不编造**：事实联网核对，写进 sources.html；模型输出只来自真实运行；跑不了的（大模型、GPU）由教师机脚本回填，未运行时显示占位（`window.XXX = null;`）。
- **真实计算**：互动不是动画，是用导出的数据 / 权重在浏览器里现场算，并与 Python 对照。
- **一份代码三处用**：实践课的代码、输出、Notebook 出自 `run_lab.py` 的同一次运行。
- **版式**：代码页 `data-fit="off"`、代码行 ≤ 86 列；比例列不用固定 px；新 class 用独有前缀；文字出处 `data-src="资料来源：…"`；无重叠（audit_overlap.js 输出无 OV / OUT）。
- **版权**：优先自绘 SVG 与脚本生成的图；第三方图片登记来源，公开发布前替换。
- **用户不需要会编程**：所有命令由你来运行；只在需要教师本人决定的事上提问。
- **学生零基础友好**：术语首次出现给中英文；代码注释写给初学者；每个实践步骤都有“结果怎么读”。

## 文件索引
| 文件 | 用途 |
|---|---|
| `references/intake.md` | ⓪ 需求访谈、① 课程内容设计（不同学科的实践课与互动怎么做） |
| `references/workflow.md` | 全部阶段的详细流程、触发语、沟通习惯 |
| `references/images.md` | 配图：自绘、计算、开放许可图库、AI 生成；登记与检查 |
| `references/authoring.md` | 一页的 HTML 骨架、页型、积木 class、版式规矩、讲稿写法 |
| `references/components.md` | 组件接口、现成组件、真实计算与对照、教师机回填 |
| `references/lab.md` | run_lab.py 的 CELLS、自检、Notebook、示例项目 |
| `references/quality.md` | 内容红线、版权、测试清单、交付说明 |
| `references/codex.md` | 在 OpenAI Codex 中使用的差异（提问方式、沙箱与网络、查看截图） |
| `templates/` | 课程需求表、课程大纲、周设计文档、课件制作约定 四个模板 |
| `styles/styles.jpg` | 三种风格的样张，给用户选风格时展示 |
| `engine/` | 一周课件的骨架（new_week.py 复制它） |
| `scripts/` | new_week.py、find_images.py（搜图、下载、登记来源）、check_week.sh、smoke_test.js、audit_overlap.js、shoot.js、contact_sheet.py |

## 环境
Python 3.9+（构建；字体裁剪可选 `fontTools` + Noto CJK 字体）；Node 18+ 与 Playwright（检查与截图：`npm i -g playwright && npx playwright install chromium`，运行时 `NODE_PATH=$(npm root -g)`）；实践课按课程需要（NumPy、pandas、scikit-learn……）。
