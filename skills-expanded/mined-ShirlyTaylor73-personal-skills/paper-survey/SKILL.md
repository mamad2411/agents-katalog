---
name: paper-survey
description: 中文学术综述报告自动生成 — 系统化完成多论文文献调研并产出 11 章 markdown 综述报告（含 LaTeX 公式可渲染）。集成 paper-search 自动检索下载、K 路并行 subagent 解析、reviewer 双层质量审查、跨 session 自动恢复。
---

# paper-survey

> **TRIGGER 关键词**：「文献调研」「综述报告」「research survey」「literature review」「调研报告」「学术综述」 / 任何要求多论文系统化整理 + 正式 markdown 报告输出的场景。
>
> **SKIP（不要使用本 skill）**：单篇论文阅读 / 简单论文检索（用 paper-search） / 不需要正式综述报告的快速摘要 / 仅需要论文清单 PDF 下载（用 paper-search）。

中文学术综述报告自动化 skill。9 个流程节点 / 6 个主阶段全自动流程，每主阶段 implementor + reviewer 双 subagent 质量门控（0b 综述选择由主 Claude 内联检查），跨 session 可恢复，集成 paper-search。

## 流程总览

```
启动检测 (-1) ─────────── spec.md 当前阶段字段权威 + 文件存在性辅助 + AskUserQuestion 确认
    ↓
头脑风暴 (0a) ─────────── 与用户对话对齐主题、范围、深度、模板分支、cwd 工作目录
    ↓
预调研 (0b) ───────────── 下载 1-3 篇主线综述 → 主 Claude 阅读 → pre_survey_notes.md
                          （无独立 reviewer，主 Claude 内联 regex 验引文）
    ↓
写 spec (0c) ──────────── spec_writer 生成 survey_spec.md + spec_reviewer 验证 + 用户最终确认
    ↓
检索下载 (1) ──────────── 按 spec 清单批量下载 PDF + 立即按 naming_convention 重命名
                          + 下载校验（size/标题/作者 fuzzy）+ 自动重试 ≤2
                          + paper_search_reviewer 验证元数据匹配
    ↓
并行解析 (2) ──────────── K 路 paper_extractor 并行（D 分组+β 时序）
                          → 全完后串行 K 路 extract_reviewer 验证
    ↓
报告骨架 (3) ──────────── outline_writer 写 outline.md（严格标题+fenced JSON block）
                          + outline_reviewer 抽样幻觉验证
    ↓
md 组装 (4) ───────────── python assets/assemble_md.py <workdir>（源路径直调，不复制）
                          → outline.md 中间产物渲染为顶层 <topic>_综述报告.md
                          → 内置 dry-run：fenced JSON parse + LaTeX $/$$ 配对
    ↓
完成度核查 (5) ─────────── validation.py 跑 17 项（16 项机械 + 1 项消费 reviewer 报告反幻觉）
                          validation_reviewer 用 ~49 处 verify_quotes_batch 并行 ≈ 2 秒，输出 reviewer 报告
    ↓
交付（用户口头确认）
```

**关键约束**：

- **阶段间严格串行**：禁止跨阶段提前执行（如还在阶段 2 不能开始 outline 起草）
- **阶段内 K 路 implementor 并行**（阶段 2 D + β 派发，单路 ≤6 篇，总并发上限 5）
- **阶段内 reviewer 等本阶段 implementor 全完才开始**

## 阶段 -1：启动检测

每次 skill 调用第一步执行。**spec.md 当前阶段字段是权威状态源**，文件存在性是辅助验证（不一致时 AskUserQuestion 升级用户）。

### 状态机表（覆盖 missing / empty / partial / inconsistent / corrupted）

| spec.md 状态 | 当前阶段字段 | 文件存在性 | 推断阶段 |
|---|---|---|---|
| 不存在 | — | 无任何子目录 | 0a 新开 |
| 不存在 | — | `_pre/` 已下载 | 0b 进行中（续上从 pre_survey_extractor） |
| 不存在 | — | `_work/pre_survey_notes.md` 存在 | 0c 写 spec |
| 存在 | `0c-completed` | `_pre/` 与 `_work/extracts/` 空 / 顶层无 *.pdf | 阶段 1 |
| 存在 | `1-completed` | 顶层 `*.pdf` 非空，`_work/extracts/` 空 | 阶段 2 |
| 存在 | `2-completed` | `_work/extracts/` 全有，`_work/outline.md` 缺 | 阶段 3 |
| 存在 | `3-completed` | `_work/outline.md` 存在，`<topic>_综述报告.md` 缺 | 阶段 4 |
| 存在 | `4-completed` | `<topic>_综述报告.md` 存在，`_reviews/validation_report.md` 缺 | 阶段 5 |
| 存在 | `5-completed` | 全部存在 + 17/17 PASS | **完成** |
| 存在 | 字段缺失 | — | 用文件存在性回退推断 |
| 存在 | 字段与文件存在性矛盾 | — | **AskUserQuestion 升级用户** |
| 损坏（解析异常） | — | — | **AskUserQuestion 升级用户** |

