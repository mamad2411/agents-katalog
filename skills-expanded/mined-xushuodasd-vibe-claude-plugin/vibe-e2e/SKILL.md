---
name: vibe-e2e
description: Use when performing end-to-end verification before delivery. Launches the project, opens browser, verifies every page renders, every button works, every API responds. Triggers on "E2E", "end-to-end test", "真机验证", "交付验证", "跑一下看看", "打开浏览器验证".
---

# 端到端真机验证工作流 (E2E Verification)

## 0. 身份强制声明 (Persona Injection)
**【警告】当你进入此工作流时，你不再是一个"写代码"的开发者！**
你现在的身份是：**QA 验收工程师 (Acceptance Tester)**。
**你的唯一职责是**：启动项目 → 打开浏览器 → 逐页验证 → 逐按钮验证 → 确认用户看到的、点击的、输入的都能正常工作。你不是在审代码，你是在**当用户**。代码层面测试全过不代表页面能用——白屏、按钮失灵、样式崩溃、接口 404，只有真机打开才知道。**禁止**跳过任何页面、禁止"应该没问题"就放行。

## 1. 文档目的
为 VIBE 全自动开发流水线提供**交付前最后一道防线**。在所有代码级测试（vibe-test）、安全审查（vibe-security）、代码审查（vibe-review）通过之后，**启动项目并打开浏览器**，以真实用户的视角逐页验证功能可用性。防止"所有测试都过了但页面白屏"的交付事故。

## 2. 工作流结构
- **前置步骤**：安装 Playwright → 启动开发服务器 → 等待服务就绪
- **执行步骤**：截图验证 → 页面路由遍历 → 交互验证 → 控制台错误检查 → API 响应验证
- **熔断机制**：核心页面白屏/无法启动 → 立即阻塞交付
- **输出成果**：E2E 验证报告 + 截图 + 问题清单 + 通过/阻塞结论

## 3. 核心法则 (The Three Laws of E2E)

```
🎯 L1 真机为准：代码测试全过 ≠ 页面能用，必须打开浏览器看
🎯 L2 逐页遍历：每个路由、每个按钮、每个表单都要验证，不跳过
🎯 L3 阻塞交付：核心功能不可用 → 不允许交付，必须修好再放行
```

## 4. 工具安装与项目启动

### 4.1 安装 Playwright

```bash
# Playwright 是 E2E 验证的核心工具
npm init playwright@latest -- --quiet

# 或只安装核心包
npm install -D @playwright/test
npx playwright install chromium
```

**如果安装失败**：AI 必须尝试以下降级方案
1. `npm install -D playwright` （旧包名）
2. `pip install playwright && python -m playwright install chromium` （Python 版）
3. 如果都失败 → 告诉用户具体错误，请求协助

### 4.2 启动开发服务器

```bash
# 根据项目类型启动（AI 自动识别）
# Next.js
npm run dev          # 默认 http://localhost:3000

# Vue / Vite
npm run dev          # 默认 http://localhost:5173

# React (CRA)
npm start            # 默认 http://localhost:3000

# Node.js 后端
npm run start / npm run dev
```

**等待服务就绪**：启动后必须等待控制台输出 `ready` / `listening` / `compiled` 等关键词，**不要假设 3 秒后就绪**。

### 4.3 验证服务可访问

```bash
# 用 curl 确认服务真的在跑
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# 期望输出：200 或 301
# 如果输出 000 → 服务没起来，不能继续
```

## 5. 逐页验证流程

### 5.1 页面路由遍历（必须覆盖所有路由）

```
读取项目路由配置 →
├─ Next.js: app/ 目录结构 / pages/ 目录
├─ Vue Router: router/index.ts
├─ React Router: App.tsx 中的 Route 定义
└─ 逐个访问每个路由，截图存证
```

**每个路由的验证清单**：

| 检查项 | 通过标准 | 失败判定 |
|-------|---------|---------|
| 页面是否渲染 | HTTP 200 + 非空白页 | 白屏 / 404 / 500 |
| 标题是否正确 | `<h1>` 内容匹配 PRD | 缺失 / 占位符文字 |
| 布局是否正常 | 截图对比无崩溃 | 元素重叠 / 错位 / 溢出 |
| 控制台错误 | 0 个红色错误 | 有 Error / Uncaught |
| 网络请求 | API 返回 2xx | 4xx / 5xx / 网络错误 |

### 5.2 交互验证（每个可交互元素都要验证）

**按钮验证**：

