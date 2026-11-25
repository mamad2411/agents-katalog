---
name: happy-visual-workflow
description: "编排 Happy/Paws 用户可见功能从开发到 PR 的交付流程。用于实现或修改 PC Web、移动端或跨端功能，并需要独立验收、一对一 E2E、截图与可播放验收视频、交互评审或 PR 前后对比时；也用于用户说‘视觉稿流程’或要求把功能完整验收到可提 PR。"
---

# Happy 功能交付编排

把一次功能交付串成一条短主线：

```text
开发 → 独立验收 → 按需一对一 E2E → 交互评审 → 可视证据交付 → PR 前后对比
```

本 Skill 只拥有顺序、Case 状态和最终 PR 证据，不复制其他 Skill 的实现细节。开始时读取 [delivery-contract.md](references/delivery-contract.md)，建立最小 Case 表。

## 先确定范围

1. 读取目标仓库的 `AGENTS.md`、`CLAUDE.md` 和更具体的目录规则。
2. 把需求拆成用户可观察的 Case；每个 Case 写一句通过标准。
3. 可见 UI 变化在改代码前保留 Before 证据或 base revision。能直接截图就截图；否则记录可从 base commit 重放的路径，不做无边界全站基线。
4. 只加载当前 gate 需要的 Skill。不要在开始时把所有 reviewer、E2E、视频和发布 Skill 一次性加载。

## 能力路由

| Gate | 首选能力 | 该能力只需返回 |
| --- | --- | --- |
| 开发 | 目标仓库开发 Skill；App 可用 `app-flow-build` | 改动、静态测试、已知风险 |
| 独立验收 | 独立 reviewer；App 可用 `app-flow-reviewer`，其他代码按 metadata 选择 code review | `pass / fail / blocked`、证据、需修项 |
| Web E2E | `web-e2e` | Case 对应关系、结果、最短复跑入口、截图、MP4 与发送状态 |
| PC 交互评审 | `pc-web-interaction-reviewer` 的回归模式 | 逐 Case 交互 verdict 与证据 |
| 移动端交互评审 | `mobile-app-interaction-reviewer` 的回归模式，结合真实设备渲染或录屏 | 逐 Case 交互 verdict 与证据 |
| 视频 | 当前平台已有 E2E/录屏能力；Web 可由 `web-e2e` 录制 | 稳定 MP4 路径、媒体校验、对应 Case |

表里的 Skill 是默认实现，不是硬编码依赖。出现更匹配的平台 Skill 时可以替换，只要遵守 [delivery-contract.md](references/delivery-contract.md) 的返回契约。编排层负责 gate 转换；被委派 Skill 不自行创建 PR、等待 CI 或合并。

## Gate 1：开发

1. 按仓库约定在正确 worktree/分支实现功能。
2. 运行与改动风险相称的 typecheck、单测和静态检查。
3. 开发者可以自测，但不能用自测替代下一步独立验收。

## Gate 2：独立验收

让与生产者分离的 reviewer 检查真实 diff、实现和测试证据：

- 功能是否符合每个 Case 的通过标准；
- 是否存在明显逻辑错误、遗漏状态或无关改动；
- 后续哪些 Case 需要 E2E。

`fail` 返回开发，只修确认问题；`blocked` 说明缺少的证据或环境。通过后才进入 E2E 判断。

## Gate 3：按需一对一 E2E

满足任一条件时运行 E2E：

- 改变用户操作路径、路由、输入、状态切换、持久化、权限或异步反馈；
- 修复一个需要真实交互才能证明的回归；
- 用户明确要求 E2E。

纯内部重构或能由静态检查、单测和视觉评审充分证明的静态变化，可以记为 `not-required`，并写明理由。

需要 E2E 时，每个需求 Case 对应一个已有或新增的最小 E2E Case。先复用已有入口；不要为一个功能扩展成全站遍历。E2E 失败返回开发，修复后只复跑受影响 Case。

## Gate 4：交互评审

在功能验收和必要 E2E 通过后，再评审最终交互：

- PC Web 使用 `pc-web-interaction-reviewer`；
- 原生移动端与窄屏 Mobile Web 使用 `mobile-app-interaction-reviewer`；
- 跨端功能分别检查受影响平台，但共享同一业务 Case ID。

PC 与 Mobile reviewer 不互相替代：PC 可用 Hover/Tooltip、锚定 Popover 和多栏承载次要信息；Mobile 必须在没有 hover 的小屏触控条件下重新安排可见入口、渐进披露、Bottom sheet/全屏流程、键盘和安全区。

评审聚焦本次 Case 的发现性、反馈、状态、布局和可访问性，不重新做无边界产品探索。任一 Case 不通过就返回开发，并重新运行被改动影响的下游 gate。

## Gate 5：可视证据交付

- 用户可见的移动端变化必须录制最终通过版本，因为用户无法直接看到执行设备。
- PC/Web Case 只要 Gate 3 要求 E2E，就必须保留同 Case 截图并录制最终通过版本；纯静态变化若 E2E 有理由记为 `not-required`，仍保留 PR Before / After，但无需为形式补视频。
- 视频只录已经通过的 E2E/验收路径，不用失败录像充当结果。
- 移动端 Case 不需要自动化 E2E 时，录制同一个最小手工验收路径，并保留 `E2E: not-required` 的理由。
- 输出稳定 MP4 绝对路径到终端；运行时提供 Happy/Paws 媒体发送能力时，必须用 `mcp__happy__send_image` 发送截图、用 `mcp__happy__send_file` 发送 MP4。发送成功才记为 `sent`；没有能力或调用失败时如实报告 `local-ready` / `blocked` 和原始错误，不宣称其他设备已收到。
- 视频是交互时序证据，不替代 UI Before / After 图片。

## Gate 6：创建 PR

所有必要 gate 通过后再提交、推送并创建 PR：

1. 可见 UI Case 在 PR 中逐项展示 `Case → Before → After`；前后图保持相同视口、缩放和页面状态。
2. 非可见改动写 `Visible UI cases: 0` 并说明原因。
3. PR 同时列出独立验收、E2E 是否需要及结果、交互评审、视频交付状态、未覆盖项。
4. 创建后打开实际 PR，确认正文和图片可渲染，然后立即返回 PR URL。

“创建 PR”不自动包含等待 CI、OTA、合并和清理。只有用户明确要求“完整交付、合并”或仓库规则把它们列为当前动作的前置条件时，才继续等待并执行对应门禁。

## 回退与完成

- 任何 gate 失败都回到开发，但只重跑被修复影响的 Case 和下游 gate。
- 独立验收与交互评审必须由生产者之外的 reviewer 完成；两者可以复用同一评审 Skill，但必须是不同评审目标和独立结论。
- 只有状态为 `pass` 或有理由的 `not-required` 才能越过 gate。
- 最终回复先给 PR/交付结果，再列 Case 结果、E2E、媒体发送状态和未完成项；不把 CI 等待时间隐藏在“创建 PR”里。
