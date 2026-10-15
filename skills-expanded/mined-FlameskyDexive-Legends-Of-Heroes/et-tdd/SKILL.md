---
name: et-tdd
description: ET test-driven development workflow for WOW. Use when implementing features or bug fixes through a complete loop of requirements, test plan, ATestHandler test writing, implementation, dotnet build ET.sln, targeted test execution, regression checks, and AGENTS.md rule updates.
---

# et-tdd - TDD 测试驱动入口

## 何时使用

- 使用测试驱动方式开发新功能或修复 Bug。
- 需要完整“需求 -> 测试方案 -> 测试用例 -> 实现 -> 编译 -> 运行 -> 回归”闭环。

## 不要加载

- 只是执行已有测试：用 `et-test-run`。
- 只是补写测试用例：用 `et-test-write`。
- 只是编译或导出：用 `et-build`。

## 默认动作

1. 先理解需求、读取相关包 `AGENTS.md`、查看现有实现与现有测试。
2. 写代码前先补 `Test.md` 或最小验证清单，明确测什么、怎么验、预期结果。
3. 先写最小可跑测试用例，再实现代码让测试通过。
4. 编写测试叠加 `et-test-write`；实现业务叠加 `et-code`；涉及异步叠加 `et-async`。
5. 编译统一走 `dotnet build ET.sln`。
6. 运行目标测试，再做必要回归；成功后也检查 `Logs/All.log`。
7. 完成后更新相关包内 `AGENTS.md`，沉淀实现原理、使用方式、测试入口或新增规则。

## 按需补读

- 编写或修改 `ATestHandler`：读取 `../et-test-write/SKILL.md`。
- 执行或排查测试：读取 `../et-test-run/SKILL.md`。
- 涉及异步安全：叠加 `et-async`。
- 涉及业务代码实现：叠加 `et-code`。
