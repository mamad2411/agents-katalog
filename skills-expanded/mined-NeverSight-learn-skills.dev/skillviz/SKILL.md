---
name: skillviz
description: "把一个 Claude Code 的 skill 或斜杠命令的执行流程，画成一张可点击的交互式 HTML 流程图——步骤怎么串、每步跑什么命令、输入产物、失败模式，并带每步一键交给 /dbg 单跑那一步。当用户想看/可视化/画出/理清某个具体 skill 或命令的流程与步骤时触发，例如「skillviz cpi」「画出 cpi 的流程」「skill 可视化」「流程图看这个 command」「visualize how skill-selector works」「这个命令有哪几步」，或想着手调试某个 skill 的某一步。范围仅限**已存在的 Claude Code skill/命令的执行流程**——不做任意系统/架构/代码的通用示意图（那用 creating-mermaid-diagrams），也不是用散文解释某个 skill 是干嘛的。"
allowed-tools: ["Bash", "Read", "Write", "Glob", "Grep"]
---

# Role: skill 流程图生成器（理解层）

分工：**你负责理解，渲染器负责画图**。你把目标 skill 的 .md（和它引用的代码）读懂，产出一份 flow JSON——步骤怎么串、每步在做什么（人话）、跑什么命令、产出什么、怎么失败；`render_flow.py` 把它确定性地渲染成流程图 HTML。禁止用正则/脚本去解析 md 结构——理解是你的活。

本技能激活时，用户通常已经点名（或在上下文里明确所指）一个要可视化的 skill/命令。若没点名，先问清要画哪个，别猜。

> 本技能自包含：渲染器 `render_flow.py` 就在技能目录里；下面命令用的 `~/.claude/skills/skillviz/` 是它装好后的位置（本仓 `skillviz/` 软链进 `~/.claude/skills/`）。flow JSON 产物落技能目录下的 `out/`（已 gitignore）。

## 步骤

### 1. 定位源文件

拿到用户所指的 skill 名或路径：

- 路径（含 `/` 或以 `.md` 结尾）→ 直接用。
- 裸名 `<n>` → 依次找 `~/.claude/commands/<n>.md`、`~/.claude/skills/<n>/SKILL.md`。
- 都没有 → 把两个位置的候选列给用户，停。
- 用户没给名字 → 问要画哪个，别自作主张挑一个。

### 2. 读懂它

- 通读 md 全文。
- 若正文引用了本机代码目录（如某分析工具的 `~/Coding/<tool>/`），读关键代码文件，拿到**真实的**数据清单（系列 ID、权重、桶定义等顶层常量）和 CLI 子命令——这些进 substeps 的 items，回答"这步到底 fetch/算了哪些东西"。
- 纯散文 skill（无代码、无编号步骤）也要拆：按它实际的执行逻辑切成 3-8 个阶段，别硬造。

### 3. 写 flow JSON

写到 `~/.claude/skills/skillviz/out/<n>.flow.json`。Schema（渲染器契约，字段名精确匹配）：

```json
{
  "skill": "cpi",
  "title": "美国 CPI 月度研判",
  "source": "~/.claude/commands/cpi.md",
  "generated": "YYYY-MM-DD",
  "lang": "zh",
  "overview": "一两句人话：这条 skill 从什么输入走到什么产出，核心骨架是什么",
  "globals": {
    "code_dir": "~/Coding/cpi_analyzer/",
    "outputs": ["产物路径 A", "产物路径 B"],
    "guards": ["边界/铁律，精选 3-8 条"]
  },
  "steps": [
    {
      "id": 1,
      "title": "Fetch + Consensus",
      "kind": "cli",
      "summary": "两三句人话：这一步做什么、为什么需要它、在整条链里承上启下什么。不是复述标题。",
      "commands": ["python3 cpi_cli.py fetch", "python3 cpi_cli.py consensus --month <YYYY-MM>"],
      "inputs": ["BLS API v2（59 系列）", "Trading Economics"],
      "outputs": ["cache/analysis_*.json"],
      "failure_modes": [{"case": "BLS API 不通", "action": "退出，查 BLS_API_KEY / 网络 / 日限额"}],
      "substeps": [
        {"title": "AGG 聚合系列（9 条）", "summary": "可选的一句解释", "items": ["CUSR0000SA0 — All items SA", "…真实条目，从代码里抽"]}
      ],
      "source_lines": "42-44",
      "next": [{"to": 3, "when": "只在有分支时给；线性流程整个字段省略"}]
    }
  ]
}
```

要求：

- **lang**（可选）：`zh` / `en`，决定渲染器**界面文字**（栏目标题、按钮、dbg 提示）的语言，默认 `zh`；`render_flow.py --lang zh|en|auto` 可覆盖（auto=跟随本字段）。**内容语言**（summary/title/substeps 等）不由此控制——你用哪种语言写，图上就是哪种；给别的语言用户生成时，直接用对方语言写内容、并把 lang 设成对应值即可。
- **kind**：`cli`（跑确定性命令）/ `llm`（模型写作/判断）/ `mixed`。
- **summary 是本工具的灵魂**：解释给"没读过这个 skill 的自己"，讲清楚做什么 + 为什么 + 上下游关系。禁止抽象套话。
- **summary/overview 用娓娓道来的完整句子写**：保留全部技术细节，但别堆 `→` 箭头链和 `A/B/C` 斜杠短语——那种压缩记法读起来吃力。像跟人当面讲解一样顺下来；密集的枚举放进 substeps 的 items，别塞进正文。
- **别糊成一坨**：overview 保持短（一两句 + 可选一句边界），左边节点已经把步骤列出来了，**别在 overview 里复述整条步骤链**。任何超过三四句的正文都用**空行分段**——渲染器认 `\n\n` 为段落、段内 `\n` 为换行，会给出呼吸感；一段不要写到七八行没有喘息。
- **commands** 保持可复制可跑；变量部分用 `<占位符>`（渲染器会标红提醒）。
- **failure_modes** 从 md 的失败表/注意事项挂到**对应步骤**，不是全堆最后。
- **substeps** 用于下钻：数据清单、narrative 小节表、分桶定义等。条目要真实（读代码得来），别写"若干系列"。
- 顺序线性时不写 `next`；有条件分支才写。

### 4. 渲染 + 打开

```bash
python3 ~/.claude/skills/skillviz/render_flow.py ~/.claude/skills/skillviz/out/<n>.flow.json --open
```

用户说了「别打开 / 就出文件 / --no-open」则去掉 `--open`。渲染器退出非零 = JSON 不合 schema，按报错修 JSON 重跑。

### 5. 完成报告

报：flow.json 与 html 路径、步数、每步一行（id + 标题 + kind）、读了哪些代码文件。提醒：图上每步的「复制调试命令」按钮 → 粘到任意会话即 `/dbg <skill> <id>` 单跑那一步（需装配套的 `/dbg` 命令，见 `commands/dbg.md`）。

## 注意

- flow JSON 是 `/dbg` 的数据源——它的质量直接决定定点调试的质量；产物路径固定在 `~/.claude/skills/skillviz/out/`，`/dbg` 就去那儿读。
- skill 更新后，让本技能对它重跑一遍即可刷新（JSON+HTML 原地覆盖）。
- 渲染器/schema 改动要双向同步：`render_flow.py` ↔ 本文件 schema 段。
- 调试单步是 `/dbg` 命令的活（它读本技能产的 flow JSON），本技能只管产图；`/dbg` 是本技能的配套命令，装法见 README。
