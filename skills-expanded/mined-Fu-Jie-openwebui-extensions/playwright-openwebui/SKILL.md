---
name: "playwright-openwebui"
description: "Use when inspecting UI bugs in OpenWebUI plugins, taking screenshots of plugin output, capturing console errors, testing Action/Filter/Pipe plugins in the chat interface, or verifying plugin installation in the Admin panel. Triggered by: plugin UI bug, Action HTML output, screenshot, console error, plugin not working, login, admin panel, chat test, function install."
---

## 重要说明 (Living Document)

> **这是一个持续演进的技能文件 (Living Skill)**  
> 每次测试会话结束后，必须将新发现的 selector、时序问题、已知坑点追加到 `.agent/learnings/playwright-tests.md`。  
> 每次新会话开始前，必须先读取该文件，避免重复踩坑。  
> 本文件本身也应在发现重大 UI 变化时更新（例如 OWUI 版本升级导致 selector 失效）。

**配套 Agent:** `plugin-tester.agent.md` — 完整的部署+测试+学习闭环。  
**Env 文件:** `.github/agents/.env.openwebui` (OPENWEBUI_URL / USERNAME / PASSWORD)  
**Scripts Env:** `scripts/.env` (api_key + url，用于 Python 部署脚本)

## Instructions

Use Playwright browser tools to test and debug OpenWebUI plugins. Start every session with the login flow. Credentials and URL are read from `.github/agents/.env.openwebui`.

### 第一步：登录（每次会话必须先执行）

