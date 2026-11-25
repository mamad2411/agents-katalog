---
name: paper-translation
description: Use when translating academic papers (PDF to Chinese Markdown), extracting PDFs with MinerU API, or needing to preserve LaTeX formulas/images/tables through a translation workflow
---

# Paper Translation

## Pre-flight Check (MANDATORY — runs every time, before anything else)

### Step 0: Determine if API extraction is needed

**If `mineru_output/full.md` already exists** (paper was already extracted by MinerU):
- Skip the token check entirely — no API call is needed.
- Jump directly to [1. Prepare](#1-prepare).

**If `mineru_output/full.md` does NOT exist** (need to call MinerU API):
- Proceed to the token check below.

### Token check (only when API extraction is needed)

Check for the MinerU API token. Try these methods in order:

1. First, try bash:
   ```bash
   source ~/.claude/skills/paper-translation/config 2>/dev/null; echo $MINERU_TOKEN
   ```
2. If bash is unavailable, read the config file directly:
   ```
   Read ~/.claude/skills/paper-translation/config and extract MINERU_TOKEN= value
   ```

### If MINERU_TOKEN is empty or not set → respond with:

```
⚠️ 需要配置 MinerU API Token 才能提取 PDF。

获取步骤（约 2 分钟）：
1. 打开 https://mineru.net ，注册/登录账号
2. 登录后访问 https://mineru.net/apiManage/token
3. 创建并复制 JWT Token（以 eyJ... 开头的长字符串）

配置方法：
  cp ~/.claude/skills/paper-translation/config.example ~/.claude/skills/paper-translation/config

然后用编辑器打开 config，将 Token 填入 MINERU_TOKEN= 后面。

或直接告诉我你的 Token，我帮你写入配置文件。
```

**Do NOT proceed until the user confirms MINERU_TOKEN is set.**

### If MINERU_TOKEN is set or full.md exists → proceed to Overview.

---

## Overview

Systematic workflow for extracting academic PDFs via MinerU API and translating them to Chinese Markdown while preserving formulas, images, tables, and code blocks. Core principle: **plan first, translate in order, verify every invariant**.

**HARD RULE:** Before ANY translation work, you MUST invoke Plan mode (`EnterPlanMode` / `/plan`) to create a structured implementation plan. Never translate directly — the plan catches missing invariants and term conflicts before they become rework.

## When to Use

- Translating academic papers (CS, ML, robotics) from PDF to Chinese Markdown
- Extracting PDFs with formulas and images via MinerU Precision API
- Need consistent terminology across multiple related papers
- Want a repeatable translation pipeline with verification checkpoints

## Workflow (5 Stages)

### 1. Prepare

```bash
# Count source lines and images before starting
wc -l mineru_output/full.md
grep -c '!\[.*\](images/' mineru_output/full.md
# Check for null bytes (MinerU OCR artifacts that break grep)
python -c "print(open('mineru_output/full.md','rb').read().count(b'\x00'))"
```

- **Clean up `output_*`:** After MinerU extraction, move contents to `<论文名>/mineru_output/`, then delete `output_*/`. This intermediate dir must not linger.
- **Formula sanitization (NEW):** MinerU API 产出的 LaTeX 常有渲染问题（`$$` 跨行断裂、内联 `$` 内下划线未转义、分隔符空格异常）。翻译前先扫描并修复：
  ```bash
  # 检查 $$ 数量是否为偶数（奇数 = 有断裂）
  grep -c '\$\$' mineru_output/full.md
  ```
  常见修复：
  - `$$` 被换行拆开 → 合并到同一行
  - `$x_i$` 中 `_` 导致 Markdown 斜体误识别 → 改为 `$x\_i$`
  - `$$` 前后缺空格导致与前文粘连 → 补空格
  - `$x _ { \tau }$` → `$x_{\tau}$`（移除 LaTeX 数学模式下的多余空格）
  - `\begin{array}{r} x \end{array}` → 单行公式去除多余 array 包装
  - `\begin{array}{l l}` → `\begin{cases}`（cases 环境是常见误用 array 的目标）
  - **判断标准：数学模式内多余空格/包装属于可读性问题；花括号内的下标/上标内容本身不可改动。** 拿不准的改动标记出来人工复核。
- Build terminology table for core terms before translating
- Confirm source file paths, line counts, image counts
- **Pseudocode detection & extraction check:** MinerU 可能**完全不提取**伪代码块（PDF 中的 Algorithm 在 `full.md` 中消失）。
  ```bash
  # 检查 full.md 中是否有伪代码特征
  grep -c -E "(Algorithm [0-9]|^ [0-9]+: )" mineru_output/full.md
  # 如果返回 0 但论文标题/摘要提到算法 → MinerU 遗漏，标记【伪代码缺失，需手动提取】
  ```
  如果伪代码存在但未被 ``` 包裹，手动包入 ` ```text ` 代码块。如果完全不存在，在译文中标注位置并告知用户。

### 2. Plan (MANDATORY)

**REQUIRED:** Invoke Claude Code Plan mode (`EnterPlanMode`) before touching any translation work. Do NOT skip this step.

**If `EnterPlanMode` tool is unavailable** (e.g., in agent/sub-agent context), manually present the plan as text: list all tasks, dependencies, output paths, and verification criteria. This text-based plan serves the same purpose.

The plan must include:
- One task per paper translation (shorter paper first)
- One task for terminology consistency check
- One task for format & path verification
- Dependencies set correctly (verification → consistency → both translations done)
- Source file line counts and image counts recorded as baselines
- Output naming convention (`*_zh.md`) explicitly stated
- Image path correction rule documented (`images/` → `medias/`)

Red flags that mean STOP and enter Plan mode:
- "This is just a simple translation"
- "I know what to do"
- "Let me just start translating directly"

**All of these mean: Stop. Enter Plan mode first.**

### 3. Execute

**Translation order:** For multiple papers, translate the shorter one first to accumulate term experience, then the longer one. For a single paper, skip this consideration.

**⚠️ 逐行翻译，不要凭理解概括：** 翻译时必须逐行对照 `full.md`，确保每个图片引用、公式、表格都被保留。最常见的 bug 是"理解后概括写译文"导致图片引用批量丢失。翻译完一段后回头扫一眼 `full.md` 对应段落，确认没有遗漏。

**LaTeX formulas — preserve content, fix rendering:**
- 保留数学内容（符号、结构、编号），但必须修复 MinerU 产出的渲染问题
- 常见修复：合并断裂 `$$`、转义内联 `$` 中的裸下划线、修正分隔符间距
- `\text{...}` 内的英文：属于公式一部分则不翻译（如 `\text{maximize}`），属于自然语言注释则翻译（如 `\text{subject to}` → `\text{满足}`）。拿不准时保留原文。
- 拿不准时不要改数学内容，标记出来人工复核
- 翻译后做闭合检查：`grep -c '\$\$' *_zh.md` 必须为偶数；`grep -c '\\\[' *_zh.md` 与 `grep -c '\\\]' *_zh.md` 必须相等

**Must preserve unchanged:**
- Image references `![...](images/xxx.jpg)`
- Tables (MinerU 输出 HTML `<table>`，用 `html_table_to_md.py` 批量转 Markdown pipe 语法：`python ~/Desktop/paper-translation/html_table_to_md.py mineru_output/full.md --in-place`。合并单元格在 pipe 格式中不可表示，拆分为独立行列)
- Code blocks (fenced and indented)
- **Pseudocode / algorithms:** MinerU 产出的伪代码通常没有 ` ``` ` 包裹，呈裸文本形态。识别特征：连续多行以 `数字:` 或 `Algorithm` / `算法` 开头。**只翻译标题（如 "算法 1: xxx"），伪代码正文（Input/Output/1:/2:/...）保留原文不动。** 如果伪代码正文被 MinerU 胡乱换行打断，可以手动将其包入 ` ```text ` 代码块以便 Markdown 正确渲染。
- `<details>` collapsible blocks — 保留结构和标签（`<summary>`）不翻译。内部文本：自然语言描述翻译；纯数据保留原文。**Mermaid 图**：节点标签保留英文原文不翻译（属于图表结构，不是自然语言）。
- References: 保留英文原文不动（作者、标题、期刊/会议名均不翻译）
- Heading hierarchy `#` / `##` / `###`

**Output location:** 翻译结果放在源 PDF 所在目录（即论文原始存放位置），而非 paper-translation 仓库目录。

**Output directory structure** (per paper):
```
<源PDF所在目录>/<论文名>/
├── medias/             # 图片，供 _zh.md 引用
├── <论文名>_zh.md       # 中文译文
├── <论文名>.pdf         # 源 PDF
└── mineru_output/      # MinerU 解析原始输出（原封不动）
    ├── full.md
    └── images/
```

**Must change:**
- Image paths: `images/xxx.jpg` → `medias/xxx.jpg`
- **Image copy (precise):** Use `copy_images.py` to copy only referenced images:
  ```bash
  python ~/Desktop/paper-translation/copy_images.py <paper_dir>
  ```
  Or manually: `grep -oP 'images/\K[^)]+' mineru_output/full.md | sort -u | while read img; do cp "mineru_output/images/$img" "medias/$img"; done`
- Body text: English → Chinese (academic style)
- Figure/Table captions: English → Chinese (e.g., "Figure 1. Overview of..." → "图1. ...概览")
- **Template noise handling:** 期刊模板残留（如占位性 "Journal Title", "XX(X):1-18", "Keywords: Class file, LATEX 2e" 等）— 保留原文并添加 `[模板残留]` 标记，不要翻译为正常内容。
- **English abbreviations:** 首次出现时保留英文缩写（如 "back-propagation through time (BPTT)" → "通过时间反向传播（BPTT, back-propagation through time）"），术语表可补充常用缩写对应关系。
- **Reference links:** MinerU **不会**解析出参考文献的 URL 或 DOI——输出是纯文本。需要从参考文献文本中手动提取 arXiv ID 构造链接：
  1. 扫描 References 章节每条文献，查找 `arXiv:XXXX.XXXXX` 或 `arxiv preprint arXiv:XXXX.XXXXX` 模式
  2. 提取 arXiv ID，构造 `https://arxiv.org/abs/XXXX.XXXXX`。注意 MinerU 可能截断 ID（如 "arXiv, YYYY" 只剩年份），此时标记该文献为 `[arXiv ID 缺失]`，不做猜测。
  3. 在正文中查找对应引用，将纯文本引用改为可点击链接格式
  4. 没有 arXiv ID 的文献保留原文不加链接，不做猜测
  - **引用格式多样性:** 学术论文的引用格式不限于 `[N]` 数字编号。常见还有 author-year 格式（`[Fujimoto et al., 2019]`）、混合格式。处理策略：
    - 先为 References 列表添加数字编号 `[1]`, `[2]`, ...
    - 正文中 author-year 引用映射到对应编号
    - 仅对有 arXiv ID 的文献添加链接
  - **⚠️ 现实预期:** arXiv ID 覆盖率视论文领域而定：ML 预印本约 70-80%，会议论文（IJCAI/AAAI/ICRA）约 20-40%。无 arXiv ID 的文献保留无链接形式。逐一提取 arXiv ID 耗时较长，可作为可选步骤。

**Terminology consistency:** 翻译开始前，扫描原文构建术语表（不要使用下面的示例术语——它们仅适用于特定领域）。术语表格式：

| English | Chinese | 备注 |
|---------|---------|------|
| <原文核心术语> | <中文译法> | <可选：首次出现位置> |

构建原则：1) 全篇同一术语用同一译法 2) 专有名词（算法名、框架名）保留英文 3) 首次出现时中英对照。以下仅为 RL 领域示例，实际翻译时根据论文领域自行构建：
| English | Chinese |
|---------|---------|
| reinforcement learning (RL) | 强化学习 |
| policy optimization | 策略优化 |
| constrained Markov decision process (CMDP) | 约束马尔可夫决策过程 |
| logarithmic barrier function | 对数障碍函数 |
| interior-point method | 内点法 |
| Lagrange multiplier | 拉格朗日乘子 |
| trust region | 信任域 |
| advantage function | 优势函数 |
| value function | 价值函数 |
| cost function | 代价函数 |
| generalized advantage estimation (GAE) | 广义优势估计 |
| proximal policy optimization (PPO) | 近端策略优化 |
| sim-to-real | 仿真到现实 |

