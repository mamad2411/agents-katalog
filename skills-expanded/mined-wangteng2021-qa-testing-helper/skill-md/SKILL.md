# QA Testing Helper

## 概述

全面的 QA 测试辅助工具，覆盖从需求分析到自动化测试的完整测试流程。采用**黑盒测试方法论**（等价类划分、边界值分析、因果图、状态迁移、场景法、错误推测），设计生产级可执行测试用例。

## 激活条件

当用户提及以下关键词时自动激活：
- 测试
- 测试用例
- unit test
- E2E test
- 自动化测试
- 单元测试
- 集成测试
- 测试覆盖
- QA
- 质量保证
- test case
- 写测试
- 覆盖率
- Jest
- Vitest
- Playwright
- Cypress
- 黑盒测试
- 等价类
- 边界值
- 状态迁移

---

## 零、黑盒测试方法论说明

### 0.1 测试方法论概览

| 方法 | 适用场景 | 核心思想 | 本 Skill 应用 |
|------|----------|----------|---------------|
| **等价类划分** | 输入数据多，无法穷举 | 将输入分成有效等价类和无效等价类，从每类中选代表性数据进行测试 | 充值金额、用户输入、数据范围 |
| **边界值分析** | 输入范围、边界条件 | 重点测试边界值及其附近的值 | 0、1、最大值、临界值 |
| **因果图** | 多个输入条件组合 | 分析输入条件之间的因果关系，设计测试用例 | PK结果判定、薪资计算触发条件 |
| **状态迁移** | 有状态的对象/流程 | 测试状态之间的转换及转换条件 | PK状态流转、订单状态 |
| **场景法** | 业务流程 | 基于用户场景设计测试用例，覆盖主流程和支流程 | 用户充值流程、PK流程 |
| **错误推测** | 经验驱动 | 基于经验推测可能出错的地方 | 网络异常、服务器超时、重复提交 |

### 0.2 测试维度覆盖要求

每条测试用例必须覆盖以下维度（根据实际情况选择）：

| 维度 | 说明 | 方法论 |
|------|------|--------|
| **功能测试** | 正常业务流程、正确输入 | 场景法、等价类 |
| **异常测试** | 错误输入、异常场景 | 错误推测、等价类 |
| **边界值测试** | 边界条件、临界值 | 边界值分析 |
| **安全测试** | 越权、数据校验、参数篡改 | 因果图 |
| **性能/并发** | 高并发场景、响应时间 | 压力测试 |
| **兼容性测试** | 多端适配、网络环境 | 组合测试 |

### 0.3 生产级测试用例标准

每条测试用例必须包含：
- ✅ 用例ID（唯一标识）
- ✅ 测试模块
- ✅ 用例标题
- ✅ 测试方法论（标注使用的测试方法）
- ✅ 前置条件
- ✅ 测试步骤（细化到字段级别）
- ✅ 预期结果（具体可验证）
- ✅ 优先级（P0/P1/P2）

### 0.4 隐含场景覆盖要求

必须覆盖的隐含场景：
- 网络异常（断网、延迟、超时）
- 重复提交
- 接口异常（返回错误、无响应）
- 数据边界（0、最大值、负数）
- 用户行为异常（快速点击、并发操作）
- 并发场景（多用户同时操作）
- 兼容性问题（多端、多语言）

## 功能模块

---

## 模块一：需求分析与测试策略

### 1.1 需求理解与分析

**功能**:
- 从用户故事 (User Story) 提取测试点
- 识别功能需求和非功能需求
- 生成测试策略文档

**输出格式**:
```
📋 测试策略文档

## 功能测试点
1. 登录功能
   - [ ] 正确账号密码登录成功
   - [ ] 错误密码登录失败
   - [ ] 空账号登录提示
   - [ ] 账号锁定后登录

2. 个人信息修改
   - [ ] 修改昵称
   - [ ] 修改头像
   - [ ] 修改手机号

## 非功能测试点
1. 性能
   - 登录响应时间 < 2s
   - 并发 100 用户

2. 安全
   - SQL 注入防护
   - XSS 防护

3. 兼容性
   - Chrome/Firefox/Safari
   - iOS/Android
```