```js
const fs = require('fs');
const path = require('path');

// 读取 .env.openwebui
function loadEnv() {
  const envPath = path.join(process.cwd(), '.github/agents/.env.openwebui');
  const raw = fs.readFileSync(envPath, 'utf-8');
  const env = {};
  for (const line of raw.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const [key, ...rest] = trimmed.split('=');
    env[key.trim()] = rest.join('=').trim();
  }
  return env;
}

const env = loadEnv();
const BASE_URL = env.OPENWEBUI_URL || 'http://localhost:3000';

// 导航到登录页
await page.goto(`${BASE_URL}/auth`, { waitUntil: 'networkidle' });

// 检查是否已登录（已登录则跳过）
const isLoggedIn = await page.locator('[id="chat-textarea"], [placeholder*="message" i], div[contenteditable]').count();

if (!isLoggedIn) {
  // 填写 email
  await page.locator('input[name="email"], input[autocomplete="username"], input[type="email"]').first().fill(env.OPENWEBUI_USERNAME);
  // 填写密码
  await page.locator('input[type="password"]').first().fill(env.OPENWEBUI_PASSWORD);
  // 点击登录
  await page.locator('button[type="submit"]').first().click();
  // 等待登录完成
  await page.waitForURL(`${BASE_URL}/**`, { timeout: 10000 });
  await page.waitForTimeout(1500);
}

console.log('✅ 已登录 OpenWebUI:', await page.title());
```

---

### 常用操作模式

#### 截图存档
```js
await page.screenshot({ path: '/tmp/owui-before-fix.png' });
```

#### 控制台 / 错误捕获
```js
const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
page.on('pageerror', err => errors.push('pageerror: ' + err.message));
await page.waitForTimeout(2000);
console.log('Console errors:', errors);
```

#### 打开管理员面板（Admin Panel）
```js
const env = loadEnv();
await page.goto(`${env.OPENWEBUI_URL}/admin`, { waitUntil: 'networkidle' });
await page.screenshot({ path: '/tmp/owui-admin.png' });
```

#### 导航到函数/插件管理（Functions）
```js
const env = loadEnv();
await page.goto(`${env.OPENWEBUI_URL}/admin/functions`, { waitUntil: 'networkidle' });
// 截图确认插件列表
await page.screenshot({ path: '/tmp/owui-functions.png' });
```

#### 安装 / 更新插件代码
```js
// 点击 "+" 新建 Function
const addBtn = page.locator('button').filter({ hasText: /add|new|\+/i }).first();
await addBtn.click();
await page.waitForTimeout(500);

// 在代码编辑器中粘贴插件代码
const editor = page.locator('.cm-content, [contenteditable="true"].CodeMirror').first();
await editor.click();
await page.keyboard.shortcut('Meta+A'); // 全选
await page.keyboard.type(pluginCode);    // 粘贴新代码（pluginCode 变量需提前赋值）
```

#### 发送聊天消息测试插件
```js
const env = loadEnv();
await page.goto(`${env.OPENWEBUI_URL}/`, { waitUntil: 'networkidle' });

// 新建对话
const newChatBtn = page.locator('button').filter({ hasText: /new chat/i }).first();
if (await newChatBtn.count()) await newChatBtn.click();
await page.waitForTimeout(800);

// 输入测试消息
const textarea = page.locator('[id="chat-textarea"], textarea, div[contenteditable]').first();
await textarea.click();
await textarea.fill('你好，请帮我总结这段文字。');

// 发送
const sendBtn = page.locator('button[data-element-id="send-message-button"], button[aria-label*="send" i]').first();
await sendBtn.click();

// 等待回复
await page.waitForSelector('.message-content, [data-role="assistant"]', { timeout: 30000 });
await page.screenshot({ path: '/tmp/owui-chat-response.png' });
```

#### 触发 Action 插件按钮
```js
// 悬浮消息，查找 Action 按钮（通常在消息底部工具栏）
const msgToolbar = page.locator('.message-toolbar, [class*="action"]').last();
await msgToolbar.hover();
await page.waitForTimeout(300);

// 点击目标 Action 按钮（按图标或 title 过滤）
const actionBtn = page.locator('button[title], button.action-button').filter({ hasText: /export|mind|思维|导出/i }).first();
await actionBtn.click();
await page.waitForTimeout(2000);
await page.screenshot({ path: '/tmp/owui-action-result.png' });
```

#### 检查 Action 插件的 HTML 输出（iframe / html code block）
```js
// Action 插件通常在消息中输出 HTML 块
const htmlBlock = page.locator('iframe, .plugin-output, code[class*="html"]').last();
const count = await htmlBlock.count();
console.log('HTML output blocks found:', count);

if (count > 0) {
  // 截取 iframe 内容
  const frame = page.frameLocator('iframe').last();
  const frameContent = await frame.locator('body').innerHTML();
  console.log('iframe body (first 500):', frameContent.substring(0, 500));
  await page.screenshot({ path: '/tmp/owui-plugin-html-output.png' });
}
```

#### 拦截网络失败请求
```js
const failedRequests = [];
page.on('requestfailed', r => failedRequests.push({ url: r.url(), error: r.failure()?.errorText }));
await page.waitForTimeout(3000);
console.log('Failed requests:', failedRequests);
```

#### 获取当前页面文本摘要
```js
const bodyText = await page.evaluate(() => document.body.innerText.substring(0, 800));
console.log('Page content:', bodyText);
```

#### 检查模型选择器（切换测试模型）
```js
// 点击模型选择按钮（顶部）
const modelSelector = page.locator('button').filter({ hasText: /model|gpt|claude|llama/i }).first();
await modelSelector.click();
await page.waitForTimeout(500);

// 从下拉列表中选择目标模型
const targetModel = page.locator('[role="option"], li').filter({ hasText: 'gpt-4' }).first();
await targetModel.click();
await page.waitForTimeout(500);
```

#### 刷新页面
```js
await page.goto(page.url(), { waitUntil: 'networkidle' });
```

#### 全流程回归探针（Plugin E2E Probe）
```js
// 捕获所有错误 + 失败请求
await page.evaluate(() => {
  window.__pluginBugLogs = { errors: [], failedRequests: [] };
  window.addEventListener('error', (e) => {
    window.__pluginBugLogs.errors.push(String(e.message || 'unknown'));
  });
  window.addEventListener('unhandledrejection', (e) => {
    window.__pluginBugLogs.errors.push(String(e.reason || 'rejection'));
  });
  const origFetch = window.fetch.bind(window);
  window.fetch = async (...args) => {
    const res = await origFetch(...args);
    if (!res.ok) window.__pluginBugLogs.failedRequests.push(`${res.status} ${String(args[0])}`);
    return res;
  };
});

// 触发 Action 按钮
const actionBtn = page.locator('button').filter({ hasText: /export|导出/i }).first();
await actionBtn.click();
await page.waitForTimeout(3000);

// 收集日志
const bugLogs = await page.evaluate(() => window.__pluginBugLogs);
console.log('E2E Probe Result:', JSON.stringify(bugLogs, null, 2));
await page.screenshot({ path: '/tmp/owui-e2e-probe.png' });
```

---

### 自我学习协议（Self-Learning Protocol）

每次会话结束前，执行以下步骤：

**Step 1 — 读取现有知识（会话开始时）**
```js
// 在执行任何测试前，读取 .agent/learnings/playwright-tests.md
// 提取：已知 selector、已验证用例、已知坑点
const fs = require('fs');
const learningsPath = '.agent/learnings/playwright-tests.md';
if (fs.existsSync(learningsPath)) {
  const knowledge = fs.readFileSync(learningsPath, 'utf-8');
  console.log('📚 Loaded learnings:', knowledge.substring(0, 300));
}
```

**Step 2 — 记录新发现（会话结束后）**

使用 AI 工具或 `fs.appendFileSync` 将以下内容追加到 `.agent/learnings/playwright-tests.md`：
- ✅ 新发现的可靠 selector（含日期和插件类型）
- ❌ 已失效的 selector（含失效原因）
- ⚡ 时序敏感点（需要 `waitForTimeout` 的场景）
- 🐛 已发现的 UI bug（含截图路径）
- 🧪 新增测试用例（描述 + 结果）

---

### 与 Scripts 集成（Deploy + Test 联动）

在 playwright 测试前，可先用 Python 脚本部署插件：

```bash
# 部署单类型插件
cd /Users/fujie/app/python/oui/openwebui-extensions
python scripts/install_all_plugins.py --types action

# 部署指定 filter
python scripts/deploy_filter.py async-context-compression

# 验证部署工具可用性
python scripts/verify_deployment_tools.py
```

`scripts/.env` 格式（与 playwright env 独立）：
```
api_key=sk-your-api-key
url=http://localhost:3000
```

---

## Tools
browser

## Scene Hints
kind: openwebui_plugin_development
accent: #10A37F
