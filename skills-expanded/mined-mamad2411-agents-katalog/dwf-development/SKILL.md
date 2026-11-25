---
name: dwf-development
description: "当用户需要单独执行 DWF 工作流的需求分析、技术方案或实现清单阶段之一时必须使用本技能。它按当前 `current_step` 或用户确认的目标阶段，只生成目标 spec 目录下对应的一个阶段文档，并请求用户确认后停止。适用于“需求拆解”“技术方案”“实现清单”“生成技术方案”“创建实现清单”“抽离某个开发阶段”等场景。可独立运行，也可作为 dwf-orchestrator 编排的工作流的一部分（state.json 中存在 `status: active` 且 `current_step` 为 `breakdown`/`plans`/`todos` 的 spec 时进入工作流模式）。"
---

# dwf-development

本技能用于执行 DWF 的需求分析、技术方案或实现清单阶段，但每次调用只处理一个阶段。它不启动完整开发工作流，不连续生成多个阶段文档。

<HARD-GATE>
以下规则不可违反：

1. **每次只处理当前阶段。**
   工作流模式下，以 active spec 的 `current_step` 为唯一入口：`breakdown` 只写 `03-需求分析/需求分析文档.md`，`plans` 只写 `04-技术方案/技术方案.md`，`todos` 只写 `05-实现清单/实现清单.md`。独立模式下，以用户确认的目标阶段为入口。不得在一次调用中连续生成多个阶段文档。

2. **目标 spec 目录由运行模式决定，不由本技能臆造。**
   - 工作流模式：读取 `.dwf/state.json`，在 `specs` 数组中找 `status: "active"` 且 `current_step` 为 `breakdown`/`plans`/`todos` 之一的 spec，以 `.dwf/specs/{spec.name}` 作为目标 spec 目录。若该 spec 的 `shared_ref` 非空（兄弟 spec），优先读取 `.dwf/specs/{shared_ref}/01-需求/`、`/02-设计稿/` 作为只读参考上下文。
    - 独立模式：`.dwf/state.json` 不存在或不存在满足条件的 active spec。先根据用户输入判断目标阶段；不明确时用 `question` 询问目标阶段。再用 `question` 询问用户目标目录，默认提议 `.dwf/specs/{今日日期}-{seq}-feat-{描述}`，其中 `seq` 扫描 `.dwf/specs/` 现有 spec 目录名中的最大序号 +1（无则 001），由用户确认或修改。

3. **不要创建完整工作流目录。**
   只创建或更新当前阶段对应的目录和文档。不要主动创建 `01-需求/`、`02-设计稿/` 或其它非当前阶段目录。不要修改已有需求文档或设计稿。项目代码目录由 dwf-coding/用户决定，本技能不创建。

4. **确认前不要覆盖已有文档。**
   如果目标 spec 目录下目标文件已存在，先读取并告知用户已有文档，询问是保留、修改还是替换。用户确认前不要覆盖。

5. **全程使用中文。**
   除非用户明确要求使用其他语言，所有与用户的交互、技能说明、生成的文档、测试记录、审计结论和产物说明都必须使用中文。代码、文件路径、命令、API 名、技术术语、第三方库名和用户提供的原文内容可以保留英文。

6. **独立模式下不要创建或推进 `.dwf/state.json`。**
   独立模式只写目标 spec 目录下当前阶段文档与该 spec 的 `_meta.json`（如本技能创建该 spec）。不要推进完整工作流。只有工作流模式下才在用户确认后更新 state.json 中该 spec 的 `current_step`。

</HARD-GATE>

## 触发后流程

### 1. 探查上下文

- 检查 `.dwf/state.json` 是否存在，确定运行模式（见步骤 2）。
- 读取需求与设计依据：目标 spec 目录下的 `01-需求/需求文档.md`、`02-设计稿/设计稿.md`；工作流模式下若该 spec 的 `shared_ref` 非空，优先读取 `.dwf/specs/{shared_ref}/01-需求/`、`/02-设计稿/` 作为只读参考上下文。
- 检查当前阶段目标文件是否已存在。

### 2. 判断运行模式与目标 spec 目录

读取 `.dwf/state.json`：

- **独立模式**：`.dwf/state.json` 不存在或不存在 `current_step` 为 `breakdown`/`plans`/`todos` 的 active spec。
  - 先从用户输入判断目标阶段：需求拆解/需求分析对应 `breakdown`，技术方案对应 `plans`，实现清单对应 `todos`；无法判断时用 `question` 让用户选择一个目标阶段。
  - 用 `question` 询问用户目标 spec 目录，默认提议 `.dwf/specs/{今日日期}-{seq}-feat-{描述}`（`seq` 扫描 `.dwf/specs/` 现有 spec 目录名中的最大序号 +1，无则 001），由用户确认或修改。
  - 如目标 spec 目录不存在，只创建它及目标阶段对应的子目录：`breakdown` 创建 `03-需求分析/`，`plans` 创建 `04-技术方案/`，`todos` 创建 `05-实现清单/`。
  - 在该 spec 目录下写一份初始 `_meta.json`（`name` 为目录名、`status: "active"`、`current_step` 为目标阶段、`is_shared_context: false`、`shared_ref: null` 等）。
  - 不创建 `.dwf/state.json`，不推进完整工作流。
  - 当前阶段完成后请求用户确认，确认后停止。

- **工作流模式**：在 `specs` 数组中找到 `status: "active"` 且 `current_step` 为 `breakdown`/`plans`/`todos` 之一的 spec。目标 spec 目录为 `.dwf/specs/{spec.name}/`。
  - 只执行该 spec 当前 `current_step` 对应的阶段。阶段完成后更新该 spec 的 `current_step`、`confirmed_stages`、`selected_plan`（plans 阶段），同步 `_meta.json` 与顶层 `updated_at`，然后停止。
  - 遵循 dwf-orchestrator 的确认机制。

