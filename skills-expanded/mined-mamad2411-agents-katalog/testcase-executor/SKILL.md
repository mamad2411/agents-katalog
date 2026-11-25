---
name: testcase-executor
description: 使用 Computer Use 执行人工测试用例，解析“模块、用例名称、步骤描述、预期结果”纯文本格式，生成内部执行计划，结合项目页面知识完成导航，记录实际结果和截图证据。用于执行测试用例、自动完成 UI 功能验证或生成测试执行结果。
---

# 测试用例执行

将人工测试用例作为只读输入，执行前生成内部执行计划，通过 Computer Use 完成功能验证，并将执行产物集中保存。

## 创建执行目录

将源测试用例文件所在的需求目录作为 `<需求目录>`。调用本 SKILL 后，先创建 `<需求目录>/execute-testcase/`。执行产物使用以下结构：

```text
<需求目录>/
└── execute-testcase/
    ├── execution-plan.yaml
    └── runs/
        ├── result-{run_id}.yaml
        └── screenshots/
```

将本次流程生成的执行计划、执行结果和截图全部保存在 `execute-testcase/` 中：

- 执行计划：`<需求目录>/execute-testcase/execution-plan.yaml`
- 执行结果：`<需求目录>/execute-testcase/runs/result-{run_id}.yaml`
- 截图：`<需求目录>/execute-testcase/runs/screenshots/`

## 读取测试用例

读取用户指定的测试用例 Markdown。正式用例使用以下字段：

- `一级模块`、`二级模块`、`三级模块`等动态模块层级。
- `用例名称`
- `步骤描述N`
- `预期结果N`

需要确认源格式时读取 [references/testcase-source.example.md](references/testcase-source.example.md)。

使用 [scripts/parse-testcase.mjs](scripts/parse-testcase.mjs) 将源用例直接转换为基础执行计划：

```bash
node "<testcase-executor目录>/scripts/parse-testcase.mjs" \
  --input "<测试用例文件>" \
  --output "<需求目录>/execute-testcase/execution-plan.yaml"
```

脚本创建输出目录并写入 YAML。基础执行计划包含 `system: null`，每条用例包含 `case_name`、`module_path`、`page_id: null`、`precondition: null` 和 `steps`。

## 准备执行计划

1. 从项目上下文、文件路径或用户指令确定 `system`，写入执行计划。
2. 使用 `module_path` 查找项目页面知识：
   - `.agent/page/{system}/menu.yaml`
   - `.agent/page/{system}/{page_id}.yaml`
3. 为每条用例填写稳定的 `page_id`。
4. 保留脚本生成的 `case_name`、`module_path`、`action` 和 `expected`。
5. 保留 `precondition`；源用例未提供时使用 `null`，该字段位于 `steps` 正前方。
6. 保存更新后的 `<需求目录>/execute-testcase/execution-plan.yaml`。

需要确认内部结构时读取 [references/execution-plan.example.yaml](references/execution-plan.example.yaml)。

前置条件仅采用源用例或用户在 Review 中提供的内容。执行时使用当前登录状态和用户指定的运行环境。步骤中明确出现的账号权限、数据状态和业务条件作为本次执行要求；缺少必要执行信息时将用例记录为 `BLOCKED`。

页面知识用于理解页面关系。DOM、Accessibility 元素、CSS Selector、XPath、临时元素索引和坐标在执行时从当前页面获取。

## 用户 Review

生成并保存完整执行计划后，在对话中提供用例数量、待补字段摘要和 `execution-plan.yaml` 文件链接，并结束当前轮次。

收到用户明确确认后，从下一轮开始初始化结果并执行页面操作。用户提出修改时，更新执行计划并再次提交 Review。

## 执行用例

1. 根据页面知识进入目标页面。
2. 根据页面识别特征确认当前页面。
3. 按顺序执行每个 `action`。
4. 每完成一步，重新获取当前页面状态。
5. 将实际表现与对应 `expected` 比较。
6. 记录每一步的 `actual` 和 `result`。
7. 汇总用例结果和整体结果。

使用以下异常处理规则：

- 找不到操作目标时，重新读取页面并重试一次。
- 页面状态与用例不一致时，停止当前用例并记录 `BLOCKED`。
- 预期结果明确不符合时，记录 `FAILED`。
- 无法可靠判断结果时，记录 `BLOCKED`。
- 未知页面保持当前状态并结束当前用例。
- 遵守 Computer Use 的确认和人工接管要求。

