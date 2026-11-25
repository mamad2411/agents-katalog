---
name: test-data-factory
description: "测试数据工厂——根据 Schema 生成 Mock 数据，支持脱敏规则、数据关联、批量生成。用于单元测试、集成测试和性能测试的测试数据准备。"
version: "4.3.8"
updated: "2026-05-14"
---

# 测试数据工厂

## 概述

测试数据工厂是**声明式测试数据生成器**。它根据 Schema 定义（JSON Schema、TypeScript 接口、数据库 DDL）自动生成符合约束的 Mock 数据，支持数据脱敏规则、表间关联和批量生成。

**核心原则：** 测试数据必须是可复现、可审计、可清理的。硬编码的测试数据 = 难以维护的测试套件。

## 何时使用

**适用场景：**
- 单元测试需要大量符合 Schema 的测试数据
- 集成测试需要填充数据库测试表
- 性能测试需要生成大规模模拟数据
- 前端开发需要 API Mock 数据
- 需要脱敏的生产数据副本

**不适用场景：**
- 少量固定测试数据（直接写 fixture 即可）
- E2E 测试中需要真实数据交互的场景
- 已经有用真实数据的测试（不需要替换）

---

## 方法论

### 步骤 1：定义数据 Schema

从以下来源提取 Schema：

| 来源 | 工具 / 方法 |
|------|-----------|
| **TypeScript 接口** | `ts-json-schema-generator` 提取 JSON Schema |
| **JSON Schema** | 直接使用 |
| **数据库 DDL** | `prisma generate` / `drizzle-kit introspect` |
| **OpenAPI** | `swagger.json` 中的 `components.schemas` |
| **GraphQL** | `gql-schema` introspection |

示例 Schema：
```json
{
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "name": { "type": "string", "minLength": 1, "maxLength": 100 },
    "email": { "type": "string", "format": "email" },
    "age": { "type": "integer", "minimum": 0, "maximum": 150 },
    "role": { "enum": ["admin", "user", "viewer"] },
    "createdAt": { "type": "string", "format": "date-time" }
  },
  "required": ["id", "name", "email", "role"]
}
```

### 步骤 2：选择工厂工具

| 工具 | 语言 | 特点 |
|------|------|------|
| **faker-js** | JS/TS | 丰富的 mock 数据生成 |
| **factory_boy** | Python | Django/ORM 集成 |
| **Bogus** | .NET | C# 假数据生成 |
| **Gofakeit** | Go | Go 随机数据生成 |
| **JSON Schema Faker** | 跨语言 | 从 JSON Schema 生成 |

### 步骤 3：实现数据工厂

工厂函数结构：
```typescript
// user.factory.ts
import { faker } from '@faker-js/faker';

export interface User {
  id: string;
  name: string;
  email: string;
  age: number;
  role: 'admin' | 'user' | 'viewer';
  createdAt: Date;
}

/**
 * 用户测试数据工厂
 * @param overrides - 覆盖默认生成值的字段
 * @returns 一个完整的 User 对象
 */
export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    age: faker.number.int({ min: 18, max: 80 }),
    role: faker.helpers.arrayElement(['admin', 'user', 'viewer']),
    createdAt: faker.date.past(),
    ...overrides, // 允许调用者覆盖
  };
}

/** 批量创建用户 */
export function createUsers(count: number, overrides: Partial<User> = {}): User[] {
  return Array.from({ length: count }, () => createUser(overrides));
}
```

### 步骤 4：定义脱敏规则

生产数据脱敏映射：

| 字段类型 | 脱敏规则 | faker 替代 |
|---------|---------|-----------|
| 姓名 | 替换为随机姓名 | `faker.person.fullName()` |
| 邮箱 | 替换为 `test-{uuid}@example.com` | `faker.internet.exampleEmail()` |
| 手机号 | 替换为 `+86 138****1234` 格式 | `faker.phone.number()` |
| 身份证号 | 替换为合法但虚构的号码 | 专用生成器 |
| 密码/Token | 替换为 `REDACTED` | 固定字符串 |
| IP 地址 | 替换为私有地址段 | `faker.internet.ipv4()` |
| 金额 | 保留分布，替换具体值 | `faker.finance.amount()` |

### 步骤 5：定义关联数据生成

```typescript
// 带关联的数据工厂
export function createOrderWithUser(overrides: Partial<Order> = {}) {
  const user = createUser();
  return {
    order: createOrder({ userId: user.id, ...overrides }),
    user,
  };
}

// 批量创建关联数据
export function createOrdersWithUsers(count: number) {
  const users = createUsers(5);
  return Array.from({ length: count }, () => {
    const user = faker.helpers.arrayElement(users);
    return createOrderWithUser({ userId: user.id });
  });
}
```

---

## 反模式

| 反模式 | 正确做法 |
|--------|---------|
| 测试中使用 `Math.random()` | 使用 `faker.seed()` 确保可复现 |
| 硬编码测试数据在测试函数中 | 使用工厂函数，集中管理数据生成 |
| 工厂生成的关联数据不一致 | 在工厂内部保证关联数据的一致性 |
| 脱敏时简单替换为 "test" | 保留数据类型和格式，只替换敏感内容 |
| 工厂函数过于复杂 | 每个工厂只负责一个实体，复杂场景使用组合 |
| 测试数据泄漏到生产环境 | 使用明显的 `test-` 前缀或专用测试数据库 |

---

## 示例

```typescript
// 单元测试中使用
import { createUser, createUsers } from '@/testing/factories/user.factory';

describe('UserService', () => {
  it('应返回年龄大于18的用户列表', () => {
    // Arrange
    const users = [
      createUser({ age: 15 }),  // 未成年
      createUser({ age: 25 }),  // 成年
      createUser({ age: 30 }),  // 成年
    ];
    
    // Act
    const adults = filterAdults(users);
    
    // Assert
    expect(adults).toHaveLength(2);
    expect(adults.every(u => u.age >= 18)).toBe(true);
  });
});
```

## 验证清单

- [ ] 工厂生成的每个字段都符合 Schema 约束
- [ ] 工厂支持 `overrides` 参数覆盖任意字段
- [ ] 可通过 `faker.seed()` 复现相同的测试数据
- [ ] 关联数据工厂保证外键一致性
- [ ] 脱敏规则覆盖所有敏感字段类型
- [ ] 工厂函数有 TypeScript 类型保护（`overrides` 为 `Partial<T>`）