### 1.2 测试范围评估

**功能**:
- 分析需求文档
- 确定测试深度 (Positive/Negative/Edge cases)
- 识别测试依赖

---

## 模块二：测试用例编写（黑盒测试方法论）

### 2.1 测试用例生成

**功能**:
- 基于需求生成测试用例
- 覆盖正常场景、边界条件、异常情况
- 生成测试用例矩阵
- **必须采用黑盒测试方法论**

#### 测试用例模板（生产级标准）

```markdown
| 用例ID | 测试模块 | 用例标题 | 测试方法 | 前置条件 | 测试步骤 | 预期结果 | 优先级 |
|--------|----------|----------|----------|----------|----------|----------|--------|
| TC001 | 登录 | 正常登录 | 场景法 | 用户未登录 | 1.输入正确账号密码 2.点击登录 | 登录成功，跳转首页 | P0 |
| TC002 | 登录 | 错误密码登录 | 等价类 | 用户未登录 | 1.输入正确账号 2.输入错误密码 3.点击登录 | 提示密码错误 | P0 |
| TC003 | 登录 | 用户名为空 | 边界值 | 用户未登录 | 1.用户名字段留空 2.输入密码 3.点击登录 | 提示用户名不能为空 | P0 |
| TC004 | 登录 | 密码边界-超长 | 边界值 | 用户未登录 | 1.输入超长密码(1000字符) 2.点击登录 | 提示密码过长或正常处理 | P1 |
| TC005 | 登录 | SQL注入尝试 | 安全测试 | 用户未登录 | 1.输入"' or '1'='1" 2.任意密码 | 登录失败，无SQL注入漏洞 | P0 |
| TC006 | 登录 | 并发登录 | 性能测试 | 用户未登录 | 1.100人同时登录 | 正常响应，无崩溃 | P1 |
```

#### 测试用例模板（字段级别细化）

```markdown
| 用例ID | 测试模块 | 用例标题 | 测试方法 | 前置条件 | 测试步骤 | 预期结果 | 优先级 |
|--------|----------|----------|----------|----------|----------|----------|--------|
| TC-001 | 退款 | 退款金额=打赏金额 | 等价类 | A充值$10，打赏给B$10 | 1.A申请退款$10 2.调用API POST /api/refund 3.body: {amount: 10, orderId: "xxx"} | B账户扣减$10等值金币 | P0 |
| TC-002 | 退款 | 退款金额<0 | 边界值 | A有打赏记录 | 1.A申请退款$-5 2.POST /api/refund 3.body: {amount: -5} | 返回400，提示"退款金额必须大于0" | P0 |
| TC-003 | 退款 | 退款金额>打赏金额 | 边界值 | A打赏$10 | 1.A申请退款$15 2.POST /api/refund 3.body: {amount: 15} | 返回400，提示"超过可退金额" | P0 |
```

### 2.2 黑盒测试方法论应用指南

#### 等价类划分示例
- **充值金额有效等价类**: 0.99 ≤ 金额 ≤ 500
- **充值金额无效等价类**: 金额 ≤ 0，金额 > 500，非数字
- **用户身份等价类**: 普通用户、公会长、主播、BD、超管

#### 边界值分析示例
- **有效直播天数**: 0天、1天、30天、31天
- **PK时长**: 0秒、1秒、300秒（5分钟）
- **金额边界**: 0、0.01、499.99、500

#### 因果图应用示例
- **PK结果判定因果关系**:
  - 原因: A贡献值 > B贡献值、A贡献值 = B贡献值、时间到
  - 结果: A胜、平局、B胜
- **薪资计算触发条件**:
  - 原因: 结算周期结束、数据完整、审核通过
  - 结果: 发送薪资通知、计算工资