### 3.5. Appendix Strategy (附录超过正文40%时启用)

当附录行数超过正文（不含 References）的 40% 时，启用分级处理。阈值判断：
```bash
BODY_END=$(grep -n "^# References\|^# REFERENCES\|^## References" mineru_output/full.md | head -1 | cut -d: -f1)
echo "Body: $BODY_END lines, Appendix: $((TOTAL - BODY_END)) lines"
```

| 附录类型 | 处理方式 |
|---------|---------|
| 理论证明（大量 `$$` 公式） | 所有 `$$` 公式保持原样；段落文字翻译为中文；证明步骤英文叙述可选翻译 |
| 训练曲线图（Figure 5-15） | 保留 `![](medias/xxx.jpg)` 引用，仅翻译图注；`<details>` 内数据表不翻译（纯数值） |
| 环境截图 | 保留图片引用，英文描述可选择性翻译 |
| 超参数表 | HTML → Markdown pipe，表头翻译，数值不变 |
| 补充讨论 | 正常翻译 |

**约束:** 即使附录极长（>500行），也不得完全跳过翻译。至少处理：① 所有 `$$` 公式保留 ② 所有 `![](medias/...)` 图片引用保留 ③ 段落文字翻译。如果实在无法完整翻译，在对应位置标注 `[附录详细内容见原文附录]`。