### 流程

1. 扫描 `{cwd}/` 下子目录，识别 `<topic>/` 工作目录
2. 对每个工作目录按上表推断当前阶段
3. 调用 `AskUserQuestion`：「检测到现有任务：[A] {topic-A} 阶段 X / [B] {topic-B} 阶段 Y。请选续哪个 / 新开 / 重跑某主题」
4. 用户选「续上」 → 跳到对应阶段；选「新开」 → 进 0a；选「重跑」 → 删除该阶段产物后重跑

**每阶段完成必做**：主 Claude 完成某阶段后立即 Edit `_work/survey_spec.md` 的 `## 当前阶段` 段为 `{N}-completed`，作为下次 session 的恢复锚点。

## 阶段 0a：头脑风暴

**目标**：与用户对话对齐：

- 主题词（中英文）
- 主题边界（明确"是什么不是什么"）
- 目标深度（学位综述 / 技术调研 / 文献快报）
- 目标论文数（≥5 篇）
- 报告字数目标（**弹性，与论文数 N 挂钩**；中文字符数；validation.py 按 spec.md 字段读取，缺省时按 N fallback 推算）：
  - N ≤ 3 → 2000（mini test 场景）
  - N ∈ [4, 7] → 3500（小规模）
  - N ∈ [8, 15] → 5500（中等规模）
  - N ≥ 16 → 7000（大规模）
- 模板分支（默认通用学术；non-technical 跳过第 4 章）
- 用户已知论文清单 / 主线综述（如有）
- 工作目录 slug

**关键确认**：必须复述工作目录绝对路径让用户确认，避免在代码仓库根目录误落 50 篇 PDF 污染 git。

## 阶段 0b：预调研

**目标**：下载 1-3 篇主线综述，主 Claude 阅读后形成 `pre_survey_notes.md`。

**步骤**：

1. 创建工作目录 `{cwd}/<topic_slug>/`（含子目录 `_pre/` 与 `_work/`）
2. 检索综述（默认源不含 semantic）：
   ```bash
   paper-search search "{topic} survey OR review OR tutorial" -n 5 -s arxiv,crossref,openreview,doaj
   ```
3. 用户给的主线综述：除非明确说"只用这一篇"，否则继续 paper-search 自动补搜
4. 下载 1-3 篇到 `_pre/`，按 naming_convention 重命名
5. 派发 `pre_survey_extractor` subagent 产出 `_work/pre_survey_notes.md`
6. **主 Claude 内联 reviewer**（不派 subagent）：regex 检查每条要点附引文 + verify_quotes_batch 抽样 3 条引文 + 子分类数 ∈ [3, 7]

**AskUserQuestion 阈值（0b）**：严格——综述检出 fuzzy < 80% / 多候选 / 0 命中都问

**失败处理**：默认源返 0 → fallback 加 semantic → 仍 0 则降级"高引论文+奠基工作" + AskUserQuestion 复述

## 阶段 0c：写 spec

**目标**：生成 `<workdir>/_work/survey_spec.md` 契约文件。

**步骤**：

1. 派发 `spec_writer` subagent
2. subagent 读 `_work/pre_survey_notes.md` + 0a 对话纪要 + 用户已知清单
3. subagent 用 `paper-search search` 补全每条论文的 arxiv_id（fuzzy ≥ 80% 直采）
4. 歧义条目攒到「待问用户」清单，一次性 `AskUserQuestion` 批量问（β 合并）
5. 派发 `spec_reviewer` subagent 验证（结构合规 + 论文清单完整 + 关键词覆盖）
6. 主 Claude 复述 spec.md 关键字段给用户**最终确认**

**失败处理**：reviewer FAIL → γ 修复 + 重试 ≤2

## 阶段 1：检索下载

**目标**：按 spec 清单批量下载所有 PDF。

**AskUserQuestion 阈值**：严格——任一论文 fuzzy < 80% / 多候选 / 0 命中 / 元数据不匹配 → 批量问

**步骤**：

