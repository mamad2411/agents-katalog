---
name: browser-record-replay
description: 对标豆包工作「浏览器录制与回放」的演示即生成（Demonstration-to-Skill）工作流。通过 antigravity-browser-bridge 启动浏览器 RPA 录制、采集用户真实网页操作与规则备注、提炼可变输入参数，并将录制轨迹自动编译沉淀为可换参复用的专属业务 Skill（含确定性快放 workflow.recording.json 与异常视觉自愈 SOP）。当用户提到“浏览器录制”、“录制与回放”、“演示一遍操作生成 skill”、“记录我控制浏览器的操作”、“browser-record-replay”或要求复现录制流程时使用。
---

# 浏览器录制与回放 & Skill 自动编译器（Browser Record & Replay）

本技能将人类在浏览器中的**一次真实操作演示**，结合用户在操作过程中的**规则备注 / 标记提取**与**对话需求说明**，自动提炼参数并编译成可反复调用、支持换参复用的结构化 **Skill**。

底层依托 `antigravity-browser-bridge` 插件的 4 个专属 RPA 录制/回放工具：
- `browser_record_start`：在当前标签页或指定网址开启 RPA 录制，弹出右下角悬浮录制胶囊 HUD。
- `browser_record_stop`：结束录制并自动去重合并步骤、提炼候选变量（`suggestedParameters`）、落盘保存至 `~/.gemini/memory/browser-bridge/recordings/`。
- `browser_record_list`：查看当前录制状态（`action="status"`）、历史录制列表（`action="list"`）或读取完整轨迹 JSON（`action="get"`）。
- `browser_record_replay`：传入 `recordingId` / `workflowPath` 与变量字典 `vars`（如 `{"keyword": "机械键盘"}`），确定性高速回放；遇页面改版或偶发弹窗时精准返回断点供 Agent 视觉自愈接管。

---

## 核心四步工作流（Standard Operating Procedure）

### 阶段 1：启动录制 或 读取已完成录制

根据用户的触发方式选择分支：

#### 分支 A：用户要求“现在开始录制我的操作”
1. 先调用 `browser_launch`（默认 `browser="edge"`）确保浏览器与「谷谷嘎嘎」扩展连接就绪。
2. 调用 `browser_record_start`（若用户指定了起始网址则传 `url`，并传入 `title`）。
3. 简短告知用户：
   - 浏览器右下角已出现**「谷谷嘎嘎 · RPA录制中」悬浮胶囊**；
   - 请直接在浏览器中按平时习惯演示一遍操作（连续打字会自动合并，密码框会自动脱敏）；
   - 操作途中随时可以点胶囊上的 **「💬 备注规则」** 补充业务条件（例如“只看销量前 10”），或点 **「🎯 标记提取」** 在页面上圈选需要抓取的列表/文本；
   - 演示完毕后，直接点击胶囊上的 **「⏹ 完成」**，或者回到对话框说一声“录好了”并补充最终需求。

#### 分支 B：用户已经用扩展录好，要求“根据刚才的录制生成 Skill / 回放”
1. 直接调用 `browser_record_stop`（若还在录制会自动停止并落盘；若用户已在页面胶囊点击过「⏹ 完成」则会直接返回刚刚完成的录制记录），或调用 `browser_record_list(action="get", recordingId="latest")` 读取最新轨迹。

---

### 阶段 2：轨迹清洗、意图对齐与变量参数化（Parameterization）

拿到录制 JSON（含 `steps`、`suggestedParameters`、`userNotes`、`extractTargets`）后，结合用户在对话中提出的业务需求进行加工：

1. **剔除无效误触**：
   - 检查 `steps`，剔除与最终业务目标无关的误点、多余来回跳转。
2. **融合用户规则备注（`userNotes` & 对话要求）**：
   - 将用户在 HUD 中留下的 `userNote`（如筛选条件、异常处理规则、提取字段要求）转化为对应步骤的执行约束或提取后处理逻辑。
3. **提炼可变输入参数（`parameters`）**：
   - 检查所有 `type`、`select`、`navigate` 步骤中的固定字面量（如搜索词 `"蓝牙耳机"`、分类筛选 `"按销量"`、起始 URL），将其替换为模板占位符 `{{参数名}}`（例如 `{{keyword}}`），并在 `parameters` 字段中记录每个参数的名称、描述、默认值和是否必填。