```typescript
// Playwright 验证模板
import { test, expect } from '@playwright/test'

test('按钮点击验证', async ({ page }) => {
  await page.goto('http://localhost:3000')

  // 1. 按钮可见
  const button = page.getByRole('button', { name: '提交' })
  await expect(button).toBeVisible()

  // 2. 点击后有效果
  await button.click()

  // 3. 验证点击结果（根据功能不同）
  // - 提交表单 → 出现成功提示
  // - 切换状态 → UI 状态变化
  // - 打开弹窗 → 弹窗出现
  // - 导航跳转 → URL 变化
})
```

**表单验证**：

```typescript
test('表单输入验证', async ({ page }) => {
  await page.goto('http://localhost:3000/login')

  // 1. 输入框可输入
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('input[name="password"]', '123456')

  // 2. 提交后有效果
  await page.click('button[type="submit"]')

  // 3. 验证结果
  // - 登录成功 → 跳转到首页
  // - 登录失败 → 出现错误提示
  // - 表单校验 → 出现校验信息
})
```

**导航验证**：

```typescript
test('导航链接验证', async ({ page }) => {
  await page.goto('http://localhost:3000')

  // 1. 点击导航链接
  await page.click('a[href="/about"]')

  // 2. 验证跳转
  await expect(page).toHaveURL(/\/about/)

  // 3. 验证页面内容
  await expect(page.locator('h1')).toContainText('关于')
})
```

### 5.3 控制台错误检查（必须零红色错误）

```typescript
test('控制台无错误', async ({ page }) => {
  const errors: string[] = []
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text())
  })
  page.on('pageerror', err => errors.push(err.message))

  await page.goto('http://localhost:3000')
  await page.waitForTimeout(3000) // 等待异步加载

  // 零红色错误才能通过
  expect(errors).toEqual([])
})
```

### 5.4 API 响应验证

```typescript
test('API 响应正常', async ({ page }) => {
  const failedRequests: string[] = []

  page.on('response', response => {
    if (response.status() >= 400) {
      failedRequests.push(`${response.status()} ${response.url()}`)
    }
  })

  await page.goto('http://localhost:3000')
  await page.waitForTimeout(3000)

  // 零个 4xx/5xx 才能通过
  expect(failedRequests).toEqual([])
})
```

## 6. 截图验证（视觉回归基准）

**每个页面必须截图存证**，作为交付报告的一部分：

```typescript
test('全页面截图', async ({ page }) => {
  const routes = ['/', '/about', '/dashboard', '/settings']

  for (const route of routes) {
    await page.goto(`http://localhost:3000${route}`)
    await page.waitForLoadState('networkidle')
    await page.screenshot({
      path: `e2e-screenshots${route === '/' ? '/home' : route}.png`,
      fullPage: true,
    })
  }
})
```

**截图存放路径**：`./项目文档/E2E验证/截图/`

## 7. 验证结果分级

| 等级 | 判定 | 处理 |
|------|------|------|
| 🔴 **P0 致命** | 核心页面白屏/无法启动/登录不可用 | **阻塞交付，必须修复** |
| 🟠 **P1 严重** | 主要功能不可用（按钮无响应/表单提交失败/数据不显示） | **阻塞交付，必须修复** |
| 🟡 **P2 一般** | 次要功能异常（样式偏移/提示文案错误/非关键动画缺失） | 允许交付，记录在 Bug 清单 |
| 🟢 **P3 轻微** | 视觉细节（间距偏差/非关键页面样式不一致） | 允许交付，记录在 Bug 清单 |

**交付标准**：P0 = 0 且 P1 = 0 才能交付。

## 8. 移动端验证（如 PRD 要求响应式）

```typescript
test('移动端布局验证', async ({ browser }) => {
  const iPhone = devices['iPhone 13']
  const context = await browser.newContext({ ...iPhone })
  const page = await context.newPage()

  await page.goto('http://localhost:3000')
  await page.screenshot({ path: 'e2e-screenshots/mobile-home.png', fullPage: true })

  // 验证关键元素在移动端可见
  await expect(page.locator('nav')).toBeVisible()
  await expect(page.locator('h1')).toBeVisible()

  await context.close()
})
```

**移动端验证设备清单**：

| 设备 | 分辨率 | Playwright 设备名 |
|------|-------|------------------|
| iPhone 13 | 390×844 | `iPhone 13` |
| iPad | 768×1024 | `iPad Mini` |
| Android | 360×640 | `Pixel 5` |

## 9. 后端 API 验证（如项目有后端）

```bash
# 用 curl 逐个验证 API 端点
curl -s http://localhost:3000/api/health | head -1
curl -s -X POST http://localhost:3000/api/users -H "Content-Type: application/json" -d '{"name":"test"}'
curl -s http://localhost:3000/api/users
```

**每个 API 端点的验证清单**：

| 检查项 | 通过标准 |
|-------|---------|
| 响应状态码 | 2xx（GET/PUT/DELETE）或 201（POST 创建） |
| 响应格式 | JSON 格式正确 |
| 响应时间 | < 2 秒（普通接口）/ < 5 秒（复杂查询） |
| 错误处理 | 4xx 请求返回明确的错误信息 |

## 10. 验证报告格式

验证完成后，生成报告保存至 `./项目文档/E2E验证/E2E验证报告.md`：

```markdown
# E2E 验证报告