1. PDF 直接落 `<workdir>/` 顶层（与 `<topic>_综述报告.md` 同层平铺）
2. 对 spec 论文清单逐条：有 arxiv_id 直接下载；无则先 search 补全
3. **下载后 3 项校验**：文件大小 > 30 KB / 第一页可抽取 / 标题作者 fuzzy ≥ 80%
4. 任一校验 FAIL → 自动重试下载 ≤ 2 次（不同源轮换）
5. 重试仍 FAIL → 三个用户出口（PDF URL / 本地 PDF / 移出清单）
6. 校验通过后立即按 naming_convention 重命名
7. 派发 `paper_search_reviewer` subagent 验证命名 + 元数据匹配
8. reviewer FAIL → γ 修复 + 重试 ≤2

## 阶段 2：并行 subagent 解析

**目标**：K 路 implementor 并行解析所有 PDF。

**派发规则（D 分组 + 二级切分）**：

1. K = spec.md 第 5 章子节数
2. 每子节论文 ≤6 篇 → 单路 implementor
3. 单子节论文 > 6 篇 → 二级切分（如 5.1 7 篇 → 5.1A 4 篇 + 5.1B 3 篇）
4. 总并发上限 5：超出时分两批，主 Claude 用 TodoWrite 跟踪进度

**β 时序**：

1. 同一条主消息内同时发起 K 个 `Agent(subagent_type="general-purpose")` 调用 paper_extractor
2. K 路全完 → 主 Claude 顺序派 K 个 extract_reviewer
3. reviewer 写入 `<workdir>/_reviews/group_<group_id>_review.md`

**FAIL 处理**：仅重派失败那一路，γ 修复 + 重试 ≤2

## 阶段 3：报告骨架

**目标**：合并所有 extracts → outline.md。

**步骤**：

1. 派发 `outline_writer` subagent（严格标题层级 + 第 5/7 章 fenced JSON block）
2. subagent 读所有 `_work/extracts/*.md` + `_work/pre_survey_notes.md` + `_work/survey_spec.md`
3. 主 Claude 用 `python -c "import json; ..."` dry run 验证所有 fenced JSON block（assemble_md.py 阶段 4 也会再次自检）
4. 派发 `outline_reviewer` 验证（结构合规 + 反幻觉抽样 + 引用对齐）
5. reviewer FAIL → γ 修复 + 重试 ≤2

## 阶段 4：md 组装

**目标**：把 outline.md 中间产物渲染为顶层 `<topic_slug>_综述报告.md`（含 LaTeX 公式）。

**步骤**：

1. 直接调用 skill 内置 python 脚本（**不复制到工作目录** — 满足顶层只 *.pdf + 综述报告.md 约束）：
   ```bash
   python <skill-path>/assets/assemble_md.py <workdir>
   ```
   `<skill-path>` 表示本 skill 的安装目录（即包含本 SKILL.md 的目录）的绝对路径，由主 Claude 在运行时解析（不要硬编码到具体用户机器路径）。
2. 输出：
   - 顶层 `<workdir>/<topic_slug>_综述报告.md`
   - stdout JSON: `{"status": "ok", "path": "...", "size_bytes": ..., "cn_chars": ..., "papers": ..., "refs": ...}`
3. **dry-run 自检**（脚本内置，失败 ≠ 0 退出）：
   - outline.md 全部 fenced JSON parse 成功
   - LaTeX `$` / `$$` 配对（行内偶数 + 行间偶数）
4. 失败处理：
   - JSON 解析错 → 主 Claude 直接 Edit `_work/outline.md` 修 JSON
   - LaTeX 配对错 → 主 Claude grep `\$` 数量 + 定位漏闭合
   - 不要修 assemble_md.py 副本（脚本不复制工作目录，统一改源即可）

## 阶段 5：完成度核查

**目标**：17 项核查全 PASS 才算完成。FAIL 上限 3 次。

**步骤**：

1. 派发 `validation_reviewer` subagent 跑反幻觉抽样（~49 处 verify_quotes_batch 并行 ≈ 2 秒）→ `<workdir>/_reviews/validation_review.md`
2. 主 Claude 跑 `python <skill-path>/assets/validation.py <workdir> --reviewer-report <workdir>/_reviews/validation_review.md`（`<skill-path>` 含义同阶段 4）
3. 综合写 `<workdir>/_reviews/validation_report.md`，列每项 PASS/FAIL
4. 任一 FAIL → γ 修复（按修复路径表分发）；3 轮仍 FAIL → 升级用户
5. 全部 PASS → Edit `_work/survey_spec.md` 当前阶段为 `5-completed`，向用户口头汇报