#### 状态迁移示例
- **PK状态**: 空闲 → 邀请中 → PK中 → 结束
- **订单状态**: 待支付 → 支付中 → 已支付 → 已完成

### 2.3 测试用例评审检查

**检查项**:
- [ ] 覆盖所有需求点
- [ ] 测试步骤清晰可执行（细化到字段级别）
- [ ] 预期结果明确（可验证）
- [ ] 优先级合理
- [ ] 无重复用例
- [ ] **已标注测试方法论**
- [ ] **覆盖隐含场景（网络异常、边界值、安全）**

### 2.4 测试数据准备

**功能**:
- 生成测试数据
- 边界值测试数据
- 异常测试数据
- **按等价类划分准备数据**

---

## 模块三：单元测试（基于黑盒测试方法论）

### 3.1 单元测试生成

#### 支持框架
- **Jest** (JavaScript/TypeScript)
- **Vitest** (Vue/Vite 项目)
- **Pytest** (Python)
- **JUnit** (Java)
- **Go test** (Go)

#### 黑盒测试方法论在单元测试中的应用

**等价类划分** - 为每个函数划分有效/无效输入：
```tsx
// 验证邮箱函数
describe('validateEmail', () => {
  // 有效等价类
  it('合法邮箱格式 test@example.com', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });
  
  // 无效等价类
  it('非法格式-无@', () => {
    expect(validateEmail('testexample.com')).toBe(false);
  });
  
  it('非法格式-无域名', () => {
    expect(validateEmail('test@')).toBe(false);
  });
});
```

**边界值分析** - 测试边界条件：
```tsx
describe('calculateDiscount', () => {
  it('金额为0边界', () => {
    expect(calculateDiscount(0)).toBe(0);
  });
  
  it('金额为0.01最小值', () => {
    expect(calculateDiscount(0.01)).toBe(0);
  });
  
  it('金额为最大值边界', () => {
    expect(calculateDiscount(999999)).toBeDefined();
  });
});
```

**错误推测** - 测试异常情况：
```tsx
describe('divide', () => {
  it('除数为0-应抛异常', () => {
    expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
  });
  
  it('除数为负数', () => {
    expect(divide(10, -2)).toBe(-5);
  });
  
  it('非数字输入-应处理', () => {
    expect(divide('10', 2)).toBeDefined(); // 或抛出类型错误
  });
});
```

#### 生成规则

**React 组件测试**:
```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('应该正确提交表单', () => {
    const mockOnSubmit = jest.fn();
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    fireEvent.change(screen.getByLabelText('账号'), { target: { value: 'test' } });
    fireEvent.change(screen.getByLabelText('密码'), { target: { value: '123456' } });
    fireEvent.click(screen.getByRole('button', { name: '登录' }));
    
    expect(mockOnSubmit).toHaveBeenCalledWith({ username: 'test', password: '123456' });
  });

  it('账号为空时应该显示错误', () => {
    const mockOnSubmit = jest.fn();
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    fireEvent.click(screen.getByRole('button', { name: '登录' }));
    
    expect(screen.getByText('账号不能为空')).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
```

**函数测试**:
```tsx
// util.ts
export function validateEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// util.test.ts
import { validateEmail } from './util';

describe('validateEmail', () => {
  it('应该返回 true 对于合法邮箱', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  it('应该返回 false 对于非法邮箱', () => {
    expect(validateEmail('invalid')).toBe(false);
    expect(validateEmail('test@')).toBe(false);
    expect(validateEmail('@example.com')).toBe(false);
  });

  it('应该返回 false 对于空字符串', () => {
    expect(validateEmail('')).toBe(false);
  });
});
```

### 3.2 测试覆盖率优化

**功能**:
- 分析现有测试覆盖率
- 识别未覆盖的代码路径
- 生成覆盖率报告

