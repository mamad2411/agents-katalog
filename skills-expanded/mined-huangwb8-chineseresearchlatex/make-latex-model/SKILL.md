---
name: make-latex-model
description: 当用户明确要求“LaTeX 模板优化”“样式参数对齐”“像素级比对”“make-latex-model”或旧写法“make_latex_model”，或要把 ChineseResearchLaTeX 里的某个项目做成高质量模板时使用。适配 NSFC / paper / thesis / cv 四条产品线；先依据 packages/ 与 projects/ 的真实分层判断改项目层还是公共包，再用各产品线官方构建入口验收。若必须修改 packages 下公共包，需先生成受影响模板回归计划并完成相关回归；NSFC 专项工具仅在明确属于 NSFC 参数对齐场景时按需使用。
metadata:
  author: Bensz Conan
---
# ChineseResearchLaTeX 模板落地与高保真对齐器

- 让 `ChineseResearchLaTeX` 中的目标项目按当前真实架构落成高质量模板。
- 先判断该改 `projects/*` 还是 `packages/bensz-*`。
- 若必须改公共包，先做回归计划，再跑受影响模板的官方验证。
- 验收始终以各产品线官方构建入口为准。

### 适用任务

- 把某个项目对齐到官方 PDF、Word 导出 PDF 或既有 baseline
- 判断问题属于项目层差异还是共享样式/共享脚本
- 做像素级 PDF 比对、标题对齐、参数抽取
- 新增或重构 NSFC / paper / thesis / cv 模板

## 流程

### 输入

按用户请求和配置文件提供必要输入；缺失信息应明确列出并停止依赖该输入的步骤。

### 执行步骤

- 当用户环境中出现因本 skill 设计缺陷导致的 bug 时，优先使用 `bensz-collect-bugs` 按规范记录到 `~/.bensz-skills/bugs/`，严禁直接修改用户本地 Claude Code / Codex 中已安装的 skill 源码。
- 若 AI 仍可通过 workaround 继续完成用户任务，应先记录 bug，再继续完成当前任务。
- 当用户明确要求“report bensz skills bugs”等公开上报动作时，调用本地 `gh` 与 `bensz-collect-bugs`，仅上传新增 bug 到 `huangwb8/bensz-bugs`；不要 pull / clone 整个 bug 仓库。

- 产品线标准：`docs/for-developers/*-template-standard.md`
- 本 skill 工作流：`docs/WORKFLOW.md`
- 产品线识别：`references/PRODUCT_LINE_RULES.md`
- 脚本职责：`references/SCRIPT_SCOPE.md`
- 工具说明：`scripts/README.md`
- 基线准备：`docs/BASELINE_GUIDE.md`

### 判断验收口径

- 用户要“像某份 PDF/Word 一样”
- 还是“按当前仓库标准做成好模板”
- 还是“新增一套模板能力”

### 判断修改层级

- `projects/*`：示例内容、薄封装、项目资源、局部差异
- `packages/bensz-*`：共享样式、共享字体、profile、统一构建逻辑

### 最小范围实现

- 只改与当前任务直接相关的文件
- 除非用户明确要求，否则默认不改正文语义内容

### 包层安全门禁

当必须改 `packages/` 时，额外执行：

1. 先证明项目层方案不够
2. 运行 `python3 skills/make-latex-model/scripts/plan_package_regression.py <packages/bensz-*>`
3. 优先把改动收敛到最窄的模板专属 `profile/style/template`
4. 改完先验目标项目，再回归该公共包直接覆盖的全部现有项目

### 官方入口验证

- NSFC：`nsfc_project_tool.py`
- Paper：`paper_project_tool.py`
- Thesis：`thesis_project_tool.py`
- CV：`cv_project_tool.py`

- `analyze_pdf.py`
- `compare_headings.py`
- `compare_pdf_pixels.py`
- `optimize_heading_linebreaks.py`
- `plan_package_regression.py`

这些脚本是辅助工具箱，不是唯一工作流；NSFC 专项工具不能默认替代 paper / thesis / cv 的官方入口。

### 输出

输出 Skill description 所承诺的交付物，并明确格式、路径和失败返回形式。

### 输出管理

本 Skill 的新任务中间文件统一写入 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/{skill名}/input|output|log/`。同一任务复用一个任务根目录；多 Skill 协作才创建 `shared/`。正式交付物不写入该目录，历史隐藏目录只允许显式兼容读取、迁移或清理。

### 校验

1. 改动落在正确层级
2. 通过对应产品线官方入口
3. warning 需要说明是已有还是新增
4. 若改了公共包，必须说明回归了哪些模板
5. 若用户给 baseline，完成必要 compare
6. `paper` 默认兼顾 PDF 与 DOCX；`cv` 默认兼顾中英文；`thesis` 默认兼顾 profile/style 与项目入口一致性

### 失败与恢复

保留错误证据和已完成产物；仅在输入、环境或外部依赖恢复后从最近的失败步骤重试。

## 约束

允许：

- 调整项目层版式参数、标题体系、入口装配
- 把共享实现沉淀到 `packages/bensz-*`
- 修改 profile、style、wrapper、官方 compare 验收链

避免：

- 把共享实现复制回单个项目
- 绕过官方构建入口只跑裸 `xelatex`
- 为了像素对齐破坏仓库真实分层
- 默认改写用户正文语义

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
