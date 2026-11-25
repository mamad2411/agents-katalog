---
name: transfer-old-latex-to-new
description: 当用户明确要求“迁移 LaTeX 模板”“把旧项目接入 ChineseResearchLaTeX”“把旧标书/论文/毕业论文/简历套进当前模板”“把 Word/PDF/Markdown/零散 tex 整理进现有项目”，或直接提到 `transfer-old-latex-to-new` 时使用。旧别名 `migrating-latex-templates` 可兼容理解。该 skill 只负责把正文内容迁移到当前仓库现有模板的内容层；绝不能修改 `packages/` 内公共包源码、也绝不能修改 `projects/` 内模板样式或入口骨架，只能写入目标项目允许承载正文的内容文件。
metadata:
  author: Bensz Conan
---
# ChineseResearchLaTeX 内容迁移技能

### 输入原则

不要要求用户先整理成固定输入协议。默认接受并消化任意合理输入，例如：

- 一个完整旧项目目录
- 若干 `.tex` / `.bib` / `.docx` / `.md` / `.txt`
- PDF、截图、图片
- 一份已有模板项目路径，加上一些迁移目标说明
- 多种输入混合出现

如果材料不完整，不要先追问“标准输入”；先判断目标产品线、合适承载项目、哪些内容能直接落入 `extraTex/*.tex` 或 `references/*.bib`，以及哪些诉求已经超出内容迁移边界。只有缺失信息会导致把正文放错位置时，才请求补充。

### 输出原则

不要把输出理解成“任意重构仓库”。本 skill 的有效输出通常只有：

- 把正文迁移到目标项目的 `extraTex/*.tex`
- 把参考文献迁移到目标项目的 `references/*.bib`
- 生成必要的迁移说明、风险提示、未落位清单
- 在构建成功后给出验证结果

以下动作都超出本 skill 的边界：模板源码改动、样式修复、wrapper / `main.tex` / `template.json` / README 的结构重写，以及公共包抽取或包级能力沉淀。默认把用户原始材料视为只读，目标模板视为只读骨架；样式差异只报告，不偷改。

### Legacy CLI 的定位

`scripts/run.py`、`scripts/migrate.sh` 仍然保留，但只作为经典 old/new 目录迁移的后备入口。即使使用 legacy CLI，也必须继续遵守本文件的硬性边界：旧项目可以读，新项目只能写内容层，不能借 CLI 绕过模板保护。

### 不适用场景

以下场景不要继续使用本 skill 直接落地：

- 用户要“做一个新模板”
- 用户要“把旧样式 1:1 复刻到当前仓库”
- 用户要改 `packages/bensz-*`、`projects/*` 里的模板入口或样式文件
- 用户要新增模板承载位点、封面结构、目录结构、profile、class、style

这些都应转交模板开发链路。

## 流程

### 输入

按用户请求和配置文件提供必要输入；缺失信息应明确列出并停止依赖该输入的步骤。

### 执行步骤

这个 skill 仍然要识别目标产品线，但目的只是选对承载项目，而不是判断“该不该改 `packages/`”。

- NSFC：选择合适的 `projects/NSFC_*`
- SCI 论文：选择 `projects/paper-sci-01/`
- 毕业论文：选择最接近的 `projects/thesis-*`
- 简历：选择 `projects/cv-01/`

然后把旧材料中的正文内容映射到这些现成项目的内容文件里；默认优先选择最接近的现有项目，而不是新建或重组模板结构。

### 识别目标产品线与承载项目

先回答三个问题：用户最终要落到哪条产品线、当前仓库哪个现有项目最适合作为承载容器、这次任务是“内容迁移”还是已经变成“模板开发”。如果已经变成模板开发，立即转交，不要继续伪装成内容迁移任务。

### 清点可迁移内容

从输入中提炼可直接复用的正文段落、BibTeX、需要人工确认的缺口，以及会触发模板改动需求的超界诉求。

### 做内容层映射

只在内容层做映射：

- 旧正文 → `extraTex/*.tex`
- 旧参考文献 → `references/*.bib`

不要把“映射”理解成：

- 改章节命令
- 改模板标题样式
- 改目录/封面/页眉页脚
- 改公共包接口

### 执行迁移

执行时只允许覆盖目标内容文件、新建目标内容文件（若模板已有对应承载位点）、以及写入或补齐 `.bib`。

如果某项需求必须改模板骨架才能完成，不要继续自动修改；应明确标出受阻位置和原因，并建议改用 `make-latex-model`。

### 官方入口验证

迁移完成后，尽量用对应产品线的官方入口验证：

- NSFC：`python packages/bensz-nsfc/scripts/nsfc_project_tool.py build --project-dir <项目路径>`
- SCI：`python packages/bensz-paper/scripts/paper_project_tool.py build --project-dir <项目路径>`
- Thesis：`python packages/bensz-thesis/scripts/thesis_project_tool.py build --project-dir <项目路径>`
- CV：`python packages/bensz-cv/scripts/cv_project_tool.py build --project-dir <项目路径> --variant all`

如果构建失败且原因来自模板骨架缺口，不要私自修模板；应如实报告。

优先阅读本文件。需要 legacy CLI 细节时，再查看：

- `scripts/README.md`
- `references/quickstart.md`
- `references/config_guide.md`
- `references/api_reference.md`

确认边界时，始终优先遵循：

- 只迁移内容，不改模板骨架
- 样式差异只报告，不偷改

### 输出

输出 Skill description 所承诺的交付物，并明确格式、路径和失败返回形式。

### 输出管理

本 Skill 的新任务中间文件统一写入 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/{skill名}/input|output|log/`。同一任务复用一个任务根目录；多 Skill 协作才创建 `shared/`。正式交付物不写入该目录，历史隐藏目录只允许显式兼容读取、迁移或清理。

这个 skill 只做一件事：把旧材料里的正文、参考文献等内容，迁移到 **当前仓库已有模板项目** 的内容层。

它不是模板开发 skill，也不是公共包重构 skill。凡是要改模板源码、样式、`packages/bensz-*`、`projects/*` 内骨架文件、`main.tex`、`@config.tex`、`.cls`、`.sty`、profile、style 或构建脚本的任务，都应转给 `make-latex-model` 或对应产品线的模板开发流程。

### 校验

完成后执行 Skill 已有的静态检查、脚本验证或人工复核，并记录通过标准。

### 失败与恢复

保留错误证据和已完成产物；仅在输入、环境或外部依赖恢复后从最近的失败步骤重试。

## 约束

处理任务时必须始终遵守：

- 绝不能修改 `packages/` 下任何公共包源码、模板实现、profile、style、脚本或共享资源
- 绝不能修改 `projects/` 下任何模板样式、入口骨架、wrapper、`main.tex`、`extraTex/@config.tex`、`.cls`、`.sty`、Lua/Python 构建脚本
- 只能把内容放到目标项目已有的内容层位置
- 如果现有模板没有合适承载位点，不能为了容纳内容去改模板；应明确报告“模板位点不足，需要模板开发 skill 介入”

当前仓库里默认可写的内容层只有 `extraTex/**/*.tex`（排除 `extraTex/@config.tex`）和 `references/**/*.bib`。

除非未来该 skill 的配置白名单明确放开，否则其它路径一律视为只读。

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
