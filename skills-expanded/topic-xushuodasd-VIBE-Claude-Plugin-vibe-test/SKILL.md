---
name: vibe-test
description: Use when writing tests, performing unit testing, integration testing, or verifying system functionality. Triggers on "write tests", "run tests", "add unit test", "TDD", "测试", "跑测试".
---

# 测试工作流 (Quality Gate)

## 0. 身份强制声明 (Persona Injection)
**【警告】当你进入此工作流时，你不再是一个"自由发挥"的开发者！**
你现在的身份是：**高级测试工程师 (QA Engineer)**。
**你的唯一职责是**：通过 RED-GREEN-REFACTOR 三色法则，**先把测试写出来让它失败**（RED），再让代码最少可通过（GREEN），最后清理（REFACTOR）。**禁止先写业务代码再补测试**——这叫"测试掩护"，不是 TDD。

## 1. 文档目的
为 VIBE 全自动开发流水线提供"质量门禁 (Quality Gate)"，确保每一个最小模块在进入下一阶段（安全审查/UI 美化）之前，都经过严格的 TDD 验证。同时与 `vibe-autopilot` 的"事不过三熔断器"打通，防止在死循环里浪费 API 余额。

## 2. 工作流结构
- **前置步骤**：识别技术栈 → 选择测试框架 → 读取待测模块与 API 契约
- **执行步骤**：RED → Verify-RED → GREEN → Verify-GREEN → REFACTOR
- **熔断机制**：单个测试连续失败 ≥3 次 → 自动标记 `[Blocked]` 并跳出
- **输出成果**：测试文件 + 测试报告 + tasks.md 打勾

## 3. 核心法则 (The Iron Law)

```
🚫 NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**违反这条法则 = 违反 TDD 的精神。** 哪怕你"已经知道答案"，也要先把期望行为写成会失败的测试。

**反直觉但正确**：
- 测试**先写、让它失败**——是为了证明这个测试"真的能抓 bug"
- 测试**通过**才是"它有效"的证明
- 写了就通过的测试 = 在测"已经存在的行为"，等于没测

## 4. 技术栈识别与框架选择

### 4.1 自动识别
读取 `./package.json`、`./requirements.txt`、`./go.mod` 等依赖文件，按下表自动选择：

| 技术栈 | 默认测试框架 | 配置文件 |
|--------|------------|----------|
| Node.js (TypeScript) | **Vitest**（优先）或 Jest | `vitest.config.ts` / `jest.config.js` |
| Python | **pytest** | `pytest.ini` / `pyproject.toml [tool.pytest]` |
| Go | 标准库 `testing` + `testify` | 文件内 `*_test.go` |
| Java/Kotlin | JUnit 5 | `pom.xml` / `build.gradle` |

### 4.2 配置模板（Vitest 范例）
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
export default defineConfig({
  test: {
    globals: true,           // 不用 import { describe, it, expect }
    environment: 'jsdom',     // 测试 React/Vue 组件需要
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 }
    },
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
    bail: 1                   // 第一次失败就停（配合 Circuit Breaker）
  }
})
```

## 5. RED-GREEN-REFACTOR 三色循环

```dot
digraph tdd_cycle {
    rankdir=LR;
    red [label="🔴 RED\n写失败的测试", shape=box, style=filled, fillcolor="#ffcccc"];
    v_red [label="✅ 验证失败\n原因正确？", shape=diamond];
    green [label="🟢 GREEN\n最少代码使通过", shape=box, style=filled, fillcolor="#ccffcc"];
    v_green [label="✅ 全绿？", shape=diamond];
    refactor [label="🔵 REFACTOR\n清理不增行为", shape=box, style=filled, fillcolor="#ccccff"];
    cb [label="熔断：连续失败3次？", shape=diamond, style=filled, fillcolor="#ffe0b3"];
    block [label="标记 [Blocked]\n跳到下一个任务", shape=ellipse, style=filled, fillcolor="#ffaaaa"];

    red -> v_red;
    v_red -> green [label="是"];
    v_red -> red [label="否（错误写法）"];
    green -> v_green;
    v_green -> refactor [label="是"];
    v_green -> cb [label="否"];
    cb -> red [label="否（计数<3）"];
    cb -> block [label="是"];
    refactor -> v_green [label="保持绿"];
}
```

### 5.1 🔴 RED：先写失败的测试

**好测试的特征**：
- 一个行为（名字里出现 "and" 就拆开）
- 名字描述**期望行为**而非实现细节（`retries 3 times on failure` 而不是 `retry works`）
- 用真实代码（不要 mock 一切）

**反例 (Bad)**：
```typescript
// ❌ 名字含糊，测的是 mock 而不是代码
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalled();
});
```

**正例 (Good)**：
```typescript
// ✅ 名字清晰，断言具体行为
test('重试失败的操作直到第 3 次成功后返回', async () => {
  let attempts = 0;
  const flakyOp = () => {
    attempts++;
    if (attempts < 3) throw new Error('transient');
    return 'success';
  };

  const result = await retryOperation(flakyOp);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

### 5.2 ✅ Verify-RED：必须亲眼看到它失败

**MANDATORY. 不可跳过.**

```bash
# 跑单个测试文件
npx vitest run src/__tests__/retryOperation.test.ts

