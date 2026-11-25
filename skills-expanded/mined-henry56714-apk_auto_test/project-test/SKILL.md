---
name: project-test
description: 审计代码变更的行为覆盖，持续扩充本仓库的静态测试与自然语言动态用例库，并执行以输出物为依据的验收测试。适用于 apk_auto_test 完成功能开发后，或需要测试、验证、回归、补充业务用例及检查测试覆盖时。
---

# 项目测试

为本仓库建立从代码变更、覆盖维护到证据化验收的完整闭环。

## 必须执行的流程

1. 找到仓库根目录中的 `test-plan.yaml`，并根据本 `SKILL.md` 确定 skill 目录。修改计划结构或分析校验错误时，阅读 [references/test-plan-schema.md](references/test-plan-schema.md)。
2. 阅读 [references/coverage-maintenance.md](references/coverage-maintenance.md)，冻结本次变更范围，并在执行验收测试前运行 `testctl.py audit`。
3. 如果审计结果为 `GAP`，就在计划的 `maintenance.editable_paths` 范围内自动新增或加强测试资产。必须同时向 `test_cases/dynamic-cases.yaml` 添加自然语言用例及其确定性实现。重复校验和审计，直到变更范围获得覆盖。不得为了让测试通过而修改产品代码。
4. 从全新快照开始执行，并遵循 [references/execute-verify.md](references/execute-verify.md)。执行器始终先运行完整静态门禁，再运行受变更功能影响或用户明确指定的动态用例。
5. 只能依据已验证的输出物作出结论。命令退出码或“命令已执行”本身都不能作为通过证据。

使用项目自身的 Python 环境调用确定性辅助程序：

```bash
python <skill-dir>/scripts/testctl.py --config <repo>/test-plan.yaml <command>
```

维护前使用 `list`、`validate`、`scope` 和 `audit`；执行时使用 `run change`、`run feature:<id>`、`run case:<id>`、`run static-full` 或 `run dynamic-all`。除非用户另有指定，否则把运行输出物放在仓库之外。

## 不可违反的约束

- 每次功能验收都必须包含 `execution.mandatory_static_target`；即使直接选择动态用例，也不能绕过静态门禁。
- 动态用例选择必须基于风险且可追溯：覆盖输出物需要记录变更路径、受影响功能、选中的用例 ID、执行器和全部覆盖缺口。
- 动态用例只有同时具备前置准备、操作、观察、断言、清理、超时、依赖、预期输出及执行器/选择器时才可执行。新增或修改用例前，阅读 [references/dynamic-case-library.md](references/dynamic-case-library.md)。
- 每条命令都必须声明证据检查。执行器需要计算日志和输出文件的哈希、解析结构化输出物并记录每项检查。证据缺失、为空、格式错误、已经过期、出现禁止的跳过或语义不符合预期时，即使命令退出码为 0，也必须判定为 `FAIL`。
- 缺少必需的设备、APK、SDK、二进制程序、变量、文件或能力时，结果必须是 `FAIL`，不能是 `SKIP` 或 `PASS`。前置条件不足时不得执行该用例。
- 执行期间把产品代码、测试代码、测试计划、用例库和本 skill 视为只读内容。任何快照变化都必须使结果变为 `STALE`。
- 不得仅为了迎合当前行为而削弱断言。如果预期行为确实发生变化，必须在用例维护摘要中记录旧契约、新契约和变更原因。
- 当输出物无法证明可观察行为时，即使运行报告显示通过，也可以降级为 `TEST_GAP`。不得把 `FAIL`、`STALE` 或 `TEST_GAP` 提升为 `PASS`。

## 完成标准

返回冻结范围摘要、覆盖输出物、新增或更新的用例、完整静态测试数量、选中的动态用例及选择原因、证据检查和哈希、适用时的环境身份、清理状态、结果输出物、最终结论和剩余风险。如果只能在真实设备上验证的用例未能完成验收，必须明确说明；仅通过模拟器自检不能证明真实设备行为。
