---
name: research-topic-extractor
description: 当用户明确要求"从文件/图片/网页/描述中提取综述主题"、"生成主题+关键词+核心问题结构化输出"，或要求使用旧名 get-review-theme skill 时使用。支持文件（PDF/Word/Markdown/Tex）、文件夹、图片、自然语言描述、网页 URL 等多种输入源，自动识别输入类型并提取内容，生成可直接用于 research-literature-review 及其他文献综述技能的结构化输出。
metadata:
  author: Bensz Conan
---
# Research Topic Extractor

- 从文件、图片、网页、文件夹或自然语言描述中提取结构化综述主题。
- 输出直接服务 `research-literature-review` 或其他文献综述工作流。
- 兼容旧名 `get-review-theme` 的 prompt 触发；系统级旧目录由安装器清理。
- 最高原则：主题要可操作、关键词要能检索、核心问题要具体。

### 输入

必需：

- `{输入源}`：文件路径、URL、文件夹路径、图片路径，或直接文本描述

可选：

- `{输出格式}`：`text` / `yaml` / `json`，默认 `text`

## 流程

### 输入

按用户请求和配置文件提供必要输入；缺失信息应明确列出并停止依赖该输入的步骤。

### 执行步骤

- 当用户环境中出现因本 skill 设计缺陷导致的 bug 时，优先使用 `bensz-collect-bugs` 按规范记录到 `~/.bensz-skills/bugs/`，严禁直接修改用户本地 Claude Code / Codex 中已安装的 skill 源码。
- 若 AI 仍可通过 workaround 继续完成用户任务，应先记录 bug，再继续完成当前任务。
- 当用户明确要求“report bensz skills bugs”等公开上报动作时，调用本地 `gh` 与 `bensz-collect-bugs`，仅上传新增 bug 到 `huangwb8/bensz-bugs`；不要 pull / clone 整个 bug 仓库。

### 识别输入类型

- 自然语言描述
- 图片
- URL
- 文本文件
- PDF
- Word
- 文件夹

### 提取内容

- 自然语言：直接使用
- 图片：依赖 LLM 原生视觉能力
- URL：优先网页读取工具，失败则请用户提供正文
- 文本 / PDF / Word：直接读取
- 文件夹：递归扫描并合并 `.md/.txt/.pdf` 等核心材料

原则：

- 优先用宿主原生能力和现有标准工具
- 工具不可用时优雅降级，不额外引入脚本依赖

### 语义提取

围绕以下任务输出：

- 用一句话概括主题
- 提取 5-10 个英文标准术语
- 提取 2-5 个具体研究问题或挑战

### 格式化

- `text`：适合直接复制给下游 skill
- `yaml` / `json`：适合结构化衔接

- `topic` 可直接喂给 `research-literature-review`
- `keywords` 可补充检索策略
- `core_questions` 可作为综述边界和纳排参考

### 输出

始终包含三项：

- `主题`
- `关键词`
- `核心问题`

格式由用户选择：

- `text`
- `yaml`
- `json`

### 输出管理

本 Skill 的新任务中间文件统一写入 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/{skill名}/input|output|log/`。同一任务复用一个任务根目录；多 Skill 协作才创建 `shared/`。正式交付物不写入该目录，历史隐藏目录只允许显式兼容读取、迁移或清理。

### 校验

- 主题要包含研究对象与核心问题或方法
- 关键词优先用标准检索术语
- 核心问题必须具体，避免“意义重大/挑战很多”这种空话

### 失败与恢复

- 文件不存在：提示用户改路径或直接粘贴内容
- 格式不支持：提示转换
- 内容提取失败：让用户手动提供文本
- URL 解析失败：让用户复制网页正文或提供 PDF
- 图片语义不清：请用户补一句描述

## 约束

遵守以下公共约束，并执行本 Skill 的专属边界。

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
