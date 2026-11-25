---
name: test-first
description: 测试用例编写规范与测试先行工作流：测试行为不测试实现，先写验收场景再写代码，先见红再见绿。用户要求写测试、补测试，或开始新功能开发时使用。
---

# test-first

## 工作流

1. 先写验收场景：标题用「业务主语 + 行为 + 条件」，按 Given / When / Then 组织。
2. 运行测试，确认它**先失败**（见红），证明测试真的在检查东西。
3. 写最少的实现让它通过（见绿），再重构，全程保持测试为绿。

## 原则

- 测试行为，不测试实现：重构不应该打碎测试。
- 按改动范围运行对应级别的测试，不每次都跑全量，见 `references/test-levels.md`。
- 验收场景的写法见 [BDD 场景](references/bdd-scenarios.md)，lint 规则见 [lint 规则](references/lint-rules.md)。

```ts
it('未登录用户访问订单页时跳转到登录页', async () => {
  // Given 未登录
  await logout()
  // When 访问订单页
  await page.goto('/orders')
  // Then 跳到登录页
  expect(page.url()).toContain('/login')
})
```
