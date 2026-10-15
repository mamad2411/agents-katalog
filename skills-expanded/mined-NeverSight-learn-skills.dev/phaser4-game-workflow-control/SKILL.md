---
name: phaser4-game-workflow-control
description: Phaser 4 游戏仓库的唯一全局工作流控制面。基于任务授权和确定性风险分类处理低风险本地工作，区分用户澄清决定，并仅对 A4-A6 具体操作及影响保留精确显式批准。
---

# Phaser 4 全局工作流控制

把本 Skill 作为 Phaser 项目生命周期的唯一状态机与风险门权威。它不是通用操作控制器；非 Phaser 操作完全移出本流程，由上层系统安全规则和用户任务处理。

## 执行顺序

1. 先把 `<skill-dir>` 解析为本 `SKILL.md` 所在目录，再读取 [控制模型](references/control-model.md)、[状态与门](references/state-gates.md) 和 [Schema](references/schemas.md)。
2. 为每项工作建立独立 Work Item；需求变化建立 Change Request，发布建立独立 Work Item。
3. 把用户当前明确请求冻结为 `taskAuthorization`，绑定原文、目标和范围。A0、A1、A2 及安全 A3 以此为任务授权，不生成 Approval Ledger 记录，也不得称为“自动批准”。
4. 在任何写入、命令副作用或外部操作前运行 `preflight`。只有无法从用户请求、代码、配置、权威工件或确定性证据判断，且会改变产品范围、用户可见行为、视觉方向、预算、合规或数据边界时才请求决定；首次模块或边界本身不是触发器。
5. A3 进入 `IMPLEMENTING` 前冻结 Implementation Package，包括任务授权 ID、基线、范围、路径所有权、委派、输出、验证与退出条件；A2 不要求 A3 包。
6. 子代理启动前生成 Delegation Package 并运行 `delegate-check`；委派只覆盖任务授权内的 A0-A3，A3 必须带 Implementation Package，代理和 ownership 必须已登记且一致。A4-A6 操作批准不能转换成委派授权。
7. 先运行 `route` 自动推导通道、缺失工件和下一条命令。实施后运行 `diff-audit`：A1/A2 或仅外部回执可用真实 `--artifact` 哈希，A3/A4 必须有真实 Git diff；验证后生成 Evidence Manifest。
8. 使用 `advance` 一次最多推进一个状态。A1/A2 在审计和证据满足后闭环；安全 A3 在 F0-F3 通过后由 `PASSED` 直接 `COMPLETE`，不强制 A4/F4。正式入口替换、迁移、删除旧实现和跨模块高影响集成进入 A4。

## 硬限制

- 产品、视觉、架构、预算、合规或数据边界的未决取舍输出 `USER_INPUT_REQUIRED`；澄清后更新任务授权、权威工件或决策记录，不写 Approval Ledger。
- 仅 A4、A5、A6 的具体操作创建 pending，并用非空 `impactSummary` 冻结影响。短回复只解释为最近 `handoff` 展示的唯一操作及影响，不能批准后续操作或扩展范围。
- A4 默认需要 F4 精确批准；A5 必须绑定本次具体外部目标与影响；A6 包括破坏性、生产迁移、真机、商店/正式发布和线上回滚，永不自动。
- 只接受固定白名单 `phaser-*` actionType。Git、Shell、文件管理、包管理、浏览器、消息、GitHub、普通云配置、第三方 API 和通用进程管理均返回 `OUT_OF_SCOPE`，不读取 Work Item/Ledger，不进入 F0-F4，也不创建审批。
- 禁止自动回滚共享工作区，禁止覆盖他人修改。并行写入必须具备互斥文件所有权。
- 启动进程前先检查同项目、类型、模式、端口、PID 与健康状态并复用。本项目本地验证、非特权、无外部写入时直接执行；不得终止归属不明的进程。
- 基线、代码/diff 指纹或范围变化后，旧审批和旧证据失效。

## 命令

首次使用先运行 `node <skill-dir>/scripts/workflow-control.mjs init ...`，它只在控制目录不存在时创建空账本、标准目录和首个 Work Item。`<skill-dir>` 必须解析为本 Skill 的实际根目录，不能按游戏项目当前工作目录猜测。之后运行 `node <skill-dir>/scripts/workflow-control.mjs <route|advance|prepare-approval|handoff|preflight|approve|delegate-check|diff-audit|evidence-check|transition|status|lint> --help`。`approve --approval-id <id> --user-text "批准"` 会从当前已展示 pending 自动生成完整记录；否定或无关文本拒绝。命令只使用 Node.js 标准库，且绝不自动回滚、发布或执行外部动作。
