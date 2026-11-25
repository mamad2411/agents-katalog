---
name: ui-testing-fake
description: 仅用于契约测试的假调试环境（test-only）：验证跨环境适配器、配置准入、证据与生命周期。它不是真实平台实现，不得据此声称任何真实桌面/Android/小程序环境已支持。
---

# UI Testing · 假环境（test-only）

## 边界

- 本 Skill 只在 `DSH_UI_TESTING_TEST_HOOKS=1` 或 `DSH_UI_TESTING_ALLOW_TEST_ENV=1` 的测试配置中可发现；生产默认不可见、不可加载。
- 假环境只提供确定性夹具：目标列表、帧/图像、网络事件、显示空间、标注与租约；不启动真实浏览器、不连接真实设备。
- 不得把假环境的通过写成真实平台可用；真实平台仍需独立适配器、独立探针与独立验收。

## 用途

用于验证三类 adapter 的公共契约：配置 revision 一致性、目标 generation、证据 envelope、P0 可选能力、取消/清理与跨环境隔离。测试记录必须区分“假适配器契约通过”与“真实平台未验证”。

## 怎么用（Agent 操作口径）

1. **先确认发现条件**：`browser_capabilities` 的 `readiness.environments` 里能看到 `fake`，且 `enabled=false` 时不要直接调工具——它还没被启用。
2. **启用并选择**：让用户（或测试脚本）在设置页面板启用 `fake` 环境；本会话选择用 `POST /plugins/ui-testing/config/select`（`scope:"session"`）。工具面会在下一步按新的启用集合重建。
3. **确认注册面**：启用 fake 后 `browser_capabilities.adapter.declaration.registeredTools` 应包含 `browser_fake_probe` + 两个环境无关诊断；Web 未启用时应**不含**任何 `browser_*` Web 工具。
4. **跑探针**：调 `browser_fake_probe`（可带 `payload`），确认返回 `environment:"fake"` 且结果 envelope 带 `configRevision`；这证明执行入口用的是当前配置。
5. **做对照**：Web 与 fake 的差异要落在"注册面 / Skill 目录 / 执行准入"三处，任一处不符就记 FAIL，别只截图。

## 断言清单（缺一条就不算契约通过）

| 检查 | 期望 |
| --- | --- |
| 配置 revision | 工具结果里的 `configRevision` 与 `GET /config` 的 `revision` 一致；旧 revision 的调用被判 `CONFIG_STALE` 或重新解析 |
| 目标 generation | `listTargets`→`bind` 后 `generation` 递增；重绑后旧帧/旧标注/旧租约按 `targetId + generation` 被拒（`GENERATION_MISMATCH`），不串目标 |
| 证据 envelope | P0 每次成功调用带 `version/scope/session/target/generation/configRevision/operation/source/capturedAt`，缺字段即 `EVIDENCE_INCOMPLETE` |
| 可选能力 | 去掉某个 P0 家族时该家族报 `unsupported`，其余家族仍可用；不得伪造空数据 |
| 取消/清理 | 取消后连接/帧源/网络/租约都被释放，不遗留后台任务 |
| 跨环境隔离 | 禁用某环境后其工具不进注册面、其 Skill 不在目录里（`ui-testing-web` 与 `ui-testing-common` 的差别就是判据） |

## 常见误判

- 用 fake 的结果去宣称 Android/桌面/小程序"已支持"——不行，那是另一套适配器与另一套验收。
- 把"工具被拒"当成隔离证据：要看**注册面/请求声明**，而不是 handler 返回 `ADAPTER_DISABLED`。
- 把"页面工具 available"当成"浏览器已经连上"：连接状态看 `connection` 轴，未启动是 `not-probed`。

三类 adapter 的接口形状与完整坑点清单是**贡献者文档**：`docs/adapters.md`（Agent 日常操作不需要读它，按上面的断言清单用工具即可）。