## 工作目录约定

```
{cwd}/<topic_slug>/
├── 2022_CoRL_R3M.pdf                # 顶层论文 PDF（命名规范，平铺）
├── 2022_arXiv_RT1.pdf
├── ...
├── <topic_slug>_综述报告.md         # 顶层最终交付（阶段 4 输出）
├── _pre/                            # 0b 预调研综述 PDF
│   └── 2025_arXiv_<survey>.pdf
├── _work/                           # 过程文件
│   ├── survey_spec.md               # 0c 输出
│   ├── pre_survey_notes.md          # 0b 输出
│   ├── outline.md                   # 3 输出（含 fenced JSON）
│   └── extracts/
│       ├── group_<group_id>_<paper_index>.md
│       └── _tmp_<group_id>_<paper_index>_full.md
└── _reviews/                        # reviewer 报告
    ├── spec_review.md               # 0c reviewer
    ├── paper_search_review.md       # 1 reviewer
    ├── group_<group_id>_review.md   # 2 reviewer
    ├── outline_review.md            # 3 reviewer
    ├── validation_review.md         # 5 reviewer
    ├── validation_report.md         # 5 综合报告
    ├── _validation_claims.json
    └── _validation_results.json
```

**关键约定**：

- 顶层只允许 `*.pdf`（论文）+ `<topic_slug>_综述报告.md`（最终交付）两类文件
- 其他所有过程产物归 `_pre/` `_work/` `_reviews/` 三个下划线前缀子目录
- `assemble_md.py` 与 `validation.py` 直接以 `<skill-path>/assets/...` 形式从 skill 安装目录调用，**不复制到工作目录**

## 集成 paper-search

paper-survey 通过 `paper-search` skill 完成所有检索/下载，详见 `references/paper_search_cheatsheet.md`。

CLI 模式（要求 `paper-search` 已在 PATH 中可用；安装方式见 paper-search skill 自身文档）：
```bash
paper-search <command> [args]
```

## 资源索引

- **assets/**：每次调用必用
  - `spec_template.md` / `naming_convention.md`
  - `assemble_md.py`（阶段 4 markdown 组装入口，标准库无依赖）
  - `pdf_extraction.py`（含 verify_quotes_batch 并行 CLI）
  - `validation.py`（17 项核查 + reviewer-report 参数 + 弹性字数档）
  - `subagent_prompts/`：**9 个** prompt 模板
    - `pre_survey_extractor.md` / `spec_writer.md` / `spec_reviewer.md`
    - `paper_search_reviewer.md` / `paper_extractor.md` / `extract_reviewer.md`
    - `outline_writer.md` / `outline_reviewer.md` / `validation_reviewer.md`
- **references/**：按需查询
  - `report_structure_11chapters.md`：11 章 markdown 渲染规范
  - `markdown_formula_convention.md`：**LaTeX 公式契约**（行内/行间分隔符 + 中文紧邻空格 + 强制级别）
  - `gb_t_7714_format.md`：参考文献格式
  - `paper_search_cheatsheet.md`：paper-search 命令速查
  - `field_extraction_schema.md`：字段抽取契约 + 阶段 5 抽样规则（含公式抽样）
  - `troubleshooting.md`：md 时代失败模式（LaTeX 配对 / fenced JSON / pipe table）

## 关键约束

1. **阶段间严格串行 / 阶段内 K 路并行**
2. **反幻觉契约 B + 抽样 C**：每字段附引文 `〔p.{页码}: "{≤30字}"〕`，未定位 → `N/A-源文本未覆盖`
3. **AskUserQuestion 阶段差异化**：
   - **0a 自由对话**：主 Claude 与用户直接对话收集主题/范围/目录，不强约束 AskUserQuestion 调用
   - **0b 严格**：综述检索 fuzzy < 80% / 多候选 / 0 命中 → 必问；批量上限 5 个 question/次
   - **0c 中等**：仅论文清单 arxiv_id 补全的关键歧义问；关键词扩展 / 章节顺序 / 命名细节不问
   - **1 严格**：每篇论文检索/下载/校验失败都问；批量合并（β）攒到一次问完
   - **2-5 不直接调**：subagent 内不许调 AskUserQuestion；FAIL 升级时由主 Claude 接管
4. **β 批量合并 AskUserQuestion**：歧义攒一次问完，不逐个打断
5. **完成度核查上限 3 次修复**，超过升级用户
6. **跨 session 重读 spec.md** 不依赖对话上下文，spec.md「当前阶段」字段为权威状态