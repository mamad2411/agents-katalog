---
name: check-impl
description: "Post-implementation reality check that verifies code assumptions are correct, not just syntactically valid. Checks API contract assumptions (response structure, parameter names), component context behavior (Modal/Drawer lifecycle, state preservation), data history compatibility (new fields on old records), cross-layer data flow traces, and requires verification tests for critical assumptions. Complements check-cross-layer: cross-layer checks structural completeness, check-impl checks assumption correctness."
---

# Implementation Reality Check

验证你写的代码是否基于真实的假设，而非"想当然"。大多数实现 bug 不是逻辑错误，而是前提假设错了。

> **Note**: 这是 **post-implementation** 安全网，与 `/trellis:check-cross-layer` 互补。
> cross-layer 检查结构完整性，本命令检查假设正确性。

---

## Execution Steps

### 1. Identify Change Scope

```bash
git diff --name-only
```

### 2. Select Applicable Check Dimensions

根据变更类型，执行对应的检查维度：

---

## Dimension A: API Contract（调用了已有 API 时）

**Trigger**: 前端新增/修改了对后端 API 的调用

**Checklist**:
- [ ] 读过 Controller/Handler 源码，确认实际响应结构？
- [ ] 找到项目中已有的同 API 调用代码作为参考？
- [ ] 请求参数名、类型、默认值从源码确认（非凭记忆）？
- [ ] 分页接口：确认了分页字段名和起始页码？

**Anti-pattern**:

| 错误假设 | 实际情况 |
|---------|---------|
| `res.data.data` 是数组 | 实际是 `{ items: [], total }` 分页结构 |
| 参数名是 `page` | 实际是 `p`，且从 1 开始 |
| 响应直接是业务数据 | 实际包了一层 `{ success, message, data }` |

---

## Dimension B: Component Context（在容器内使用组件时）

**Trigger**: 在 Modal / Drawer / Tab / 条件渲染块内使用有状态组件

**Checklist**:
- [ ] 确认容器关闭/切换时是否销毁子组件？
- [ ] 如需保持状态：是否用了 keepDOM / destroyOnClose={false} 等配置？
- [ ] 受控组件的 value 与外部 state 是否正确绑定？
- [ ] 找到项目中同容器内的组件用法作为参考？

**Anti-pattern**:

| 错误假设 | 实际情况 |
|---------|---------|
| Modal 关闭后表单状态保留 | 默认销毁子组件，再开状态丢失 |
| value 传了就是受控 | 某些组件需 initValue + value 配合 |
| 组件在任何地方行为一致 | 容器上下文会影响挂载/卸载行为 |

---

## Dimension C: Data History（修改了数据模型时）

**Trigger**: 数据库表新增/修改了字段

**Checklist**:
- [ ] 历史记录的新字段值是什么（空/零值/null）？
- [ ] 用新字段过滤时，历史数据能否被正确查到？
- [ ] 是否需要降级查询路径（如从其他表补查历史数据）？
- [ ] 写入链路中新字段的值从哪来？来源是否可靠？

**Anti-pattern**:

| 错误假设 | 实际情况 |
|---------|---------|
| 加了字段就有数据 | 旧记录新字段全是零值/空值 |
| 只查聚合表就够了 | 聚合表缺维度，需从明细表降级查询 |
| 字段值肯定有 | 某些调用链路中该值可能为空 |

---

## Dimension D: Data Flow Trace（跨层变更时）

**Trigger**: 变更涉及 前端 ↔ API ↔ 数据库 的数据传递

**Checklist**:
- [ ] 模拟一条完整请求路径：前端发什么 → 后端收什么 → 查出什么 → 返回什么 → 前端解析什么？
- [ ] 前端参数名 === 后端 Query/Body 参数名？
- [ ] 后端返回结构 === 前端解析结构？
- [ ] 空值/零值场景：不填该字段时，每一层的行为是否正确？

**Anti-pattern**:

| 错误假设 | 实际情况 |
|---------|---------|
| 代码看起来对就能跑 | 参数名差一个字母、嵌套差一层 |
| 只检查非空路径 | 空值路径才是出 bug 最多的地方 |
| 前后端分别看都没问题 | 放一起跑时数据对不上 |

---

## Dimension E: Verification Tests（验证关键假设的测试）

**Trigger**: 任何涉及 Dimension A-D 的变更

光靠肉眼审查不够，关键假设必须有可运行的验证手段。根据变更类型选择合适的验证方式：

**API Contract 验证**:
- [ ] 写一个请求测试，验证实际响应结构与代码解析逻辑匹配
- [ ] 覆盖正常路径和空值/零值路径

**数据模型验证**:
- [ ] 写查询测试，用真实数据（含历史旧记录）验证过滤/聚合结果正确
- [ ] 新字段为空时的查询行为是否符合预期

**跨层数据流验证**:
- [ ] 写端到端测试，从请求发起到响应解析，验证完整路径数据一致
- [ ] 覆盖边界场景：空参数、特殊字符、零值

**验证原则**:
- 不要求高覆盖率，但每个 Dimension 中发现的关键假设至少有一个测试保护
- 优先写能暴露"想当然"问题的测试，而非走过场的 happy path
- 如果无法写自动化测试，记录手动验证步骤和预期结果

**Anti-pattern**:

| 错误做法 | 正确做法 |
|---------|---------|
| 只写 happy path 测试 | 优先覆盖假设最脆弱的路径 |
| 测试写了但没跑 | 测试必须实际运行并通过 |
| "这个太简单不用测" | 越简单的假设越容易错（参数名、嵌套层级） |

---

## Common Issues Quick Reference

| Issue | Root Cause | Prevention |
|-------|------------|------------|
| API 调用返回 undefined | 响应结构假设错误 | 读 Controller 确认 |
| 组件状态莫名丢失 | 容器销毁了子组件 | 检查容器生命周期 |
| 筛选后数据为空 | 历史记录缺字段 | 验证旧数据查询路径 |
| 参数传了但后端没收到 | 参数名不匹配 | 源码级确认参数名 |
| 看着对但跑不通 | 只做了静态审查 | 模拟完整数据流 |

---

## Output

Report:
1. 本次变更涉及哪些维度
2. 每个维度的检查结果
3. 发现的问题及修复建议（直接修复）
