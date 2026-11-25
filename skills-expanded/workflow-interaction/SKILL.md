---
title: 工作流交互手册
id: workflow-interaction
type: skill
tags: [workflow, 交互, 探索, 语义, 增强模式, 输入]
---

# 工作流交互手册

> 探索与操作真实界面的细则。何时读：进入 Phase 1 探索、首次桌面/浏览器操作、遇到交互形态不确定时。
> 系统提示词只管原则（语义优先、证据纪律）；本文管怎么做。已证实过的规则禁止重新探索。

## 一、探索入口（按场景二选一）

### 浏览器探索与反爬预检

- 网页场景直接用 `browser_*` 工具链（snapshot → click/type）；不涉及桌面语义工具。
- 反爬预检：站点可能弹验证码/滑块/登录墙——先以普通导航探一次目标页，命中即按 workflow-recovery 的阻塞分类处置，不反复试探触发风控。
- 网页元素定位与提交模式（@eN ref → OCR → evaluate 降级链）见 skill: workflow-design「工具使用要点」「模式 F」。

## 二、目标绑定（桌面任务第一步）

- 用户在前台 Nuphus 提交任务，**前台 ≠ 任务目标**。
- 先 `desktop_targets_list` 查本机应用/窗口 → 主模型结合任务选择 → `desktop_target_bind` 启动/激活，后续观察与增强判断传返回的 `target_token`。
- 多窗口从返回候选选，不猜窗口句柄。合法跨应用步骤重新绑定，不另向用户确认。
- 启动 GUI 优先用 bind 的本机目录入口；旧环境用 `system_shell` 时必须非阻塞（Windows `Start-Process` / macOS `open` / Linux 后台），禁止前台等待退出的启动方式。

## 三、桌面语义探索（UIA/Accessibility-first）

### 行为确认清单（探索前向用户逐项确认）

| 项 | 确认内容 |
|----|----------|
| 触发方式 | 功能从哪里进（按钮 / 菜单 / 快捷键 / 托盘） |
| 关闭方式 | 弹窗/窗口怎么退（X / Esc / 取消按钮），有无强制模态 |
| 状态可用性 | 按钮何时禁用/置灰，操作前需要什么前置状态 |
| 完成标志 | 怎么判定操作成功（提示文案 / 状态变化 / 新页面） |

无法确认的项在探索中验证，验证到的写入 params.json；与用户口头约定冲突时以用户为准。

### 语义候选读取

- 候选输出是完整 JSON 分页：`next_cursor` 非空 → 同次 `observation_token` + cursor 续查；`view=regions` 查可深入区域，用返回 `subtree_id` 发起新观察；菜单传 `scope=menu`。
- 树未读完整、候选未展示完、控件原生不支持是三种不同情况——不得断言缺失的按钮一定在后半段。
- `desktop_semantic_candidate` 查选中项详情与 `workflow_step`；执行结果同样返回稳定步骤。
- 定位不精确：先分页、缩小区域、重识别视觉锚点；仍无法唯一定位 → 标「未识别」+ `request_user_input(region)`（首选方案，非降级）。
- 坐标空间：以工具返回的单位和窗口/屏幕原点为准；截图像素 ≠ 桌面逻辑坐标（macOS Retina / 多屏尤甚），本地工具换算，不凭模型估算。
- 语义动作重放：保存候选返回的 `workflow_step`，运行时 `desktop_semantic_action`。**禁止**保存临时 `observation_token` / `candidate_id` / 自由坐标 / 固定 hwnd。
- 旧 hwnd 参数兼容；新步骤一律 `desktop_input(target_locator=成功 workflow_step.params.locator, launch_ref=有则沿用, ...)`，本地重定位窗口，不加固定 hwnd 激活步骤。

## 四、增强模式（desktop_agent_step）

前提：工具列表存在 `desktop_agent_step`（增强判断模型已配置）。不存在则跳过本节，走普通语义/视觉路径，不循环请求缺失工具。

- 每个新的可执行桌面决策先 `desktop_agent_step(goal)`；不要绕过它自行开始同一轮候选选择。
- `needs_primary_decision` → 主模型直接从返回 `action_space` 选并 `desktop_semantic_execute`，不重复请求增强判断。
- `needs_input_value` → 主模型补业务文本为 `value`，调用返回的 `desktop_semantic_execute` 候选（该文本不发给增强判断模型）。
- `needs_primary_completion_check` → 主模型结合业务目标确认是否结束。
- `needs_observation` → 动作可能已发送但结果未确认：先读新界面，不重发点击/发送/提交。
- 增强判断模型不生成坐标、脚本、选择器、输入内容；未配置/转交主模型/不可用/UIA 不适用 → 落回普通语义 → 视觉 → 鼠标。
- 已获同一控件「缺少所需能力」的证据后，不重复调用增强判断期待新能力。

## 五、执行动作细则

| 场景 | 执行标准 |
|------|----------|
| 动作语义混合 | 按动作判断，不要求整应用单一方式：无 SetValue 的文本框 → 语义 Focus + `desktop_input`；原生菜单不可用但有快捷键 → `desktop_input(hotkey)` |
| 填表/文本编辑 | 显式 `desktop_input(send="none")`；仅任务要求提交且发送方式已确认时才指定 enter/快捷键 |
| 开关/设置 | 优先 `set_checked` + 目标状态；不把「开启」固化成每次反转的 toggle |
| 回执判读 | `dispatch_state` 与 effect 分开读：sent/partial/unknown 不自动重发；unverifiable 先观察/等待后置条件，不宣称业务完成。事件已发送、控件状态变化、业务完成三件事分别判断 |
| 已发送未知结果 | 刷新相关区域、查能力与后置条件，改用有证据的路径；仅业务意图或人授权限缺失时问用户，不重复发送结果未知的提交动作 |
| 视觉回退 | 平台无语义工具或应用无有效 UIA 时，用实际可用的视觉/鼠标工具；坐标必须来自最新本地观察（capture_id + element_id 让本地换算，禁止试探屏幕坐标、禁止为修坐标移动用户窗口）。macOS 截图需录屏权限，纯 Accessibility 不需要；权限缺失说明授权入口后重试，不循环调用 |

## 六、用户交互粒度

- 每次 `request_user_input` / `wait` 只问一件事，不塞复合问题。
- **step_form 例外**：需用户补录同一阶段的多个子步骤 → `request_user_input(input_type="step_form", title, prompt, default_stage=当前阶段名)` 一次收齐；提交返回 `{"stage":"...","steps":[...]}`，取消返回 `__CANCELLED__`。
- 用对方能直接理解的表述（「左侧列表里一个联系人」而非「会话列表中的条目」）。

## 七、截图卫生

| 场景 | 操作 |
|------|------|
| 验证完毕的截图 | 立即 Delete（`$env:TEMP` 下） |
| 禁止 | 项目根目录积累临时截图 |
| 需复用 | 存 `plugin/workflows/{id}/screenshots/` |
