---
name: research-citation-check
description: 当用户明确要求"核查/优化综述 `{主题}_review.tex` 的正文引用"、"运行 research-citation-check"，或要求使用旧名 check-review-alignment skill 时使用。通过宿主 AI 的语义理解逐条核查引用是否与文献内容吻合，只在发现致命性引用错误时对"包含引用的句子"做最小化改写，并优先复用 `research-literature-review` 的渲染脚本输出 PDF/Word，过渡期允许 fallback 到旧名 systematic-literature-review。核心原则：不为了改而改，无法确定是否为致命性错误时保留原样并在报告中警告。⚠️ 不适用：用户只是想生成系统综述正文（应使用 research-literature-review）；用户只是想新增/核对 BibTeX 条目（应使用专门的 bib 管理流程）。
metadata:
  author: Bensz Conan
---
# Research Citation Check

- 用于检查已有 `{主题}_review.tex` 的正文引用是否真的与对应论文内容一致。
- 只在确认存在致命错误时最小化改写“包含该引用的句子”。
- 渲染 PDF/Word 优先依赖 `research-literature-review`；准备结构化输入不依赖该 skill。
- 兼容旧名 `check-review-alignment` 的 prompt 触发；`.check-review-alignment/` 仍是稳定历史工作区名。

### 输入

- `work_dir`：包含 `*_review.tex` 与 `.bib`
- 可选 `--tex`：指定 tex 文件名

### 核心原则

- 不为了改而改
- 无法确认时不动
- 只改必要句子
- 保留所有 LaTeX 命令结构

## 流程

### 输入

按用户请求和配置文件提供必要输入；缺失信息应明确列出并停止依赖该输入的步骤。

### 执行步骤

- 当用户环境中出现因本 skill 设计缺陷导致的 bug 时，优先使用 `bensz-collect-bugs` 按规范记录到 `~/.bensz-skills/bugs/`，严禁直接修改用户本地 Claude Code / Codex 中已安装的 skill 源码。
- 若 AI 仍可通过 workaround 继续完成用户任务，应先记录 bug，再继续完成当前任务。
- 当用户明确要求“report bensz skills bugs”等公开上报动作时，调用本地 `gh` 与 `bensz-collect-bugs`，仅上传新增 bug 到 `huangwb8/bensz-bugs`；不要 pull / clone 整个 bug 仓库。

### 依赖检查

- 只有执行渲染时才强制检查 `research-literature-review`，过渡期可 fallback 到 `systematic-literature-review`
- 若只是 `--prepare`，不要求渲染依赖可用

### 预检与定位

- 找到 `*_review.tex` 与对应 `.bib`
- 缺任何核心文件时立即停止

### 结构化上下文抽取

```bash
cd /path/to/research-citation-check
python3 scripts/run_ai_alignment.py --work-dir "/path/to/work_dir" --prepare
```

- 生成 `ai_alignment_input.json`
- 输入中至少包含：句子、bibkey、文献元信息、DOI/URL、PDF 摘要段或 BibTeX 摘要

### AI 语义核查

- 证据优先级：PDF 摘要段 > BibTeX abstract/title > 仅从句子推断
- 每条引用都要判断是否为：
  - `fake_citation`
  - `wrong_citation`
  - `contradictory_citation`
  - `weak_support`
  - `overclaim`
  - `style_issue`
- 无法确认时保持原样，并记录到 Warnings

### 报告

- 报告至少包含：
  - Summary
  - 具体细节
  - Critical Fixes (P0)
  - Warnings (P1)
  - Rendering Result
- 每条引用的细节至少包含：标题、DOI、原句、文献实际内容、合理性评估、问题级别

### 渲染

```bash
cd /path/to/research-citation-check
python3 scripts/run_ai_alignment.py --work-dir "/path/to/work_dir" --render
```

### 输出

- `{work_dir}/.check-review-alignment/ai_alignment_report.md`
- `{work_dir}/.check-review-alignment/ai_alignment_input.json`
- 修改后的 `{主题}_review.tex`
- 新生成的 `{主题}_review.pdf`
- 新生成的 `{主题}_review.docx`

### 输出管理

本 Skill 的新任务中间文件统一写入 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/{skill名}/input|output|log/`。同一任务复用一个任务根目录；多 Skill 协作才创建 `shared/`。正式交付物不写入该目录，历史隐藏目录只允许显式兼容读取、迁移或清理。

### 校验

- 配置见 `config.yaml`
- 脚本入口：`scripts/run_ai_alignment.py`
- 渲染依赖：`research-literature-review`（fallback：`systematic-literature-review`）

### 失败与恢复

保留错误证据和已完成产物；仅在输入、环境或外部依赖恢复后从最近的失败步骤重试。

## 约束

- P0：必须修，允许最小改写或修正错误 bibkey
- P1：仅警告，不改写
- P2：完全跳过
- 禁止：
  - 改写未包含引用的句子
  - 整段重写
  - 引入新 bibkey（除非修复错误 key）
  - 伪造论文内容

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