4. **把业务规则编译成结构化步骤，而不是只写进 SKILL.md**：
   - 用户备注或对话要求「重复 N 次」「每次间隔 3–5 秒」「确认任务已完成」「失败重试」「按页面状态分支」时，用 `loop` / `throttle` / `assert` / `retry` / `if` / `evaluate` + `saveAs` 写进 `workflow.steps`，让规则真的被确定性执行。
   - `vars` 可以传数组（`loop.items` 用 `{{数组变量}}`）；`{{变量|url}}` 拼查询串、`{{变量|json}}` 生成合法 JS 字面量。完整字段见模板第 4 节。
   - 这些步骤不是录制动作，必须标 `"synthesized": true` 并在 SKILL.md 写明规则来源；录制清洗后保留的步骤仍带 `sourceStepIndex`。

---

### 阶段 3：编译沉淀为可复用专属 Skill

除非用户明确要求只做一次性回放，否则默认将清洗并参数化后的流程编译保存为一个独立的全局 Skill，存放路径为：
`~/.gemini/config/skills/<skill-slug>/`

一个编译完成的浏览器自动化 Skill 必须包含以下两个文件（参考 [compiled-skill-template.md](file:///C:/Users/25350/.gemini/config/plugins/antigravity-browser-bridge/skills/browser-record-replay/references/compiled-skill-template.md)）：

1. **`workflow.recording.json`（确定性回放与参数定义文件）**：
   - 保存包含 `parameters` 定义和已替换为 `{{变量名}}` 占位符的 `steps` 数组。
   - 供 `browser_record_replay(workflowPath="<绝对路径>", vars={...})` 直接读取并高速执行。
2. **`SKILL.md`（Agent 调度与异常自愈指南）**：
   - **Frontmatter**：清晰的 `name` 与包含业务触发词的 `description`。
   - **输入参数表**：列出所有 `{{变量名}}`、含义与默认值。
   - **首选快放指令（Fast Path）**：指导 Agent 先调用 `browser_launch` 确认连接，再调用 `browser_record_replay` 传入 `workflow.recording.json` 绝对路径和本次用户的 `vars` 参数一键跑完流程并拿到 `extractedData`。
   - **分步语义说明与视觉自愈兜底（Self-Healing Fallback）**：按顺序写出每一步的业务意图与多重定位特征；当 `browser_record_replay` 因网页改版或偶发弹窗返回 `failedStepIndex` 时，Agent 无需重头再来，直接从 `failedStepIndex` 开始调用 `browser_snapshot` 识别当前页面并完成剩余步骤。
   - **结果交付规范**：说明如何整理 `extractedData`（如输出 Markdown 表格、保存本地 CSV/JSON 或结合其他工具处理）。
3. **编译门禁（强制，防「文档幻觉」）**：两个文件生成后立即运行
   `node scripts/validate-compiled-skill.js <skill目录> --recording <原始录制.json>`。
   存在 ERROR 一律修完再交付，WARN 逐条确认或在 SKILL.md 写明理由。
   - 严禁把录制轨迹里没有的页面、动作、参数写成「标准流程」——文档与 `workflow.recording.json` 脱节时，回放必然跑不完目标；
   - 每个录制来源的 step 保留 `sourceStepIndex` 指向原始录制，被删除的步骤写明清洗理由；规则补写的 step 必须标 `synthesized: true`（校验器会递归检查 loop/if/retry 的子步骤）；
   - `scripts/` 下每个辅助脚本必须有明确执行入口（`browser_evaluate` 或 `node`），不允许无引用的死代码；
   - SKILL.md 第一步必须是 `browser_record_replay(workflowPath, vars)` 确定性快放，自然语言 SOP 只能作断点兜底。

---

### 阶段 4：验证与交付报告

生成完毕后，向用户汇报：
1. 展示从演示操作中识别出的核心步骤流与提炼出的可变参数列表（如 `{{keyword}}`）。
2. 提供新生成的 `SKILL.md` 和 `workflow.recording.json` 文件路径链接。
3. **必须试跑验证**：用 `browser_record_replay` 实跑一遍编译后的 `workflow.recording.json`，把结果（完成/中断步骤、环境、时间）写进 SKILL.md 或 CHANGELOG；未试跑的产物显式标注 `verified:false`，不得声称「已验证」。
4. 说明下次如何一句话触发该 Skill（例如：“用 `xxx` 技能帮我查一下‘机械键盘’的数据”）。
