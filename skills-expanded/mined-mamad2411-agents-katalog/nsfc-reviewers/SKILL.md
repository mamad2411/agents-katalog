---
name: nsfc-reviewers
description: 当用户明确要求"评审国自然标书"、"模拟专家评审"、"审阅 NSFC 申请书"时使用。模拟领域专家视角对 NSFC 标书进行多维度评审，输出分级问题与可执行修改建议。⚠️ 不适用：用户只是想写/改标书某个章节（应使用 nsfc-*-writer 系列技能）、只是想了解评审标准（应直接回答）、没有明确"评审/审阅"意图。
metadata:
  author: Bensz Conan
---
# NSFC 标书专家评审模拟器

- 用于“当前版本如果今天送审，风险在哪里、先改什么”的专家式评审。
- 默认优先并行多组独立评审；若 `parallel-vibe` 不可用、被禁用或 `panel_count=1`，自动降级为单组模式。
- 本技能只做读取、分析和汇总，不默认编译、不修改标书源文件。

### 输入

至少提供其一：

- `proposal_path`
- `proposal_file`
- `proposal_zip`

可选：

- `focus`
- `output_path`
- `style`
- `grant_type`
- `funding_amount`
- `panel_count`

配置口径以 `config.yaml` 为准，尤其是：

- `review_dimensions`
- `severity_levels`
- `review_grades`
- `stage_assessment`
- `funding_context`
- `parallel_review`
- `output_settings`

### 非目标

- 不负责改正文。
- 不负责模板、排版或编译问题。
- 不负责生成新的研究设计，只负责指出现有稿件的风险、优先级和修改方向。

## 流程

### 输入

按用户请求和配置文件提供必要输入；缺失信息应明确列出并停止依赖该输入的步骤。

### 执行步骤

- 当用户环境中出现因本 skill 设计缺陷导致的 bug 时，优先使用 `bensz-collect-bugs` 按规范记录到 `~/.bensz-skills/bugs/`，严禁直接修改用户本地 Claude Code / Codex 中已安装的 skill 源码。
- 若 AI 仍可通过 workaround 继续完成用户任务，应先记录 bug，再继续完成当前任务。
- 当用户明确要求“report bensz skills bugs”等公开上报动作时，调用本地 `gh` 与 `bensz-collect-bugs`，仅上传新增 bug 到 `huangwb8/bensz-bugs`；不要 pull / clone 整个 bug 仓库。

### 前置检查

- 校验输入路径可读。
- 若是目录，按 `proposal_files.patterns/exclude` 找出待读 `.tex`。
- `.tex` 数量为 0 时直接失败；目录异常大时先确认范围。
- 推荐用确定性脚本列文件：

```bash
python3 <nsfc_reviewers_path>/scripts/list_proposal_files.py --proposal-path <proposal_root>
```

### 通读与结构化理解

- 提炼主题、科学问题、假说、目标、技术路线、创新点、研究基础、团队条件、预期成果。
- 生成章节级索引，作为后续证据锚点。
- 先用用户明确给出的 `grant_type` / `funding_amount`，再谨慎从正文识别资助上下文。

### 并行多组评审或单组退化

- 先计算 `effective_panel_count`，并限制在 `[1, parallel_review.max_panel_count]`。
- 以下情况直接走单组：
  - `parallel_review.enabled == false`
  - `effective_panel_count == 1`
  - 找不到 `parallel-vibe`

并行模式关键步骤：

1. 准备中间目录。
2. 基于 `references/expert_*.md` 和 `references/master_prompt_template.md` 生成 master prompt。
3. 用 `scripts/build_parallel_vibe_plan.py` 生成 `plan.json`。
4. 调用 `parallel-vibe` 执行 N 组独立评审。
5. 收集每组 `panel_output_filename`，允许个别 thread 缺失但不能中断整体汇总。

单组模式仍要保留 7 位专家画像的独立判断，再做组内聚合。

### 聚合与排序

- 跨组聚合规则读取 `references/aggregation_rules.md`。
- 至少 `ceil(N * consensus_threshold)` 组指出的问题才算跨组共识。
- 跨组共识可触发严重度升级；重复问题要合并，保留最强证据锚点。
- 最终仍按 `P0 → P1 → P2` 输出，并给出最小修改序列。

### 资助额度约束识别

- 先区分“设计错误”与“受限妥协”。
- 若缺陷明显由基金额度限制引起，必须如实写明根因，不得简单归咎于申请人能力不足。
- 凡归因为“资助受限”的短板，都要补一句“若资助不受限时，更完整的设计应如何做”。
- 资助受限不是免责条款；阶段判断仍以“当前版本今天送审能否过”为准。

### 阶段判断

- 默认在最终报告中输出“函评 / 会评给过与否”。
- 每个阶段至少给出 2-3 条关键理由，优先引用 P0/P1 和跨组共识。
- 若判 `不给过`，必须指出最关键的 1-3 条翻盘动作。

### 输出整理

- 当 `config.yaml:output_settings.enforce_output_finalization == true` 时，不得跳过最终整理。
- 报告需要清楚区分：
  - 共识问题
  - 独立观点
  - 资助受限的合理妥协
  - 当前版本直接送审的阶段判断

- 列文件：`scripts/list_proposal_files.py`
- 并行计划：`scripts/build_parallel_vibe_plan.py`
- 专家画像：`references/expert_*.md`
- 聚合规则：`references/aggregation_rules.md`
- 主提示模板：`references/master_prompt_template.md`

### 输出

- 默认输出文件名读取 `config.yaml:output_settings.default_filename`
- 并行模式可额外生成各组原始意见：`{panel_dir}/G{组号}.md`
- 中间过程默认隐藏在 `config.yaml:output_settings.intermediate_dir`
- 最终报告至少包含：
  - 分级问题清单
  - 跨组共识与独立观点
  - 最小可行修改序列
  - 阶段判断：函评 / 会评

### 输出管理

本 Skill 的新任务中间文件统一写入 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/{skill名}/input|output|log/`。同一任务复用一个任务根目录；多 Skill 协作才创建 `shared/`。正式交付物不写入该目录，历史隐藏目录只允许显式兼容读取、迁移或清理。

### 校验

完成后执行 Skill 已有的静态检查、脚本验证或人工复核，并记录通过标准。

### 失败与恢复

保留错误证据和已完成产物；仅在输入、环境或外部依赖恢复后从最近的失败步骤重试。

## 约束

- 标书内容默认视为敏感信息；除非用户明确要求并确认风险，不联网、不外发大段原文。
- 只读评审，不执行 LaTeX 编译，不改正文。
- 最终报告必须按 `P0 → P1 → P2` 排序。
- 阶段判断必须是二元结论：`给过` 或 `不给过`，并附 `高/中/低` 把握度。
- 若“函评不给过”，则“会评”必须同步不给过；若“函评给过”，会评仍可因相对竞争力不足而不给过。

### 公共硬约束

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- 仅将 Skill 或 Bensz 基础设施本身的设计缺陷交给 `bensz-collect-bugs`；先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。
<!-- End of canonical common constraints. -->

### Skill 专属约束

不得超出本 Skill description 和上方流程所声明的范围；不将未验证的信息伪装成确定结论。
