---
name: playwright-performance-optimization
category: software-development
description: "Playwright E2E 测试性能优化的10个实战技巧。从45分钟压缩到8分钟的经验总结：并行化、浏览器复用、选择性执行、智能等待、数据预置、资源拦截、测试分割、缓存登录态、基础设施优化、持续监控。"
---

# Playwright 性能优化：缩短测试时间的 10 个实用技巧

> 来源：https://cloud.tencent.com/developer/article/2621628（霍格沃兹-测试开发学社，腾讯云开发者社区）
> 原文将 45 分钟测试套件缩减到 8 分钟，以下为经过实战验证的 10 个技巧。

## 何时使用本 skill

- E2E 测试套件执行时间太长（10min+），需要优化
- CI 流水线测试环节是瓶颈
- Playwright 测试不稳定、经常超时
- 测试脚本中存在大量 `waitForTimeout` / `sleep`
- 需要建立分层测试策略（冒烟 / 回归 / 全量）

---

## 技巧 1：并行化（性价比最高）

Playwright 原生支持并行，调整配置即可：

```ts
// playwright.config.ts
export default {
  workers: process.env.CI ? 4 : 2, // CI 用 4 个 worker，本地用 2 个
  fullyParallel: true, // 所有测试文件并行执行
  // 有全局状态依赖时改为：
  // fullyParallel: false,
  // 但依然保持 worker 数量
};
```

**要点**：保证测试文件独立性。共享数据库用 `beforeAll` / `afterAll` 管理隔离。
**效果**：仅此一项即可减少 65% 执行时间。

---

## 技巧 2：浏览器复用（减少启动开销）

每个测试都启动新浏览器 → 复用实例：

```ts
// 手动管理浏览器实例
let browser: Browser;

test.beforeAll(async () => {
  browser = await chromium.launch();
});

test.beforeEach(async ({ page }) => {
  const context = await browser.newContext();
  page = await context.newPage();
});
```

**注意**：每个测试必须用独立的 `browserContext`，防止状态污染。

---

## 技巧 3：选择性执行（分层策略）

不是每次提交都跑全量，建立分层：

```json
{
  "scripts": {
    "test:smoke": "playwright test --grep '@smoke'",
    "test:regression": "playwright test --grep '@regression'",
    "test:changed": "playwright test $(git diff --name-only HEAD~1 | grep -E '\\.spec\\.ts$')"
  }
}
```

标签用法：

```ts
test('关键登录流程 @smoke', async ({ page }) => { /* 每次 CI 执行 */ });
test('边界条件测试 @regression', async ({ page }) => { /* 每日执行 */ });
```

**最佳实践**：pre-commit 钩子只跑 `@smoke`，夜间 CI 跑完整套件。

---

## 技巧 4：智能等待（告别硬编码 sleep）

```ts
// ❌ 糟糕
await page.waitForTimeout(5000);

// ✅ 正确
await page.waitForLoadState('networkidle');
await page.locator('.data-loaded').waitFor({ state: 'visible' });

// 等待 API 请求完成
const responsePromise = page.waitForResponse('/api/data');
await page.click('#load-data');
const response = await responsePromise;

// 自定义条件
await page.waitForFunction(() => document.querySelectorAll('.item').length >= 10);
```

**效果**：平均等待时间从固定 5 秒降到 0.5-2 秒。

---

## 技巧 5：数据预置（而非动态生成）

避免测试中执行耗时操作。预置测试数据 + 快照恢复：

```ts
// 全局 setup
async function globalSetup() {
  await seedDatabase({
    standardUsers: 5,
    adminUsers: 1,
    products: 50
  });
}

// 测试中直接使用预置数据
test('用户操作', async ({ page }) => {
  await page.goto(`/user/${process.env.TEST_USER_ID}`);
});
```

---

## 技巧 6：资源拦截（阻止不必要的加载）