## 判定结果

- `PASSED`：操作完成，预期结果全部满足。
- `FAILED`：操作完成，至少一个预期结果明确不满足。
- `BLOCKED`：因页面、环境、账号、数据或识别问题无法完成验证。

`actual` 记录实际观察到的业务结果。

## 保存执行结果

将结果保存到 `<需求目录>/execute-testcase/runs/result-{run_id}.yaml`，截图保存到 `<需求目录>/execute-testcase/runs/screenshots/`。

使用 [scripts/result-record.mjs](scripts/result-record.mjs) 初始化结果。脚本自动填充系统、环境、执行时间、用例名称、`module_path`、`precondition`、`page_id`、步骤和预期结果，`actual_url` 初始为空。

```js
var resultTools = await import(
  "<testcase-executor目录>/scripts/result-record.mjs"
);
var executionResult = resultTools.createResult({
  executionPlan,
  environment: "PRE",
});
var pathTestcase = await import("node:path");
var resultPath = pathTestcase.join(
  "<需求目录>",
  "execute-testcase",
  "runs",
  `result-${executionResult.run_id}.yaml`,
);
await resultTools.writeResult({
  result: executionResult,
  outputPath: resultPath,
});
```

进入页面后记录浏览器当前的实际 URL：

```js
resultTools.recordCaseUrl({
  result: executionResult,
  caseNo: 1,
  actualUrl: "https://webqc-pre.baimeihome.com/busi/qc-report-review/list",
});
```

每完成一个步骤，填写实际结果、步骤状态和截图路径：

```js
resultTools.recordStep({
  result: executionResult,
  caseNo: 1,
  stepNo: 1,
  actual: "查询结果总数为22条",
  status: "PASSED",
  screenshots: ["screenshots/example.png"],
});
```

全部步骤完成后汇总结果并写入文件：

```js
resultTools.finalizeResult({ result: executionResult });
await resultTools.writeResult({
  result: executionResult,
  outputPath: resultPath,
});
```

Agent填写用例的 `actual_url`，以及每一步的 `actual`、`status` 和 `screenshots`。需要确认最终格式时读取 [references/result.example.yaml](references/result.example.yaml)。

## 截图规则

截图用于证明测试结论。

必须截图：

1. 预期结果需要通过页面内容证明。
2. 验证结果跨页面或分页；对每个包含验证结果的页面分别截图。
3. 用例结果为 `FAILED` 或 `BLOCKED`。
4. 新增、保存、提交、审核、删除等操作引起关键业务状态变化。

不需要截图：

- 单纯点击菜单或切换页面。
- 输入查询条件的中间过程。
- 页面滚动过程。
- 重复点击和重试过程。
- 已有截图完整覆盖相同证据。

截图要求：

- 等待页面加载完成、结果稳定后截图。
- 尽量同时包含页面标题、查询条件和结果区域。
- 失败时先保留完整错误页面和提示信息。
- 一张截图可以被多个步骤引用。
- 每条 `PASSED` 用例至少保留一组核心结果截图。
- `FAILED` 和 `BLOCKED` 必须至少保留一张截图。

## 保存截图

调用 `sky.get_app_state()` 获取当前应用状态，将 `state.screenshot.url` 传给 [scripts/save-screenshot.mjs](scripts/save-screenshot.mjs)。

```js
var { saveScreenshot } = await import(
  "<testcase-executor目录>/scripts/save-screenshot.mjs"
);

var savedScreenshot = await saveScreenshot({
  screenshotUrl: state.screenshot.url,
  outputDir: "<需求目录>/execute-testcase/runs/screenshots",
  runId: "20260730_153000",
  caseNo: 1,
  stepNo: 5,
  shotNo: 2,
  label: "page2",
});
```

将返回的 `relativePath` 写入结果文件的 `screenshots` 列表。

截图文件名格式：

```text
{run_id}_case{用例序号}_step{步骤序号}_{截图序号}_{内容说明}.png
```

`run_id` 使用执行开始时间，格式为 `YYYYMMDD_HHmmss`。序号从 `01` 开始，内容说明使用简短的小写英文和数字。
