---
name: browser-testing
description: "浏览器自动化测试方法论——混合模式测试：agent-browser（看清）+ Playwright MCP（操作）。精确获取页面结构 + 稳定执行交互操作。用于 /browser-test 和 /bug-fix 命令的执行。"
version: "4.7.25"
updated: "2026-05-25"
---

# 浏览器自动化测试

## 概述

**混合模式：agent-browser（看清）+ Playwright MCP（操作）**

本质：**精确获取 + 稳定执行**——agent-browser snapshot -i 以极低成本获取页面结构（DOM 快照 + 元素引用），Playwright MCP 负责可靠的交互操作（点击/填写/导航/截图）。

- **agent-browser snapshot -i**：廉价页面结构获取，返回元素引用（@ref），token 消耗极低
- **Playwright MCP**：稳定执行交互——browser_click / browser_type / browser_navigate / browser_take_screenshot 等，CI 可重复
- **agent-browser CLI**：补充操作——console 日志、network 请求、viewport 调整等诊断能力

**前置条件：** `agent-browser` 已安装（`npm i -g agent-browser && agent-browser install`），Playwright MCP 已配置。

## 测试用例格式

每条用例输出到 `.jarvis/YYYY-MM-DD/testing/<topic>-browser-test-cases.md`：

```markdown
### TC-001: <用例名称>
- **前置条件**：<URL、登录状态、数据准备>
- **操作步骤**：
  1. 导航到 <页面>
  2. 点击/输入 <元素>
  3. 验证 <结果>
- **预期结果**：<具体可验证的结果>
- **验证方式**：截图 / 状态检查 / 元素文本匹配
- **优先级**：P0（阻塞）/ P1（重要）/ P2（次要）
```

## 执行流程

按优先级从高到低逐条执行。

### 初始化：打开浏览器

```bash
agent-browser open <url>          # 默认无头，加 --headed 可见
agent-browser profile list        # 若需复用 Chrome 登录态，先查 profile
agent-browser --profile "Default" open <url>  # 使用现有 Chrome 登录态
```

### 每条用例的标准操作序列（混合模式）

```bash
# 1. 获取页面快照（agent-browser 精确获取元素引用）
agent-browser snapshot -i

# 2. 交互操作（Playwright MCP 稳定执行）
mcp__playwright__browser_click({target: "<element-ref>"})       # 点击元素
mcp__playwright__browser_type({target: "<ref>", text: "..."})   # 输入文本
mcp__playwright__browser_press_key({key: "Enter"})              # 按键
mcp__playwright__browser_navigate({url: "<URL>"})               # 导航
mcp__playwright__browser_hover({target: "<ref>"})               # 悬停

# 3. 截图留证（Playwright MCP）
mcp__playwright__browser_take_screenshot({type: "png"})         # 截图
mcp__playwright__browser_take_screenshot({fullPage: true})      # 全页截图

# 4. 验证（agent-browser 诊断 + Playwright 快照）
agent-browser snapshot -i                                        # 确认元素引用变化
mcp__playwright__browser_snapshot()                              # Playwright 无障碍快照
agent-browser console                                            # 检查控制台日志
agent-browser errors                                             # 检查 JS 异常
agent-browser network requests --filter api                      # 检查 API 请求
agent-browser get url                                            # 确认当前 URL
```

**执行规则：**
- agent-browser snapshot -i 获取元素引用（看清），Playwright MCP 执行操作（执行）
- 每次关键交互后截图（点击按钮、提交表单、页面跳转后）
- 失败立即记录，截图保存失败状态
- 前置条件不满足则标记"跳过"，写明原因
- 页面异常时 `agent-browser close` 清理后重试
- 不用硬等待；用 `agent-browser wait "<selector>"` 或 Playwright `browser_wait_for` 确认页面状态

## Bug 复现模式

接到 Bug 报告后：

1. 读取复现步骤
2. `agent-browser open <url>` → `agent-browser snapshot -i` → 逐步执行操作
3. 异常发生时立即截图：`agent-browser screenshot bug-xxx.png` + `agent-browser screenshot --annotate`
4. 收集证据：
   - `agent-browser console` — JS 错误
   - `agent-browser errors` — 未捕获异常
   - `agent-browser network requests` — 失败的网络请求
   - `agent-browser get text @eN` — 页面异常文本
5. 尝试至少 1 个变体确认触发边界
6. 输出复现证据：截图路径、操作步骤、实际 vs 预期

## 响应式/多视口测试

对于需要验证响应式的页面：

```bash
agent-browser set viewport 375 812   # 移动端
agent-browser screenshot mobile.png
agent-browser set viewport 768 1024  # 平板
agent-browser screenshot tablet.png
agent-browser set viewport 1280 800  # 桌面
agent-browser screenshot desktop.png
```

## 本地开发环境测试

### 工具可用性矩阵

| 平台/环境 | Preview MCP | agent-browser CLI | Playwright MCP | Chrome DevTools MCP |
|-----------|------------|-------------------|----------------|---------------------|
| Claude Code（桌面版） | ✅ 可用 | ✅ 可用 | ✅ 可用 | ✅ 可用 |
| Claude Code（终端/CLI） | ❌ 不可用 | ✅ 可用 | ✅ 可用 | ✅ 可用 |
| OpenCode | ❌ 不可用 | ✅ 可用 | ✅ 可用 | ✅ 可用 |
| Codex | ❌ 不可用 | ✅ 可用 | ✅ 可用 | ✅ 可用 |

