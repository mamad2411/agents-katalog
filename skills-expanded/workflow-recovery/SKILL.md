---
title: 工作流故障恢复
id: workflow-recovery
type: skill
tags: [workflow, 恢复, 失败, 断点续连, 阻塞]
---

# 工作流故障恢复

> 何时读：`workflow_run` 返回 `{"failed":true,...}` 时。
> 核心判界：**运行时阻塞就地解决，设计缺陷才改文件。**

## 处置顺序

1. **识别阻塞**：解析 `error` 归类——验证码 / 弹窗 / 登录态 / 网络 / 元素未出现。
2. **就地解决**（优先级从高到低）：
   - 工具列表存在 `desktop_agent_step`（增强模式）→ 每个新桌面决策先调它；`needs_primary_decision` 主模型直接从 `action_space` 选并执行；`needs_input_value` 主模型补 `value`；`needs_observation` 先读新界面不重发。
   - 无增强入口但有语义工具 → `desktop_semantic_observe` / `desktop_semantic_execute`。
   - 语义不可用 → 截图/OCR/坐标工具（最后手段）。
   - 浏览器场景继续 `browser_*`。
   - 探索成功后把候选返回的 `workflow_step` 原样固化为 `desktop_semantic_action`；禁止保存临时 token / candidate ID。
   - 解决后状态即保留。
3. **断点续连**：重新 `workflow_run` 传**同一 id**——引擎自动跳过 `completed_steps`，从失败步骤继续。**禁止**新建/复制/改名工作流来「重跑」。⚠️ 同 id 重跑复现同一失败时，先读下方「断点续连状态污染」，不要连续重试。
4. **改文件判界**：只有确认设计缺陷（参数/选择器/步骤逻辑错误）才改 workflow / params；运行时阻塞（验证码、弹窗、外部状态变化）一律就地解决，不靠改工作流规避。
5. **重试上限**：同一步骤同一阻塞连续失败 3 次 → 停止重试，用 `completed_steps` 向用户汇报已完成进度与阻塞原因，等待指示。禁止无限重跑或整单重开。

## 失败重跑后

- 若因探索不全导致失败：补探索 → 更新 params.json `exceptions`（W4）→ 再续跑。
- 恢复经验（非显而易见的解法）→ `ui_maps_save_experience`。

## 断点续连状态污染（capture 步骤被跳过）

**症状**：同 id 连续重跑在同一处失败（`completed_steps` 完全一致），修正参数/就地解决均无效。
**根因**：续跑跳过上次已成功的 `capture` 步骤且**不重新生成其变量**——下游读到的是上一次 run 的陈旧值（失效 hwnd、旧 query、旧坐标），必然复现同一失败。
**判别证据**（三占其二即可判定，不要继续改 workflow/params）：
1. 本应产出的截图/文件不存在，重跑后仍未生成 → capture 步骤被跳过；
2. 变量池里是陈旧值（对照上次 run 的时间戳）；
3. 失败步骤的 `run_history` 时长异常短（秒级）却列出大量步骤。

**处置**：清空该工作流的 `run_history`（置 `[]`）→ 同 id 重跑，从头完整执行。
**禁止**：靠改步骤 id 绕过（上游 capture 变量依旧陈旧）；把它误判为设计缺陷去改 params。