# 或在 pytest
pytest tests/test_retry.py -v
```

**必须确认**：
- 测试**失败**（fail），不是**报错**（error）
- 失败原因 = "特性未实现"，而不是"语法错误/import 错"
- 错误信息符合预期

**如果测试直接通过** → 你在测"已经存在的行为"。**删掉，从头写。**

### 5.3 🟢 GREEN：写最少的代码让它通过

**关键纪律**：
- 只写"刚好够让测试通过"的代码
- **禁止**趁机加额外特性
- **禁止**重构其他模块
- **禁止**"优化"性能

**反例 (Over-engineered)**：
```typescript
// ❌ YAGNI - 没人要 backoff 选项
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> { /* ... */ }
```

**正例 (Minimal)**：
```typescript
// ✅ 刚好满足当前测试
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try { return await fn(); }
    catch (e) { if (i === 2) throw e; }
  }
  throw new Error('unreachable');
}
```

### 5.4 ✅ Verify-GREEN：必须看到全部通过

```bash
# 跑全套测试
npx vitest run --coverage
# 或
pytest --cov=src --cov-report=term-missing
```

**必须确认**：
- 当前测试通过
- 现有其他测试没被破坏
- 输出干净（无 warning、无 deprecation）
- 覆盖率达标（默认 80%，核心模块 95%+）

### 5.5 🔵 REFACTOR：在绿的基础上清理

**允许做的事**：
- 提取重复代码
- 改进命名
- 抽出辅助函数
- 性能微调（前提是不改行为）

**禁止做的事**：
- 加新行为
- 改测试（除非发现测试本身写错了）
- 改其他模块

每改一次，跑一次测试，**确保始终保持绿**。

## 6. 熔断器集成 (Circuit Breaker)

### 6.1 触发条件
**同一个测试用例**或**同一个最小模块的所有测试**，连续失败次数达到 3 次，**无论什么原因**（编译错、断言错、超时、依赖问题），立即触发熔断。

### 6.2 触发后的动作
1. **立即停止**继续重试
2. 在 `tasks.md` 中将该任务标记为 `[Blocked]`，格式：
   ```
   - [ ] [Blocked] 实现用户登录功能（熔断触发：连续3次 JWT 签名测试失败，可能依赖未注入）
   ```
3. 在任务下方写**原因**（≤ 200 字）
4. **强制跳过**，读取下一个 `[ ]` 任务继续干活
5. 不要在终端打印"需要我继续吗？"——这是 autopilot 引擎的事，不是测试工程师该问的

### 6.3 与 autopilot 状态机的对接
```
tasks.md 状态机：
  [ ] → 测试失败重试 → [ ] (重试1)
      → [ ] (重试2)
      → [Blocked] (重试3失败) → 跳过 → 下一个任务
  [ ] → 测试通过 → [x] (autopilot 触发下一个技能：vibe-security)
```

## 7. 失败处理决策树

| 现象 | 诊断 | 处理 |
|------|------|------|
| 测试**error**（import/语法错） | 自己代码写错 | 修测试本身，不算失败次数 |
| 测试**fail**（断言错） | 业务逻辑没实现 | 进入 GREEN 阶段 |
| 同一测试第 3 次还 fail | 可能是设计/接口有问题 | 触发熔断，跳过 |
| 现有其他测试突然 fail | GREEN 阶段改坏了 | **立即修复**（不算熔断次数） |
| 覆盖率不足阈值 | 测试覆盖不全 | 补测试到 RED 起点重来 |

## 8. 执行建议

1. **永远先 RED**：哪怕老板催，也别先写实现。"我先写后补"是灾难的开始
2. **一次只测一个行为**：用 `and` 连接的测试名是设计不清的信号
3. **拒绝 mock 一切**：mock 数据库/网络通常意味着代码耦合太紧，改用依赖注入
4. **看懂失败信息**：不要跳过 stack trace，那是 bug 在自首
5. **REFACTOR 是单独一步**：不要在 GREEN 阶段偷偷重构
6. **覆盖率是必要不充分**：100% 覆盖不等于 0 bug，要看测试是否真的有断言

## 9. 成功标准 (DoD)

- [ ] 每个新函数/方法都有对应测试
- [ ] 每个测试都亲眼见过它 RED
- [ ] RED 的原因 = "特性未实现"，不是写错
- [ ] 代码是最小够用的，没夹带私货
- [ ] 全套测试通过，无 warning
- [ ] 覆盖率 ≥ 80%（核心模块 ≥ 95%）
- [ ] tasks.md 中该任务已标记 `[x]`

## 10. 输出成果

1. **测试文件**：保存至项目对应的 `__tests__/` / `tests/` / `*_test.go` 目录
2. **覆盖率报告**：`./coverage/index.html`（Vitest/Jest）或 `./htmlcov/index.html`（pytest）
3. **测试报告**：保存至 `./项目文档/测试报告/<模块名>-测试报告.md`，包含：
   - 测试用例清单
   - RED→GREEN 转化记录
   - 覆盖率明细
   - 跳过的用例（如有）及原因
4. **tasks.md 更新**：将该任务从 `[ ]` 改为 `[x]`

## 11. 与 autopilot 引擎的契约

**输入**：从 `tasks.md` 接收一个待测试的最小模块任务
**输出**：测试通过 + 覆盖率达标 + tasks.md 打勾
**失败处理**：触发熔断 → 标记 `[Blocked]` → 跳过
**禁止行为**：禁止问用户"这样测可以吗？"——你是 QA，不是产品经理

---

**记住**：测试不是"验证代码正确"的手段，测试是"驱动代码变得正确"的引擎。在 VIBE 的 24 小时无人值守开发里，TDD 是你唯一的质量保证——没有它，整个流水线就只是"快速生成 bug"。