**覆盖率目标**:
- 语句覆盖率: > 80%
- 分支覆盖率: > 75%
- 函数覆盖率: > 90%

### 3.3 Mock 与 Stub

**功能**:
- 自动生成 Mock
- 模拟 API 响应
- 模拟依赖模块

```tsx
// Mock API
jest.mock('./api', () => ({
  fetchUser: jest.fn(() => Promise.resolve({ id: 1, name: 'Test' }))
}));

// Mock 模块
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;
mockedAxios.get.mockResolvedValue({ data: { id: 1 } });
```

### 3.4 测试重构

**功能**:
- 识别重复测试代码
- 提取公共测试逻辑
- 优化测试结构

---

## 模块四：E2E 测试

### 4.1 Playwright 测试

#### 4.1.1 基础测试结构
```typescript
import { test, expect } from '@playwright/test';

test.describe('用户登录', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('正常登录流程', async ({ page }) => {
    await page.fill('[data-testid=username]', 'test@example.com');
    await page.fill('[data-testid=password]', 'password123');
    await page.click('[data-testid=login-button]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('.user-name')).toContainText('Test User');
  });

  test('错误密码应该提示错误', async ({ page }) => {
    await page.fill('[data-testid=username]', 'test@example.com');
    await page.fill('[data-testid=password]', 'wrongpassword');
    await page.click('[data-testid=login-button]');
    
    await expect(page.locator('.error-message')).toContainText('密码错误');
  });
});
```

#### 4.1.2 Page Object Model
```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.page.fill('[data-testid=username]', username);
    await this.page.fill('[data-testid=password]', password);
    await this.page.click('[data-testid=login-button]');
  }

  async getErrorMessage() {
    return this.page.locator('.error-message').textContent();
  }
}

// tests/login.spec.ts
test('登录测试', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('test@example.com', 'password123');
  
  await expect(page).toHaveURL('/dashboard');
});
```

#### 4.1.3 API Mock
```typescript
test('模拟 API 响应', async ({ page }) => {
  await page.route('**/api/user', async route => {
    await route.fulfill({
      status: 200,
      body: JSON.stringify({ id: 1, name: 'Mock User' })
    });
  });
  
  await page.goto('/profile');
  await expect(page.locator('.user-name')).toContainText('Mock User');
});
```

#### 4.1.4 网络拦截
```typescript
test('验证 API 请求', async ({ page }) => {
  const request = await page.waitForRequest('**/api/login');
  
  await page.fill('[data-testid=username]', 'test@example.com');
  await page.click('[data-testid=login-button]');
  
  expect(request.postDataJSON()).toEqual({
    username: 'test@example.com',
    password: 'password123'
  });
});
```

### 4.2 Cypress 测试

#### 4.2.1 基础测试
```javascript
describe('用户登录', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('正常登录', () => {
    cy.get('[data-testid=username]').type('test@example.com');
    cy.get('[data-testid=password]').type('password123');
    cy.get('[data-testid=login-button]').click();
    
    cy.url().should('include', '/dashboard');
    cy.get('.user-name').should('contain', 'Test User');
  });
});
```

#### 4.2.2 模拟 API
```javascript
it('模拟 API 响应', () => {
  cy.intercept('GET', '**/api/user', {
    statusCode: 200,
    body: { id: 1, name: 'Mock User' }
  }).as('getUser');
  
  cy.visit('/profile');
  cy.wait('@getUser');
  cy.get('.user-name').should('contain', 'Mock User');
});
```

### 4.3 移动端测试 (Detox/Appium)

#### Detox 示例 (React Native)
```typescript
describe('登录流程', () => {
  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('正常登录', async () => {
    await element(by.id('username')).typeText('test@example.com');
    await element(by.id('password')).typeText('password123');
    await element(by.id('login-button')).tap();
    
    await expect(element(by.id('dashboard'))).toBeVisible();
  });
});
```

---

## 模块五：集成测试

