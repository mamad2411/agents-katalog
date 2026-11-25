---
name: complete-example
description: 当用户明确要求"填充示例内容""生成示例""补充 LaTeX 示例"时使用。AI 增强版 LaTeX 示例智能生成器，实现 AI 与硬编码的有机融合：AI 做"语义理解"（分析章节主题、推理资源相关性、生成连贯叙述），硬编码做"结构保护"（格式验证、哈希校验、访问控制）。
metadata:
  author: Bensz Conan
---
# complete-example Skill

- 用于给现有 LaTeX 项目补“示例内容”，不是写真实科研结论。
- AI 负责语义理解、资源关联和叙事生成；硬编码负责文件扫描、结构保护、格式验证和备份。
- 重点是“生成得像一个完整示例”，同时不破坏模板骨架和系统文件。

### 输入

必需：

- `project`：项目名称或路径。

常用可选参数：

- `content_density`：`minimal` / `moderate` / `comprehensive`
- `output_mode`：`preview` / `apply` / `report`
- `target_files`：默认自动检测 `extraTex/*.tex`
- `narrative_hint`：指导示例叙事方向，但仍属于“示例场景”

默认值与细节统一读取 `config.yaml`。

### 适用与不适用

- 适用：需要为 NSFC / thesis / paper 等项目补示例章节、示例表格、示例图文叙事。
- 不适用：真实科研写作、模板修复、结构性重构、修改系统配置文件。

## 流程

### 输入

按用户请求和配置文件提供必要输入；缺失信息应明确列出并停止依赖该输入的步骤。

### 执行步骤

- 当用户环境中出现因本 skill 设计缺陷导致的 bug 时，优先使用 `bensz-collect-bugs` 按规范记录到 `~/.bensz-skills/bugs/`，严禁直接修改用户本地 Claude Code / Codex 中已安装的 skill 源码。
- 若 AI 仍可通过 workaround 继续完成用户任务，应先记录 bug，再继续完成当前任务。
- 当用户明确要求“report bensz skills bugs”等公开上报动作时，调用本地 `gh` 与 `bensz-collect-bugs`，仅上传新增 bug 到 `huangwb8/bensz-bugs`；不要 pull / clone 整个 bug 仓库。

1. 扫描项目中的 figures、code、references 等资源。
2. AI 分析章节主题、关键概念、语气和上下文。
3. AI 推理资源与章节的相关性，并决定内容类型组合。
4. 生成连贯的示例叙述，可参考 `narrative_hint`。
5. 用硬编码模板包装成合法 LaTeX。
6. 自检并优化生成内容。
7. 执行格式与结构验证，需要时生成质量报告。

- AI：语义分析、资源选择、文本生成、自我优化。
- 硬编码：文件扫描、Top-K 选择、LaTeX 包装、格式保护、备份、日志、结构校验。

重点关注 `config.yaml` 中的：

- `parameters.*`
- `run_management.*`
- `scan.*`
- `generation.*`
- `generation.section_hierarchy.*`
- `generation.templates.*`

### 输出

- 所有运行产物写入 `{project_path}/.complete_example/<run_id>/`
- 典型结构：
  - `backups/`
  - `logs/`
  - `analysis/`
  - `output/`
  - `metadata.json`
- `output_mode=apply` 时才写回项目；其它模式只给预览或报告。

### 输出管理

本 Skill 的新任务中间文件统一写入 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/{skill名}/input|output|log/`。同一任务复用一个任务根目录；多 Skill 协作才创建 `shared/`。正式交付物不写入该目录，历史隐藏目录只允许显式兼容读取、迁移或清理。

### 校验

完成后执行 Skill 已有的静态检查、脚本验证或人工复核，并记录通过标准。

### 失败与恢复

保留错误证据和已完成产物；仅在输入、环境或外部依赖恢复后从最近的失败步骤重试。

## 约束

- 禁止修改系统文件：`main.tex`、`extraTex/@config.tex`、`@config.tex`
- 黑名单文件要做访问控制与哈希校验；若检测到非法修改尝试，必须拒绝。
- `main.tex` 只允许 `\section` / `\subsection`；输入类 `extraTex/*.tex` 只允许 `\subsubsection` / `\subsubsubsection`
- 生成内容必须保持“示例”属性，不伪装成真实实验或真实数据来源。

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
