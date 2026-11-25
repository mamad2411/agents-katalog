---
name: node-naming
description: >-
  JS/TS 命名约定——变量、函数、类、接口、类型、常量、文件名与 React 组件/Hook/props。
  涵盖 camelCase/PascalCase/SCREAMING_SNAKE、布尔前缀、双轨文件命名（Node kebab-case /
  React PascalCase）、无 IFoo 前缀、utils 反模式。Use when naming identifiers, choosing
  file names, debating UserProfile.tsx vs user-profile.ts, useAuth hooks, onSave props,
  Button.test.tsx, PascalCase components, or reviewing naming in PRs.
user-invocable: true
metadata:
  author: skills-repo
  version: 2.0.0
---

**Persona:** 你是 Node/TypeScript 代码可读性工程师。你相信好名字是最廉价的文档，坏名字是最隐蔽的 bug 源。

**模式：**

- **Coding 模式** — 为新代码选名。按速查表与最佳实践依次检查；有疑义时，以最能表达意图的名字为准。
- **Review 模式** — 审查 PR diff 中的命名。重点找缩写滥用、`IFoo` 前缀、`utils`/`helpers` 反模式、布尔裸名、React 组件文件用小写。
- **Audit 模式** — 全库命名审计。用子代理并行扫描：(1) 布尔裸名，(2) `I` 前缀接口，(3) `utils/helpers` 文件，(4) 文件命名风格与双轨一致性。

---

# Node.js / TypeScript 命名约定

> 拿不准时，优先保持**文件内**一致性，而非强行套用本指南。

## 速查表

| 元素 | 约定 | 示例 |
|------|------|------|
| 变量、函数、方法 | `camelCase` | `fetchUser`, `userCount` |
| 类、接口、类型、枚举 | `PascalCase` | `UserService`, `HttpClient` |
| 常量（顶层不可变） | `SCREAMING_SNAKE_CASE` | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_MS` |
| 私有字段（类内） | `#camelCase` 或 `_camelCase` | `#token`, `_cache` |
| 布尔变量/参数/字段 | `is`/`has`/`can`/`should` 前缀 | `isReady`, `hasPermission` |
| Node/通用文件名 | `kebab-case` | `user-service.ts`, `http-client.ts` |
| React 组件文件 | `PascalCase.tsx` | `UserProfile.tsx` |
| React Hook 文件 | `use` + `camelCase.ts` | `useAuth.ts` |
| React 事件 prop | `on` + 动作 | `onSave`, `onUserSelect` |
| 测试文件 | `<基名>.test.ts(x)` | `user-service.test.ts`, `Button.test.tsx` |
| 枚举成员 | `PascalCase` 或 `SCREAMING_SNAKE`（保持一致） | `Status.Pending`, `HttpMethod.GET` |
| 泛型类型参数 | 单字母或 `TPascalCase` | `T`, `TValue`, `TKey` |
| 接口 | **无 `I` 前缀** | `Repository`（非 `IRepository`） |

## 双轨文件命名

Node/后端/通用工具默认 `kebab-case`；React 组件与 Hook 是**例外**，必须用 `PascalCase` / `use*`：

```ts
// Node — kebab-case 文件
// order-processor.ts
export class OrderProcessor {}
```

```tsx
// React — PascalCase 组件文件
// features/checkout/PaymentForm.tsx
export function PaymentForm() {
  return <form>...</form>
}
```

不要用 `user-profile.tsx` 命名组件——JSX 靠首字母区分组件与 HTML 标签，小写文件名会破坏这一约定。

## 避免 Stuttering

导入路径已携带模块名，标识符不要再重复：

```ts
// ✓ Good
import { parse } from './url.ts'
parse(rawUrl)

// ✗ Bad
import { parseUrl } from './url.ts'
parseUrl(rawUrl)
```

## 容易遗漏的约定

**双轨文件命名：** `user-service.ts`（Node）与 `UserProfile.tsx`（React）并存是刻意的。全库按文件角色选轨，不要混用。

**React 组件文件必须 PascalCase：** `PaymentForm.tsx`，不是 `payment-form.tsx`。

**事件处理器按动作命名：** `saveUserData()` 优于 `handleClick()`；React 回调 prop 用 `onSave` 而非 `onClick` 当语义是保存时。

**枚举零值哨兵：** 用 `Unknown`/`None` 作零值，避免未初始化被误当真实状态。

**工厂函数用 `create*`：** `createLogger()`，不用 `newLogger()`（Go 风格）。

## 分类详解

完整规则、示例与理由见：

- **[变量、布尔、缩写与作用域](./references/identifiers.md)** — 大小写、作用域长度、布尔前缀、缩写、概念名一致
- **[文件、目录与模块](./references/files-modules.md)** — kebab-case 默认、一概念一文件、utils 反模式、目录组织
- **[函数、方法与事件处理器](./references/functions-methods.md)** — 动词/名词、工厂函数、事件处理器语义命名
- **[类型、接口、常量与枚举](./references/types-constants.md)** — 无 `I` 前缀、常量角色命名、枚举零值、泛型
- **[测试文件命名](./references/testing.md)** — `.test.ts(x)`、co-locate、集成测试后缀
- **[React 命名](./references/react.md)** — 组件/Hook/props/事件、双轨细则、目录与 index 模式

## 常见反模式

| 反模式 | 替换方案 |
|--------|----------|
| `IRepository` 接口 | `Repository`（无前缀） |
| `utils.ts` / `helpers.ts` | 按职责拆分为 `date.ts`、`url.ts` 等 |
| `user-profile.tsx` 组件文件 | `UserProfile.tsx` |
| `UseAuth.ts` / `use-auth.ts` Hook 文件 | `useAuth.ts` |
| `flag`、`temp`、`data` 裸名 | `isEnabled`、`cachedUser`、`responsePayload` |
| `handleClick`、`doThing` | `saveUserData`、`validateSchema` |
| 布尔裸字段 `active` | `isActive` |
| `any` 类型别名 `Data` | 具体类型或泛型参数 |
| Node 文件 `UserService.ts` | `user-service.ts` |
| React prop `UserName` | `userName` |
| 测试集中到顶层 `tests/` | 与源码同目录 co-locate |

---

交叉引用：格式约定见 `node-code-style`；文档注释见 `node-documentation`；类型设计见 `node-types`；测试行为命名见 `node-testing`。