### 5.1 API 集成测试
```typescript
describe('用户 API', () => {
  it('应该创建用户', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'test@example.com' })
      .expect(201);
    
    expect(response.body).toHaveProperty('id');
    expect(response.body.name).toBe('Test');
  });

  it('应该验证邮箱格式', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'invalid' })
      .expect(400);
    
    expect(response.body.error).toContain('邮箱格式错误');
  });
});
```

### 5.2 数据库集成测试
```typescript
describe('用户仓库', () => {
  beforeEach(async () => {
    await db.clear('users');
  });

  it('应该保存用户', async () => {
    const user = await userRepository.create({
      name: 'Test',
      email: 'test@example.com'
    });
    
    expect(user.id).toBeDefined();
    
    const saved = await userRepository.findById(user.id);
    expect(saved.name).toBe('Test');
  });
});
```

---

## 模块六：测试报告与度量

### 6.1 测试报告生成

**功能**:
- 汇总测试执行结果
- 生成测试覆盖率报告
- 统计测试通过率

**报告模板**:
```
📊 测试报告

## 执行摘要
- 总测试数: 150
- 通过: 145 (96.67%)
- 失败: 5 (3.33%)
- 跳过: 0

## 覆盖率
- 语句覆盖率: 82.5%
- 分支覆盖率: 76.3%
- 函数覆盖率: 91.2%

## 失败用例
1. TC045 - 登录-错误密码提示 (Element not found)
2. TC078 - 支付-超时处理 (Timeout)

## 风险评估
- 高风险: 支付模块 (未覆盖边界场景)
- 中风险: 用户中心 (部分 API 未测试)
```

### 6.2 测试度量分析

**指标**:
- 测试执行时间
- 测试稳定性 (Flaky rate)
- 代码覆盖率趋势
- 测试缺陷比

---

## 模块七：测试环境管理

### 7.1 测试配置

**Jest 配置**:
```javascript
module.exports = {
  testEnvironment: 'jsdom',
  collectCoverage: true,
  coverageThreshold: {
    branches: 75,
    functions: 90,
    lines: 80,
    statements: 80
  },
  setupFilesAfterEnv: ['<rootDir>/setupTests.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  }
};
```

**Playwright 配置**:
```typescript
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests',
  retries: 2,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['json', { outputFile: 'test-results.json' }]],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry'
  }
});
```

### 7.2 CI/CD 集成

**GitHub Actions**:
```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run test:coverage
      - run: npm run test:e2e
```

---

## 模块八：测试最佳实践

### 8.1 测试命名规范

**结构**: `[模块]_[场景]_[预期结果]`

```typescript
// Good
it('应该正确处理空数组返回 false', () => { });
it('登录失败时应该显示错误提示', () => { });

// Bad
it('test1', () => { });
it('登录', () => { });
```

### 8.2 测试分层策略

| 层级 | 占比 | 框架 | 目的 |
|------|------|------|------|
| 单元测试 | 70% | Jest/Vitest | 快速反馈 |
| 集成测试 | 20% | Jest/Supertest | 验证交互 |
| E2E 测试 | 10% | Playwright | 端到端验证 |

### 8.3 测试数据管理

**原则**:
- 使用工厂模式生成测试数据
- 每个测试独立数据
- 测试后清理数据

```typescript
// 工厂函数
async function createUser(overrides = {}) {
  return await User.create({
    name: 'Test User',
    email: 'test@example.com',
    ...overrides
  });
}

// 测试中使用
it('应该更新用户', async () => {
  const user = await createUser({ name: 'Old Name' });
  await user.update({ name: 'New Name' });
  expect(user.name).toBe('New Name');
});
```

---

## 输出格式

