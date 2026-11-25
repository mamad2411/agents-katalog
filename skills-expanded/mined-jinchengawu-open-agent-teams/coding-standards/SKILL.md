---
name: coding-standards
description: TypeScript 和 React 开发的编码标准与最佳实践。在编写或审查代码时激活。提供命名、类型、组件设计、Hook 提取、状态管理等规范。
---

# 编码标准与最佳实践

## 核心原则

| 原则           | 说明                                     |
| -------------- | ---------------------------------------- |
| **可读性优先** | 代码被阅读的次数多于被编写的次数         |
| **KISS**       | 最简单的解决方案就是有效的，避免过度工程 |
| **DRY**        | 将通用逻辑提取到函数中，避免复制粘贴     |
| **YAGNI**      | 不要构建不需要的功能                     |

## 详细规范

- [references/typescript.md](references/typescript.md) - 命名、类型、模块、async/await
- [references/react.md](references/react.md) - 组件、Hooks、useEffect、API（React Query）、表单、i18n、性能优化
- [references/testing.md](references/testing.md) - 测试金字塔、单元测试、组件测试、Mock
- [references/error-handling.md](references/error-handling.md) - 错误边界、边界条件、防御性编程
- [references/security.md](references/security.md) - XSS 防护、敏感数据处理、输入验证

## 代码异味速查

| 异味           | 阈值    | 解决方案         |
| -------------- | ------- | ---------------- |
| 大组件         | >200 行 | 拆分组件         |
| 大工具文件     | >100 行 | 按功能拆分文件   |
| 长函数         | >50 行  | 拆分成小函数     |
| useState 过多  | >5 个   | 提取 Hook 或拆分 |
| useEffect 过多 | >3 个   | 提取到独立 Hook  |
| 深嵌套         | >4 层   | 尽早返回         |
| Props 过多     | >7 个   | 合并为对象或拆分 |
| Props 透传     | >2 层   | 使用 Context     |

## 提取 Hook 信号

当组件包含以下任一情况时，**必须**提取自定义 Hook：

| 信号               | 判断标准                             | 重构方向                      |
| ------------------ | ------------------------------------ | ----------------------------- |
| 多个关联 useEffect | ≥2 个 useEffect 处理同一业务         | 提取为 `use<Feature>` Hook    |
| 表单逻辑内嵌       | useForm + reset + watch + 自定义提交 | 提取为 `use<Entity>Form` Hook |
| 状态+副作用耦合    | useState + useEffect 共同管理数据流  | 提取为自定义 Hook             |
| 可复用的有状态逻辑 | 状态逻辑在多处重复或明显可复用       | 提取为共享 Hook               |

## 注释规范

| 场景                 | 是否需要注释 | 说明                              |
| -------------------- | ------------ | --------------------------------- |
| 复杂业务逻辑         | 必须         | 解释 why，不解释 what             |
| 临时方案 / Tech Debt | 必须         | `// TODO: xxx` 或 `// FIXME: xxx` |
| Hack / Workaround    | 必须         | 说明原因和移除条件                |
| 自解释的代码         | 不需要       | 好的命名胜过注释                  |

```typescript
// 使用 BigNumber 避免 JS 浮点数精度问题
const total = new BigNumber(price).times(amount);

// TODO: 等后端支持批量接口后重构为单次请求
for (const order of orders) {
  await submitOrder(order);
}
```