> **混合模式**：agent-browser snapshot -i 精确获取页面结构（看清），Playwright MCP 稳定执行交互操作（操作）。Chrome DevTools MCP 用于前端调试（性能追踪/渲染分析/网络诊断/控制台调试）。

### 方案 A：有 Preview MCP 时（Claude Code 桌面版）

1. `mcp__chrome-devtools__list_pages` — 检查是否已有运行中的预览服务器
2. 若未运行且 `.claude/launch.json` 已配置：
   ```
   mcp__chrome-devtools__navigate_page({name: "<config-name>"})
   ```
3. 获取本地 URL 后使用 `agent-browser open <url>` 或 `preview_screenshot` 进行测试
4. 测试完成后可保留服务器供后续使用

### 方案 B：无 Preview MCP 时（Claude Code 终端 / OpenCode / Codex）

1. 通过 Bash 启动 dev server（后台运行）：
   ```bash
   npm run dev &
   ```
2. 用 agent-browser 打开页面：
   ```bash
   agent-browser open http://localhost:<port>
   ```
3. 页面快照 + 截图验证：
   ```bash
   agent-browser snapshot -i
   agent-browser screenshot
   ```
4. 响应式多视口测试：
   ```bash
   agent-browser set viewport 375 812   # 移动端
   agent-browser screenshot mobile.png
   agent-browser set viewport 768 1024  # 平板
   agent-browser screenshot tablet.png
   agent-browser set viewport 1280 800  # 桌面
   agent-browser screenshot desktop.png
   ```

## 报告模板

`.jarvis/YYYY-MM-DD/testing/<topic>-browser-test-report.md`：

```markdown
# 浏览器自动化测试报告

## 测试概览
| 总用例 | 通过 | 失败 | 跳过 | 通过率 |
|--------|------|------|------|--------|
| N      | N    | N    | N    | XX%    |

## 环境信息
- 测试 URL：<URL>
- 测试时间：<timestamp>
- 浏览器视口：<尺寸>

## 详情
### TC-001: <名称> — ✅ 通过
- 截图：<路径>

### TC-002: <名称> — ❌ 失败
- 预期：<结果> / 实际：<结果>
- 截图：<路径>
- 控制台错误：<错误信息>
- 网络异常：<失败请求>
- 疑似原因：<分析>

## 失败汇总
| 用例 | 严重度 | 故障类型 | 疑似根因 |
|------|--------|---------|---------|
```

## 修复闭环

1. 全部通过 → ✅ 闭环完成
2. 存在失败 → Browser Test Findings → `/review-fix` 修复 → 仅重跑失败用例 → 更新报告
3. 最多 2 轮，第 3 轮仍失败标记 BLOCKED

## 红线

- 不写用例直接操作浏览器（缺少可追溯的测试计划）
- 失败不截图、不记录控制台/网络错误（缺少证据）
- 跳过用例不标注原因
- 伪造测试结果
- 执行破坏性操作（删除数据、发起支付等）
- 用硬等待（sleep/wait）替代 `agent-browser wait` 轮询确认页面状态

## 职责分工

### 测试文档编写 vs 测试执行
- **test-doc-writer Agent**：负责在测试执行前根据需求文档和前端变更编写结构化测试用例文档，输出到 `.jarvis/YYYY-MM-DD/testing/<topic>-test-cases.md`
- **browser-test-expert**：负责读取已有测试文档中的用例并逐条执行，输出测试报告到 `.jarvis/YYYY-MM-DD/testing/<topic>-browser-test-report.md`
- **职责边界**：测试执行 Agent 不得自行编写或修改测试用例文档，测试文档编写 Agent 不得执行浏览器测试。测试用例必须在测试执行前由 test-doc-writer 编写完成。

## 测试报告模板

执行完成后按以下模板输出测试报告（输出到 `.jarvis/YYYY-MM-DD/testing/<topic>-browser-test-report.md`）：

### 汇总

| 指标 | 数值 |
|------|------|
| 总计 | N |
| 通过 | N ✅ |
| 失败 | N ❌ |
| 阻塞 | N ⚠️ |

### 详细结果

#### TC-XXX: 用例标题 — ✅/❌
- **预期:** ...
- **实际:** ...
- **截图证据:** <路径>
- **可能原因:** （仅失败时）
- **关联代码:** <文件:行号>（仅失败时）

### 失败用例清单
- [ ] TC-XXX: 简短描述

## 失败用例交接格式

测试失败后，向修复 Agent 传递以下信息：

```json
{
  "failedCases": [
    {
      "id": "TC-XXX",
      "title": "用例标题",
      "expected": "预期结果",
      "actual": "实际结果",
      "screenshot": "截图路径",
      "possibleCause": "可能原因分析",
      "relatedCode": "关联代码位置"
    }
  ]
}
```

或 markdown 格式：

```markdown
## 失败用例交接
### TC-XXX: 用例标题
- **预期:** ...
- **实际:** ...
- **截图证据:** <路径>
- **可能原因:** <分析>
- **关联代码:** <文件:行号>
```