### 测试用例输出
```markdown
## 测试用例: 用户登录

### TC001 - 正常登录
- **优先级**: P0
- **前置条件**: 用户未登录
- **测试步骤**:
  1. 打开登录页面
  2. 输入正确账号: test@example.com
  3. 输入正确密码: password123
  4. 点击登录按钮
- **预期结果**: 
  - 跳转至首页
  - 显示用户信息

### TC002 - 错误密码
- **优先级**: P0
- **前置条件**: 用户未登录
- **测试步骤**:
  1. 打开登录页面
  2. 输入正确账号
  3. 输入错误密码
  4. 点击登录按钮
- **预期结果**: 显示错误提示
```

### 代码生成输出
```typescript
// 测试文件: src/components/__tests__/LoginForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from '../LoginForm';

describe('LoginForm', () => {
  // ... 测试代码
});
```

---

## 适用框架

| 类别 | 框架 | 支持 |
|------|------|------|
| 单元测试 | Jest | ✅ |
| 单元测试 | Vitest | ✅ |
| 单元测试 | Pytest | ✅ |
| E2E 测试 | Playwright | ✅ |
| E2E 测试 | Cypress | ✅ |
| 移动端 | Detox | ✅ |
| 移动端 | Appium | ✅ |
| API 测试 | Supertest | ✅ |
| API 测试 | REST-assured | ✅ |

---

## 使用示例

### 示例 1: 生成测试用例
```
用户: 为用户登录功能生成测试用例
Skill: 分析需求，生成完整的测试用例矩阵
```

### 示例 2: 编写单元测试
```
用户: 为这个函数写单元测试
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
Skill: 生成完整的 Jest 测试文件
```

### 示例 3: 编写 E2E 测试
```
用户: 写一个登录流程的 Playwright 测试
Skill: 生成完整的 E2E 测试代码
```

### 示例 4: 分析测试覆盖率
```
用户: 检查测试覆盖率并给出优化建议
Skill: 运行覆盖率分析，识别未覆盖代码
```

---

## 注意事项

1. 测试代码应与生产代码同等质量
2. 保持测试独立性，避免相互依赖
3. 测试数据应可重复使用
4. 定期清理过时测试用例
5. E2E 测试应使用稳定的 selectors (data-testid)

---

## 附录：黑盒测试方法论快速参考

### A.1 等价类划分快速指南

| 输入类型 | 有效等价类 | 无效等价类 |
|----------|-----------|-----------|
| 数值范围 | 0 < x ≤ 500 | x ≤ 0, x > 500, 非数字 |
| 字符串 | 2-20字符 | < 2, > 20, 空 |
| 邮箱 | 合法邮箱格式 | 无@, 无域名, 包含空格 |
| 日期 | 有效日期范围 | 过去日期, 未来日期, 非法格式 |

### A.2 边界值快速指南

| 类型 | 边界值 |
|------|--------|
| 数值范围 | 最小值, 最小值+1, 最大值-1, 最大值 |
| 字符串 | 0字符, 1字符, 最大-1字符, 最大字符 |
| 数组 | 空数组, 1个元素, 满数组 |
| 时间 | 0秒, 1秒, 59秒, 60秒 |

### A.3 隐含测试场景清单

- [ ] 网络异常（断网、延迟、高延迟）
- [ ] 服务器超时
- [ ] 接口返回错误码
- [ ] 并发请求
- [ ] 重复提交
- [ ] 快速连续点击
- [ ] 越权访问
- [ ] 参数篡改
- [ ] Session/Cookie 失效
- [ ] 数据边界（0、负数、超大值）
- [ ] 空数据、空列表
- [ ] 多语言/国际化
- [ ] 跨时区
- [ ] 多端兼容（iOS/Android/Web）
- [ ] 弱网环境

### A.4 生产级用例评估标准

| 评估项 | 标准 |
|--------|------|
| 可执行性 | 测试步骤明确到可由任何人执行 |
| 可验证性 | 预期结果可自动化验证 |
| 独立性 | 测试用例间无依赖 |
| 覆盖率 | 覆盖正常+异常+边界 |
| 方法论 | 每条用例标注测试方法 |
| 粒度 | 细化到接口/字段级别 |