### 4. Fix

Common issues and their fixes:

| Issue | Detection | Fix |
|-------|-----------|-----|
| Placeholder text left in output | Manual review of figure captions | Read each section, insert actual images |
| Missing images | `grep -c '!\[.*\](images/'` mismatch | Compare counts vs original, add missing figures |
| Image path pointing to wrong directory | Visual inspection | Correct to `medias/` prefix |
| Inconsistent terminology | `grep` key terms in both outputs | Align to glossary |
| **Formula rendering broken** | `$$` count odd, `_` inside `$...$` not escaped, delimiter spacing wrong | Fix rendering: rejoin split `$$`, escape bare `_` → `\_`, fix spacing. Do NOT change math content. Flag uncertain cases for manual review. |
| **Pseudocode translated as body text** | Algorithm lines (e.g., `1: for ... do`) appear in Chinese | Scan mineru_output for `Algorithm` / `算法` / consecutive `数字:` lines. Wrap in ` ```text ` if not already fenced. Restore original English for pseudocode body; only translate title/header. |
| **Reference `[N]` has no link** | Plain `[1]` in text, not clickable | **首选方案：调用 MCP 工具 `resolve_reference`** 单条查找或 `batch_resolve_references` 批量补全 DOI/URL。回退方案：扫描参考文献文本中的 arXiv ID 模式（`arXiv:XXXX.XXXXX`）手动构造链接。无 arXiv ID → leave unlinked。 |
| **OCR artifacts in output** | Control chars (`^C`), broken text (`Fujimoto and \n\n Gu`), char substitutions (`\textcircled{2}` → `2`) | Scan for `[\x00-\x08\x0b\x0c\x0e-\x1f]` control chars → delete. Rejoin text split by spurious newlines. Flag suspicious substitutions for manual review. |

### 5. Verify

Run these checks before declaring done. **Windows 注意:** `grep -P` 不可用，统一使用 `grep -E`。

```bash
# Image count (if appendix truncated per Section 3.5, count will differ — note in report)
SRC_IMG=$(grep -c '!\[.*\](images/' mineru_output/full.md)
TRG_IMG=$(grep -c '!\[.*\](medias/' *_zh.md)
echo "Source images: $SRC_IMG  Translation: $TRG_IMG"
# TRG_IMG < SRC_IMG 且差异 >10% → 逐行检查 full.md 漏了哪些图

