---
name: re-flow-orchestrator
description: 逆向破解总编排——完整授权破解任务的状态机与流程衔接：INIT→ENV→SANDBOX→RECON→CAPTURE(可选)→UNPACK(可选)→ANALYZE→BYPASS→PACKAGE→DONE，按阶段调度 re-env-sandbox / re-flow-recon / capture / unpack / analyze 与下载层三件套，BYPASS/PACKAGE 阶段复用 windows-license-crack 主 skill 的算法推导、运行时绕过与打包细节。当用户给出目标程序要求完整破解（含环境准备）、或需要查看/推进任务进度时使用。触发词：完整破解、开始破解任务、破解流程、任务状态、下一步。
agent_created: true
x-alice-class: reverse
---# 逆向破解总编排（re-flow-orchestrator）

## 单一职责

只做一件事：**端到端任务编排与状态流转**——决定"现在该做哪一步、下一步交给谁"。
不亲自执行任何阶段的具体操作，全部委派给下层 skill 与知识库。

## 状态机

`INIT → ENV → SANDBOX → RECON → CAPTURE(可选) → UNPACK(可选) → ANALYZE → BYPASS → PACKAGE → DONE`

| 状态 | 动作 | 委派对象 |
|---|---|---|
| INIT | 接收目标、建任务目录与 `state.md` | 本 skill |
| ENV | 环境自检；缺工具则触发下载链 | re-tool-manifest → re-tool-registry → re-tool-downloader → re-tool-manifest |
| SANDBOX | 隔离环境与快照基线、网络/时间策略、符号 | re-env-sandbox |
| RECON | 侦察与目标画像（8 项）、路线决策 | re-flow-recon |
| CAPTURE | 网络取证（侦察显示联网验证时） | re-flow-capture |
| UNPACK | 脱壳（侦察判定有壳时） | re-flow-unpack |
| ANALYZE | 静态定位关键函数 → 断点与数据流追踪 → hook/patch 决策 → 补丁与回归验证 | re-flow-analyze |
| BYPASS | 算法推导 / 运行时绕过 | windows-license-crack 主 skill 第 4-7 步 |
| PACKAGE | 启动器工程化 + 打包分发 | windows-license-crack 主 skill 第 8-9 步 |
| DONE | 汇总交付物，收尾 | 本 skill |

状态持久化：任务目录 `state.md`（当前状态、已完成步骤、证据文件索引、下一步动作）。

**ANALYZE 与 BYPASS 的分工**：ANALYZE 负责"找到并证明"（定位、追踪、改、验证），BYPASS 负责"做成可靠方案"（Frida 过滤式 hook、启动器工程化、跨机器授权码）。两者常交织——ANALYZE 验证不通过时回到 BYPASS 换 hook 方案，再回到 ANALYZE 复验。

## 阶段跳转规则

| 侦察结论 | 跳转 |
|---|---|
| 无壳、验证逻辑简单 | RECON → ANALYZE（跳过 CAPTURE/UNPACK） |
| 无网络行为 | 跳过 CAPTURE |
| UPX/MPRESS 压缩壳 | UNPACK → ANALYZE |
| VMP 虚拟化 | CAPTURE 与 UNPACK 并行；ANALYZE 走 API 边界定位，BYPASS 走 API 边界 hook |
| 存在完整性自检 | ANALYZE 阶段选 hook 而非 patch（re-flow-analyze 阶段三决策表） |
| 目标在 VM 里行为异常 | 回到 SANDBOX 处理反虚拟机检测，再重跑 RECON |
| ANALYZE 回归验证未通过 | 回滚补丁 → 回 BYPASS 换方案 → 再进 ANALYZE 复验 |
| 阶段失败 | 记录 state.md，按 windows-license-crack 速查表回退或换路线 |

## 输入与输出

- **输入**：目标程序路径；可选：授权码样本、目标机器码、交付要求
- **输出**：任务目录（`state.md` / `env.md` / `report-recon.md` / `capture/` / `dump/` / `analyze/` / 最终工具包 zip）

## 与两层的调用关系

- **同一业务层**：re-env-sandbox、re-flow-recon、re-flow-capture、re-flow-unpack、re-flow-analyze —— orchestrator 按状态依次调度，五者互不直调，只经 orchestrator 串联（保证衔接与状态一致）
- **下载服务层**：仅在 ENV 状态按需调用一次链路 `registry → downloader → manifest`；日常可脱离本流程独立复用（单独问"装个工具"就只走下载层）
- **知识库层**：windows-license-crack 主 skill 提供 BYPASS / PACKAGE 两阶段的深度方法、脚本与判据表

## 执行顺序（硬性）

1. 下载层先就位：registry 出清单 → downloader 执行 → manifest 登记（首次一次性，后续复用）
2. 环境先隔离：SANDBOX 建快照基线与网络/时间策略（工具装完即打 `01-tools` 快照，之后每个破坏性动作前回滚）
3. 流程层按状态机推进：ENV 自检 → SANDBOX → RECON → CAPTURE → UNPACK → ANALYZE → BYPASS → PACKAGE
4. 每次开工先读 `state.md` 恢复进度，阶段完成即回写状态
5. ANALYZE 未通过回归验证前，不得进入 PACKAGE —— 未经验证的补丁打包分发，问题会在用户机器上爆发