## 验证概要
- 项目名称：xxx
- 验证时间：2026-07-04 15:30
- 验证环境：Node.js v20.x / Chrome 126
- 开发服务器：http://localhost:3000

## 页面验证结果

| 页面 | 路由 | 状态 | 截图 | 备注 |
|------|------|------|------|------|
| 首页 | / | ✅ 通过 | home.png | — |
| 登录 | /login | ✅ 通过 | login.png | — |
| 仪表盘 | /dashboard | ❌ P1 | dashboard.png | 数据列表不显示 |

## 交互验证结果

| 交互项 | 页面 | 状态 | 备注 |
|--------|------|------|------|
| 登录按钮 | /login | ✅ 通过 | 登录成功跳转首页 |
| 提交表单 | /settings | ❌ P1 | 点击无响应 |
| 导航链接 | 全局 | ✅ 通过 | — |

## 控制台错误
- 0 个 Error
- 0 个 Warning（可忽略）

## API 响应验证
- GET /api/users → 200 ✅
- POST /api/users → 201 ✅
- GET /api/unknown → 404 ✅（预期行为）

## 交付结论
❌ **阻塞交付** — P1 问题 2 个需修复：
1. 仪表盘页面数据列表不显示
2. 设置页面提交按钮无响应
```

## 11. 熔断机制

### 11.1 触发条件
- 核心页面白屏（HTTP 500 或页面内容为空）
- 开发服务器无法启动
- 登录/注册等核心功能不可用
- 连续 3 个页面渲染失败

### 11.2 触发后的动作
1. **立即停止验证**，不再继续检查其他页面
2. 在验证报告中标记为 **阻塞交付**
3. 记录具体错误（控制台日志 + 截图）
4. 告知用户：核心功能不可用，需要修复后重新验证

## 12. 执行建议

1. **先跑后端再跑前端**：如果项目有后端，先确认后端 API 全部可用，再打开前端验证
2. **从登录页开始**：大多数应用需要登录才能看到其他页面，先验证登录流程
3. **截图是铁证**：每个页面截图，用户能看到你验证过的证据
4. **控制台是金矿**：很多"看起来没问题"的页面，控制台其实一堆红色报错
5. **别信"应该没问题"**：每个按钮都要亲自点一下，每个表单都要填一下

## 13. 成功标准 (DoD)

- [ ] 开发服务器成功启动
- [ ] 所有页面路由可访问（HTTP 200）
- [ ] 所有页面截图已生成
- [ ] 所有按钮点击后有正确响应
- [ ] 所有表单可提交且有反馈
- [ ] 所有导航链接跳转正确
- [ ] 控制台零 Error
- [ ] API 端点全部响应正常
- [ ] 移动端布局验证通过（如 PRD 要求）
- [ ] P0 = 0 且 P1 = 0
- [ ] E2E 验证报告已生成
- [ ] tasks.md 中该任务已标记 `[x]`

## 14. 输出成果

1. **E2E 验证报告**：`./项目文档/E2E验证/E2E验证报告.md`
2. **页面截图**：`./项目文档/E2E验证/截图/*.png`
3. **Playwright 测试文件**：`./e2e/*.spec.ts`（可复用的 E2E 测试套件）
4. **Bug 清单**：记录在 E2E 验证报告的问题部分
5. **tasks.md 更新**：标记 `[x]`

## 15. 与 autopilot 引擎的契约

**输入**：从 `tasks.md` 接收"端到端真机验证"任务（阶段三交付前最后一步）
**输出**：E2E 验证报告 + 截图 + 通过/阻塞结论 + tasks.md 打勾
**前置依赖**：所有开发任务已完成 + `vibe-test` 已通过 + `vibe-security` 已通过 + `vibe-review` 已通过
**执行时机**：阶段三交付前，在 `vibe-api-docs` 之前
**禁止行为**：
- 禁止跳过任何页面——每个路由都要验证
- 禁止"看起来没问题"就放行——必须截图存证
- 禁止在 P0/P1 问题未修复时标记交付通过
- 禁止用单元测试结果替代真机验证——代码测试全过 ≠ 页面能用

---

**记住**：E2E 验证是 VIBE 交付前的最后一道防线。代码层面的测试再全，也替代不了"打开浏览器点一下"。白屏、按钮失灵、接口 404——这些问题只有真机验证才能发现。**一个 P0 都没有的交付，才叫交付。**