# Formula integrity (must be even; count should be close to source)
SRC_FM=$(grep -c '\$\$' mineru_output/full.md)
TRG_FM=$(grep -c '\$\$' *_zh.md)
echo "Source $$: $SRC_FM  Translation $$: $TRG_FM"
# 偏差 >30% = 公式丢失，逐行检查

# Terminology consistency (multi-paper only; skip for single paper)
grep -o "约束马尔可夫\|对数障碍\|内点法\|拉格朗日\|信任域" *_zh.md | sort | uniq -c

# Image files actually exist in medias/
ls medias/ | wc -l

# Reference links (use -E not -P for Windows compatibility)
grep -cE '\[[0-9]+\]' *_zh.md | head -5
grep -cE '\[[0-9]+\]\(' *_zh.md | head -5
```

## MinerU API Quick Reference

**提取脚本:** `extract_pdfs.py`（与本 SKILL.md 同目录）— 批量上传 PDF → 轮询解析状态 → 下载解压 ZIP 结果。

**⚠️ 安全提示:** 不要在命令行中直接传入 Token（会留在 shell 历史中）。始终：
1. 先用 Write 工具将 Python 脚本写入文件（脚本内从 config 文件读取 Token）
2. 再用 Bash 工具执行脚本文件
3. 这样 Token 不会出现在命令日志中

**使用方法:**
```bash
cd ~/.claude/skills/paper-translation
# 编辑 extract_pdfs.py 中的 PDFS 列表，添加要解析的 PDF
# 然后运行:
python extract_pdfs.py
```
输出目录为 `output_<论文名>/`，后续按 Prepare 步骤移到 `<论文名>/mineru_output/`。

**Token 获取:** https://mineru.net/apiManage/token  
**API docs:** https://mineru.net/apiManage/docs

## Effective Guiding Patterns

These instructions produced the best results:

| Instruction | Effect |
|-------------|--------|
| "Don't modify the original files" | Established `_zh` suffix naming convention |
| "Make a plan first" | Triggered Plan mode → task breakdown → ordered execution |
| "Use skills frequently" (stored in memory) | Auto-triggered writing-plans, subagent-driven workflows |
| Approve plan before execution | Prevented directional rework |
| Explicit terminology requirements | Ensured cross-paper consistency |

## Common Mistakes

- **Batch-translating both papers at once** — First paper's translation choices inform the second; translating shorter one first builds a term base
- **Skipping image path correction** — MinerU outputs `images/` but `_zh.md` is at paper root level; always change to `medias/` and copy images over
- **Relying on grep alone for image verification** — Some images are in `<details>` blocks; also check figure captions manually
- **Using placeholder text** — "实验图表保持不变" is not acceptable; every image and caption must be present in the translation
- **Not verifying formula closure** — A single unclosed `$$` breaks all subsequent Markdown rendering; always check even counts
- **Leaving HTML tables unconverted** — MinerU outputs `<table>` HTML tags, which render poorly in most Markdown viewers; always convert to `|` pipe syntax
- **Leaving `output_*` directories behind** — After moving contents to `<论文名>/mineru_output/`, always delete the intermediate `output_*/` directory
- **Translating pseudocode body** — MinerU outputs algorithms as bare text (no ` ``` `). Only translate the title (e.g., "Algorithm 1: ..."); the pseudocode body (Input/Output/lines like `1: for...`) must stay in English. If the mineru output has no code fence, add ` ```text ` around the pseudocode block.

## MCP Tools (参考文献链接解析)

本 skill 提供一组 MCP 工具，通过 CrossRef 和 arXiv API 自动查找论文的 DOI 和 URL，弥补 MinerU 不输出参考文献链接的缺陷。

### 可用工具

| 工具 | 用途 | 调用时机 |
|------|------|----------|
| `resolve_reference` | 输入论文标题（+ 可选作者），返回 DOI、URL、期刊、年份 | Fix 阶段逐条补全参考文献链接 |
| `batch_resolve_references` | 输入参考文献列表，批量查 CrossRef 返回 DOI | Fix 阶段一次性补全整篇论文的参考文献 |
| `lookup_arxiv` | 输入 arXiv ID，返回标题、作者、DOI、PDF 链接 | Execute 阶段验证 arXiv 引用；Fix 阶段补全 arXiv ID 截断的文献 |
| `search_arxiv` | 输入关键词，在 arXiv 搜索匹配论文 | Prepare 阶段发现相关论文；Fix 阶段确认模糊引用 |

### 使用示例

**单条查找（Fix 阶段逐条处理）：**
```
调用 MCP 工具 resolve_reference
  title: "Attention Is All You Need"
  author: "Vaswani"