### 3. 生成需求分析文档

**进入条件**：独立模式且目标阶段为 `breakdown`，或工作流模式且 spec 的 `current_step` 为 `breakdown`。

1. 读取需求文档（若存在）；若 `shared_ref` 非空，读取其 `01-需求/`、`02-设计稿/` 作为只读上下文。
2. 按照 `references/breakdown_template.md` 中的模板生成文档，覆盖：
   - **目标端：** PC 端 / 移动端 / 双端。
   - **页面与功能拆解：** 按页面分别列出每个页面的端、依赖与功能模块；跨页面共享模块单独归类。
   - **素材/依赖清单：** 需要用户提供哪些素材（如 API 密钥、账号、第三方服务凭证、图片素材等）。
   - **范围边界：** 明确不在本次实现内的部分。
3. 保存到 `{目标 spec 目录}/03-需求分析/需求分析文档.md`。
4. 使用 `question` 工具向用户展示文档并请求确认。
5. **等待用户确认。**
   - 如果用户选择"需要修改"或输入修改意见：直接修改文档，再次使用 `question` 工具请求确认。
   - 只有在用户选择"确认"后：
     - 独立模式：停止。
     - 工作流模式：把该 spec 的 `current_step` 更新为 `"plans"`、把 `breakdown` 追加到 `confirmed_stages`，同步 `_meta.json` 与 `updated_at`，然后停止并把控制权交回 dwf-orchestrator。**完成 breakdown 推进后，若该 spec 为初始化 spec（`is_shared_context: true`）且其需求覆盖多个页面/复杂模块，提醒 dwf-orchestrator 主动询问用户是否拆分迭代——本技能不直接拆分，由 orchestrator 拆分。**

### 4. 生成技术方案

**进入条件**：独立模式且目标阶段为 `plans`，或工作流模式且 spec 的 `current_step` 为 `plans`。

1. 读取需求文档与需求分析文档；若 `shared_ref` 非空，读取其作为只读上下文。
2. 分析代码库（如果存在），了解当前架构、约定和模式。
3. 按照 `references/plans_template.md` 中的模板生成技术方案，**必须提供至少 2 个并列方案**。每个方案包括：
   - 框架/技术栈选型及其理由
   - 需要的第三方库
   - 后端接口需求（需要后端提供哪些接口、接口字段定义）
   - 数据模型变更
   - 受影响的文件和模块
   - 风险评估和缓解策略
   - 优劣对比
4. 在 `{目标 spec 目录}/04-技术方案/技术方案.md` 中包含所有方案及方案对比表。
5. 使用 `question` 工具向用户展示方案并请求选择。
6. **等待用户选择。**
   - 如果用户选择"需要修改"或输入修改意见：直接修改文档，再次使用 `question` 工具请求确认。
   - 只有在用户选择某个方案后：
     - 独立模式：停止。
     - 工作流模式：把该 spec 的 `selected_plan` 记录所选方案、`current_step` 更新为 `"todos"`、把 `plans` 追加到 `confirmed_stages`，同步 `_meta.json` 与 `updated_at`，然后停止并把控制权交回 dwf-orchestrator。

### 5. 生成实现清单

**进入条件**：独立模式且目标阶段为 `todos`，或工作流模式且 spec 的 `current_step` 为 `todos`。

1. 读取需求文档、需求分析文档和技术方案（以 `selected_plan` 指定的方案为主）；若 `shared_ref` 非空，读取其作为只读上下文。
2. 将选定方案分解为具体的、有序的任务，遵循 `references/todos_template.md` 中的模板。任务要求：
   - **尽可能拆分，不要一次性实现某个功能或页面**（例如一个页面应拆为骨架、组件A、组件B、状态接入、接口联调、样式等独立任务）。
   - 足够具体，可以无歧义地执行。
   - 按依赖关系排序（前面的任务为后面的任务解除阻塞）。
   - 分配优先级（必须/应该/可以/不会，MoSCoW）。
   - 每个任务都必须包含“编码规范检查”和“验证标准”，确保 coding 阶段能逐项核对。
3. 保存到 `{目标 spec 目录}/05-实现清单/实现清单.md`。
4. 使用 `question` 工具向用户展示实现清单并请求确认。
5. **等待用户确认。**
   - 如果用户选择"需要修改"或输入修改意见：直接修改文档，再次使用 `question` 工具请求确认。
   - 只有在用户选择"确认"后：
     - 独立模式：停止。
     - 工作流模式：把该 spec 的 `current_step` 更新为 `"code"`、把 `todos` 追加到 `confirmed_stages`，同步 `_meta.json` 与 `updated_at`，然后停止并把控制权交回 dwf-orchestrator。

## 已有文档处理

如果目标文件已存在：

1. 读取现有文档。
2. 总结当前文档的主要内容。
3. 询问用户要如何处理：
   - 保留现有文档，仅查看或总结。
   - 基于现有文档修改。
   - 替换为新文档。
4. 只有用户明确选择修改或替换后，才能写入文件。

修改已有文档时，保留原有结构，除非用户要求重写。不要创建 `文档-v2.md` 之类的新版本文件，除非用户明确要求。

## 完成前检查

结束前确认：

- 只创建或更新了目标 spec 目录下当前阶段对应的一个文档。
- 独立模式下没有创建 `.dwf/state.json`。
- 独立模式下没有推进后续阶段。
- 工作流模式下没有在一次调用中连续生成多个阶段文档。
- 文档内容为中文。
- 文档遵循 `references/` 中的对应模板。
- 已说明保存路径和下一步需要用户确认的事项。