拦截图片、字体、分析脚本等对测试无价值的资源：

```ts
// 在 beforeEach 中
await page.route('**/*.{png,jpg,jpeg,gif,svg}', route => route.abort());
await page.route('**/analytics.js', route => route.abort());
await page.route('**/ads/*', route => route.abort());

// 精细控制
await page.route('**/*', route => {
  const type = route.request().resourceType();
  if (['image', 'media', 'font'].includes(type)) return route.abort();
  return route.continue();
});
```

**效果**：页面加载时间平均减少 40%。

---

## 技巧 7：测试分割（平衡并行与串行）

混合策略效果更好：

```ts
export default {
  projects: [
    {
      name: '串行-关键路径',
      testMatch: '**/*.critical.spec.ts',
      fullyParallel: false,
      workers: 1
    },
    {
      name: '并行-功能测试',
      testMatch: '**/*.spec.ts',
      testIgnore: '**/*.critical.spec.ts',
      fullyParallel: true,
      workers: 4
    }
  ]
};
```

或在一个文件中混合：

```ts
test.describe.serial('用户注册流程', () => {
  test('步骤1: 填写信息', () => {});
  test('步骤2: 验证邮箱', () => {});
});

test.describe('商品浏览功能', () => {
  test('搜索商品', () => {});
  test('筛选结果', () => {});
});
```

---

## 技巧 8：缓存利用（复用登录状态）

登录通常是测试中最耗时的部分：

```ts
// storageState.ts — 创建可复用的认证状态
import { test as setup } from '@playwright/test';

setup('准备登录状态', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#username', 'testuser');
  await page.fill('#password', 'password123');
  await page.click('#submit');
  await page.waitForURL('/dashboard');
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
```

```ts
// playwright.config.ts
export default {
  use: {
    storageState: 'playwright/.auth/user.json'
  },
  globalSetup: require.resolve('./storageState.ts')
};
```

**注意**：定期更新缓存状态，避免会话过期。

---

## 技巧 9：基础设施优化（硬件与环境）

CI 分片执行 + Node.js LTS + SSD：

```yaml
# GitHub Actions 示例
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: |
          npm ci --omit=dev --ignore-scripts
          npm install @playwright/test playwright
      - run: npx playwright test --shard=${{ matrix.shard }}/${{ strategy.job-total }}
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report-${{ matrix.shard }}
          path: playwright-report/
```

**本地**：Node.js 最新 LTS（V8 优化提升执行速度）+ SSD。

---

## 技巧 10：持续监控（建立性能基线）

```ts
test('性能回归检查', async ({ page }) => {
  const startTime = Date.now();
  await page.goto('/dashboard');
  await page.click('#load-report');
  await page.waitForSelector('.report-loaded');
  const duration = Date.now() - startTime;
  expect(duration).toBeLessThan(3000); // 必须小于 3 秒
});
```

开启 trace 分析慢测试：

```ts
export default {
  use: {
    trace: process.env.CI ? 'on-first-retry' : 'retain-on-failure',
  }
};
```

**建议**：建立仪表板跟踪每次提交的测试执行时间，某测试突然变慢时立即告警。

---

## 实战组合拳

1. **先上并行化** — 见效最快
2. **优化等待逻辑和数据准备** — 消除硬等待
3. **实现分层测试和资源拦截** — 减少不必要的执行和加载
4. **基础设施和监控** — 巩固成果

**原则**：优化基于数据。使用 `--reporter=line` 查看每个测试的时间，优先优化最耗时的 10%。有些测试本身就慢（如完整业务流程），不要过度优化。

## 英文关键命令备注

| 场景 | 命令 |
|------|------|
| 冒烟测试 | `npx playwright test --grep '@smoke'` |
| 分片执行 | `npx playwright test --shard 1/4` |
| 查看测试耗时 | `npx playwright test --reporter=line` |
| 生成 trace | `npx playwright show-trace trace.zip` |