返回: DOI: 10.xxxx, URL: https://doi.org/...
→ 在译文中将纯文本引用改为可点击链接格式
```

**批量查找（Fix 阶段一次性处理）：**
```
调用 MCP 工具 batch_resolve_references
  references: ["Attention Is All You Need", "BERT: Pre-training of Deep...", ...]
返回: 共 30 条，找到 21 条 DOI (70%)
→ 有 DOI 的添加链接，无 DOI 的保留原文
```

**arXiv ID 补全（Fix 阶段修复截断）：**
```
调用 MCP 工具 lookup_arxiv
  arxiv_id: "1910.09615"
返回: Title, Authors, DOI, PDF link
→ 如原文 arXiv ID 被截断（只剩年份），用完整信息补全引用
```

### 注意事项

- CrossRef API 免费但有限速：单条查找无限制，批量查找建议每次 ≤50 条
- arXiv API 在国内网络可能超时——如 `lookup_arxiv` 失败，回退到手动构造 `https://arxiv.org/abs/<ID>` 链接
- MCP 查找结果仅供参考，标题匹配不精确时需人工验证 DOI 正确性
- 会议论文（IJCAI/AAAI/ICRA）CrossRef 覆盖率 60-80%，预印本覆盖率 90%+，无 DOI 的保留无链接形式
